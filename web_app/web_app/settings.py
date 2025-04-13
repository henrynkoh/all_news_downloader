import streamlit as st
import json
import os

# Default settings
DEFAULT_SETTINGS = {
    "theme": "dark",
    "display": {
        "table_height": 600,
        "max_results_display": 100,
        "show_source_distribution": True
    },
    "search": {
        "default_pages": 5,
        "max_pages": 20,
        "default_sources": ["naver_news", "google_search"],
        "request_delay": 1.5
    },
    "advanced": {
        "request_timeout": 10,
        "cache_results": True,
        "cache_expiry_hours": 24,
        "parallel_requests": False
    }
}

def load_settings():
    """Load settings from settings.json file, or return defaults"""
    settings_path = os.path.join(os.path.dirname(__file__), 'settings.json')
    
    if os.path.exists(settings_path):
        try:
            with open(settings_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading settings: {str(e)}")
            return DEFAULT_SETTINGS
    else:
        # Create the default settings file if it doesn't exist
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS

def save_settings(settings):
    """Save settings to settings.json file"""
    settings_path = os.path.join(os.path.dirname(__file__), 'settings.json')
    
    try:
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Error saving settings: {str(e)}")
        return False

def settings_page():
    """Settings page with configuration options"""
    st.title("⚙️ Settings")
    
    # Load current settings
    settings = load_settings()
    
    # Create tabs for different settings categories
    display_tab, search_tab, advanced_tab, about_tab = st.tabs(["Display", "Search", "Advanced", "About"])
    
    # Display Settings
    with display_tab:
        st.subheader("Display Settings")
        
        # Table height
        settings["display"]["table_height"] = st.slider(
            "Results Table Height (pixels)", 
            min_value=300, 
            max_value=1200, 
            value=settings["display"]["table_height"],
            step=50,
            help="Height of the results table in pixels"
        )
        
        # Max results to display
        settings["display"]["max_results_display"] = st.slider(
            "Maximum Results to Display", 
            min_value=50, 
            max_value=500, 
            value=settings["display"]["max_results_display"],
            step=10,
            help="Maximum number of results to show in the table (all results will still be exported)"
        )
        
        # Show source distribution
        settings["display"]["show_source_distribution"] = st.checkbox(
            "Show Source Distribution", 
            value=settings["display"]["show_source_distribution"],
            help="Display a summary of sources next to search results"
        )
        
        # Theme
        theme_options = {
            "dark": "Dark Mode",
            "light": "Light Mode"
        }
        settings["theme"] = st.selectbox(
            "Theme",
            options=list(theme_options.keys()),
            format_func=lambda x: theme_options[x],
            index=list(theme_options.keys()).index(settings["theme"])
        )
    
    # Search Settings
    with search_tab:
        st.subheader("Search Settings")
        
        # Default pages
        settings["search"]["default_pages"] = st.number_input(
            "Default Pages to Search",
            min_value=1,
            max_value=settings["search"]["max_pages"],
            value=settings["search"]["default_pages"],
            help="Default number of pages to search per source"
        )
        
        # Max pages
        settings["search"]["max_pages"] = st.number_input(
            "Maximum Pages to Search",
            min_value=5,
            max_value=50,
            value=settings["search"]["max_pages"],
            help="Maximum number of pages that can be searched per source"
        )
        
        # Request delay
        settings["search"]["request_delay"] = st.slider(
            "Request Delay (seconds)",
            min_value=0.5,
            max_value=5.0,
            value=settings["search"]["request_delay"],
            step=0.1,
            help="Delay between requests to prevent rate limiting"
        )
    
    # Advanced Settings
    with advanced_tab:
        st.subheader("Advanced Settings")
        
        # Request timeout
        settings["advanced"]["request_timeout"] = st.slider(
            "Request Timeout (seconds)",
            min_value=5,
            max_value=30,
            value=settings["advanced"]["request_timeout"],
            step=1,
            help="Maximum time to wait for a response from a source"
        )
        
        # Cache results
        settings["advanced"]["cache_results"] = st.checkbox(
            "Cache Search Results",
            value=settings["advanced"]["cache_results"],
            help="Store search results in cache to improve performance for repeated searches"
        )
        
        if settings["advanced"]["cache_results"]:
            # Cache expiry
            settings["advanced"]["cache_expiry_hours"] = st.number_input(
                "Cache Expiry (hours)",
                min_value=1,
                max_value=168,  # 1 week
                value=settings["advanced"]["cache_expiry_hours"],
                help="How long to keep cached results before refreshing"
            )
        
        # Experimental features
        st.subheader("Experimental Features")
        st.warning("These features are experimental and may not work correctly.")
        
        # Parallel requests
        settings["advanced"]["parallel_requests"] = st.checkbox(
            "Enable Parallel Requests",
            value=settings["advanced"]["parallel_requests"],
            help="Query multiple sources simultaneously (may cause rate limiting issues)"
        )
        
        # Clear cache button
        if settings["advanced"]["cache_results"]:
            if st.button("Clear Cache"):
                st.cache_data.clear()
                st.success("Cache cleared successfully!")
    
    # About tab
    with about_tab:
        st.subheader("About News & Content Downloader")
        
        st.markdown("""
        ### Version 1.0
        
        This application allows you to search and download content from multiple sources including news sites, 
        blogs, and social media platforms.
        
        #### Features:
        - Multi-source search
        - Data visualization
        - Excel export
        - Customizable settings
        
        #### Source Code:
        The source code for this application is available on GitHub.
        
        #### Support:
        For support or feature requests, please open an issue on GitHub.
        """)
    
    # Save button
    if st.button("Save Settings", type="primary"):
        if save_settings(settings):
            st.success("Settings saved successfully!")
        else:
            st.error("Failed to save settings. Please try again.")
    
    # Reset button
    if st.button("Reset to Defaults"):
        if save_settings(DEFAULT_SETTINGS):
            st.success("Settings reset to defaults!")
            st.rerun()  # Reload the page to show defaults
        else:
            st.error("Failed to reset settings. Please try again.")

if __name__ == "__main__":
    st.set_page_config(page_title="Settings", layout="wide", page_icon="⚙️")
    settings_page() 