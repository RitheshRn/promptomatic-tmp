from typing import List
dspy_modules = {
    "dspy.Predict": "Basic predictor. Does not modify the signature. Handles the key forms of learning (i.e., storing the instructions and demonstrations and updates to the LM).",
    "dspy.ChainOfThought": "Teaches the LM to think step-by-step before committing to the signature's response.",
    "dspy.ProgramOfThought": "Teaches the LM to output code, whose execution results will dictate the response.",
    "dspy.ReAct": "An agent that can use tools to implement the given signature.",

}

def improvise_raw_input(human_input: str) -> str:
    return f"""You are a helpful assistant that generates an effective prompt from a given human input.
    Given the human input below, create an improved version that is:
    - More specific and clear
    - Well-structured and concise
    - Free of typos and grammatical errors
    - Complete with all original information and intent
    - Do not include any new or additional information in the output

    Strictly, do not solve/resolve/answer the human input. Only improve/rephrase the prompt.
    
    Original Input: {human_input}
    
    Enhanced Input: """

# def simplify_human_feedback(human_input: str) -> str:
#     return f"""
#     You are a helpful assistant that simplifies human feedback.
#     Given the prompt and the feedback, incorporate the feedback in the prompt and generate a new prompt.

#     Examples:
#     Prompt: Identify the sentiment of given word
#     Feedback: It need not just be word it can be sentence or a paragraph
#     New Prompt: Identify the sentiment of the given word/sentence/paragraph

#     Prompt: Summarize the given text
#     Feedback: summary does not contain names of persons
#     New Prompt: Summarize the given text in detail including the names of persons

#     {human_input}
#     New Prompt: """

def simplify_human_feedback(human_input: str) -> str:
    return f"""
    You are a helpful assistant that simplifies human feedback.
    Given the prompt and the feedback, incorporate the feedback in the prompt and generate a new prompt.

    Examples:
    Prompt: Create a 5-step plan for launching a small business
    Feedback: {{"5-step": "The plan should be more comprehensive, with 8-10 steps", "small business": "Specifically focus on e-commerce businesses"}}
    New Prompt: Create a comprehensive 8-10 step plan for launching an e-commerce business

    Prompt: Write a product description for a fitness tracker
    Feedback: {{"product description": "Include technical specifications and pricing", "fitness tracker": "This is specifically for the XFit Pro 3000 model"}}
    New Prompt: Write a product description for the XFit Pro 3000 fitness tracker that includes technical specifications and pricing information

    Prompt: Analyze the performance of the marketing campaign
    Feedback: {{"Analyze the performance": "Break down the analysis by demographic segments and ROI metrics", "marketing campaign": "Focus on the Q3 social media initiatives specifically"}}
    New Prompt: Break down the performance of the Q3 social media marketing initiatives by demographic segments and ROI metrics

    Prompt: Design a weekly meal plan with nutritional information
    Feedback: {{"Design a weekly meal plan": "make it 2 weeks insted", "nutritional information": "need macro breakdwn + prep time", "weekly meal plan": "for athlete w/ lactose issues training 4 marathon"}}
    New Prompt: Develop a comprehensive two-week meal plan for a lactose-intolerant marathon runner, featuring detailed macronutrient breakdowns and preparation times for each meal

    Prompt: Tell me how to fix the printer issue
    Feedback: {{"Tell me": "sounds demanding, need more polite language", "printer issue": "HP LaserJet Pro MFP M428fdw showing 'toner low' error"}}
    New Prompt: Could you please provide guidance on resolving the 'toner low' error on my HP LaserJet Pro MFP M428fdw printer?

    {human_input}
    New Prompt: """


def generate_sample_data_from_task_description(task_description: str) -> str:

    return f"""
    You are a helpful assistant that generates sample data for a given task description.
    Task description: {task_description}

    Generate 1 example of input data that would be relevant to the task description. Output the input data in a json format.
    Sample data needs to have the model input and expected output.
    Example:
    Task description: somethign related to questions and answers
    Output: {{"question": "What is the capital of France?", "answer": "Paris"}}

    Task description: something related to text generation
    Output: {{"text": "This is a sample text for text generation"}}

    Task description: something related to classification
    Output: {{"input_field_1": "value_1", "input_field_2": "value_2", "input_field_3": "value_3"}}

    Now for the task description: {task_description}
    Output: """



# def generate_sample_data_from_task_description_and_human_input(task_description: str, human_input: str) -> str:

#     return f"""You are a meticulous and creative assistant tasked with generating diverse sample data based on a provided task description and human input. The goal is to create structured, relevant, and accurate sample data in JSON format.

# Instructions:

# 1. If the human input already contains sample data, extract and use that sample data.
# 2. If the human input does not provide sample data, generate three diverse examples based on the task description.
# 3. Ensure the examples are varied, relevant, and well-structured while maintaining accuracy.
# 4. The output JSON format should contain fields relevant to the context, not necessarily restricted to "input" and "answer".
# 5. The JSON fields should match the nature of the task. For example:
#     - If the task is about explaining a concept, fields may be "question" and "explanation".
#     - If the task involves describing a process, fields may be "step" and "description".
#     - If the task requires comparisons, fields may be "entity_1", "entity_2", and "comparison".
# 6. Ensure that field names are contextually meaningful.
# 7. Format the output as a JSON list of dictionaries.
# 8. Make sure the sample data is as diverse as possible. The style, tone, and complexity of the sample data should be different.
# 9. If the sample data is all the same, then paraphrase the sample data to make it different.

# Examples:
# Task Description: Identify the sentiment of the text
# Human Input: Identify the sentiment of the text
# Output: [{{"text": "The weather was gloomy, with heavy clouds looming over the city, but there was no rain.", "sentiment": "negative"}}, ...]

# Task Description: Translate the text from English to French
# Human Input: Translate the text from English to French
# Output: [{{"text": "The weather was gloomy, with heavy clouds looming over the city, but there was no rain.", "translation": "Le temps était mauvais, avec des nuages lourds qui se posaient sur la ville, mais il n'y avait pas de pluie."}}]

# Task Description: Summarize the text
# Human Input: Summarize the text
# Output: [{{"text": "The weather was gloomy, with heavy clouds looming over the city, but there was no rain.", "summary": "The weather was gloomy, with heavy clouds looming over the city, but there was no rain."}}, ...]

# Task Description: Identify the entities in the text
# Human Input: Identify the entities in the text
# Output: [{{"text": "The weather was gloomy, with heavy clouds looming over the city, but there was no rain.", "entities": ["weather", "clouds", "rain"]}}, ...]

# Based on the above examples, generate sample data for the following task description:
# Task Description: {task_description}
# Human Input: {human_input}
# Output:"""

# def generate_sample_data_from_task_description_and_human_input(task_description: str, human_input: str) -> str:

#     return f"""
#     You are a meticulous and creative assistant tasked with generating sample data based on a provided task description and human input. The goal is to create diverse, relevant, and accurate sample data in JSON format.

#     Instructions:
#     1. If the human input already contains sample data, extract and use that sample data.
#     2. If the human input does not provide sample data, generate 3 examples based on the task description.
#     3. Ensure the examples are as diverse and detailed as possible while remaining aligned with the task description.
#     4. Format all generated data in proper JSON format.
#     5. Most importantly, make sure the sample data is as diverse as possible.

#     Task Description: {task_description}
#     Human Input: {human_input}

#     Output:
#     - 3 JSON-formatted examples of sample data. Make it a list of dictionaries. 
#     """

# def generate_task_description_from_sample_data(sample_data: str) -> str:

#     return f"""
#     You are a helpful assistant that generates a task description from a given sample data.
#     Sample data: {sample_data}

#     Generate a task description that would be relevant to the sample data. Output the task description in a string.
#     Restrict the task description to one or two lines. Keep the task description concise and to the point andas generic as possible.
#     """

# def generate_task_description_from_sample_data(sample_data: str) -> str:

#     return f"""
#     You are a thoughtful assistant specializing in generating task descriptions from given sample data.

#     Sample Data: {sample_data}

#     Your task is to:
#     1. Extract and articulate a concise, relevant task description based on the sample data.
#     2. Restrict the task description to one or two lines, ensuring it is concise, clear, and precise.
#     3. Generalize the task description to make it broadly applicable while maintaining relevance to the sample data.
#     4. Generate the task description in second person.

#     Output the task description as a concise string.
#     """

# def generate_task_description_from_sample_data(sample_data: str) -> str:

#     return f"""
#     You are a thoughtful assistant specializing in generating problem statements from given sample data.

#     Your task is to:
#     1. Analyze the sample data and identify the core problem or challenge it represents. The sample data has both input and output fields. 
#     2. The problem statement should be crafted to enable an AI system to generate the desired output based on the provided input. The input and output fields are included in the sample data above.
#     3. Articulate a problem statement that defines the issue or need clearly and succinctly.
#     4. Ensure the problem statement is framed as a general challenge or opportunity for resolution.
#     5. Generate the problem statement in second person, ensuring clarity and precision.
#     6. Note: Assume the output field in the sample data doesn't exist and frame the Task Description accordingly.
#     7. Keep the task description as generic as possible.

#     Here are a few examples of Sample Data and Task Descriptions:

#     Sample Data: [{{"text": "Given the text: 'The weather was gloomy, with heavy clouds looming over the city, but there was no rain.', classify the sentiment as positive, negative, or neutral.","sentiment": "The sentiment is negative."}}]
#     Task Description: Given the text, classify the sentiment as positive, negative, or neutral.

#     Sample Data: [{{"text": "Translate the following English sentence to French: 'The cat is sleeping on the couch.'", "target_text": "Le chat dort sur le canapé."}}]
#     Task Description: Translate the sentence from English to French.

#     Sample Data: [{{"text": "Summarize the following passage: 'Artificial Intelligence has significantly impacted various industries, from healthcare to finance. It enables automation of tasks, improves decision-making processes, and opens new opportunities for innovation.'", "summary": "AI has transformed industries by enabling automation, enhancing decision-making, and fostering innovation."}}]
#     Task Description: Summarize the passage.

#     Sample Data: {sample_data}
#     Task Description:"""

def generate_task_description_from_sample_data(sample_data: str) -> str:
    return f"""
    You are an AI task analyst. Given a JSON data sample, analyze it to identify:
    
    1. TASK TYPE: First identify the fundamental task type (e.g., Classification, Question-Answering, Translation, Summarization, Math Problem, etc.)
    
    2. INPUT-OUTPUT STRUCTURE:
       - Identify all input fields in the JSON
       - Identify the target/output field(s)
       - Note the relationship between input and output
    
    3. TASK DESCRIPTION:
       - Write a clear, concise description of what needs to be done
       - Focus on the transformation from input to desired output
       - Avoid mentioning the specific field names from the JSON
       - Make it generic enough to apply to similar examples
    
    Examples:
    
    Sample Data: {{"question": "What is the capital of France?", "answer": "Paris"}}
    Analysis:
    - Task Type: Question Answering (QA)
    - Input Fields: question
    - Output Field: answer
    - Task Description: Given a question, provide a relevant answer. If answer cannot be obtained return "Cannot answer question"
    
    Sample Data: {{"text": "The weather is terrible today.", "label": "negative"}}
    Analysis:
    - Task Type: Sentiment Classification
    - Input Fields: text
    - Output Field: label
    - Task Description: Analyze the given text and classify its sentiment as positive, negative, or neutral.
    
    Now analyze this sample:
    {sample_data}
    
    Provide your analysis following the same structure above.
    """

def generate_output_format_from_task_description_and_sample_data(task_description: str, sample_data: str) -> str:

    return f"""
    You are a helpful assistant that recommends an output format from a given task description and sample data.
    Task description: {task_description}
    Sample data: {sample_data}

    Generate an output format that would be relevant to the task description and sample data. Restrict the output format to the following options: json, text, html, markdown, csv, xml, yaml, html, markdown, csv, xml, yaml.
    Do not include any explanation in the output. Just the output format.
    """

def generate_style_guide_from_task_description_and_sample_data(task_description: str, sample_data: str) -> str:

    return f"""
    You are a helpful assistant that generates a style guide from a given task description and sample data.
    Task description: {task_description}
    Sample data: {sample_data}

    style guide is a set of rules that the model should follow to generate the output. Like tone, style, etc.

    Generate a style guide that would be relevant to the task description and sample data. Restrict the style guide to the following options: formal, informal, technical, creative, academic, business, legal, medical, scientific, etc.
    Do not include any explanation in the output. Just the style guide. Keep the style guide short and concise.
    """

def generate_constraints_from_task_description_and_sample_data(task_description: str, sample_data: str) -> str:

    return f"""
    You are a helpful assistant that generates constraints from a given task description and sample data.
    Task description: {task_description}
    Sample data: {sample_data}

    constraints are the limitations that the model should follow to generate the output. Like the maximum length of the output, etc.

    Generate constraints that would be relevant to the task description and sample data. Restrict the constraints to the following options: maximum length of the output, maximum number of tokens, maximum number of characters, etc.
    Do not include any explanation in the output. Just the constraints. Keep the constraints short and concise.
    """

def generate_task_type_from_task_description_and_sample_data(task_description: str, sample_data: str) -> str:

    return f"""
    You are a helpful assistant that generates a task type from a given task description and sample data.
    Task description: {task_description}
    Sample data: {sample_data}

    task type is the type of task that the model should perform. Like classification, qa, generation, translation.

    Generate a task type that would be relevant to the task description and sample data. Restrict the task type to the following options: classification, qa, generation, translation.
    Do not include any explanation in the output. Just the task type. Output the task type in a string.
    Example: classification
    """

