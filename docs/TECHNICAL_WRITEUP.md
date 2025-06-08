# Technical Writeup

## Executive Summary

This document presents the design, implementation, and evaluation of the sentiment analysis dashboard. The system demonstrates streamlined text processing through a pipeline with comprehensive real-time monitoring, user experience, and immediate feedback.

## Project Objectives

### Primary Goals
1. **Orchestrated Workflow**: Create an intuitive text processing pipeline for sentiment analysis
2. **Real-time Monitoring**: Implement immediate feedback and metrics visualization
3. **User-Friendly Interface**: Provide an interactive dashboard for all operations

### Success Criteria
- ✅ Functional sentiment analysis pipeline
- ✅ Real-time dashboard with interactive text processing
- ✅ Comprehensive metrics collection and visualization
- ✅ Configurable retry mechanisms and error handling

## System Design

### Architecture Overview
The project contains following key components:

1. **Orchestrator**: Central pipeline controller managing the complete workflow
2. **Action**: Model operations for tokenization, embedding, and sentiment analysis
3. **Metrics**: In-memory metrics collection and system monitoring
4. **Dashboard**: Streamlit-based user interface managing the pipeline

### Technology Choices

- **Python**: Primary development language
- **PyTorch**: Deep learning framework
- **Transformers (Hugging Face)**: Pre-trained model library with models
- **Pandas**: Data manipulation for metrics display and processing
- **Streamlit**: Interactive UI framework
- **Plotly**: Interactive visualization library for metrics and performance charts
- **psutil**: System resource monitoring
- **GPUtil**: GPU utilization monitoring and memory tracking
- **PyYAML**: Configuration file parsing and management
- **Tenacity**: Configurable retry mechanisms with exponential backoff

## Implementation Details

### Core Components

#### Orchestrator Class (`src/pipeline.py`)
```python
class Orchestrator:
    def process_text(self, text):
        # Process through Action steps with retry mechanisms
        # Record metrics and return results
```

#### Action Class (`src/model.py`)
```python
class Action:
    
    def tokenize(self, text):
        # tokenization
    
    def generate_embeddings(self, tokens):
        # Embedding
    
    def analyze_sentiment(self, text):
        # Sentiment analysis 
```

#### Metrics Class (`src/monitoring.py`)
```python
class Metrics:
    
    def record_step(self, step_name, duration, status='success'):
        # Record individual step performance
    
    def get_summary(self):
        # Provide comprehensive metrics summary
```

### Pipeline Workflow

#### Step-by-Step Processing
1. **Text Input**: User provides text through dashboard interface
2. **Execution Tracking**: Metrics system begins monitoring
3. **Tokenization**: tokenizer processes input text
4. **Embedding Generation**: Extract token embeddings
5. **Sentiment Analysis**: Classifies sentiment with confidence scores
6. **Result Aggregation**: Combine all outputs with metadata and timing
7. **Metrics Recording**: Update execution history and performance statistics

#### Retry Mechanism Implementation
```python
@retry(
    stop=stop_after_attempt(self.config["retry"]["max_attempts"]),
    wait=wait_exponential(
        multiplier=self.config["retry"]["backoff_factor"], 
        min=self.config["retry"]["min_time_multiplier"], 
        max=self.config["retry"]["max_time_multiplier"]
    )
)
def _process_step(self, step_name, data, step_func):
    # Execute step with automatic retry logic
```

## Error Handling and Recovery

### Error Classification and Handling

#### Retry-Eligible Errors
- **Model Loading Issues**: Temporary network or resource problems
- **Processing Timeouts**: Temporary computational delays
- **Memory Pressure**: Temporary resource constraints

#### Non-Retryable Errors
- **Invalid Input**: Malformed or unsupported text formats
- **Configuration Errors**: Invalid model specifications or parameters
- **System Limits**: Insufficient resources for operation

### Recovery Strategies
1. **Exponential Backoff**: Graduated retry delays based on configuration
2. **Graceful Degradation**: Error reporting with continued operation
3. **User Feedback**: Immediate error notifications in dashboard
4. **Automatic Recovery**: Retry mechanisms without user intervention

## Dashboard and User Experience

### Interactive Interface Components

#### Sentiment Analysis Page
- **Quick Test Buttons**: Pre-configured positive, neutral, and negative examples
- **Custom Text Input**: Free-form text area for user-provided content
- **Real-time Results**: Immediate display of sentiment and confidence scores

#### Execution History Page
- **Summary Metrics**: Total executions, success rates, and average duration
- **Detailed History**: Chronological list of all processing attempts
- **Error Tracking**: Failed execution details and error messages

#### System Metrics Page
- **Pipeline Statistics**: Execution counts, success rates, and performance metrics
- **Step Performance**: Individual step timing and success rates
- **System Resources**: CPU, Memory, GPU usage with real-time updates

## Security

### Data Privacy and Security
- **No Persistence**: All text data processed in memory only
- **Model Integrity**: Trusted models from Hugging Face Hub
- **Local Processing**: No external API calls for text analysis

## Lessons Learned
- **Retry Mechanism**: Retry can help to recover the instance without having it halted or introduced single point of failure
- **Configuration**: Configuration enable easy customerization without code changes, also contribute to different deployment
- **Logging**: Add excessive logs can help troubleshooting
- **Monitor**: Dashboard provide informative notification about performance and alerts if anything goes wrong

## Future Enhancement
- **Microservice Architecture**: build REST endpoint for service-to-service communication and separate component for scalability
- **Queue Integration**: Asynchronous processing capabilities
- **Container Deployment**: Docker and Kubernetes support
- **Alert System**: Monitors should trigger alerts for certain thresholds
- **Persistence Options**: Optional data storage and retrieval
