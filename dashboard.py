import streamlit as st
import pandas as pd
import plotly.express as px
import time
from src.pipeline import Orchestrator


# Initialize session state
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = None


def main():
    st.set_page_config(
        page_title="Sentiment Analysis Dashboard", 
        page_icon="🤖", 
        layout="wide"
    )
    
    st.title("🤖 Sentiment Analysis Dashboard")
    st.markdown("Sentiment analysis with real-time monitoring")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("📋 Navigation")
    page = st.sidebar.selectbox("Choose a page:", [
        "Sentiment Analysis",
        "Execution History", 
        "System Metrics",
    ])

    # Load pipeline
    if st.session_state.pipeline is None:
        try:
            with st.spinner("Loading Pipeline..."):
                st.session_state.pipeline = Orchestrator()
            st.success("✅ Pipeline loaded successfully!")
        except Exception as e:
            st.error(f"❌ Failed to load pipeline: {str(e)}")
            st.stop()
    
    # Render selected page
    if page == "Sentiment Analysis":
        render_sentiment_analysis()
    elif page == "Execution History":
        render_execution_history()
    elif page == "System Metrics":
        render_system_metrics()


def render_sentiment_analysis():
    """Render sentiment analysis interface"""
    st.header("🧪 Sentiment Analysis")
    
    # Quick buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("😊 Positive"):
            test_text = "I love this food!"
            process_text(test_text)
    with col2:
        if st.button("😐 Neutral"):
            test_text = "This is a regular text."
            process_text(test_text)
    with col3:
        if st.button("😞 Negative"):
            test_text = "This system is terrible and doesn't work at all. Very disappointed."
            process_text(test_text)
    
    st.markdown("---")
    
    # Custom text input
    st.subheader("Custom Text Processing")
    text_input = st.text_area(
        "Enter text to analyze:",
        placeholder="Type your text here...",
        height=100
    )
    
    if st.button("🚀 Process Text", type="primary", disabled=not text_input.strip()):
        if text_input.strip():
            process_text(text_input)


def process_text(text):
    try:
        with st.spinner("Processing text..."):
            start_time = time.time()
            result = st.session_state.pipeline.process_text(text)
            processing_time = time.time() - start_time
        
        st.success(f"✅ Processing completed in {processing_time:.2f}s")
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Analysis Results")
            st.json({
                "sentiment": result["sentiment"],
                "confidence": f"{result['sentiment_confidence']:.3f}",
                "status": result["status"]
            })
        
        with col2:
            st.subheader("📈 Processing Stats")
            st.json({
                "text_length": result["text_length"],
                "token_count": result["token_count"],
                "embedding_dim": result["embedding_dim"],
                "timestamp": result["timestamp"]
            })
            
    except Exception as e:
        st.error(f"❌ Processing failed: {str(e)}")


def render_execution_history():
    st.header("📜 Execution History")
    
    history = st.session_state.pipeline.metrics.get_execution_history()
    
    if not history:
        st.info("No executions yet!")
        return
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_executions = len(history)
    successful = len([h for h in history if h['status'] == 'success'])
    failed = total_executions - successful
    avg_duration = sum(h['duration'] for h in history) / total_executions if history else 0
    
    with col1:
        st.metric("Total Executions", total_executions)
    with col2:
        st.metric("Successful", successful)
    with col3:
        st.metric("Failed", failed)
    with col4:
        st.metric("Avg Duration", f"{avg_duration:.2f}s")
    
    # Recent executions table
    st.subheader("Recent Executions")
    
    # Prepare data for table
    table_data = []
    for h in reversed(history):  # most recent first
        table_data.append({
            'Timestamp': h['timestamp'].strftime('%H:%M:%S'),
            'Text': h['text'],
            'Status': '✅ Success' if h['status'] == 'success' else '❌ Failed',
            'Duration': f"{h['duration']:.2f}s",
            'Steps': len(h['steps'])
        })
    
    if table_data:
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True)
    
    # Performance over time
    if len(history) > 1:
        st.subheader("Performance Over Time")
        
        perf_data = []
        for h in history:
            perf_data.append({
                'Time': h['timestamp'],
                'Duration': h['duration'],
                'Status': h['status']
            })
        
        perf_df = pd.DataFrame(perf_data)
        fig = px.line(perf_df, x='Time', y='Duration', color='Status',
                     title="Processing Duration Over Time")
        st.plotly_chart(fig, use_container_width=True)


def render_system_metrics():
    st.header("📊 Metrics Summary")
    
    metrics = st.session_state.pipeline.metrics.get_summary()
    
    # Pipeline Statistics
    st.subheader("🚀 Pipeline Statistics")
    pipeline_stats = metrics.get('pipeline_stats', {})
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Executions", pipeline_stats.get('total', 0))
    with col2:
        st.metric("Successful", pipeline_stats.get('successful', 0))
    with col3:
        st.metric("Failed", pipeline_stats.get('failed', 0))
    with col4:
        success_rate = pipeline_stats.get('success_rate', 0)
        st.metric("Success Rate", f"{success_rate:.1%}")
    
    # Step Performance Statistics
    st.subheader("⚙️ Step Performance")
    step_stats = metrics.get('step_stats', {})
    
    if step_stats:
        step_data = []
        for step_name, stats in step_stats.items():
            step_data.append({
                'Step': step_name.replace('_', ' ').title(),
                'Total': stats['total'],
                'Success': stats['success'],
                'Failure': stats['failure'],
                'Success Rate': f"{stats['success_rate']:.1%}"
            })
        
        step_df = pd.DataFrame(step_data)
        st.dataframe(step_df, use_container_width=True)
    else:
        st.info("No step statistics available yet")
    
    # System Resource Statistics
    st.subheader("💻 System Resources")
    system_stats = metrics.get('system', {})
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        cpu_percent = system_stats.get('cpu_percent', 0)
        st.metric("CPU Usage", f"{cpu_percent:.1f}%")
    with col2:
        memory_percent = system_stats.get('memory_percent', 0)
        st.metric("Memory Usage", f"{memory_percent:.1f}%")
    with col3:
        gpu_percent = system_stats.get('gpu_percent', 0)
        st.metric("GPU Usage", f"{gpu_percent:.1f}%")
    with col4:
        gpu_memory_percent = system_stats.get('gpu_memory_percent', 0)
        st.metric("GPU Memory", f"{gpu_memory_percent:.1f}%")

if __name__ == "__main__":
    main() 