def generate_input_fields_from_task_description_and_sample_data(task_description: str, sample_data: str) -> str:

    return f"""
    You are a helpful assistant that identifies input fields in the sample data based on task description.
    Task description: {task_description}
    Sample data: {sample_data}

    For the above task description which fields in the sample data will be the input fields?
    Do not include any fields that are not part of the sample data or are not relevant to the task description. Output the input fields in a list of strings.
    Example: ["input_field_1"]
    """

def generate_output_fields_from_task_description_and_sample_data(task_description: str, sample_data: str) -> str:

    return f"""
    You are a helpful assistant that identifies output fields in the sample data based on task description.
    Task description: {task_description}
    Sample data: {sample_data}

    For the above task description which fields in the sample data will be the output fields?
    Do not include any fields that are not part of the sample data or are not relevant to the task description. Output the output fields in a list of strings.
    Example: ["output_field_1"]
    """

# def generate_dspy_module_from_task_description_and_sample_data(task_description: str, sample_data: str) -> str:

#     return f"""
#     You are a helpful assistant that selects a dspy module from a given task description and sample data.
#     Task description: {task_description}
#     Sample data: {sample_data}

#     Here are the dspy modules that are available and their description: {dspy_modules}

#     Make sure you select only one module from the above list. If you are not sure, select dspy.Predict. 
#     Do not include any explanation in the output. Just the module name.
#     """

def generate_dspy_module_from_task_description_and_sample_data(task_description: str, sample_data: str) -> str:
    dspy_modules = {
        "dspy.Predict": "Basic predictor. Does not modify the signature. Handles the key forms of learning (i.e., storing the instructions and demonstrations and updates to the LM).",
        "dspy.ChainOfThought": "Teaches the LM to think step-by-step before committing to the signature's response.",
        "dspy.ProgramOfThought": "Teaches the LM to output code, whose execution results will dictate the response.",
        "dspy.ReAct": "An agent that can use tools to implement the given signature."
    }
    
    # Convert modules dictionary to formatted string
    formatted_modules = "\n".join([f"- {module}: {description}" for module, description in dspy_modules.items()])
    
    return f"""
    You are an expert DSPy module selector that accurately identifies the most appropriate module for different NLP and ML tasks.

    Your task is to analyze the given task description and sample data, then select the single most appropriate DSPy module that would best implement this functionality.

    Task description: {task_description}
    Sample data: {sample_data}

    Available DSPy modules:
    {formatted_modules}

    Module selection guidelines:
    - dspy.Predict: Use for straightforward tasks where the model can directly produce the desired output without special reasoning processes.
    - dspy.ChainOfThought: Use for complex reasoning tasks that benefit from step-by-step thinking before arriving at an answer.
    - dspy.ProgramOfThought: Use for tasks that involve computation, data manipulation, or algorithm execution where generating and running code would be beneficial.
    - dspy.ReAct: Use for tasks that require external tool use, information lookup, or multi-step interaction with external systems.

    Few-shot examples:

    Example 1:
    Task description: Classify the sentiment of movie reviews as positive, negative, or neutral.
    Sample data: {{"review": "The film was a complete waste of time with terrible acting and a nonsensical plot.", "sentiment": "negative"}}
    Selected module: dspy.Predict

    Example 2:
    Task description: Solve mathematical word problems by determining the correct equation to use and calculating the answer.
    Sample data: {{"problem": "If a train travels at 60 mph for 3 hours and then increases speed to 80 mph for 2 more hours, what is the total distance traveled?", "solution": "For the first segment: distance = 60 mph × 3 h = 180 miles. For the second segment: distance = 80 mph × 2 h = 160 miles. Total distance = 180 miles + 160 miles = 340 miles.", "answer": "340 miles"}}
    Selected module: dspy.ChainOfThought

    Example 3:
    Task description: Calculate statistical measures for a dataset including mean, median, mode, and standard deviation.
    Sample data: {{"data": [12, 15, 18, 22, 15, 10, 9, 15, 22], "statistics": {{"mean": 15.33, "median": 15, "mode": 15, "std_dev": 4.55}}}}
    Selected module: dspy.ProgramOfThought

    Example 4:
    Task description: Search for information about specific companies and compile key business metrics and recent news.
    Sample data: {{"company": "Tesla", "report": {{"industry": "Automotive/Clean Energy", "market_cap": "$752.29B", "recent_news": "Tesla announced new Gigafactory expansion in Austin, Texas.", "key_competitors": ["Ford", "GM", "Rivian", "Lucid"]}}}}
    Selected module: dspy.ReAct

    Based on the task description and sample data provided, select the most appropriate module.
    
    Output only the module name without any explanation or additional text:
    """

# def extract_task_description_from_human_input(human_input: str) -> str:

#     return f"""You are a meticulous assistant specializing in generating detailed task descriptions from human inputs.

# Human Input: {human_input}

# Your task is to:
# 1. Extract the most detailed and comprehensive task description from the human input, ensuring it captures all possible nuances and requirements.
# 2. Generate the task description based on the human input. The task description should be in second person.
# 3. If the Human Input has Feedback in it, then strictly follow the feedback and do not deviate from it.

# Output the task description as a detailed string."""

