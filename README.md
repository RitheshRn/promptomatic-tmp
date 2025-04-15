## ⚠️ 🔴 WARNING: Work in Progress

> I plan to open-source this project in the coming weeks. At the moment, I’m finalizing experiments and refining the API documentation. This repository is under active development and is not yet ready for production use.
>
> - Codebase, features, and structure are **unstable** and may change without notice.  
> - Documentation is **incomplete** and not reflective of the final implementation.  
> - Please **do not share, fork, or distribute** without explicit permission.
>
> If you're reviewing this as part of a collaboration or evaluation, reach out to the author(@RitheshRn) for context and guidance.


<div align="center">
  <img src="images/logo1.png" alt="Promptomatic Logo" width="400"/>
  
  <h1>Promptomatic</h1>
  <h3>A Framework for LLM Prompt Optimization</h3>
</div>

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-Apache-green.svg" alt="License">
</div>

<p align="center">
  <a href="#-overview">Overview</a> |
  <a href="#-key-features">Key Features</a> |
  <a href="#-why-promptomatic">Why Promptomatic</a> |
  <a href="#-system-architecture">Architecture</a> |
  <a href="#%EF%B8%8F-installation">Installation</a> |
  <a href="#-quick-start">Quick Start</a> |
  <a href="#-api-documentation">API</a> |
  <a href="#-cli-usage">CLI</a> |
  <a href="#-benchmarks">Benchmarks</a>
</p>

---

## 📋 Overview

Promptomatic is an AI-driven framework designed to automate and optimize large language model (LLM) prompts. It provides a structured approach to prompt optimization, ensuring consistency, cost-effectiveness, and high-quality outputs while reducing the trial-and-error typically associated with manual prompt engineering.

The framework leverages the power of DSPy and advanced optimization techniques to iteratively refine prompts based on task requirements, synthetic data, and user feedback. Whether you're a researcher exploring LLM capabilities or a developer building production applications, Promptomatic provides a comprehensive solution for prompt optimization.

## 🌟 Key Features

- **Zero-Configuration Intelligence**: Automatically analyzes tasks, selects techniques, and configures prompts
- **Automated Dataset Generation**: Creates synthetic training and testing data tailored to your specific domain
- **Task-Specific Optimization**: Selects the appropriate DSPy module and metrics based on task type
- **Real-Time Human Feedback**: Incorporates user feedback for iterative prompt refinement
- **Comprehensive Session Management**: Tracks optimization progress and maintains detailed logs
- **Framework Agnostic Design**: Supports multiple LLM providers (OpenAI, Anthropic, Cohere)
- **CLI and API Interfaces**: Flexible usage through command-line or REST API

## 🤔 Why Promptomatic?

### Challenges in Prompt Engineering

1. **Complexity** - Crafting effective prompts requires domain expertise and iteration
2. **Inconsistency** - LLMs are sensitive to prompt variations, leading to unpredictable outputs
3. **Evaluation Difficulty** - Testing prompt effectiveness requires extensive manual effort
4. **Cost Inefficiency** - Inefficient prompts waste computational resources
5. **Technical Barriers** - Non-technical users struggle with prompt optimization

### Promptomatic's Solutions

1. **Automated Optimization** - Reduces prompt engineering from weeks to hours
2. **Task-Specific Templates** - Ensures consistent, reliable results
3. **Integrated Metrics** - Automatically evaluates prompt performance
4. **Resource Efficiency** - Optimizes prompts for better cost-performance
5. **Intuitive Interfaces** - Makes prompt optimization accessible to all users

## 🏗 System Architecture

Promptomatic follows a modular architecture with the following key components:

### Core Components
- **Config**: Configuration management for optimization tasks
- **PromptOptimizer**: Core optimization engine utilizing DSPy
- **SessionManager**: Tracks optimization progress across multiple sessions
- **FeedbackStore**: Handles user feedback for iterative refinement

### Interfaces
- **CLI**: Command-line interface for direct usage
- **API**: REST API for integration with web applications

### Optimization Flow
1. **Task Analysis**: Extract task type and requirements from user input
2. **Synthetic Data Generation**: Create tailored examples for training
3. **DSPy Module Selection**: Choose optimal module based on task
4. **Prompt Compilation**: Optimize using MIPROv2 trainer
5. **Evaluation**: Measure performance with task-specific metrics
6. **Feedback Integration**: Refine based on user feedback

## ⚙️ Installation

### Prerequisites
- Python 3.8+
- DSPy library
- NLTK library
- Flask (for API)

### Install from Source

```bash
# Clone the repository
git clone https://github.com/<XYZ>/promptomatic.git
cd promptomatic

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```
### Configure Environment Variables

```bash
# Set up API keys for LLM providers
export OPENAI_API_KEY="your_openai_api_key"
export ANTHROPIC_API_KEY="your_anthropic_api_key"
```

## 🚀 Quick Start

### Basic Usage

```python
from promptomatic.core.main import optimize_prompt

# Optimize a prompt with default settings
result = optimize_prompt(
    human_input="Classify text into positive/negative sentiment"
)

# Print the optimized prompt
print(result['result'])

# Print the session ID for future reference
print("Session ID:", result['session_id'])
```

### Optimizing with Feedback

