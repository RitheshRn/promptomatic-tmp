"""
Core module for prompt optimization functionality.
"""

import dspy
import ast
import json
from typing import Dict, List, Type, Optional, Union
from datetime import datetime
from dspy.evaluate import Evaluate
import nltk
import os
import logging

from ..utils.parsing import parse_dict_strings
from ..core.config import Config
from ..core.session import OptimizationSession
from ..metrics.metrics import MetricsManager

# Setup module logger
logger = logging.getLogger(__name__)

class PromptOptimizer:
    """
    Handles the optimization of prompts using DSPy.
    
    Attributes:
        config (Config): Configuration for optimization
        lm: Language model instance
        optimized_prompt (str): Latest optimized prompt
        data_template (Dict): Template for data structure
    """
    
    def __init__(self, config: Config):
        """
        Initialize the optimizer with configuration.
        
        Args:
            config (Config): Configuration object containing optimization parameters
        """
        self.config = config
        self.lm = None
        self._ensure_nltk_data()
        
        # Use module-level logger
        self.logger = logger
        self.logger.info("PromptOptimizer initialized")

    def _ensure_nltk_data(self):
        """Ensure required NLTK data is available."""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            logger.info("Downloading required NLTK data...")
            nltk.download('punkt')
            nltk.download('averaged_perceptron_tagger')
            nltk.download('wordnet')
    
    def create_signature(self, name: str, input_fields: List[str], 
                        output_fields: List[str]) -> Type[dspy.Signature]:
        """
        Create a DSPy signature for the optimization task.
        
        Args:
            name (str): Name of the signature
            input_fields (List[str]): List of input field names
            output_fields (List[str]): List of output field names
            
        Returns:
            Type[dspy.Signature]: DSPy signature class
        """
        cleaned_name = name.strip('_').strip()
        
        # Parse fields if they're strings
        input_fields = self._parse_fields(input_fields)
        output_fields = self._parse_fields(output_fields)
        
        # Create signature class
        class_body = {
            '__annotations__': {},
            '__doc__': self.config.task
        }
        
        # Add input and output fields
        for field in input_fields:
            field = field.strip('"\'')
            class_body['__annotations__'][field] = str
            class_body[field] = dspy.InputField()
            
        for field in output_fields:
            field = field.strip('"\'')
            class_body['__annotations__'][field] = str
            class_body[field] = dspy.OutputField()
        
        return type(cleaned_name, (dspy.Signature,), class_body)
    
    def _parse_fields(self, fields: Union[List[str], str]) -> List[str]:
        """Parse field definitions from string or list."""
        if isinstance(fields, str):
            fields = fields.strip()
            if not (fields.startswith('[') and fields.endswith(']')):
                fields = f"[{fields}]"
            return ast.literal_eval(fields)
        return fields

    def generate_synthetic_data(self) -> List[Dict]:
        """Generate synthetic training data based on sample data in batches."""
        try:
            sample_data = self._prepare_sample_data()
            template = {key: '...' for key in sample_data.keys()}

            # On average, 4 characters make up a token
            no_of_toks_in_sample_data = len(str(sample_data))/4
            
            # Calculate batch size based on token limits (assuming 16k token limit)
            # Leave room for prompt overhead and response
            max_samples_per_batch = min(50, max(1, int(8000 / no_of_toks_in_sample_data)))
            
            all_synthetic_data = []
            remaining_samples = self.config.synthetic_data_size
            
            # Initialize LLM once for all batches
            tmp_lm = dspy.LM(
                self.config.config_model_name,
                api_key=self.config.config_model_api_key,
                api_base=self.config.config_model_api_base,
                max_tokens=self.config.config_max_tokens,
                cache=False
            )
            
            while remaining_samples > 0:
                batch_size = min(max_samples_per_batch, remaining_samples)
                prompt = self._create_synthetic_data_prompt(sample_data, template, batch_size)
                
                response = tmp_lm(prompt)[0]
                response = self._clean_llm_response(response)
                
                batch_data = json.loads(response)
                all_synthetic_data.extend(batch_data)
                
                remaining_samples -= batch_size
                self.logger.info(f"Generated {len(all_synthetic_data)} samples out of {self.config.synthetic_data_size}")
            
            del tmp_lm
            return all_synthetic_data
            
        except Exception as e:
            self.logger.error(f"Error generating synthetic data: {str(e)}")
            raise

    def _prepare_sample_data(self) -> Dict:
        """Prepare sample data for synthetic data generation."""
        if isinstance(self.config.sample_data, str):
            try:
                data = ast.literal_eval(self.config.sample_data)
                return data[0] if isinstance(data, list) else data
            except (SyntaxError, ValueError) as e:
                raise ValueError(f"Invalid sample data format: {str(e)}")
        elif isinstance(self.config.sample_data, list):
            return self.config.sample_data[0]
        elif isinstance(self.config.sample_data, dict):
            return self.config.sample_data
        else:
            raise ValueError(f"Unexpected sample_data type: {type(self.config.sample_data)}")

    def _create_synthetic_data_prompt(self, sample_data: Dict, template: Dict, batch_size: int) -> str:
        """Create prompt for synthetic data generation with specified batch size."""
        return f"""Generate {batch_size} diverse yet structurally similar samples based on the provided example.

### Example:
{json.dumps(sample_data, indent=2)}

### Requirements:
- Maintain the structure and format of the example.
- Ensure all keys and values are strictly in string format.
- Introduce diversity while preserving logical consistency.
- Avoid duplicating exact data from the example.
- Return data as a valid JSON array of objects.
- Do not include numbering or labels in the output.

### Output Format:
{json.dumps([template], indent=2)}"""

    def _clean_llm_response(self, response: str) -> str:
        """Clean and format LLM response."""
        if "```json" in response:
            response = response.split("```json")[1].strip()
        if "```" in response:
            response = response.split("```")[0].strip()
        return response.strip()

    def run(self, initial_flag: bool = True) -> Dict:
        """
        Run the optimization process.
        
        Args:
            initial_flag (bool): Whether this is the initial optimization
            
        Returns:
            Dict: Optimization results including metrics
        """
        try:
            # Create signature
            signature = self.create_signature(
                name=f"{self.config.task_type.upper()}Signature",
                input_fields=self.config.input_fields,
                output_fields=self.config.output_fields
            )

            # Generate or prepare training data
            if not self.config.train_data:
                synthetic_data = self.generate_synthetic_data()
                self.config.train_data = synthetic_data[:self.config.train_data_size]
                self.config.valid_data = synthetic_data[self.config.train_data_size:]

            # Prepare datasets
            trainset, validset = self._prepare_datasets()
            validset_full = (self._prepare_full_validation_dataset() 
                           if self.config.valid_data_full else validset)

            # Initialize trainer
            trainer = self._initialize_trainer()

            # Compile program
            if self.config.dspy_module == dspy.ReAct:
                program = self.config.dspy_module(signature, tools=self.config.tools)
            else:
                program = self.config.dspy_module(signature)
            
            # Get evaluation metrics
            eval_metrics = self.get_final_eval_metrics()
            
            # Evaluate initial prompt
            evaluator = Evaluate(devset=validset_full, metric=eval_metrics)
            initial_score, initial_results = evaluator(program=program, return_outputs=True)
            
            # Compile optimized program
            compiled_program = self._compile_program(trainer, program, trainset, validset)
            
            # Evaluate optimized prompt
            optimized_score, optimized_results = evaluator(
                program=compiled_program, return_outputs=True
            )

            try:
                opt_instructions = compiled_program.signature.instructions
            except:
                opt_instructions = compiled_program.predict.signature.instructions
            
            # Prepare and return results
            return self._prepare_results(
                opt_instructions,
                initial_score,
                optimized_score
            )

        except Exception as e:
            self.logger.error(f"Error in optimization run: {str(e)}")
            return {'error': str(e), 'session_id': self.config.session_id}

    def _prepare_datasets(self):
        """Prepare training and validation datasets."""
        input_fields = (ast.literal_eval(self.config.input_fields) 
                       if isinstance(self.config.input_fields, str) 
                       else self.config.input_fields)
        
        if isinstance(input_fields, (list, tuple)):
            trainset = [dspy.Example(**ex).with_inputs(*input_fields) 
                       for ex in self.config.train_data]
            validset = [dspy.Example(**ex).with_inputs(*input_fields) 
                       for ex in self.config.valid_data]
        else:
            trainset = [dspy.Example(**ex).with_inputs(input_fields) 
                       for ex in self.config.train_data]
            validset = [dspy.Example(**ex).with_inputs(input_fields) 
                       for ex in self.config.valid_data]
        
        return trainset, validset

    def _prepare_full_validation_dataset(self):
        """Prepare full validation dataset if available."""
        input_fields = (ast.literal_eval(self.config.input_fields) 
                       if isinstance(self.config.input_fields, str) 
                       else self.config.input_fields)
        
        if isinstance(input_fields, (list, tuple)):
            return [dspy.Example(**ex).with_inputs(*input_fields) 
                    for ex in self.config.valid_data_full]
        return [dspy.Example(**ex).with_inputs(input_fields) 
                for ex in self.config.valid_data_full]

    def _initialize_trainer(self):
        """Initialize the DSPy trainer."""
        return dspy.MIPROv2(
            metric=self.get_eval_metrics(),
            init_temperature=0.7,
            auto=self.config.miprov2_init_auto,
            num_candidates=self.config.miprov2_init_num_candidates
        )

    def _compile_program(self, trainer, program, trainset, validset):
        """Compile the program using the trainer."""
        return trainer.compile(
            program,
            trainset=trainset,
            valset=validset,
            requires_permission_to_run=False,
            max_bootstrapped_demos=self.config.miprov2_compile_max_bootstrapped_demos,
            max_labeled_demos=self.config.miprov2_compile_max_labeled_demos,
            num_trials=self.config.miprov2_compile_num_trials,
            minibatch_size=self.config.miprov2_compile_minibatch_size
        )

    def _prepare_results(self, optimized_prompt: str, 
                        initial_score: float, optimized_score: float) -> Dict:
        """Prepare the final results dictionary."""
        return {
            'result': optimized_prompt,
            'session_id': self.config.session_id,
            'metrics': {
                'initial_prompt_score': initial_score,
                'optimized_prompt_score': optimized_score
            }
        }

    def get_eval_metrics(self):
        """Get evaluation metrics for the task type."""
        if isinstance(self.config.output_fields, str):
            output_fields = ast.literal_eval(self.config.output_fields)
        else:
            output_fields = self.config.output_fields
        
        MetricsManager.configure(output_fields)
        return MetricsManager.get_metrics_for_task(self.config.task_type)
    
    def get_final_eval_metrics(self):
        """Get final evaluation metrics for the task type."""
        return MetricsManager.get_final_eval_metrics(self.config.task_type) 