def generate_sample_data_from_task_description_and_raw_input_with_question_and_context(
    task_description: str, human_input: str, question: str = "", context: str = ""
) -> str:
    
    question_context_section = ""
    if question or context:
        question_context_section = "\n\nAdditional Information:"
        if question:
            question_context_section += f"\nQuestion: {question}"
        if context:
            question_context_section += f"\nContext: {context}"
    
    return f"""You are a meticulous and creative assistant tasked with generating diverse, high-quality sample data based on a provided task description and human input. Your goal is to create structured, relevant, and realistic sample data in JSON format that could be used for AI training and evaluation.

Instructions:

1. First, carefully analyze the task description, human input{', question, and context' if question_context_section else ''} to determine:
   - The core objective of the task
   - The expected input/output relationship
   - Any specific formats, constraints, or edge cases that should be represented

2. If the human input already contains sample data:
   - Extract and refine the existing sample data
   - Ensure it follows proper JSON formatting
   - Add additional examples if the provided samples are too limited

3. If the human input does not provide sample data:
   - Generate 3-5 diverse examples that comprehensively cover the task domain
   - Include examples of varying complexity and different edge cases
   - Ensure examples reflect realistic usage scenarios
   - Ensure each sample has input and output fields

4. Choose JSON field names that are:
   - Contextually appropriate to the domain
   - Consistent with standard naming conventions
   - Self-descriptive and intuitive

5. Structure your JSON based on the task type:
   - Classification tasks: "input" (or domain-specific name) and "label"/"category"/"class"
   - Generation tasks: "prompt"/"context" and "response"/"output"/"generation"
   - Extraction tasks: "text"/"document" and "extracted_items"/"entities"/"key_points"
   - Comparison tasks: Appropriate entity names and "comparison"/"similarity"/"difference"/"relationship"
   - Multi-step tasks: Consider nested structures that capture intermediate steps
   - Question answering tasks: "question", "context", and "answer"
   - Summarization tasks: "text"/"document" and "summary"

6. Ensure diversity across examples in:
   - Content topics and domains
   - Complexity levels (simple, moderate, complex)
   - Length and structure
   - Edge cases and special conditions
   - Linguistic style and tone (formal, casual, technical, etc.)

7. For multi-turn interactions or processes:
   - Include examples with different numbers of turns/steps
   - Show progression through the task

8. Format the output as a valid, properly indented JSON list of dictionaries{question_context_section}

Examples:
Task Description: You are tasked with analyzing text content to determine the emotional sentiment expressed within. Your goal is to carefully evaluate each piece of text and classify it according to the emotional tone it conveys. You should consider the overall impression of the text, accounting for nuanced language, potential sarcasm, and contextual cues that might influence interpretation. For each text sample, provide a sentiment classification (positive, negative, or neutral) and indicate the intensity or confidence level of this classification as a numerical value. This analysis should be applicable to various text lengths and styles, from concise statements to more elaborate expressions.
Human Input: Identify the sentiment of the text
Output: [
  {{"text": "The weather was gloomy today.", "sentiment": "negative", "intensity": 0.6}},
  {{"text": "I just got promoted at work!", "sentiment": "positive", "intensity": 0.9}},
  {{"text": "The restaurant was neither good nor bad.", "sentiment": "neutral", "intensity": 0.2}}
]

Task Description: You are tasked with developing customized nutritional meal plans that accommodate specific dietary restrictions while supporting fitness objectives. For each plan, you should create a comprehensive daily breakdown that includes multiple meals tailored to meet the nutritional requirements of individuals with gluten intolerance who are simultaneously working to build muscle mass. Each meal plan should specify detailed ingredients that comply with gluten-free dietary needs, provide precise macronutrient calculations to support muscle development, include caloric information for energy tracking, and offer practical preparation time estimates. The meal structures should be varied and balanced across breakfast, lunch, dinner, and strategic snacks to maintain consistent protein intake throughout the day while ensuring all ingredients are completely free of gluten contamination.
Human Input: I need meal plans for someone with gluten intolerance who is also trying to build muscle
Output: [
  {{
    "day": 1,
    "dietary_restrictions": ["gluten-free"],
    "fitness_goal": "muscle building",
    "meals": [
      {{
        "type": "breakfast",
        "name": "Protein-Packed Smoothie Bowl",
        "ingredients": ["greek yogurt", "banana", "berries", "gluten-free granola", "chia seeds", "protein powder"],
        "macros": {{"protein": 35, "carbs": 45, "fat": 12}},
        "total_calories": 428,
        "prep_time_minutes": 10
      }},
      {{
        "type": "lunch",
        "name": "Quinoa Bowl with Grilled Chicken",
        "ingredients": ["quinoa", "grilled chicken breast", "avocado", "cherry tomatoes", "cucumber", "olive oil", "lemon juice"],
        "macros": {{"protein": 42, "carbs": 38, "fat": 18}},
        "total_calories": 482,
        "prep_time_minutes": 25
      }},
      {{
        "type": "dinner",
        "name": "Baked Salmon with Sweet Potato and Vegetables",
        "ingredients": ["salmon fillet", "sweet potato", "broccoli", "olive oil", "garlic", "herbs"],
        "macros": {{"protein": 38, "carbs": 35, "fat": 22}},
        "total_calories": 490,
        "prep_time_minutes": 35
      }},
      {{
        "type": "snack",
        "name": "Protein Shake with Nuts",
        "ingredients": ["whey protein isolate", "almond milk", "mixed nuts"],
        "macros": {{"protein": 28, "carbs": 8, "fat": 14}},
        "total_calories": 266,
        "prep_time_minutes": 3
      }}
    ]
  }}
]

Task Description: Your task is to answer questions based on the provided context. The questions will vary in complexity, from simple fact retrieval to more nuanced inquiries requiring inference and synthesis of information. You must carefully analyze the context to extract relevant information, resolve references, and provide accurate, concise answers that directly address the question. Your responses should be fully supported by the context without introducing external information or assumptions beyond what can be reasonably inferred from the provided text.
Human Input: Question answering based on context
Question: What caused the economic recession of 2008?
Context: The financial crisis of 2008, one of the most severe economic downturns since the Great Depression, was primarily triggered by the collapse of the U.S. housing market. Years of risky lending practices, especially in the subprime mortgage sector, led to a housing bubble. When this bubble burst, it caused massive defaults on mortgage payments. Financial institutions that had heavily invested in mortgage-backed securities and other complex financial instruments faced catastrophic losses. The collapse of Lehman Brothers in September 2008 sent shockwaves through global financial markets, freezing credit markets and precipitating a widespread economic contraction.
Output: [
  {{
    "question": "What caused the economic recession of 2008?",
    "context": "The financial crisis of 2008, one of the most severe economic downturns since the Great Depression, was primarily triggered by the collapse of the U.S. housing market. Years of risky lending practices, especially in the subprime mortgage sector, led to a housing bubble. When this bubble burst, it caused massive defaults on mortgage payments. Financial institutions that had heavily invested in mortgage-backed securities and other complex financial instruments faced catastrophic losses. The collapse of Lehman Brothers in September 2008 sent shockwaves through global financial markets, freezing credit markets and precipitating a widespread economic contraction.",
    "answer": "The economic recession of 2008 was caused by the collapse of the U.S. housing market following a housing bubble created by years of risky lending practices in the subprime mortgage sector. When the bubble burst, it led to massive mortgage defaults, catastrophic losses for financial institutions that had invested heavily in mortgage-backed securities, and a credit market freeze following the collapse of Lehman Brothers in September 2008."
  }},
  {{
    "question": "When did Lehman Brothers collapse?",
    "context": "The financial crisis of 2008, one of the most severe economic downturns since the Great Depression, was primarily triggered by the collapse of the U.S. housing market. Years of risky lending practices, especially in the subprime mortgage sector, led to a housing bubble. When this bubble burst, it caused massive defaults on mortgage payments. Financial institutions that had heavily invested in mortgage-backed securities and other complex financial instruments faced catastrophic losses. The collapse of Lehman Brothers in September 2008 sent shockwaves through global financial markets, freezing credit markets and precipitating a widespread economic contraction.",
    "answer": "Lehman Brothers collapsed in September 2008."
  }}
]

Task Description: Your task is to summarize long documents or passages of text into concise, informative summaries that capture the essential information and main points. Each summary should accurately represent the key ideas, arguments, facts, and conclusions from the original text while significantly reducing length. You should prioritize the most important information while omitting unnecessary details, examples, or repetitive content. The summaries should maintain the original tone, perspective, and intended meaning of the source material without introducing new ideas or personal interpretations. Each summary should be coherent and well-structured, with logical flow and connections between ideas, even when condensing complex content.
Human Input: Summarize this article
Context: The rapid evolution of artificial intelligence (AI) in recent years has sparked both excitement and concern across various sectors of society. On one hand, AI technologies have demonstrated remarkable capabilities in areas such as healthcare, where machine learning algorithms can now detect certain cancers with accuracy rivaling that of trained radiologists. Similarly, in environmental science, AI systems are helping researchers model climate change patterns and identify potential solutions with unprecedented precision. These advancements suggest a future where complex problems might be addressed more effectively through human-AI collaboration. On the other hand, the acceleration of AI development has raised significant ethical and societal questions. Issues of privacy have become paramount as AI systems require vast amounts of data, often personal in nature, to function effectively. The potential for algorithmic bias has also emerged as a critical concern, with multiple studies demonstrating how AI systems can inadvertently perpetuate or even amplify existing societal prejudices when trained on biased data sets. Perhaps most pressing are the questions surrounding automation and employment. While some economists argue that AI will create new job categories that we cannot yet envision, others point to historical examples where technological advancement led to significant workforce displacement. This debate is particularly relevant in sectors like transportation, where autonomous vehicle technology threatens to disrupt millions of driving jobs worldwide. The governance of AI presents another challenge. Currently, regulatory frameworks lag significantly behind technological development, creating a situation where powerful AI systems are being deployed with limited oversight. This has prompted calls from various stakeholders, including many leading AI researchers themselves, for thoughtful regulation that can mitigate risks while allowing beneficial innovation to continue. As we navigate this complex landscape, one thing remains clear: the impact of AI will not be determined by the technology alone, but by the human choices that shape its development and application. The coming decades will require careful consideration of how we can harness the potential of AI while ensuring it serves humanity's best interests and reflects our core values.
Output: [
  {{
    "context": "The rapid evolution of artificial intelligence (AI) in recent years has sparked both excitement and concern across various sectors of society. On one hand, AI technologies have demonstrated remarkable capabilities in areas such as healthcare, where machine learning algorithms can now detect certain cancers with accuracy rivaling that of trained radiologists. Similarly, in environmental science, AI systems are helping researchers model climate change patterns and identify potential solutions with unprecedented precision. These advancements suggest a future where complex problems might be addressed more effectively through human-AI collaboration. On the other hand, the acceleration of AI development has raised significant ethical and societal questions. Issues of privacy have become paramount as AI systems require vast amounts of data, often personal in nature, to function effectively. The potential for algorithmic bias has also emerged as a critical concern, with multiple studies demonstrating how AI systems can inadvertently perpetuate or even amplify existing societal prejudices when trained on biased data sets. Perhaps most pressing are the questions surrounding automation and employment. While some economists argue that AI will create new job categories that we cannot yet envision, others point to historical examples where technological advancement led to significant workforce displacement. This debate is particularly relevant in sectors like transportation, where autonomous vehicle technology threatens to disrupt millions of driving jobs worldwide. The governance of AI presents another challenge. Currently, regulatory frameworks lag significantly behind technological development, creating a situation where powerful AI systems are being deployed with limited oversight. This has prompted calls from various stakeholders, including many leading AI researchers themselves, for thoughtful regulation that can mitigate risks while allowing beneficial innovation to continue. As we navigate this complex landscape, one thing remains clear: the impact of AI will not be determined by the technology alone, but by the human choices that shape its development and application. The coming decades will require careful consideration of how we can harness the potential of AI while ensuring it serves humanity's best interests and reflects our core values.",
    "summary": "Artificial intelligence has rapidly evolved, offering promising advancements in healthcare and environmental science while raising significant concerns. Ethical issues include privacy concerns due to data requirements, potential algorithmic bias that could amplify societal prejudices, and workforce disruption from automation, particularly in sectors like transportation. Regulatory frameworks currently lag behind technological development, prompting calls for thoughtful oversight that balances risk mitigation with innovation. Ultimately, AI's impact will be shaped by human choices in its development and application, requiring careful consideration to ensure the technology serves humanity's best interests and reflects core values."
  }},
  {{
    "context": "Recent studies on the effects of meditation on brain structure and function have revealed promising implications for mental health treatment. In a longitudinal study conducted over eight weeks, researchers at the University of Wisconsin-Madison found that regular meditation practice, consisting of just 20 minutes daily, led to measurable increases in gray matter density in regions of the brain associated with attention, emotional regulation, and empathy. Functional MRI scans showed reduced activity in the amygdala, the brain's threat detection center, suggesting decreased stress reactivity among participants. Particularly noteworthy was the finding that these neurological changes correlated with participants' self-reported improvements in anxiety and depression symptoms, with an average reduction of 38% on standardized psychological assessments. The study's control group, which engaged in relaxation exercises without meditation's mindfulness component, showed significantly smaller improvements, indicating that meditation's effects extend beyond mere relaxation. These findings align with previous research suggesting meditation's potential as a complementary treatment for various mental health conditions. However, researchers caution that while promising, meditation should be viewed as one component of a comprehensive treatment approach rather than a standalone solution for clinical mental health disorders.",
    "summary": "Research from the University of Wisconsin-Madison demonstrates that just 20 minutes of daily meditation over eight weeks increases gray matter density in brain regions associated with attention, emotional regulation, and empathy. Brain scans revealed reduced amygdala activity, indicating decreased stress reactivity, while participants reported a 38% reduction in anxiety and depression symptoms on standardized assessments. The control group engaging only in relaxation exercises showed significantly smaller improvements, suggesting meditation's benefits extend beyond relaxation. While promising as a complementary treatment for mental health conditions, researchers emphasize that meditation should be part of a comprehensive treatment approach rather than a standalone solution for clinical disorders."
  }}
]

Task Description: Your task is to classify and categorize text or documents according to predefined labeling systems or taxonomies. For each document or text excerpt, you should carefully analyze the content and assign the most appropriate category labels from the available options. Your classifications should be consistent with the provided taxonomy definitions and examples, ensuring that similar content receives similar categorization. You should be able to identify key elements within the text that indicate specific categories, recognize relevant patterns, and understand the distinguishing features between different categories. Additionally, you should maintain sensitivity to context and cultural nuances that might affect classification decisions. The goal is to create accurate, consistent categorizations that could be used for organizing, filtering, and analyzing large collections of textual information.
Human Input: Classify news articles by topic
Question: What category does this article belong to?
Context: The European Central Bank announced today it would hold interest rates steady at 3.5%, defying market expectations of a quarter-point reduction. ECB President Christine Lagarde cited persistent inflationary pressures and stronger-than-expected quarterly growth figures as key factors in the decision. "While we have seen improvement in the inflation outlook, core inflation remains elevated, and we need convincing evidence of a sustained return to our target before adjusting our policy stance," Lagarde stated during the press conference following the announcement. The euro strengthened against major currencies immediately after the news, while European stock markets showed mixed reactions. Economists now expect the ECB to potentially begin easing monetary policy in the third quarter, assuming inflation continues its downward trajectory.
Output: [
  {{
    "question": "What category does this article belong to?",
    "context": "The European Central Bank announced today it would hold interest rates steady at 3.5%, defying market expectations of a quarter-point reduction. ECB President Christine Lagarde cited persistent inflationary pressures and stronger-than-expected quarterly growth figures as key factors in the decision. "While we have seen improvement in the inflation outlook, core inflation remains elevated, and we need convincing evidence of a sustained return to our target before adjusting our policy stance," Lagarde stated during the press conference following the announcement. The euro strengthened against major currencies immediately after the news, while European stock markets showed mixed reactions. Economists now expect the ECB to potentially begin easing monetary policy in the third quarter, assuming inflation continues its downward trajectory.",
    "category": "Business & Economy",
    "subcategory": "Central Banking & Monetary Policy",
    "confidence": 0.95,
    "key_indicators": ["European Central Bank", "interest rates", "inflationary pressures", "monetary policy", "Christine Lagarde"]
  }},
  {{
    "question": "What category does this article belong to?",
    "context": "Scientists at the University of California, Berkeley have developed a new CRISPR-based technique that can detect and potentially correct genetic mutations with unprecedented precision. The method, dubbed CRISPR-Scan, combines traditional CRISPR-Cas9 technology with advanced machine learning algorithms to identify off-target effects before they occur. In laboratory tests with human cell lines, the new approach reduced unintended genetic modifications by over 96% compared to conventional CRISPR methods. "This represents a significant step toward making gene editing safe enough for human therapeutic applications," said Dr. Jennifer Doudna, co-inventor of CRISPR technology and leader of the research team. The breakthrough could accelerate the development of treatments for genetic disorders like sickle cell anemia, cystic fibrosis, and Huntington's disease. The team has published their findings in the latest issue of Nature Biotechnology and has filed for patents on the new technology.",
    "category": "Science & Technology",
    "subcategory": "Biotechnology & Genetic Engineering",
    "confidence": 0.98,
    "key_indicators": ["CRISPR", "genetic mutations", "gene editing", "Dr. Jennifer Doudna", "genetic disorders", "Nature Biotechnology"]
  }}
]

Based on the above examples, generate sample data for the following task description:
Task Description: {task_description}
Human Input: {human_input}{question_context_section}
Output:"""

def complete_the_main_example_simple(task_description: str, task: str, question: str = "", context: str = "") -> str:
    # Build optional fields section
    additional_info = ""
    if question:
        additional_info += f"Question: {question}\n"
    if context:
        additional_info += f"Context: {context}\n"

    return f"""Based on the detailed task description, short task description, question(if provided), and context, provide a expected output for the task in JSON format.

Detailed Task Description: {task_description}
Short task description: {task}
{additional_info}
Output:"""

def get_expected_answer_from_sample_data(task_description: str, sample_data: str) -> str:
    return f"""Solve the given task based on the sample data.

Note: Strictly, do not alter the structure of sample data. Only add the missing expected results fields if they are not present in the sample data. For example, if it's summarization related task, only add the missing `summary` fields if they are not present in the sample data.

Instructions:
1. Analyze the sample data and task description carefully
2. Identify which fields need to be present in the expected output fields. See if the output fields already present in the sample data. If not, generate the expected output fields.
3. Format your response as a valid JSON object containing only these output fields

Examples:

Example 1:
Task: Classify the sentiment of customer reviews
Sample Data: {{"text": "This product completely failed after just two uses."}}
Expected Answer With Sample Data: {{"text": "This product completely failed after just two uses.", "sentiment": "negative"}}

Example 2:
Task: Answer questions based on provided context
Sample Data: {{"question": "What is the capital of France?", "context": "France is a country in Western Europe with several overseas territories. Its capital is Paris, which is known for the Eiffel Tower and the Louvre Museum."}}
Expected Answer With Sample Data: {{"question": "What is the capital of France?", "context": "France is a country in Western Europe with several overseas territories. Its capital is Paris, which is known for the Eiffel Tower and the Louvre Museum.", "answer": "Paris"}}

Example 3:
Task: Summarize articles into concise versions
Sample Data: {{"article": "Artificial intelligence has rapidly evolved in recent years, transforming industries from healthcare to finance. Machine learning algorithms now power recommendation systems, automated diagnosis tools, and predictive analytics platforms. These technologies promise increased efficiency and novel solutions to complex problems."}}
Expected Answer With Sample Data: {{"article": "Artificial intelligence has rapidly evolved in recent years, transforming industries from healthcare to finance. Machine learning algorithms now power recommendation systems, automated diagnosis tools, and predictive analytics platforms. These technologies promise increased efficiency and novel solutions to complex problems.", "summary": "AI has advanced quickly, changing healthcare and finance through machine learning applications in recommendations, diagnostics, and predictions, offering efficiency gains and new approaches to difficult challenges."}}

Example 4:
Task: Extract key entities from text
Sample Data: {{"text": "Apple Inc. announced their new iPhone model will be released next Friday in San Francisco, according to CEO Tim Cook."}}
Expected Answer With Sample Data: {{"text": "Apple Inc. announced their new iPhone model will be released next Friday in San Francisco, according to CEO Tim Cook.", "entities": [{{"entity": "Apple Inc.", "type": "ORGANIZATION"}}, {{"entity": "iPhone", "type": "PRODUCT"}}, {{"entity": "San Francisco", "type": "LOCATION"}}, {{"entity": "Tim Cook", "type": "PERSON"}}, {{"entity": "next Friday", "type": "DATE"}}]}}

Your Task:
Task: {task_description}
Sample Data: {sample_data}
Expected Answer With Sample Data:"""

