"""
Sources package for News & Content Downloader.

This package contains modules for different content sources and integrations.
"""

from datetime import datetime

# Available sources configuration
AVAILABLE_SOURCES = {
    "naver_news": {
        "name": "Naver News",
        "icon": "🇰🇷",
        "description": "Korean news articles from Naver",
        "function": "get_naver_news"
    },
    "google_search": {
        "name": "Google Search",
        "icon": "🔍",
        "description": "Web search results from Google",
        "function": "get_google_search_results"
    }
}

def get_source_function(source_key):
    """Get the function for a specific source"""
    if source_key not in AVAILABLE_SOURCES:
        return None
        
    function_name = AVAILABLE_SOURCES[source_key]["function"]
    
    # Import the appropriate function
    if function_name == "get_naver_news":
        from .naver_news import get_naver_news
        return get_naver_news
    elif function_name == "get_google_search_results":
        # This is defined in the main app for now
        from ..app import get_google_search_results
        return get_google_search_results
    
    return None
