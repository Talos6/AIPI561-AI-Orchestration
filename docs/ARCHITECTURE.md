# Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Pipeline                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                Streamlit Dashboard                          ││
│  │              (dashboard.py)                                 ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          ││
│  │  │ Sentiment   │  │ Execution   │  │   System    │          ││
│  │  │ Analysis    │  │ History     │  │  Metrics    │          ││
│  │  └─────────────┘  └─────────────┘  └─────────────┘          ││
│  └─────────────────────────────────────────────────────────────┘│
│                                ▲                                │
│                                │                                │
│  ┌─────────────────────────────▼───────────────────────────────┐│
│  │                Pipeline Orchestrator                        ││
│  │              (src/pipeline.py)                              ││
│  └─────────────────────────────────────────────────────────────┘│
│                │                              │                 │
│                ▼                              ▼                 │
│  ┌─────────────────────────────┐  ┌────────────────────────────┐│
│  │         Action              │  │        Metrics             ││
│  │      (src/model.py)         │  │    (src/monitoring.py)     ││
│  │                             │  │                            ││
│  │ • Text Tokenization         │  │ • Execution Tracking       ││
│  │ • Embedding Generation      │  │ • Performance Metrics      ││
│  │ • Sentiment Analysis        │  │ • System Resource          ││
│  └─────────────────────────────┘  └────────────────────────────┘│
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                Configuration Management                     ││
│  │                    (config.yaml)                            ││
│  │  ┌─────────┐               ┌─────────┐                      ││
│  │  │ Models  │               │  Retry  │                      ││
│  │  │         │               │ Settings│                      ││
│  │  └─────────┘               └─────────┘                      ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### Core Components

#### 1. Orchestrator (`src/pipeline.py`)
- **Role**: Central workflow coordinator and main pipeline controller
- **Responsibilities**:
  - Manages complete text processing workflow
  - Implements retry mechanisms with configurable parameters
  - Handles error recovery and exception management

#### 2. Action (`src/model.py`)
- **Role**: Model operations and text processing actions
- **Responsibilities**:
  - Text tokenization using BERT tokenizer
  - Embedding generation from transformer models
  - Sentiment analysis using pre-trained models

#### 3. Metrics (`src/monitoring.py`)
- **Role**: In-memory metrics collection and system monitoring
- **Responsibilities**:
  - System resource monitoring
  - Step-level performance analysis
  - Execution history management

#### 4. Dashboard (`dashboard.py`)
- **Role**: User interface and system management
- **Responsibilities**:
  - Interactive sentiment analysis interface
  - Real-time metrics visualization
  - Execution history display

## Data Flow Architecture

```
User Input
    │
    ▼
┌─────────────────┐
│ Orchestrator    │
│ (process_text)  │
└─────────────────┘
    │
    ▼
┌─────────────────┐     ┌─────────────────┐
│ Action:         │────▶│ Metrics:        │
│ • Tokenize      │     │ • Track Step    │
│ • Embed         │     │ • Record Time   │
│ • Analyze       │     │ • Monitor       │
└─────────────────┘     └─────────────────┘
    │                           │
    ▼                           ▼
┌─────────────────┐     ┌─────────────────┐
│ Result          │◄────│ Dashboard       │
│ Processing      │     │ Update          │
└─────────────────┘     └─────────────────┘
    │
    ▼
Dashboard Display
```

## Monitoring Architecture

### Metrics Categories

#### Pipeline Metrics
- **Execution Statistics**: Total, successful, failed counts
- **Success Rates**: Real-time success percentage
- **Processing Times**: Duration tracking per execution
- **Step Performance**: Individual step timing and success rates

#### System Metrics
- **CPU Usage**: Real-time processor utilization
- **Memory Usage**: RAM consumption monitoring
- **GPU Usage**: Graphics processor utilization (if available)
- **GPU Memory**: VRAM usage tracking

#### User Experience Metrics
- **Response Times**: End-to-end processing duration
- **Error Rates**: Failure frequency and patterns
- **Usage Patterns**: Text length and processing frequency