def complete_the_main_example( task: str, question: str = "", context: str = "") -> str:
    # Build optional fields section
    additional_info = ""
    if question:
        additional_info += f"Question: {question}\n"
    if context:
        additional_info += f"Context: {context}\n"

    return f"""Based on the detailed task description, short task description, question(if available), and context, provide a complete solution to the task.
Note that question or context might be absent in some cases, but you should still provide the most appropriate response based on available information.

# Reference Examples:

## Example 1: Sentiment Analysis
Short task description: Identify the sentiment of the text
Question: The weather was gloomy today.
Output: {{"text": "The weather was gloomy today.", "sentiment": "negative", "intensity": 0.6}}

## Example 2: Question Answering
Short task description: Question answering based on context
Context: The financial crisis of 2008, one of the most severe economic downturns since the Great Depression, was primarily triggered by the collapse of the U.S. housing market. Years of risky lending practices, especially in the subprime mortgage sector, led to a housing bubble. When this bubble burst, it caused massive defaults on mortgage payments. Financial institutions that had heavily invested in mortgage-backed securities and other complex financial instruments faced catastrophic losses. The collapse of Lehman Brothers in September 2008 sent shockwaves through global financial markets, freezing credit markets and precipitating a widespread economic contraction.
Question: What caused the economic recession of 2008?
Output: {{
  "question": "What caused the economic recession of 2008?",
  "context": "The financial crisis of 2008, one of the most severe economic downturns since the Great Depression, was primarily triggered by the collapse of the U.S. housing market. Years of risky lending practices, especially in the subprime mortgage sector, led to a housing bubble. When this bubble burst, it caused massive defaults on mortgage payments. Financial institutions that had heavily invested in mortgage-backed securities and other complex financial instruments faced catastrophic losses. The collapse of Lehman Brothers in September 2008 sent shockwaves through global financial markets, freezing credit markets and precipitating a widespread economic contraction.",
  "answer": "The economic recession of 2008 was caused by the collapse of the U.S. housing market following a housing bubble created by years of risky lending practices in the subprime mortgage sector. When the bubble burst, it led to massive mortgage defaults, catastrophic losses for financial institutions that had invested heavily in mortgage-backed securities, and a credit market freeze following the collapse of Lehman Brothers in September 2008."
}}

## Example 3: Text Summarization
Short task description: Summarize this article
Context: Climate change poses one of the most significant challenges to global biodiversity. Recent studies indicate that rising temperatures are altering habitats faster than many species can adapt. In the Arctic, sea ice reduction has disrupted feeding patterns for polar bears, forcing them to spend more time on land where food sources are less abundant. Meanwhile, coral reefs worldwide are experiencing unprecedented bleaching events due to ocean warming and acidification. Scientists estimate that over 50% of the world's coral reefs have been damaged, threatening the roughly 25% of marine species that depend on these ecosystems. While some species demonstrate remarkable adaptive capacity, many lack the genetic variability or reproductive rates necessary to evolve quickly enough. Conservation efforts now increasingly focus on identifying and protecting climate refugia—areas that may remain relatively stable despite changing conditions—while also establishing migration corridors to facilitate species movement toward more favorable environments.
Output: {{
  "context": "Climate change poses one of the most significant challenges to global biodiversity. Recent studies indicate that rising temperatures are altering habitats faster than many species can adapt. In the Arctic, sea ice reduction has disrupted feeding patterns for polar bears, forcing them to spend more time on land where food sources are less abundant. Meanwhile, coral reefs worldwide are experiencing unprecedented bleaching events due to ocean warming and acidification. Scientists estimate that over 50% of the world's coral reefs have been damaged, threatening the roughly 25% of marine species that depend on these ecosystems. While some species demonstrate remarkable adaptive capacity, many lack the genetic variability or reproductive rates necessary to evolve quickly enough. Conservation efforts now increasingly focus on identifying and protecting climate refugia—areas that may remain relatively stable despite changing conditions—while also establishing migration corridors to facilitate species movement toward more favorable environments.",
  "summary": "Climate change is rapidly altering habitats beyond many species' adaptation capabilities, with Arctic sea ice reduction affecting polar bear feeding patterns and ocean warming damaging over 50% of coral reefs worldwide, threatening 25% of marine species. While some species can adapt, many lack the necessary genetic variability or reproductive rates for rapid evolution. Conservation strategies now focus on protecting climate refugia and establishing migration corridors to help species access more favorable environments."
}}

Strictly, output your answer in JSON format. It should cover all the information provided in context(if provided) and question(if provided) and the answer(you need to generate) in JSON format.

# Your Task:
Short task description: {task}
{additional_info}
Output:"""

def generate_sample_data_from_sample_data(task: str, complete_sample: str) -> str:
    
    return f"""You are a meticulous and creative assistant tasked with generating diverse, high-quality sample data based on a provided task description and sample data. Your goal is to create structured, relevant, and realistic data in JSON format that could be used for AI training and evaluation.
The data you generate should be based on the sample data provided and should strictly adhere to the format of the sample data.

# Sample Data:
{complete_sample}

# Task Description:
{task}

Instructions:

1. First, carefully analyze both the task description and sample data to determine:
   - The core objective of the task
   - The expected input/output relationship
   - Any specific formats, constraints, or edge cases that should be represented

2. From the sample data, extract and refine the existing data
   - Ensure it follows proper JSON formatting
   - Add additional examples if the provided samples are too limited

3. Based on task description and sample data, generate 3-5 diverse examples that comprehensively cover the task domain
   - Include examples of varying complexity and different edge cases
   - Ensure examples reflect realistic usage scenarios

4. Choose JSON field names that are:
   - Contextually appropriate to the domain
   - Consistent with standard naming conventions
   - Self-descriptive and intuitive

5. Structure your JSON based on the task type:
   - Classification tasks: "input" (or domain-specific name) and "label"/"category"/"class"
   - Generation tasks: "prompt"/"context" and "response"/"output"/"generation"
   - Extraction tasks: "text"/"document" and "extracted_items"/"entities"/"key_points"
   - Comparison tasks: Appropriate entity names and "comparison"/"similarity"/"difference"/"relationship"
   - Multi-step tasks: Consider nested structures that capture intermediate steps
   - If the task description is not clear, use the sample data to generate the data

6. Ensure diversity across examples in:
   - Content topics and domains
   - Complexity levels (simple, moderate, complex)
   - Length and structure
   - Edge cases and special conditions
   - Linguistic style and tone (formal, casual, technical, etc.)

7. For multi-turn interactions or processes:
   - Include examples with different numbers of turns/steps
   - Show progression through the task

8. Format the output as a valid, properly indented JSON list of dictionaries

"""

def generate_sample_data_from_task_description_and_raw_input_old(task_description: str, human_input: str) -> str:


    return f"""You are a meticulous and creative assistant tasked with generating diverse, high-quality sample data based on a provided task description and human input. Your goal is to create structured, relevant, and realistic sample data in JSON format that could be used for AI training and evaluation.

Instructions:

1. First, carefully analyze both the task description and human input to determine:
   - The core objective of the task
   - The expected input/output relationship
   - Any specific formats, constraints, or edge cases that should be represented

2. If the human input already contains sample data:
   - Extract and refine the existing sample data
   - Ensure it follows proper JSON formatting
   - Add additional examples if the provided samples are too limited

3. If the human input does not provide sample data:
   - Generate 3-5 diverse examples that comprehensively cover the task domain
   - Include examples of varying complexity and different edge cases
   - Ensure examples reflect realistic usage scenarios

4. Choose JSON field names that are:
   - Contextually appropriate to the domain
   - Consistent with standard naming conventions
   - Self-descriptive and intuitive

5. Structure your JSON based on the task type:
   - Classification tasks: "input" (or domain-specific name) and "label"/"category"/"class"
   - Generation tasks: "prompt"/"context" and "response"/"output"/"generation"
   - Extraction tasks: "text"/"document" and "extracted_items"/"entities"/"key_points"
   - Comparison tasks: Appropriate entity names and "comparison"/"similarity"/"difference"/"relationship"
   - Multi-step tasks: Consider nested structures that capture intermediate steps

6. Ensure diversity across examples in:
   - Content topics and domains
   - Complexity levels (simple, moderate, complex)
   - Length and structure
   - Edge cases and special conditions
   - Linguistic style and tone (formal, casual, technical, etc.)

7. For multi-turn interactions or processes:
   - Include examples with different numbers of turns/steps
   - Show progression through the task

8. Format the output as a valid, properly indented JSON list of dictionaries

Examples:
Task Description: You are tasked with analyzing text content to determine the emotional sentiment expressed within. Your goal is to carefully evaluate each piece of text and classify it according to the emotional tone it conveys. You should consider the overall impression of the text, accounting for nuanced language, potential sarcasm, and contextual cues that might influence interpretation. For each text sample, provide a sentiment classification (positive, negative, or neutral) and indicate the intensity or confidence level of this classification as a numerical value. This analysis should be applicable to various text lengths and styles, from concise statements to more elaborate expressions.
Human Input: Identify the sentiment of the text
Output: [
  {{"text": "The weather was gloomy today.", "sentiment": "negative", "intensity": 0.6}},
  {{"text": "I just got promoted at work!", "sentiment": "positive", "intensity": 0.9}},
  {{"text": "The restaurant was neither good nor bad.", "sentiment": "neutral", "intensity": 0.2}}
]

Task Description: You are tasked with developing customized nutritional meal plans that accommodate specific dietary restrictions while supporting fitness objectives. For each plan, you should create a comprehensive daily breakdown that includes multiple meals tailored to meet the nutritional requirements of individuals with gluten intolerance who are simultaneously working to build muscle mass. Each meal plan should specify detailed ingredients that comply with gluten-free dietary needs, provide precise macronutrient calculations to support muscle development, include caloric information for energy tracking, and offer practical preparation time estimates. The meal structures should be varied and balanced across breakfast, lunch, dinner, and strategic snacks to maintain consistent protein intake throughout the day while ensuring all ingredients are completely free of gluten contamination.
Human Input: I need meal plans for someone with gluten intolerance who is also trying to build muscle
Output: [
  {{
    "day": 1,
    "dietary_restrictions": ["gluten-free"],
    "fitness_goal": "muscle building",
    "meals": [
      {{
        "type": "breakfast",
        "name": "Protein-Packed Smoothie Bowl",
        "ingredients": ["greek yogurt", "banana", "berries", "gluten-free granola", "chia seeds", "protein powder"],
        "macros": {{"protein": 35, "carbs": 45, "fat": 12}},
        "total_calories": 428,
        "prep_time_minutes": 10
      }},
      {{
        "type": "lunch",
        "name": "Quinoa Bowl with Grilled Chicken",
        "ingredients": ["quinoa", "grilled chicken breast", "avocado", "cherry tomatoes", "cucumber", "olive oil", "lemon juice"],
        "macros": {{"protein": 42, "carbs": 38, "fat": 18}},
        "total_calories": 482,
        "prep_time_minutes": 25
      }},
      {{
        "type": "dinner",
        "name": "Baked Salmon with Sweet Potato and Vegetables",
        "ingredients": ["salmon fillet", "sweet potato", "broccoli", "olive oil", "garlic", "herbs"],
        "macros": {{"protein": 38, "carbs": 35, "fat": 22}},
        "total_calories": 490,
        "prep_time_minutes": 35
      }},
      {{
        "type": "snack",
        "name": "Protein Shake with Nuts",
        "ingredients": ["whey protein isolate", "almond milk", "mixed nuts"],
        "macros": {{"protein": 28, "carbs": 8, "fat": 14}},
        "total_calories": 266,
        "prep_time_minutes": 3
      }}
    ]
  }}
]

Task Description: Your objective is to conduct comprehensive analysis of customer support interactions to extract actionable insights regarding customer satisfaction, issue resolution, and agent performance. You need to process conversational transcripts between support agents and customers, identifying primary and secondary issues raised during each interaction. For each conversation, you should evaluate sentiment progression throughout the exchange, noting initial customer emotional states and how these evolve during the interaction. You must assess agent performance metrics including response times, empathy levels, and solution effectiveness. The analysis should categorize issues by type, document resolution status, and tag conversations with relevant keywords to enable trend identification. Your output should maintain the full conversation transcript with precise timestamps while providing detailed analytical metrics that can inform support team training and process improvements.
Human Input: We need to analyze customer chat transcripts
Output: [
  {{
    "conversation_id": "CS-2023-04182",
    "customer_id": "CID-58291",
    "support_agent_id": "AGT-114",
    "timestamp": "2023-10-15T14:32:10Z",
    "duration_minutes": 12.5,
    "transcript": [
      {{
        "speaker": "system",
        "text": "Chat session initiated",
        "timestamp": "2023-10-15T14:32:10Z"
      }},
      {{
        "speaker": "agent",
        "text": "Hello! Thank you for contacting support. How may I assist you today?",
        "timestamp": "2023-10-15T14:32:15Z"
      }},
      {{
        "speaker": "customer",
        "text": "Hi, I've been charged twice for my subscription this month and I want a refund.",
        "timestamp": "2023-10-15T14:32:45Z"
      }},
      {{
        "speaker": "agent",
        "text": "I'm sorry to hear about the double charge. Let me look into that for you. Could you please confirm your email address associated with the account?",
        "timestamp": "2023-10-15T14:33:10Z"
      }},
      {{
        "speaker": "customer",
        "text": "It's customer@example.com",
        "timestamp": "2023-10-15T14:33:25Z"
      }}
    ],
    "analysis": {{
      "primary_issue": "billing_double_charge",
      "secondary_issues": ["refund_request"],
      "customer_sentiment": {{
        "initial": "frustrated",
        "final": "neutral",
        "sentiment_trajectory": [-0.6, -0.4, -0.2]
      }},
      "agent_performance": {{
        "response_time_avg_seconds": 22,
        "empathy_score": 0.8,
        "solution_effectiveness": 0.7
      }},
      "resolution": {{
        "status": "resolved",
        "action_taken": "refund_processed",
        "follow_up_required": false
      }},
      "tags": ["billing", "refund", "subscription", "double_charge"]
    }}
  }}
]

Task Description: Your task is to translate natural language database query requests into properly structured SQL statements that can be directly executed against a relational database. For each request, you must analyze the intended query objective and produce syntactically correct SQL code that accurately retrieves the requested information. You should account for the underlying database schema by identifying relevant tables, their column structures, and the relationships between them. Your SQL queries should implement appropriate table joins, filtering conditions, sorting specifications, and aggregation functions as required by the query intent. Additionally, you must provide clear explanations of how each query works, detailing the logic behind table relationships, filtering criteria, and any performance considerations. The SQL code you generate should follow best practices for readability with proper indentation and line breaks, while ensuring optimal query performance through appropriate indexing hints where necessary.
Human Input: Generate SQL queries from natural language instructions
Output: [
  {{
    "instruction": "Find all customers who made purchases over $500 in the last month",
    "database_context": {{
      "tables": [
        {{
          "name": "customers",
          "columns": ["customer_id", "first_name", "last_name", "email", "registration_date"]
        }},
        {{
          "name": "orders",
          "columns": ["order_id", "customer_id", "order_date", "total_amount", "status"]
        }}
      ],
      "relationships": [
        {{"from": "customers.customer_id", "to": "orders.customer_id"}}
      ]
    }},
    "sql_query": "SELECT c.customer_id, c.first_name, c.last_name, c.email, o.total_amount\\nFROM customers c\\nJOIN orders o ON c.customer_id = o.customer_id\\nWHERE o.order_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)\\nAND o.total_amount > 500\\nORDER BY o.total_amount DESC;",
    "explanation": "This query joins the customers and orders tables on the customer_id field. It filters orders from the last month with a total amount greater than $500, and returns customer details along with the order amount, sorted by amount in descending order."
  }},
  {{
    "instruction": "Show me the average rating for each product category",
    "database_context": {{
      "tables": [
        {{
          "name": "products",
          "columns": ["product_id", "name", "category_id", "price"]
        }},
        {{
          "name": "categories",
          "columns": ["category_id", "category_name"]
        }},
        {{
          "name": "reviews",
          "columns": ["review_id", "product_id", "customer_id", "rating", "review_text", "review_date"]
        }}
      ],
      "relationships": [
        {{"from": "products.category_id", "to": "categories.category_id"}},
        {{"from": "reviews.product_id", "to": "products.product_id"}}
      ]
    }},
    "sql_query": "SELECT c.category_name, ROUND(AVG(r.rating), 2) as average_rating, COUNT(r.review_id) as review_count\\nFROM categories c\\nJOIN products p ON c.category_id = p.category_id\\nJOIN reviews r ON p.product_id = r.product_id\\nGROUP BY c.category_id, c.category_name\\nHAVING COUNT(r.review_id) > 5\\nORDER BY average_rating DESC;",
    "explanation": "This query calculates the average rating for each product category by joining the categories, products, and reviews tables. It only includes categories with more than 5 reviews and sorts the results by the average rating in descending order."
  }}
]

Task Description: You are tasked with creating a diverse collection of educational writing prompts specifically designed for high school English and composition classes. Each prompt should be carefully crafted to develop specific writing skills appropriate for students in grades 9-12. Your prompts should include detailed contextual information, clear learning objectives, and skill development targets that align with educational standards for secondary language arts. For narrative prompts, provide example responses that demonstrate expected creative elements and storytelling techniques. For analytical prompts, include structured frameworks that guide students through the organization of their arguments or analyses. Each prompt should be categorized by difficulty level, appropriate grade range, and estimated completion time to assist teachers in curriculum planning. Additionally, include assessment rubrics with specific criteria that can be used to evaluate student submissions against learning objectives, providing a comprehensive tool for both instruction and evaluation.
Human Input: I need writing prompts for high school students
Output: [
  {{
    "prompt_id": 1,
    "prompt_text": "Write a short story where a character discovers an unexpected talent during a crisis.",
    "grade_level": "9-10",
    "difficulty": "medium",
    "skills_developed": ["character development", "plot structure", "conflict resolution"],
    "example_response": "The first tremor hit during fifth period chemistry. Mr. Sandoval had just started explaining covalent bonds when the floor began to vibrate beneath our feet. A few nervous laughs rippled through the classroom. Growing up in California meant earthquakes were nothing new, but something felt different this time...",
    "rubric": {{
      "character_development": "Character shows clear growth or revelation",
      "setting": "Crisis situation is believable and well-described",
      "plot": "Logical progression from crisis to discovery of talent",
      "theme": "Exploration of hidden potential or self-discovery"
    }},
    "estimated_writing_time_minutes": 45
  }},
  {{
    "prompt_id": 2,
    "prompt_text": "Compare and contrast two technological innovations that changed how people communicate.",
    "grade_level": "11-12",
    "difficulty": "challenging",
    "skills_developed": ["analytical thinking", "research", "comparative analysis", "historical context"],
    "suggested_structure": {{
      "introduction": "Present the two innovations and thesis statement",
      "body_paragraphs": [
        "Historical context for first innovation",
        "Historical context for second innovation",
        "Impact analysis of first innovation",
        "Impact analysis of second innovation",
        "Direct comparison of impacts",
        "Societal implications of both"
      ],
      "conclusion": "Synthesis of findings and future outlook"
    }},
    "estimated_writing_time_minutes": 60
  }}
]

Based on the above examples, generate sample data for the following task description:
Note: When creating sample data, always use JSON format that aligns exactly with the task description requirements. Make sure to include all expected output fields alongside input fields, as these are essential for demonstrating the complete input-output relationship.
Task Description: {task_description}
Human Input: {human_input}
Output:"""

