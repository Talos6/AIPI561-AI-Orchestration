import torch
from transformers import AutoTokenizer, AutoModel, pipeline
from loguru import logger


class Action:
    
    def __init__(self, config):
        self.config = config
        self._load_models()
    
    def _load_models(self):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.config["models"]["tokenizer_model"]
            )
            self.embedding_model = AutoModel.from_pretrained(
                self.config["models"]["embedding_model"]
            )
            self.embedding_model.eval()
            
            self.sentiment_model = pipeline(
                "sentiment-analysis",
                model=self.config["models"]["sentiment_model"]
            )
            
        except Exception as e:
            raise RuntimeError(f"Failed to load models: {str(e)}")
    
    def tokenize(self, text):
        try:
            tokens = self.tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True
            )
            return tokens
            
        except Exception as e:
            logger.error(f"Tokenization failed: {str(e)}")
            raise
    
    def generate_embeddings(self, tokens):
        try:
            with torch.no_grad():
                outputs = self.embedding_model(**tokens)
                embeddings = outputs.last_hidden_state[:, 0, :].numpy()
            
            return embeddings[0]
            
        except Exception as e:
            logger.error(f"Embedding generation failed: {str(e)}")
            raise
    
    def analyze_sentiment(self, text):
        try:
            result = self.sentiment_model(text)[0]
            
            return {
                "label": result["label"],
                "confidence": result["score"]
            }
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {str(e)}")
            raise
