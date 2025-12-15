"""
LLM Client
Handles communication with Large Language Models (OpenAI, Azure OpenAI)
"""

import os
from typing import Dict, Any


class LLMClient:
    """Client for interacting with Language Models."""
    
    def __init__(self, provider: str = "openai", model: str = "gpt-4", **kwargs):
        """
        Initialize the LLM Client.
        
        Args:
            provider: LLM provider (openai or azure)
            model: Model name to use
            **kwargs: Additional provider-specific configuration
        """
        self.provider = provider
        self.model = model
        self.config = kwargs
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the specific LLM client based on provider."""
        if self.provider == "openai":
            self._init_openai()
        elif self.provider == "azure":
            self._init_azure()
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _init_openai(self):
        """Initialize OpenAI client."""
        try:
            import openai
            
            # Get API key from environment or config
            api_key = self.config.get('api_key') or os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
            
            # Fix SSL certificate issue by removing invalid SSL_CERT_FILE env var
            if 'SSL_CERT_FILE' in os.environ:
                original_ssl_cert = os.environ['SSL_CERT_FILE']
                if not os.path.exists(original_ssl_cert):
                    del os.environ['SSL_CERT_FILE']
            
            # Initialize OpenAI client
            self.client = openai.OpenAI(
                api_key=api_key,
                timeout=60.0,
                max_retries=2
            )
            print(f"✓ OpenAI client initialized with model: {self.model}")
            
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
    
    def _init_azure(self):
        """Initialize Azure OpenAI client."""
        try:
            import openai
            
            # Azure-specific configuration
            api_key = self.config.get('api_key') or os.getenv('AZURE_OPENAI_API_KEY')
            endpoint = self.config.get('endpoint') or os.getenv('AZURE_OPENAI_ENDPOINT')
            
            if not api_key or not endpoint:
                raise ValueError("Azure OpenAI credentials not found.")
            
            self.client = openai.AzureOpenAI(
                api_key=api_key,
                api_version="2024-02-01",
                azure_endpoint=endpoint
            )
            print(f"✓ Azure OpenAI client initialized with model: {self.model}")
            
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
    
    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 4000) -> str:
        """
        Generate text using the LLM.
        
        Args:
            prompt: Input prompt for the model
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert cloud solutions architect and presales consultant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
                
        except Exception as e:
            print(f"❌ Error generating response: {str(e)}")
            raise
    
    def generate_structured(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate structured output (JSON) using the LLM.
        
        Args:
            prompt: Input prompt
            schema: Expected JSON schema
            
        Returns:
            Structured output as dictionary
        """
        import json
        
        structured_prompt = f"""
        {prompt}
        
        Respond with valid JSON matching this schema:
        {json.dumps(schema, indent=2)}
        """
        
        response = self.generate(structured_prompt)
        
        try:
            # Extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            json_str = response[start:end]
            return json.loads(json_str)
        except Exception as e:
            print(f"❌ Error parsing structured output: {str(e)}")
            return {"error": str(e), "raw_response": response}