def generate_sample_data_from_task_description_and_raw_input(task_description: str, human_input: str) -> str:

    return f"""You are a meticulous and creative assistant tasked with generating diverse sample data based on a provided task description and human input. The goal is to create structured, relevant, and accurate sample data in JSON format.

Instructions:

1. If the human input already contains sample data, extract and use that sample data.
2. If the human input does not provide sample data, generate three diverse examples based on the task description.
3. Ensure the examples are varied, relevant, and well-structured while maintaining accuracy.
4. The output JSON format should contain fields relevant to the context, not necessarily restricted to "input" and "answer".
5. The JSON fields should match the nature of the task. For example:
    - If the task is about explaining a concept, fields may be "question" and "explanation".
    - If the task involves describing a process, fields may be "step" and "description".
    - If the task requires comparisons, fields may be "entity_1", "entity_2", and "comparison".
6. Ensure that field names are contextually meaningful.
7. Format the output as a JSON list of dictionaries.
8. Make sure the sample data is as diverse as possible. The style, tone, and complexity of the sample data should be different.
9. If the sample data is all the same, then paraphrase the sample data to make it different.
10. Strictly, the sample data should also contain the expected output fields relevant to the task description. For example, if the task description is about summarizing a text, the sample data should also contain the "summary" field, if the task description is about QA pairs, the sample data should also contain the "answer" field, etc.

Examples:
Task Description: Identify the sentiment of the text
Human Input: Identify the sentiment of the text
Output: [{{"text": "The weather was gloomy, with heavy clouds looming over the city, but there was no rain.", "sentiment": "negative"}}, ...]

Task Description: Translate the text from English to French
Human Input: Translate the text from English to French
Output: [{{"text": "The weather was gloomy, with heavy clouds looming over the city, but there was no rain.", "translation": "Le temps était mauvais, avec des nuages lourds qui se posaient sur la ville, mais il n'y avait pas de pluie."}}]

Task Description: Summarize the text
Human Input: Summarize the text
Output: [{{"text": "The weather was gloomy, with heavy clouds looming over the city, but there was no rain.", "summary": "The weather was gloomy, with heavy clouds looming over the city, but there was no rain."}}, ...]

Task Description: Identify the entities in the text
Human Input: Identify the entities in the text
Output: [{{"text": "The weather was gloomy, with heavy clouds looming over the city, but there was no rain.", "entities": ["weather", "clouds", "rain"]}}, ...]

Based on the above examples, generate sample data for the following task description:
Task Description: {task_description}
Human Input: {human_input}
Output:"""

def extract_task_description_from_raw_input(human_input: str) -> str:

    return f"""You are a meticulous assistant specializing in generating comprehensive task descriptions from human inputs that enable AI training and evaluation.

Your task is to:
1. Extract and expand the most detailed task description from the human input, ensuring it captures all nuances, requirements, constraints, and implicit expectations.
2. Generate the task description in second person (using "you" and "your"), formatted as clear actionable instructions.
3. If the Human Input contains Feedback, prioritize and strictly incorporate this feedback into the task description.
4. Ensure the description includes or implies:
   - The type and structure of expected inputs
   - The nature and format of desired outputs
   - Any quality standards or success criteria that could inform evaluation metrics
   - Edge cases or special conditions that should be handled
   - Domain context relevant to generating realistic synthetic data
5. Format the description with appropriate paragraph breaks, bullet points, or numbered steps if the task involves a sequential process.
6. Preserve any technical terminology, domain-specific language, or specialized vocabulary used in the original input.

Examples:

Human Input: I need a sentiment analyzer for tweets about our product.
Output: You are tasked with developing a sentiment analysis system specifically designed to evaluate customer opinions expressed in tweets about a product. Your analysis should categorize each tweet into positive, negative, or neutral sentiment classifications, with an optional intensity score that indicates the strength of the expressed sentiment. You should pay particular attention to product-specific terminology, common abbreviations used in social media, and contextual cues that might affect interpretation. Your analysis should be robust enough to handle the informal language, hashtags, emoticons, and abbreviated text commonly found in tweets. The system should also identify key product features or aspects mentioned in the tweets to enable aspect-based sentiment analysis, allowing for more granular insights into which specific product elements receive positive or negative feedback.

Human Input: Write a program that checks if a string is a palindrome.
Output: You are tasked with creating a function that determines whether a given string qualifies as a palindrome. Your solution should evaluate if the string reads the same forward and backward, ignoring case sensitivity, spaces, and non-alphanumeric characters during the comparison. Your implementation should handle various edge cases, including empty strings, single-character strings, and inputs containing special characters or numbers. The function should accept any text string as input and return a boolean value: true if the processed string is a palindrome and false if it is not. Ensure your solution is efficient with optimal time and space complexity, suitable for potentially processing large strings or multiple string evaluations in sequence.

Human Input: Summarize news articles.
Output: You are tasked with creating concise summaries of news articles that capture the essential information while reducing the content to approximately 20% of its original length. Your summaries should identify and prioritize the key facts, including the who, what, when, where, why, and how elements central to the story. You should maintain neutrality in your summarization, avoiding the introduction of bias not present in the original text. Your output should begin with a headline or title that encapsulates the main point of the article, followed by the condensed content organized in order of importance. Important names, organizations, locations, dates, and statistics must be preserved in the summary. You should also retain any crucial direct quotes that represent significant positions or statements from key individuals relevant to the story.

Human Input: Create a meal plan generator for weight loss. Feedback: {{"meal plan generator": "should include nutritional information, preparation time, and difficulty level", "weight loss": "focused on high protein, low carb diets"}}
Output: You are tasked with developing a comprehensive meal planning system specifically designed for weight loss through high-protein, low-carbohydrate dietary approaches. Your system should generate customized daily and weekly meal schedules that adhere to specified macronutrient distributions prioritizing protein intake while limiting carbohydrate consumption. For each meal suggestion, you must include complete nutritional information detailing calories, protein, carbohydrates, fats, and fiber content to help users track their nutritional intake accurately. Additionally, each recipe or meal recommendation should specify estimated preparation time and a difficulty level rating to help users plan according to their cooking skills and available time. The meal plans should offer sufficient variety to prevent dietary fatigue while maintaining adherence to the nutritional framework required for effective weight management. Your suggestions should also consider practical aspects such as ingredient availability, meal prep possibilities, and strategies for maintaining compliance with the high-protein, low-carb approach in various social and dining situations.

Human Input: I need an image caption generator.
Output: You are tasked with developing an image captioning system that automatically generates descriptive text for visual content. Your system should produce clear, concise, and accurate descriptions that convey the key elements present in each image, including main subjects, actions, settings, and significant visual details. The captions should vary in length based on image complexity, typically ranging from 1-3 sentences. You should prioritize accessibility considerations, ensuring captions provide adequate information for visually impaired users to understand the image content. Your captions should maintain a neutral, objective tone while accurately representing cultural, contextual, and environmental elements within the image. The system should handle diverse image types, including photographs, illustrations, diagrams, and infographics, adapting the captioning style appropriately for each format. When appropriate, your captions should also convey emotional context or mood evident in the image without making subjective interpretations beyond what is visually apparent.

Human Input: Write a text adventure game.
Output: You are tasked with creating an interactive text-based adventure game that engages players through descriptive narratives and choice-driven gameplay. Your game should present players with richly detailed environments, characters, and situations, followed by multiple decision options that meaningfully impact the story progression. You should implement a branching narrative structure where player choices lead to different outcomes, creating multiple possible pathways through the game. The writing should be immersive and evocative, using second-person perspective to place the player directly in the story. You must include a clear objective or quest for the player to pursue, balanced with interesting obstacles, puzzles, and character interactions that create engaging gameplay. Your implementation should track relevant player statistics or inventory items that influence available choices and outcomes. The game should feature multiple possible endings determined by the cumulative effect of player decisions throughout the adventure. Additionally, you should incorporate appropriate pacing, building tension at key moments and providing quieter moments for exploration and discovery.

Human Input: I need a system that can detect credit card fraud.
Output: You are tasked with developing a sophisticated fraud detection system specifically designed to identify potentially fraudulent transactions in credit card usage patterns. Your system should analyze transaction data in real-time, evaluating multiple factors including but not limited to geographic location, transaction amount, merchant category, transaction frequency, and deviation from established user patterns. You should implement both rule-based detection mechanisms for known fraud patterns and machine learning algorithms capable of identifying subtle anomalies that might indicate fraudulent activity. Your solution must minimize false positives to avoid unnecessary disruption to legitimate customer transactions while maintaining high sensitivity to actual fraud attempts. The system should assign a risk score to each transaction, allowing for different intervention thresholds based on risk level, customer history, and transaction characteristics. Additionally, your system should continuously learn and adapt to evolving fraud techniques by incorporating feedback from confirmed fraud cases and legitimate transactions that were initially flagged as suspicious.

Human Input: Explain how a random forest algorithm works.
Output: You are tasked with providing a comprehensive explanation of the random forest algorithm that is both technically accurate and accessible to individuals with a basic understanding of machine learning concepts. Your explanation should define random forests as an ensemble learning method that operates by constructing multiple decision trees during training and outputting the class (for classification) or mean prediction (for regression) of the individual trees. You should clarify the key mechanisms that differentiate random forests from individual decision trees, specifically bootstrap aggregating (bagging) for selecting training samples and random feature selection at each split. You must explain how these techniques help overcome the overfitting problems common to individual decision trees. Your description should include the algorithm's training process, prediction methodology, and the mathematical intuition behind why combining multiple "weak learners" creates a stronger overall model. Additionally, you should address practical considerations including random forests' advantages (handling high-dimensional data, built-in feature importance, robustness to outliers) and limitations (interpretability challenges, computational requirements for large datasets). Where appropriate, include simple examples to illustrate key concepts.

Human Input: {human_input}
Output:"""


