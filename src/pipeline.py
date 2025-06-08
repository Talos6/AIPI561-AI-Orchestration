import time
import yaml
from tenacity import retry, stop_after_attempt, wait_exponential
from datetime import datetime
from src.model import Action
from src.monitoring import Metrics


class Orchestrator:
    
    def __init__(self, config_path = "config.yaml"):
        self.config = self._load_config(config_path)
        self.action = Action(self.config)
        self.metrics = Metrics()
        
    def _load_config(self, config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _process_step(self, step_name, data, step_func):
        @retry(
            stop=stop_after_attempt(self.config["retry"]["max_attempts"]),
            wait=wait_exponential(
                multiplier=self.config["retry"]["backoff_factor"], 
                min=self.config["retry"]["min_time_multiplier"], 
                max=self.config["retry"]["max_time_multiplier"]
            )
        )
        def _execute_step():
            return step_func(data)
        
        start_time = time.time()
        
        try:
            result = _execute_step()
            duration = time.time() - start_time
            self.metrics.record_step(step_name, duration, 'success')
            return result
            
        except Exception:
            duration = time.time() - start_time
            self.metrics.record_step(step_name, duration, 'failure')
            raise
    
    def process_text(self, text):
        self.metrics.start_execution(text)
        
        try:
            # Step 1: Tokenization
            tokens = self._process_step(
                "tokenization",
                text,
                lambda x: self.action.tokenize(x)
            )
            
            # Step 2: Embedding Generation
            embeddings = self._process_step(
                "embedding_generation",
                tokens,
                lambda x: self.action.generate_embeddings(x)
            )
            
            # Step 3: Sentiment Analysis
            sentiment_result = self._process_step(
                "sentiment_analysis",
                text,
                lambda x: self.action.analyze_sentiment(x)
            )
            
            # Step 4: Post-processing
            final_result = self._process_step(
                "post_processing",
                {
                    "text": text,
                    "tokens": tokens,
                    "embeddings": embeddings,
                    "sentiment": sentiment_result
                },
                lambda x: self._post_process(x)
            )
            
            self.metrics.finish_execution('success')
            return final_result
            
        except Exception as e:
            self.metrics.finish_execution('failure', str(e))
            raise
    
    def _post_process(self, data):
        return {
            "timestamp": datetime.now().isoformat(),
            "text": data["text"],
            "text_length": len(data["text"]),
            "token_count": data["tokens"]["input_ids"].shape[1],
            "embedding_dim": data["embeddings"].shape[0],
            "sentiment": data["sentiment"]["label"],
            "sentiment_confidence": data["sentiment"]["confidence"],
            "status": "success"
        }
    