# AIPI561-AI-Orchestration

A interactive sentiment analysis system with real-time monitoring and comprehensive dashboard interface.

## 📖 Documentation

### Architecture & Design
- **[Architecture Documentation](docs/ARCHITECTURE.md)** - Complete system architecture, components, and design patterns
- **[Technical Writeup](docs/TECHNICAL_WRITEUP.md)** - Detailed implementation analysis and technical insights

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- 4GB RAM minimum (8GB recommended)
- Internet connection for initial model downloads

### Installation

```bash
# Clone repository
git clone https://github.com/Talos6/AIPI561-AI-ORCHESTRATION.git
cd AIPI561-AI-ORCHESTRATION

# Install dependencies
pip install -r requirements.txt

# Launch dashboard
streamlit run dashboard.py
```

### Access
Open your browser to `http://localhost:8501` to access the interactive dashboard.

## 📊 Features

### Core Capabilities
- **Real-time Sentiment Analysis**: Process text instantly with BERT and DistilBERT models
- **Interactive Dashboard**: Streamlit-based interface with immediate feedback
- **Comprehensive Monitoring**: System metrics, performance tracking, and execution history
- **Configurable Processing**: YAML-based configuration for easy customization

### Interactive Dashboard
- **Sentiment Analysis**: Enter text or use quick test buttons
- **Execution History**: View processing history and performance metrics
- **System Metrics**: Monitor system resources and pipeline statistics

### Technical Highlights
- **Single Instance Architecture**: Simplified deployment and management
- **In-Memory Processing**: No file persistence for enhanced privacy and speed
- **Retry Mechanisms**: Configurable exponential backoff with error recovery
- **System Monitoring**: Real-time CPU, Memory, and GPU usage tracking

## 🔧 Configuration

Edit `config.yaml` to customize behavior