def complete_sample_data(task_description: str, task: str, response: str) -> str:
    return f"""
    You are a helpful assistant that completes the sample data for the following task description.
    The new data should have input fields and expected output fields that are relevant to the task description. If the expected output fields are not present, generate those fields accordingly.
    
    Instructions:
    1. Analyze the task description and current data carefully
    2. Identify the key input and output fields required for the task
    3. Add any missing expected output fields that would be needed
    4. Ensure your completed data maintains the same structure as the current data
    5. Create realistic, diverse examples that cover a range of scenarios
    6. Make sure the completed data is properly formatted and valid JSON
    
    Task Description: {task_description}
    Human Input: {task}
    
    Current data: {response}
    
    Examples of completing sample data:
    
    Example 1:
    Task Description: Create a sentiment analysis system that can classify customer reviews as positive, negative, or neutral.
    Human Input: Analyze sentiment in product reviews
    Current data: [
      {{"review": "This product completely failed after just two uses."}}
    ]
    New data: [
      {{"review": "This product completely failed after just two uses.", "sentiment": "negative", "confidence": 0.92}},
      {{"review": "Works exactly as described and arrived ahead of schedule!", "sentiment": "positive", "confidence": 0.88}},
      {{"review": "The quality is acceptable for the price point, but there are better options available.", "sentiment": "neutral", "confidence": 0.75}}
    ]
    
    Example 2:
    Task Description: Develop a system that can extract key information from résumés, including education, work experience, and skills.
    Human Input: Extract information from résumés
    Current data: [
      {{"text": "Jane Doe\\nEducation\\nMaster of Science in Computer Science, Stanford University, 2018-2020\\nBachelor of Engineering, MIT, 2014-2018\\n\\nExperience\\nSoftware Engineer, Google, 2020-Present\\nSoftware Engineering Intern, Facebook, Summer 2019\\n\\nSkills\\nPython, Java, C++, Machine Learning, Docker, Kubernetes"}}
    ]
    New data: [
      {{"text": "Jane Doe\\nEducation\\nMaster of Science in Computer Science, Stanford University, 2018-2020\\nBachelor of Engineering, MIT, 2014-2018\\n\\nExperience\\nSoftware Engineer, Google, 2020-Present\\nSoftware Engineering Intern, Facebook, Summer 2019\\n\\nSkills\\nPython, Java, C++, Machine Learning, Docker, Kubernetes",
        "extracted_information": {{
          "name": "Jane Doe",
          "education": [
            {{"degree": "Master of Science", "field": "Computer Science", "institution": "Stanford University", "years": "2018-2020"}},
            {{"degree": "Bachelor of Engineering", "field": "", "institution": "MIT", "years": "2014-2018"}}
          ],
          "experience": [
            {{"position": "Software Engineer", "company": "Google", "duration": "2020-Present"}},
            {{"position": "Software Engineering Intern", "company": "Facebook", "duration": "Summer 2019"}}
          ],
          "skills": ["Python", "Java", "C++", "Machine Learning", "Docker", "Kubernetes"]
        }}
      }},
      {{"text": "John Smith\\nSummary\\nExperienced product manager with 8+ years in the tech industry.\\n\\nWork History\\nSenior Product Manager, Amazon, 2019-Present\\nProduct Manager, Microsoft, 2015-2019\\n\\nEducation\\nMBA, Harvard Business School, 2013-2015\\nB.Sc in Economics, University of Pennsylvania, 2009-2013\\n\\nTechnical Skills\\nSQL, Tableau, JIRA, Agile methodologies, A/B testing\\n\\nLanguages\\nEnglish (native), Spanish (fluent), Mandarin (conversational)",
        "extracted_information": {{
          "name": "John Smith",
          "education": [
            {{"degree": "MBA", "field": "", "institution": "Harvard Business School", "years": "2013-2015"}},
            {{"degree": "B.Sc", "field": "Economics", "institution": "University of Pennsylvania", "years": "2009-2013"}}
          ],
          "experience": [
            {{"position": "Senior Product Manager", "company": "Amazon", "duration": "2019-Present"}},
            {{"position": "Product Manager", "company": "Microsoft", "duration": "2015-2019"}}
          ],
          "skills": ["SQL", "Tableau", "JIRA", "Agile methodologies", "A/B testing"],
          "languages": ["English (native)", "Spanish (fluent)", "Mandarin (conversational)"]
        }}
      }}
    ]
    
    Example 3:
    Task Description: Create a question-answering system that can provide accurate answers to medical questions based on provided context.
    Human Input: Answer medical questions
    Current data: [
      {{"question": "What are the common symptoms of diabetes?"}}
    ]
    New data: [
      {{"question": "What are the common symptoms of diabetes?",
        "context": "Diabetes is a chronic condition characterized by high blood sugar levels. Common symptoms of diabetes include frequent urination, increased thirst, unexplained weight loss, extreme hunger, blurry vision, numbness or tingling in hands or feet, fatigue, and slow-healing sores. Type 1 diabetes symptoms often develop quickly, while Type 2 diabetes symptoms may develop slowly or be mild enough to go unnoticed for years.",
        "answer": "The common symptoms of diabetes include frequent urination, increased thirst, unexplained weight loss, extreme hunger, blurry vision, numbness or tingling in hands or feet, fatigue, and slow-healing sores. Type 1 diabetes symptoms typically develop rapidly, while Type 2 diabetes symptoms may develop gradually or be mild enough to go unnoticed."
      }},
      {{"question": "How is high blood pressure diagnosed?",
        "context": "High blood pressure (hypertension) is diagnosed through blood pressure measurements. Blood pressure is recorded as two numbers: systolic pressure (the pressure when the heart beats) over diastolic pressure (the pressure when the heart rests). A normal blood pressure reading is less than 120/80 mm Hg. Elevated blood pressure is 120-129 systolic and less than 80 diastolic. Hypertension Stage 1 is 130-139 systolic or 80-89 diastolic. Hypertension Stage 2 is 140 or higher systolic or 90 or higher diastolic. A hypertensive crisis is a reading over 180/120 mm Hg. Diagnosis typically requires multiple elevated readings on different occasions.",
        "answer": "High blood pressure is diagnosed through multiple blood pressure measurements taken on different occasions. A reading of 130-139 systolic or 80-89 diastolic is classified as Hypertension Stage 1, while a reading of 140 or higher systolic or 90 or higher diastolic indicates Hypertension Stage 2. Normal blood pressure is less than 120/80 mm Hg."
      }}
    ]
    
    Example 4:
    Task Description: Build a system that can generate concise summaries of scientific articles while preserving the key findings and methodology.
    Human Input: Summarize scientific papers
    Current data: [
      {{"title": "Effects of Climate Change on Coastal Ecosystems", 
        "abstract": "This study examines the impact of rising sea levels and increasing ocean temperatures on coastal wetland ecosystems. Through a 10-year longitudinal study of three wetland sites along the eastern seaboard, we documented significant shifts in species composition, carbon sequestration capacity, and ecosystem resilience. Our findings indicate that while some wetland systems demonstrate remarkable adaptive capacity, the rate of environmental change is exceeding adaptation thresholds in vulnerable locations. This research contributes to predictive models for coastal conservation and may inform climate adaptation policies."
      }}
    ]
    New data: [
      {{"title": "Effects of Climate Change on Coastal Ecosystems", 
        "abstract": "This study examines the impact of rising sea levels and increasing ocean temperatures on coastal wetland ecosystems. Through a 10-year longitudinal study of three wetland sites along the eastern seaboard, we documented significant shifts in species composition, carbon sequestration capacity, and ecosystem resilience. Our findings indicate that while some wetland systems demonstrate remarkable adaptive capacity, the rate of environmental change is exceeding adaptation thresholds in vulnerable locations. This research contributes to predictive models for coastal conservation and may inform climate adaptation policies.",
        "summary": "A decade-long study of eastern seaboard wetlands reveals that climate change is causing significant shifts in species composition and carbon sequestration capacity. While some wetland ecosystems show adaptive capacity, many vulnerable locations face environmental changes that exceed their adaptation thresholds. The findings contribute to coastal conservation models and climate policy development."
      }},
      {{"title": "Neuroplasticity in Adult Learning: A Meta-Analysis", 
        "abstract": "Neuroplasticity, the brain's ability to reorganize itself by forming new neural connections, has been extensively studied in developmental contexts but remains incompletely understood in adult learning. This meta-analysis synthesizes findings from 78 studies published between 2005-2023, encompassing data from 4,302 adult participants engaged in various learning tasks. Our analysis reveals statistically significant patterns of neural adaptation across different age groups, learning modalities, and cognitive domains. Notably, we identified consistent structural and functional changes in the hippocampus and prefrontal cortex, even in adults over 65 years of age, challenging previous assumptions about reduced plasticity in older adults. The results suggest that specific training protocols may enhance neuroplastic responses regardless of age, with potential applications in educational and therapeutic contexts.",
        "summary": "This meta-analysis of 78 studies with 4,302 adult participants challenges assumptions about reduced neuroplasticity in older adults. The research identified significant neural adaptations across different age groups, learning approaches, and cognitive domains, with consistent structural and functional changes observed in the hippocampus and prefrontal cortex even in adults over 65. The findings suggest that properly designed training protocols could enhance neuroplasticity regardless of age, offering potential applications in education and therapy."
      }}
    ]
    
    New data:
    """

def convert_few_shot_examples_to_json(few_shot_examples: str) -> str:
    return f"""
    You are a helpful assistant that converts the following examples to a json format. Output a single json object only.
    
    Examples: {few_shot_examples}
    Output:"""


# def extract_task_description_from_human_input(human_input: str) -> str:

#     return f"""You are a meticulous assistant specializing in generating comprehensive task descriptions from human inputs that enable AI training and evaluation.

# Human Input: {human_input}

# Your task is to:
# 1. Extract and expand the most detailed task description from the human input, ensuring it captures all nuances, requirements, constraints, and implicit expectations.
# 2. Generate the task description in second person (using "you" and "your"), formatted as clear actionable instructions.
# 3. If the Human Input contains Feedback, prioritize and strictly incorporate this feedback into the task description.
# 4. Ensure the description includes or implies:
#    - The type and structure of expected inputs
#    - The nature and format of desired outputs
#    - Any quality standards or success criteria that could inform evaluation metrics
#    - Edge cases or special conditions that should be handled
#    - Domain context relevant to generating realistic synthetic data
# 5. Format the description with appropriate paragraph breaks, bullet points, or numbered steps if the task involves a sequential process.
# 6. Preserve any technical terminology, domain-specific language, or specialized vocabulary used in the original input.

# Output only the extracted task description as a detailed, contextually-rich string without any preamble, explanation, or meta-commentary. The description should be sufficiently complete that an AI model could use it to generate appropriate synthetic data examples and evaluation metrics without requiring additional information."""

def extract_sample_data_from_human_input(human_input: str) -> str:

    return f"""
    You are a helpful assistant that extracts sample data from a given human input.
    Human input: {human_input}
    Extract the sample data from the human input. Output the sample data in a json format.
    If the sample data cannot be extracted, output 'None'. If expected output or golden answer is not present, generate those fields accordingly.
    """

def extract_output_format_from_human_input(human_input: str) -> str:

    return f"""
    You are a helpful assistant that extracts output format from a given human input.
    Human input: {human_input}
    Extract the output format from the human input. Output the output format in a string.
    If the output format cannot be extracted, output 'None'.
    """

def extract_style_guide_from_human_input(human_input: str) -> str:

    return f"""
    You are a helpful assistant that extracts style guide from a given human input.
    Human input: {human_input}
    Extract the style guide from the human input. Output the style guide in a string.
    If the style guide cannot be extracted, output 'None'.
    """

def extract_constraints_from_human_input(human_input: str) -> str:

    return f"""
    You are a helpful assistant that extracts constraints from a given human input.
    Human input: {human_input}
    Extract the constraints from the human input. Output the constraints in a string.
    If the constraints cannot be extracted, output 'None'.
    """ 

def extract_tools_from_raw_input(human_input: str) -> str:

    return f"""
    You are a helpful assistant that extracts tools from a given human input.
    Human input: {human_input}
    Extract the tools from the human input. Output the tools in a string.
    If the tools cannot be extracted, output 'None'.
    """

def extract_metrics_from_human_input(human_input: str) -> str:

    return f"""
    You are a helpful assistant that extracts metrics from a given human input.
    Human input: {human_input}
    Extract the metrics from the human input. Output the metrics in a string.
    If the metrics cannot be extracted, output 'None'.
    """

# def extract_task_type_from_human_input(human_input: str) -> str:

#     return f"""
#     You are a helpful assistant that extracts task type from a given human input.
#     Human input: {human_input}
#     Extract the task type from the human input. Output the task type in a string.
#     If the task type cannot be extracted, output 'None'. Restrict the task type to the following options: classification, qa, generation, translation, agentic.
#     """ 