```python
from promptomatic.core.main import optimize_with_feedback, save_feedback

# Save feedback for a specific session
feedback = save_feedback(
    text="Classify text",
    start_offset=0,
    end_offset=13,
    feedback="Classify Twitter posts for sentiment analysis",
    prompt_id="your_session_id"
)

# Optimize with feedback
result = optimize_with_feedback("your_session_id")
print(result['result'])
```

## 🔌 API Documentation [WIP]

### Starting the API Server

```bash
# Run the Flask API server
python -m promptomatic.api
```

### API Endpoints [WIP]

#### Optimize Prompt (`POST /optimize`)

```bash
curl -X POST http://localhost:5000/optimize \
  -H "Content-Type: application/json" \
  -d '{"human_input": "Classify text sentiment into positive or negative"}'
```

#### Optimize with Feedback (`POST /optimize-with-feedback`)

```bash
curl -X POST http://localhost:5000/optimize-with-feedback \
  -H "Content-Type: application/json" \
  -d '{"session_id": "your_session_id"}'
```

#### Add Feedback (`POST /comments`)

```bash
curl -X POST http://localhost:5000/comments \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Classify text sentiment",
    "startOffset": 0,
    "endOffset": 22,
    "comment": "Specify that this is for social media posts",
    "promptId": "your_session_id"
  }'
```

#### Get Session Information (`GET /session/<session_id>`)

```bash
curl -X GET http://localhost:5000/session/your_session_id
```

## 💻 CLI Usage

Promptomatic provides a command-line interface for easy use:

### Basic Optimization

```bash
python -m promptomatic.cli.main --human_input "Classify text sentiment into positive or negative" --model_name "gpt-4" --model_provider "openai"
```

### Advanced Configuration

```bash
python -m promptomatic.cli.main \
  --human_input "Summarize this article" \
  --model_name "gpt-4" \
  --model_provider "openai" \
  --synthetic_data_size 50 \
  --train_ratio 0.3 \
  --task_type "summarization"
```

### Managing Feedback

```bash
# List all feedback
python -m promptomatic.cli.main --list_feedbacks

# Export feedback to file
python -m promptomatic.cli.main --export_feedbacks "feedback_export.json" --prompt_id "your_session_id"
```

## 📊 Benchmarks

Promptomatic has been extensively tested across various task categories and datasets:

### Performance Comparison

| Task | Dataset | Metric | Manual 0-shot | Manual 4-shot | Promptify | Adalflow | Promptomatic |
|------|---------|--------|--------------|--------------|-----------|----------|--------------|
| Math | GSM8k | EM | 0.4753 | 0.7313 | 0.6049 | 0.7672 | 0.7323 |
| QA | Squad2 | BertScore | 0.8596 | 0.8914 | 0.9086 | 0.9216 | 0.9129 |
| Summarization | XSum | BertScore | 0.84 | 0.8612 | 0.1773 | 0.8612 | 0.8645 |
| Text Classification | AG News | F1 | 0.661 | 0.746 | 0.84 | 0.746 | 0.858 |
| Text Generation | CommonGen | BertScore | 0.8914 | 0.8966 | 0.8943 | 0.9038 | 0.9016 |

*All benchmarks conducted using gpt-3.5-turbo*

### Competitive Analysis

| Framework | Automatic training data creation | Automatic technique selection | Automatic metric selection | Zero-learning curve | Real-time human feedback | Cost & Latency | Prompt Management | GUI |
|-----------|----------------------------------|-------------------------------|----------------------------|---------------------|--------------------------|----------------|-------------------|-----|
| DSPy | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| AdalFlow | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| Promptify | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| LangChain Prompt Canvas | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| PromptWizard | ✅ | 🟡 | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Promptomatic | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

## 🔧 Advanced Usage

### Supported Task Types

Promptomatic supports various NLP tasks:

- **Classification**: Text categorization tasks
- **Question Answering**: Extracting answers from contexts
- **Generation**: Creative text generation
- **Summarization**: Condensing longer texts
- **Translation**: Converting between languages
- **Reasoning**: Step-by-step problem solving

### Supported LLM Providers

- OpenAI (GPT-3.5, GPT-4)
- Anthropic (Claude)
- Cohere
- Custom providers via LM Manager

### Custom Metrics

Extend the `MetricsManager` to add custom evaluation metrics:

```python
from promptomatic.metrics.metrics import MetricsManager

# Register a custom metric for your task
@staticmethod
def _custom_metric(example, pred, instructions=None, trace=None):
    # Implement your custom metric
    return score

# Add to metrics map
MetricsManager.get_metrics_for_task = lambda task_type: (
    _custom_metric if task_type == "custom_task" else MetricsManager._default_metrics
)
```

## 🛣️ Roadmap

### Short-Term Goals

1. Complete template management system for reusable prompts
2. Enhance synthetic data generation for specialized domains
3. Expand benchmarking capabilities across more LLMs

### Long-Term Vision

- Multi-framework support (DSPy, AdalFlow, AutoPrompt)
- Dynamic reinforcement learning-based optimization
- Community-driven prompt repository ("HuggingFace for Prompts")

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the Apache License - see the LICENSE file for details.

## 📧 Contact

For questions or feedback, please open an issue on GitHub or contact the project maintainers. (Rithesh Murthy, @RitheshRn)

---

<p align="center">
  <b>Promptomatic: Optimizing LLM prompts, so you don't have to.</b>
</p>
