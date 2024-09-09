import os

class Config:
    TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY')
    if not TAVILY_API_KEY:
        raise ValueError("TAVILY_API_KEY environment variable is not set")