# def extract_task_type_from_human_input(task_description: str, human_input: str, sample_data: str) -> str:
#     return f"""
#     You are a precise and meticulous assistant tasked with extracting the task type based on a given task description, human input, and sample data. Use the detailed descriptions of task categories to ensure accurate identification.

#     Task Categories:
#     - **classification**: Tasks that involve assigning predefined categories or labels to input data. Examples include sentiment analysis, spam detection, or image categorization.
#     - **qa**: Short for "question answering," tasks in this category involve answering specific questions based on input data, which could be a document, text, or context.
#     - **generation**: Tasks that require creating or producing content. This includes text generation, story creation, summarization, or paraphrasing.
#     - **translation**: Tasks that involve converting content from one language to another while retaining its meaning and context.
#     - **summarization**: Tasks that involve summarizing a given text or document into a concise summary.

#     Instructions:
#     1. Analyze the task description, human input, and sample data together to determine the task type.
#     2. Match the input against the task category descriptions provided above.
#     3. Output the task type as a string restricted to one of the following: classification, qa, generation, translation, summarization.
#     4. If the task type cannot be clearly identified, output 'None'.
#     5. The task type should be one of the following: classification, qa, generation, translation, summarization.

#     Task Description: {task_description}
#     Human Input: {human_input}
#     Sample Data: {sample_data}

#     Task Type:
#     """

def extract_task_type_from_raw_input(task_description: str, human_input: str, sample_data: str) -> str:

    example_10 = '''
    Example 10:
    Task Description: Identify and fix the bugs in the following JavaScript code snippet that should filter an array of numbers to return only even numbers.
    Human Input: Debug this JavaScript code
    Sample Data: {"buggy_code": "function filterEvenNumbers(arr) {\\n  const result = [];\\n  for (let i = 0; i <= arr.length; i++) {\\n    if (arr[i] % 2 = 0) {\\n      result.push(arr[i]);\\n    }\\n  }\\n  return results;\\n}", "fixed_code": "function filterEvenNumbers(arr) {\\n  const result = [];\\n  for (let i = 0; i < arr.length; i++) {\\n    if (arr[i] % 2 === 0) {\\n      result.push(arr[i]);\\n    }\\n  }\\n  return result;\\n}", "explanation": "Fixed three bugs: 1) Loop condition should be i < arr.length (not <=) to avoid out-of-bounds access, 2) Comparison operator should be === (not =) which is assignment, 3) Return variable name should be result (not results)."}
    Task Type: code_debugging
    Reasoning: This task involves identifying and fixing errors in existing code, making it a code debugging task.
    '''
    return f"""
    You are a specialized AI task classifier with expertise in identifying different natural language processing and machine learning task types. Your goal is to precisely determine the task type from given information.

    Task Categories (organized by primary function):

    Text Classification Tasks:
    - **classification**: Assigning predefined categories or labels to inputs. Examples: sentiment analysis (positive/negative/neutral), topic categorization, spam detection, intent classification, content moderation, document categorization.
    - **multi_label_classification**: Assigning multiple applicable labels simultaneously to a single input. Examples: emotion detection (can be both "sad" and "angry"), content tagging, product categorization.
    
    Information Retrieval Tasks:
    - **qa**: Question answering tasks that provide direct answers to specific questions based on provided context. Examples: factoid QA, reading comprehension, knowledge-base QA.
    - **information_extraction**: Identifying and extracting specific structured information from unstructured text. Examples: named entity recognition, relationship extraction, event extraction, key-value extraction.
    
    Text Generation Tasks:
    - **generation**: Creating original content based on instructions or context. Examples: story writing, article creation, code generation, creative writing, data augmentation.
    - **summarization**: Condensing longer texts into shorter versions while preserving key information. Examples: document summarization, bullet point creation, abstract generation, meeting notes summarization.
    - **translation**: Converting content from one language to another while preserving meaning. Examples: language translation, dialect adaptation, specialized domain translation.
    - **paraphrasing**: Rewriting content while maintaining the same meaning but using different words/structures. Examples: text simplification, style transfer, plagiarism avoidance.
    
    Dialogue Tasks:
    - **conversation**: Managing multi-turn interactions with context preservation. Examples: chatbots, virtual assistants, customer service automation, dialogue systems.
    - **negotiation**: Managing conversations aimed at reaching agreements. Examples: price negotiation, scheduling coordination, resource allocation.
    
    Programming and Code Tasks:
    - **code_generation**: Creating functional code based on requirements or specifications. Examples: function implementation, algorithm development, API integration code, script creation.
    - **code_explanation**: Analyzing and explaining existing code in natural language. Examples: code documentation, explaining function purpose and implementation details, tutorial creation.
    - **code_completion**: Completing partial code snippets based on context. Examples: function completion, implementing missing methods, finishing partially written algorithms.
    - **code_debugging**: Identifying and fixing errors in existing code. Examples: error correction, performance optimization, edge case handling.
    
    Agentic Tasks:
    - **planning**: Breaking down complex goals into actionable steps or creating roadmaps. Examples: project planning, task decomposition, strategy development, workflow creation.
    - **tool_use**: Using specific tools or external resources to accomplish a goal. Examples: API interactions, database queries, web searching, calendar management.
    - **decision_making**: Evaluating options and making choices based on criteria. Examples: comparative analysis, prioritization, risk assessment, option selection.
    - **process_automation**: Creating systems to automate recurring tasks or workflows. Examples: workflow automation, trigger-action planning, conditional processes.
    
    Specialized Tasks:
    - **reasoning**: Tasks requiring step-by-step logical thinking and problem solving. Examples: mathematical problem solving, logical puzzles, algorithmic thinking, chain-of-thought reasoning.
    - **recommendation**: Suggesting items or actions based on provided preferences or history. Examples: product recommendations, content suggestions, personalized advice.
    - **data_analysis**: Analyzing and interpreting structured data to extract insights. Examples: trend analysis, statistical interpretation, data visualization recommendations.

    Step-by-step analysis process:
    1. First, understand the overall objective by carefully examining:
       - The task description for explicit function or purpose statements
       - The input-output relationship in the sample data
       - The structure and nature of the expected outputs
    
    2. Identify key characteristics of the task:
       - Does it involve categorizing/labeling inputs? → Classification family
       - Does it involve creating new content? → Generation family
       - Does it involve answering questions? → QA or information retrieval
       - Does it involve back-and-forth interaction? → Dialogue tasks
    
    3. Consider the specific features of the output format:
       - Are outputs selected from predefined classes or are they free-form?
       - Does the task involve extracting specific information or creating entirely new content?
       - Is there a significant transformation of the input (like summarization or translation)?
       - Does the task require maintaining context across multiple exchanges?
    
    4. Make your final determination based on the closest match to the task categories.

    Examples:
    
    Example 1:
    Task Description: Analyze customer reviews to determine if they express positive, negative, or neutral sentiment.
    Human Input: Classify the sentiment of this product review
    Sample Data: {{"text": "The battery life is terrible and it stopped working after a week.", "sentiment": "negative"}}
    Task Type: classification
    Reasoning: This task requires assigning a single sentiment label (positive, negative, or neutral) to each review, which is a classic text classification task.
    
    Example 2:
    Task Description: Answer questions about company policies using information from the employee handbook.
    Human Input: What does our handbook say about remote work?
    Sample Data: {{"question": "How many vacation days do new employees receive?", "context": "New employees are eligible for 15 paid vacation days per year, accrued monthly starting from their first day.", "answer": "New employees receive 15 paid vacation days per year."}}
    Task Type: qa
    Reasoning: This task involves providing direct answers to specific questions based on provided context, which is quintessential question answering.
    
    Example 3:
    Task Description: Create engaging blog post introductions based on provided topics and keywords.
    Human Input: Write an introduction for a blog post about sustainable gardening
    Sample Data: {{"topic": "Benefits of meditation", "keywords": ["stress reduction", "mindfulness", "mental health"], "introduction": "In our fast-paced world, finding moments of peace has become more essential than ever. Meditation offers a sanctuary of calm that not only reduces stress but also enhances overall mental wellbeing through mindfulness practices."}}
    Task Type: generation
    Reasoning: This task requires creating original content (blog introductions) based on provided inputs, making it a text generation task.
    
    Example 4:
    Task Description: Convert English product descriptions into Spanish for an e-commerce website expansion.
    Human Input: Translate this product description to Spanish
    Sample Data: {{"english": "Wireless headphones with noise-cancellation technology and 20-hour battery life.", "spanish": "Auriculares inalámbricos con tecnología de cancelación de ruido y 20 horas de duración de batería."}}
    Task Type: translation
    Reasoning: This task involves converting content from one language (English) to another (Spanish) while preserving the meaning and context, which is a translation task.
    
    Example 5:
    Task Description: Create concise summaries of research papers for a scientific digest publication.
    Human Input: Summarize this research paper abstract
    Sample Data: {{"full_text": "Recent advances in artificial intelligence have led to significant improvements in natural language processing tasks. This paper presents a novel approach to question answering that combines transformer-based language models with knowledge graph integration. Our method demonstrates a 15% improvement over state-of-the-art baselines on standard benchmarks while requiring 30% less computational resources during inference. Furthermore, we show that our approach is particularly effective for domains with specialized vocabulary such as medicine and law.", "summary": "This paper introduces a new question answering method that combines transformer models with knowledge graphs, achieving 15% better performance than existing methods while using 30% less computing power. The approach works especially well for specialized fields like medicine and law."}}
    Task Type: summarization
    Reasoning: This task involves condensing a longer text (research paper) into a shorter version while preserving key information, which is a summarization task.
    
    Example 6:
    Task Description: For each customer support ticket, identify all relevant product categories and issue types to route to appropriate departments.
    Human Input: Tag this customer complaint with all relevant categories
    Sample Data: {{"ticket_text": "My premium subscription was charged twice this month, and when I tried to use the video editing feature, it kept crashing on my Windows laptop.", "categories": ["billing", "software bug", "video editor", "windows platform"]}}
    Task Type: multi_label_classification
    Reasoning: This task requires assigning multiple applicable labels to each ticket (billing issues, software bugs, specific features, and platforms), making it a multi-label classification task.
    
    Example 7:
    Task Description: Extract structured information about events mentioned in news articles, including the date, location, participants, and event type.
    Human Input: Pull out the key event details from this news text
    Sample Data: {{"article": "On Tuesday, Amazon announced its acquisition of healthcare startup Health Navigator for an undisclosed amount. The deal, which took place in Seattle, was confirmed by Amazon spokesperson John Smith and Health Navigator founder Dr. David Thompson.", "extracted_info": {{"event_type": "acquisition", "date": "Tuesday", "location": "Seattle", "acquiring_company": "Amazon", "acquired_company": "Health Navigator", "spokesperson": "John Smith", "founder": "Dr. David Thompson"}}}}
    Task Type: information_extraction
    Reasoning: This task involves identifying and extracting specific structured information (event details) from unstructured text (news articles), making it an information extraction task.
    
    Example 8:
    Task Description: Review this mathematical word problem and provide a step-by-step solution showing your reasoning process.
    Human Input: Solve this algebra problem
    Sample Data: {{"problem": "A train travels from city A to city B at 60 mph and returns at 40 mph. If the total trip takes 5 hours, what is the distance between the cities?", "solution": "Step 1: Let's call the distance between cities d miles.\nStep 2: Time for first leg = d/60 hours (time = distance/speed)\nStep 3: Time for return leg = d/40 hours\nStep 4: Total time = d/60 + d/40 = 5 hours\nStep 5: Convert to equation: d/60 + d/40 = 5\nStep 6: Find common denominator: (2d + 3d)/120 = 5\nStep 7: Simplify: 5d/120 = 5\nStep 8: Solve for d: 5d = 5 × 120 = 600\nStep 9: Therefore, d = 120 miles"}}
    Task Type: reasoning
    Reasoning: This task requires step-by-step logical thinking and problem solving to work through a mathematical problem, making it a reasoning task.
    
    Example 9:
    Task Description: Create a Python function that calculates the Fibonacci sequence up to n terms with efficient memoization.
    Human Input: Write a Fibonacci sequence generator in Python
    Sample Data: {{"requirements": "Implement a function that returns the Fibonacci sequence up to n terms with memoization for efficiency", "code": "def fibonacci(n):\\n    fib_cache = {{0: 0, 1: 1}}\\n    def fib_memo(k):\\n        if k in fib_cache:\\n            return fib_cache[k]\\n        fib_cache[k] = fib_memo(k-1) + fib_memo(k-2)\\n        return fib_cache[k]\\n    \\n    result = []\\n    for i in range(n):\\n        result.append(fib_memo(i))\\n    return result", "explanation": "This implementation uses memoization via a dictionary to store previously calculated Fibonacci values, avoiding redundant calculations and improving performance."}}
    Task Type: code_generation
    Reasoning: This task involves creating functional code (a Python function) based on specific requirements, making it a code generation task.
        
    Example 11:
    Task Description: Design a workflow that helps a small e-commerce business process customer orders from initial placement to delivery confirmation.
    Human Input: Create a business process for handling online orders
    Sample Data: {{"goal": "Streamline order processing for an e-commerce business", "workflow": [{{"step": 1, "name": "Order Received", "description": "System captures order details and payment information", "triggers": ["Send confirmation email to customer", "Create order record in database"]}}, {{"step": 2, "name": "Inventory Verification", "description": "Check if items are in stock", "decision_point": {{"condition": "all items available?", "if_true": "Proceed to Packaging", "if_false": "Contact customer about backorder options"}}}}, {{"step": 3, "name": "Packaging", "description": "Items are picked from warehouse shelves and packaged for shipping"}}, {{"step": 4, "name": "Shipping", "description": "Generate shipping label and dispatch with carrier", "triggers": ["Update order status to 'Shipped'", "Send tracking information to customer"]}}, {{"step": 5, "name": "Delivery Confirmation", "description": "Track package until confirmed delivery", "triggers": ["Update order status to 'Delivered'", "Send feedback request email after 3 days"]}}]}}
    Task Type: planning
    Reasoning: This task involves breaking down a complex process (order handling) into a series of actionable steps and creating a workflow, making it a planning task.
    
    Example 12:
    Task Description: Evaluate these three different marketing strategies for a new fitness app launch and recommend the best approach based on the target demographic and budget constraints.
    Human Input: Which marketing strategy should we choose?
    Sample Data: {{"context": {{"product": "Fitness tracking app with social features", "target_demographic": "Adults 25-40 interested in fitness", "quarterly_budget": "$50,000"}}, "options": [{{"strategy": "Influencer Marketing", "description": "Partner with fitness influencers for sponsored content", "estimated_cost": "$30,000", "estimated_reach": "500,000 impressions", "pros": ["Builds credibility quickly", "Targeted audience alignment"], "cons": ["High upfront cost", "Results dependent on influencer selection"]}}, {{"strategy": "Paid Social Advertising", "description": "Targeted ads on Instagram and Facebook", "estimated_cost": "$25,000", "estimated_reach": "800,000 impressions", "pros": ["Precise audience targeting", "Scalable and adjustable"], "cons": ["Ad fatigue", "Increasing competition and costs"]}}, {{"strategy": "Content Marketing & SEO", "description": "Create valuable fitness content and optimize for search engines", "estimated_cost": "$20,000", "estimated_reach": "300,000 impressions in first quarter, growing over time", "pros": ["Long-term value", "Builds organic traffic"], "cons": ["Slower initial results", "Requires consistent content creation"]}}], "recommendation": {{"selected_strategy": "Paid Social Advertising", "rationale": "Best balance of immediate reach and cost-effectiveness for the target demographic. The budget allows for sufficient testing and optimization, and the strategy can be scaled based on initial performance. Recommend allocating 20% to small influencer partnerships for additional credibility.", "implementation_timeline": ["Week 1-2: Audience research and ad creative development", "Week 3: Initial campaign launch and A/B testing", "Week 4-8: Optimization based on performance data", "Week 9-12: Scale successful ad sets and expand to new audiences"]}}}}
    Task Type: decision_making
    Reasoning: This task involves evaluating multiple options against specific criteria and recommending the best choice, making it a decision-making task.

    Task Description: {task_description}
    Human Input: {human_input}
    Sample Data: {sample_data}

    Provide your analysis in the following format:
    Task Type: [single task type from the categories above]
    Reasoning: [brief explanation of why you chose this task type, highlighting key characteristics]
    """

