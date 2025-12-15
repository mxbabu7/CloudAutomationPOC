"""
AI Configuration Manager
Handles loading and managing AI provider settings
"""
import os
from pathlib import Path
from typing import Optional


class AIConfig:
    """AI Configuration Manager"""
    
    def __init__(self):
        self.load_env()
        
    def load_env(self):
        """Load environment variables from .env file if it exists"""
        env_file = Path(__file__).parent.parent / ".env"
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
    
    @property
    def ai_enabled(self) -> bool:
        """Check if AI is enabled"""
        return os.getenv('ENABLE_AI', 'true').lower() == 'true'
    
    @property
    def provider(self) -> str:
        """Get AI provider"""
        return os.getenv('AI_PROVIDER', 'openai')
    
    @property
    def openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key"""
        return os.getenv('OPENAI_API_KEY')
    
    @property
    def openai_model(self) -> str:
        """Get OpenAI model"""
        return os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    
    @property
    def azure_endpoint(self) -> Optional[str]:
        """Get Azure OpenAI endpoint"""
        return os.getenv('AZURE_OPENAI_ENDPOINT')
    
    @property
    def azure_api_key(self) -> Optional[str]:
        """Get Azure OpenAI API key"""
        return os.getenv('AZURE_OPENAI_API_KEY')
    
    @property
    def azure_deployment(self) -> str:
        """Get Azure OpenAI deployment name"""
        return os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4o')
    
    @property
    def azure_api_version(self) -> str:
        """Get Azure OpenAI API version"""
        return os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
    
    @property
    def github_token(self) -> Optional[str]:
        """Get GitHub token"""
        return os.getenv('GITHUB_TOKEN')
    
    @property
    def github_model(self) -> str:
        """Get GitHub model"""
        return os.getenv('GITHUB_MODEL', 'gpt-4o')
    
    @property
    def temperature(self) -> float:
        """Get model temperature"""
        return float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
    
    @property
    def max_tokens(self) -> int:
        """Get max tokens"""
        return int(os.getenv('MAX_TOKENS', '4000'))
    
    def validate(self) -> tuple[bool, str]:
        """
        Validate configuration
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.ai_enabled:
            return True, "AI is disabled"
        
        if self.provider == 'openai':
            if not self.openai_api_key or self.openai_api_key == 'your-openai-api-key-here':
                return False, "OpenAI API key not configured. Please set OPENAI_API_KEY in .env file"
        
        elif self.provider == 'azure':
            if not self.azure_api_key or self.azure_api_key == 'your-azure-openai-key-here':
                return False, "Azure OpenAI API key not configured. Please set AZURE_OPENAI_API_KEY in .env file"
            if not self.azure_endpoint or self.azure_endpoint == 'https://your-resource.openai.azure.com/':
                return False, "Azure OpenAI endpoint not configured. Please set AZURE_OPENAI_ENDPOINT in .env file"
        
        elif self.provider == 'github':
            if not self.github_token or self.github_token == 'your-github-token-here':
                return False, "GitHub token not configured. Please set GITHUB_TOKEN in .env file"
        
        else:
            return False, f"Invalid AI provider: {self.provider}. Use 'openai', 'azure', or 'github'"
        
        return True, "Configuration valid"


# Global config instance
config = AIConfig()
