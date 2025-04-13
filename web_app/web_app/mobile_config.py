"""
Mobile-specific configurations for News & Content Downloader app
This module provides customized UI and functionality for mobile devices
"""

import streamlit as st
import os
import platform

def detect_platform():
    """Detect whether we're running on mobile or desktop"""
    # This is a best-effort detection, not perfect
    user_agent = st.get_option("browser.gatherUsageStats")
    is_ios = "iOS" in user_agent if user_agent else False
    is_android = "Android" in user_agent if user_agent else False
    is_mobile = is_ios or is_android
    
    # Fallback detection using screen width
    if not is_mobile and "get_page_width" in dir(st):
        width = st.get_page_width()
        is_mobile = width < 768
    
    return {
        "is_mobile": is_mobile,
        "is_ios": is_ios,
        "is_android": is_android,
        "device_info": platform.platform()
    }

def setup_mobile_ui():
    """Configure UI for mobile devices"""
    platform_info = detect_platform()
    
    if platform_info["is_mobile"]:
        # Apply mobile-specific CSS
        st.markdown(
            """
            <style>
            /* Mobile-specific styles */
            .stButton button {
                height: 3rem;
                font-size: 1rem;
                width: 100%;
            }
            
            /* Increase form element sizes for touch */
            .stTextInput input, .stNumberInput input, .stTextArea textarea {
                font-size: 1rem;
                padding: 0.75rem;
            }
            
            /* Make checkboxes and radio buttons larger */
            .stCheckbox label, .stRadio label {
                font-size: 1rem;
            }
            
            /* Adjust table display for narrow screens */
            table {
                font-size: 0.85rem;
                width: 100%;
                display: block;
                overflow-x: auto;
            }
            
            /* Adjust column display */
            .st-bx {
                flex-wrap: wrap;
            }
            
            /* Make sure sidebar is better for mobile */
            .css-1v3fvcr, .css-1iyw2u1, .css-1l4y5mu {
                width: 100%;
                margin-left: 0;
            }
            
            /* Adjust header and text sizes */
            h1 {
                font-size: 1.5rem !important;
            }
            
            h2 {
                font-size: 1.3rem !important;
            }
            
            h3 {
                font-size: 1.1rem !important;
            }
            
            p, li, div {
                font-size: 0.95rem !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # Return mobile configuration settings
        return {
            "use_compact_layout": True,
            "limit_results": 20,  # Show fewer results on mobile
            "table_height": 400,  # Smaller table height
            "use_pagination": True,
            "disable_visualizations": False,
            "visualization_simplified": True,
            "download_enabled": platform_info["is_ios"]  # iOS often has more limitations
        }
    else:
        # Default desktop settings
        return {
            "use_compact_layout": False,
            "limit_results": 50,
            "table_height": 600,
            "use_pagination": False,
            "disable_visualizations": False,
            "visualization_simplified": False,
            "download_enabled": True
        }

def get_mobile_downloads_dir():
    """Get appropriate downloads directory for mobile"""
    # iOS with Pythonista
    if 'Pythonista3' in os.path.abspath(os.getcwd()):
        return os.path.join(os.path.expanduser("~/Documents"), "downloads")
    # iOS with Pyto
    elif 'Pyto' in os.path.abspath(os.getcwd()):
        return os.path.join(os.path.expanduser("~/Documents"), "downloads")
    # Android with Pydroid
    elif 'com.termux' in os.path.abspath(os.getcwd()):
        return os.path.join(os.path.expanduser("~/storage/downloads"), "news_downloader")
    # Default
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, "downloads")

def create_mobile_navigation():
    """Create a touch-friendly navigation for mobile"""
    platforms = detect_platform()
    
    if platforms["is_mobile"]:
        # Create a dropdown for navigation instead of buttons
        nav_options = {
            "🔍 Search": "search",
            "📊 Visualize": "visualize", 
            "📣 Create Ads": "ads",
            "⚙️ Settings": "settings"
        }
        
        # Store current page in session state if not there
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'search'
            
        # Use a selectbox for navigation
        current_label = next((k for k, v in nav_options.items() if v == st.session_state.current_page), list(nav_options.keys())[0])
        selected_label = st.selectbox("Navigation", list(nav_options.keys()), index=list(nav_options.keys()).index(current_label))
        
        # Update page if changed
        if nav_options[selected_label] != st.session_state.current_page:
            st.session_state.current_page = nav_options[selected_label]
            st.rerun()
            
        return True
    
    # Return False to indicate standard navigation should be used
    return False

# Example usage in main app
if __name__ == "__main__":
    # This is just for testing this module independently
    st.title("Mobile UI Test")
    
    mobile_settings = setup_mobile_ui()
    st.write("Mobile settings:", mobile_settings)
    
    platform_info = detect_platform()
    st.write("Platform detection:", platform_info)
    
    downloads_dir = get_mobile_downloads_dir()
    st.write("Downloads directory:", downloads_dir)
    
    is_mobile_nav = create_mobile_navigation()
    st.write("Using mobile navigation:", is_mobile_nav) 