# def extract_input_fields_from_human_input(human_input: str) -> str:

#     return f"""
#     You are a helpful assistant that extracts input fields from a given human input.
#     Human input: {human_input}
#     Extract the input fields from the human input. Output the input fields in a list of strings.
#     If the input fields cannot be extracted, output 'None'.
#     """

def extract_input_fields_from_human_input(task_description: str, human_input: str, sample_data: str) -> str:
    return f"""
    You are a helpful assistant tasked with extracting input fields based on a given task description, human input, and sample data.

    Definitions:
    - Input fields: The keys in the JSON data that are required as input to perform the task. These fields provide the information to the system to generate the desired output.

    Instructions:
    1. Analyze the task description, human input, and sample data to identify the input fields.
    2. Only extract the keys from the JSON that represent input fields, which are required to generate an output.
    3. Do not include any output fields or values from the JSON.
    4. Output the input fields as a list of strings.
    5. If no input fields can be identified, output 'None'.

    Examples:
    - Task: Answer questions about geography.
      Sample Data: {{
          "question": "What is the capital of France?",
          "answer": "The capital of France is Paris."
      }}
      Input Fields: ["question"]

    - Task: Sentiment classification for a given text.
      Sample Data: {{
          "text": "The movie was fantastic!",
          "sentiment": "positive"
      }}
      Input Fields: ["text"]

    - Task: Text generation based on a prompt.
      Sample Data: {{
          "prompt": "Write a poem about the ocean.",
          "generated_text": "The ocean, vast and deep, holds secrets..."
      }}
      Input Fields: ["prompt"]

    Task Description: {task_description}
    Human Input: {human_input}
    Sample Data: {sample_data}

    Extracted Input Fields:
    """

def extract_fields_from_sample_data(task_description: str, sample_data: str, allowed_fields: List[str]) -> str:
    """
    Creates a prompt that instructs an LLM to extract both input and output fields from sample data based on the task.
    This combined approach is more token-efficient than making separate calls.
    """
    return f"""
    You are a specialized AI analyst tasked with precisely identifying both input and output fields from provided data structures.

    Definitions:
    - Input fields: The keys in the JSON data that represent information REQUIRED to perform the task. These fields serve as inputs to the system/model and must exist before the task can be executed.
    - Output fields: The keys in the JSON data that represent results, classifications, or any information generated as a response to the inputs.

    IMPORTANT RULES:
    1. For INPUT fields:
       - ONLY identify fields that are TRUE INPUTS - provided by users or from external sources
       - EXCLUDE any fields that are generated outputs, metadata (like IDs, timestamps), or derived calculations
       - For each field, ask: "Could the system complete the task if this field were missing?" If NO, it's an input field

    2. For OUTPUT fields:
       - Identify fields that represent the RESULTS or GENERATED CONTENT i.e. the field that represents teh main objective of the task
       - Include fields that contain information created by the system in response to the inputs. Unless explicitly mentioned in the task description, the output fields should not include metadata like IDs, timestamps, score, confidence, reasoning, or other information that is not directly generated by the system.

    3. Some fields might be neither inputs nor outputs (metadata, system configuration, etc.)

    Strictly only consider only the outer most JSON in the nested JSON. Do not include any fields from the inner JSONs.

    Step-by-step analysis process:
    1. Carefully examine the task description to understand the core purpose
    2. Review the sample data structure systematically
    3. For each field, determine whether it's an input, output, or neither
    4. Consider nested structures - both inputs and outputs can exist at multiple levels
    5. Output ONLY the field names as JSON arrays of strings, maintaining exact key names

    Examples:
    - Task: Answer questions about geography.
      Sample Data: {{
          "question": "What is the capital of France?",
          "answer": "The capital of France is Paris.",
          "confidence": 0.98,
          "question_id": "geo-123"
      }}
      Allowed Fields: ["question", "answer", "confidence", "question_id"]
      Analysis: {{
          "input_fields": ["question"],
          "output_fields": ["answer"]
      }}
      Reasoning: Only the question needs to exist beforehand; answer and confidence are generated outputs, question_id is metadata.

    - Task: Translation between languages.
      Sample Data: {{
          "source_text": "Hello world",
          "source_language": "English",
          "target_language": "Spanish",
          "translation": "Hola mundo",
          "detected_language": "English (confidence: 0.99)"
      }}
      Allowed Fields: ["source_text", "source_language", "target_language", "translation", "detected_language"]
      Analysis: {{
          "input_fields": ["source_text", "target_language"],
          "output_fields": ["translation"]
      }}
      Reasoning: The system needs the source text and desired target language to perform translation. source_language is optional as it can be detected, translation is the output, and detected_language is an analysis result.
      
    - Task: Generate personalized meal plans.
      Sample Data: {{
          "dietary_restrictions": ["gluten-free", "dairy-free"],
          "fitness_goal": "weight loss",
          "calories_per_day": 1800,
          "meals": [
              {{
                  "name": "Breakfast Buddha Bowl",
                  "ingredients": ["quinoa", "avocado", "spinach", "tofu"],
                  "calories": 450,
                  "protein_grams": 22,
                  "preparation_time": 15
              }}
          ],
          "total_protein": 95,
          "meal_plan_id": "MP-29384"
      }}
      Allowed Fields: ["dietary_restrictions", "fitness_goal", "calories_per_day", "meals", "total_protein", "meal_plan_id"]
      Analysis: {{
          "input_fields": ["dietary_restrictions", "fitness_goal", "calories_per_day"],
          "output_fields": ["meals"]
      }}
      Reasoning: The system needs to know dietary restrictions, fitness goals, and calorie targets to generate a meal plan. The meals, total_protein are generated outputs, and meal_plan_id is metadata.
      
    - Task: Analyze sentiment in customer reviews.
      Sample Data: {{
          "review_text": "The service was terrible and the food was cold.",
          "product_id": "PROD-5839",
          "sentiment": "negative",
          "sentiment_score": -0.75,
          "key_phrases": ["terrible service", "cold food"],
          "categories": ["service quality", "food temperature"]
      }}
      Allowed Fields: ["review_text", "product_id", "sentiment", "sentiment_score", "key_phrases", "categories"]
      Analysis: {{
          "input_fields": ["review_text"],
          "output_fields": ["sentiment"]
      }}
      Reasoning: The system requires the review text to analyze sentiment and needs the product_id to associate the analysis with a specific product. The sentiment classification, score, key phrases, and categories are all analysis outputs.
      
    - Task: Generate SQL queries from natural language.
      Sample Data: {{
          "natural_language_query": "Find all customers who spent more than $1000 last month",
          "database_schema": {{
              "tables": ["customers", "orders", "products"],
              "relationships": ["customers.id = orders.customer_id", "orders.product_id = products.id"]
          }},
          "sql_query": "SELECT c.name, SUM(o.amount) AS total_spent FROM customers c JOIN orders o ON c.id = o.customer_id WHERE o.order_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH) GROUP BY c.id HAVING total_spent > 1000 ORDER BY total_spent DESC;",
          "explanation": "This query joins customers and orders tables, filters for orders from the last month, calculates the total amount spent per customer, and returns only those who spent over $1000."
      }}
      Allowed Fields: ["natural_language_query", "database_schema", "sql_query", "explanation"]
      Analysis: {{
          "input_fields": ["natural_language_query", "database_schema"],
          "output_fields": ["sql_query"]
      }}
      Reasoning: The system needs both the natural language query to understand what SQL to generate and the database schema to create syntactically correct SQL with proper table/column references. The SQL query and explanation are generated outputs.
      
    - Task: Create educational writing prompts for students.
      Sample Data: {{
          "grade_level": "9-10",
          "subject": "English Literature",
          "skill_focus": ["critical analysis", "textual evidence", "thesis development"],
          "prompt_text": "Analyze how the theme of identity is developed through symbolism in 'The Great Gatsby'. Support your analysis with specific examples from the text.",
          "example_response": "In F. Scott Fitzgerald's 'The Great Gatsby', the green light at the end of Daisy's dock symbolizes Gatsby's hopes and dreams...",
          "rubric": {{
              "thesis": "Clear, debatable thesis statement that addresses the prompt",
              "evidence": "Relevant textual evidence with proper citations",
              "analysis": "Thoughtful interpretation that connects evidence to thesis"
          }},
          "difficulty": "challenging",
          "estimated_completion_time": 45
      }}
      Allowed Fields: ["grade_level", "subject", "skill_focus", "prompt_text", "example_response", "rubric", "difficulty", "estimated_completion_time"]
      Analysis: {{
          "input_fields": ["grade_level", "subject", "skill_focus"],
          "output_fields": ["prompt_text"]
      }}
      Reasoning: The system needs to know the grade level, subject, and skills to focus on in order to generate an appropriate writing prompt. Everything else is output generated by the system.

    Task Description: {task_description}
    Sample Data: {sample_data}
    Allowed Fields: {allowed_fields}

    Strictly, only consider the fields in the Allowed Fields list. Provide your analysis in the following JSON format:
    {{
        "input_fields": ["field1", "field2", ...],
        "output_fields": ["field1", "field2", ...],
        "reasoning": "Brief explanation of your analysis"
    }}
    """


# def extract_output_fields_from_human_input(human_input: str) -> str:

#     return f"""
#     You are a helpful assistant that extracts output fields from a given human input.
#     Human input: {human_input}
#     Extract the output fields from the human input. Output the output fields in a list of strings.
#     If the output fields cannot be extracted, output 'None'.
#     """

def extract_output_fields_from_human_input(task_description: str, human_input: str, sample_data: str) -> str:
    return f"""
    You are a helpful assistant tasked with extracting output fields based on a given task description, human input, and sample data.

    Definitions:
    - Output fields: The keys in the JSON data that represent the result or output produced by the system based on the input fields.

    Instructions:
    1. Analyze the task description, human input, and sample data to identify the output fields.
    2. Only extract the keys from the JSON that represent output fields, which indicate the results produced by the task.
    3. Do not include any input fields or values from the JSON.
    4. Output the output fields as a list of strings.
    5. If no output fields can be identified, output 'None'.

    Examples:
    - Task: Answer questions about geography.
      Sample Data: {{
          "question": "What is the capital of France?",
          "answer": "The capital of France is Paris."
      }}
      Output Fields: ["answer"]

    - Task: Sentiment classification for a given text.
      Sample Data: {{
          "text": "The movie was fantastic!",
          "sentiment": "positive"
      }}
      Output Fields: ["sentiment"]

    - Task: Text generation based on a prompt.
      Sample Data: {{
          "prompt": "Write a poem about the ocean.",
          "generated_text": "The ocean, vast and deep, holds secrets..."
      }}
      Output Fields: ["generated_text"]

    Task Description: {task_description}
    Human Input: {human_input}
    Sample Data: {sample_data}

    Extracted Output Fields:
    """
