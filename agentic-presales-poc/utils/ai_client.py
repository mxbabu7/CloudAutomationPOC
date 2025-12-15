"""
AI Client - Unified interface for OpenAI, Azure OpenAI, and GitHub Models
"""
import os
from config.ai_config import config
from openai import OpenAI, AzureOpenAI
import httpx


class AIClient:
    """Unified AI client for multiple providers"""
    
    def __init__(self):
        self.config = config
        self.client = None
        self._initialize_client()
    
    def _get_http_client(self):
        """Create HTTP client with SSL verification handling"""
        # Check if SSL verification should be disabled
        disable_ssl = os.getenv('DISABLE_SSL_VERIFY', 'false').lower() == 'true'
        
        if disable_ssl:
            print("⚠️ SSL verification is disabled (not recommended for production)")
            return httpx.Client(verify=False)
        
        return None  # Use default
    
    def _initialize_client(self):
        """Initialize the appropriate AI client based on configuration"""
        if not self.config.ai_enabled:
            return
        
        http_client = self._get_http_client()
        
        try:
            if self.config.provider == 'openai':
                self.client = OpenAI(
                    api_key=self.config.openai_api_key,
                    http_client=http_client
                )
                self.model = self.config.openai_model
            
            elif self.config.provider == 'azure':
                self.client = AzureOpenAI(
                    api_key=self.config.azure_api_key,
                    api_version=self.config.azure_api_version,
                    azure_endpoint=self.config.azure_endpoint,
                    http_client=http_client
                )
                self.model = self.config.azure_deployment
            
            elif self.config.provider == 'github':
                # GitHub Models uses OpenAI-compatible API
                self.client = OpenAI(
                    base_url="https://models.inference.ai.azure.com",
                    api_key=self.config.github_token,
                    http_client=http_client
                )
                self.model = self.config.github_model
        
        except Exception as e:
            print(f"⚠️ Failed to initialize AI client: {e}")
            print("⚠️ AI features will be disabled")
            self.client = None
    
    def chat_completion(self, messages: list, temperature: float = None, max_tokens: int = None) -> str:
        """
        Send chat completion request
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (optional)
            max_tokens: Maximum tokens to generate (optional)
            
        Returns:
            Generated text response
        """
        if not self.config.ai_enabled or not self.client:
            raise RuntimeError("AI is not enabled or configured")
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature or self.config.temperature,
            max_tokens=max_tokens or self.config.max_tokens
        )
        
        return response.choices[0].message.content
    
    def analyze_with_prompt(self, system_prompt: str, user_content: str, temperature: float = None) -> str:
        """
        Analyze content with a system prompt
        
        Args:
            system_prompt: System instructions
            user_content: Content to analyze
            temperature: Sampling temperature (optional)
            
        Returns:
            Analysis result
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
        
        return self.chat_completion(messages, temperature)


# Global AI client instance
ai_client = AIClient()
