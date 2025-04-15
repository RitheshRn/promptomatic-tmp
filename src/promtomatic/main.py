"""
Main entry point for the Promtomatic prompt optimization tool.
"""

import os
import sys
import json
import dspy
import nltk
import traceback
from datetime import datetime
from typing import Dict, Optional

from promtomatic.core.config import Config
from promtomatic.core.optimizer import PromptOptimizer
from promtomatic.core.session import SessionManager, OptimizationSession
from promtomatic.core.feedback import Feedback, FeedbackStore
from promtomatic.cli.parser import parse_args

# Initialize global managers
session_manager = SessionManager()
feedback_store = FeedbackStore()

# Compatibility layer for the backend
class OptimizationSessionWrapper:
    """Wrapper class to maintain compatibility with the old API"""
    def __init__(self, session_manager):
        self.session_manager = session_manager
    
    def __getitem__(self, session_id):
        return self.session_manager.get_session(session_id)
    
    def __setitem__(self, session_id, session):
        # This won't be called directly, as sessions are managed through session_manager
        pass
    
    def __contains__(self, session_id):
        return self.session_manager.get_session(session_id) is not None
    
    def get(self, session_id, default=None):
        return self.session_manager.get_session(session_id) or default

# Create global instance for backward compatibility
optimization_sessions = OptimizationSessionWrapper(session_manager)

def process_input(**kwargs) -> Dict:
    """
    Process initial optimization request.
    
    Args:
        **kwargs: Configuration parameters
        
    Returns:
        Dict: Optimization results
    """
    session_id = str(datetime.now().timestamp())
    session = None
    
    try:
        # Create config
        config = Config(**kwargs)
        config.session_id = session_id
        
        # Create and store session
        session = session_manager.create_session(
            session_id=session_id,
            initial_input=config.task,
            config=config
        )
        
        # Initialize language model with configurable parameters
        lm = dspy.LM(
            config.model_name,
            api_key=config.model_api_key,
            api_base=config.model_api_base,
            temperature=config.temperature,
            max_tokens=config.max_tokens
        )
        dspy.configure(lm=lm)
        
        # Create and run optimizer
        optimizer = PromptOptimizer(config)
        optimizer.lm = lm
        
        result = optimizer.run(initial_flag=True)
        
        # Update session with optimized prompt
        if isinstance(result.get('result'), str):
            session.update_optimized_prompt(result['result'])
        
            return result
            
    except Exception as e:
        error_msg = str(e)
        trace = traceback.format_exc()
        
        if session:
            session.logger.add_entry("ERROR", {
                "error": error_msg,
                "traceback": trace,
                "stage": "Initial Optimization"
            })
        
        return {
            'error': error_msg,
            'traceback': trace,
            'session_id': session_id if session_id else None
        }

def optimize_with_feedback(session_id: str) -> Dict:
    """
    Optimize prompt based on feedback for a given session.
    
    Args:
        session_id (str): Session identifier
        
    Returns:
        Dict: Optimization results
    """
    try:
        session = session_manager.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        # Get the latest feedback for this session
        session_feedbacks = feedback_store.get_feedback_for_prompt(session_id)
        if not session_feedbacks:
            raise ValueError("No feedback found for this session")
        
        # Use the latest feedback
        latest_feedback = max(session_feedbacks, key=lambda x: x['created_at'])
        
        # Create feedback config
        feedback_config = Config(
            raw_input=f"Prompt: {session.latest_optimized_prompt}\nFeedback: {latest_feedback['feedback']}",
            original_raw_input=session.config.original_raw_input,
            synthetic_data_size=session.config.synthetic_data_size,
            train_ratio=session.config.train_ratio,
            task_type=session.config.task_type,
            model_name=session.config.model_name,
            model_provider=session.config.model_provider,
            model_api_key=session.config.model_api_key,
            model_api_base=session.config.model_api_base,
            dspy_module=session.config.dspy_module,
            session_id=session_id
        )
        
        # Initialize optimizer
        optimizer = PromptOptimizer(feedback_config)
        
        # Reset DSPy configuration for this thread
        dspy.settings.configure(reset=True)
        
        # Initialize language model
        lm = dspy.LM(
            feedback_config.model_name,
            api_key=feedback_config.model_api_key,
            api_base=feedback_config.model_api_base,
            temperature=feedback_config.temperature,
            max_tokens=feedback_config.max_tokens
        )
        
        # Configure DSPy with the new LM instance
        dspy.configure(lm=lm)
        optimizer.lm = lm
        
        # Run optimization
        result = optimizer.run(initial_flag=False)
        
        # Update session with new optimized prompt if successful
        if isinstance(result.get('result'), str):
            session.update_optimized_prompt(result['result'])
        
        return result
        
    except Exception as e:
        error_msg = str(e)
        trace = traceback.format_exc()
        
        if session:
            session.logger.add_entry("ERROR", {
                "error": error_msg,
                "traceback": trace,
                "stage": "Feedback Optimization"
            })
        
        return {
            'error': error_msg,
            'traceback': trace,
            'session_id': session_id,
            'result': None,
            'metrics': None
        }

def save_feedback(text: str, start_offset: int, end_offset: int, 
                feedback: str, prompt_id: str) -> Dict:
    """
    Save a feedback for a prompt.
    
    Args:
        text (str): Text being feedbacked on
        start_offset (int): Feedback start position
        end_offset (int): Feedback end position
        feedback (str): Feedback text
        prompt_id (str): Associated prompt ID
        
    Returns:
        Dict: Saved feedback details
    """
    try:
        new_feedback = Feedback(
            text=text,
            start_offset=start_offset,
            end_offset=end_offset,
            feedback=feedback,
            prompt_id=prompt_id
        )
        
        # Store feedback
        feedback_store.add_feedback(new_feedback)
        
        # Add to session if exists
        session = session_manager.get_session(prompt_id)
        if session:
            session.add_feedback(new_feedback)
        
        return new_feedback.to_dict()
        
    except Exception as e:
        if prompt_id:
            session = session_manager.get_session(prompt_id)
            if session:
                session.logger.add_entry("ERROR", {
                "error": str(e),
                "traceback": traceback.format_exc(),
                    "stage": "Feedback Addition"
            })
        raise

def main():
    """Main entry point for the CLI application."""
    try:
        # Parse command line arguments
        args = parse_args()

        # Process optimization
        if args.get('raw_input') or args.get('huggingface_dataset_name'):
            result = process_input(**args)
            print(json.dumps(result, indent=2))
            return
        
        # Handle feedback management commands
        if args.get('list_feedbacks'):
            print(json.dumps(feedback_store.get_all_feedbacks(), indent=2))
            return
            
        if args.get('analyze_feedbacks'):
            analysis = feedback_store.analyze_feedbacks(args.get('prompt_id'))
            print(json.dumps(analysis, indent=2))
            return
            
        if args.get('export_feedbacks'):
            feedback_store.export_to_file(
                args.get('export_feedbacks'),
                args.get('prompt_id')
            )
            return
        
        print("No valid command specified. Use --help for usage information.")
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
