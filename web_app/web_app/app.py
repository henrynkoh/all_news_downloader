import streamlit as st
import pandas as pd
import os
import sys
import random
from datetime import datetime
import streamlit.components.v1 as components
import time
from functools import lru_cache
import matplotlib.pyplot as plt
from io import BytesIO

# Add parent directory to path to import the crawler modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the source modules
try:
    from sources import AVAILABLE_SOURCES, get_source_function
except ImportError:
    # Define a fallback if sources module isn't available
    from naver_news_downloader import get_naver_news, save_to_excel
    
    # Placeholder functions for Google Search and YouTube
    def get_google_search_results(keyword, max_pages=1, start_page=1):
        """Placeholder function for Google Search results"""
        results = []
        # Generate some dummy results
        for i in range(1, random.randint(5, 10)):
            results.append({
                '제목': f"Google result: {keyword} - Article {i}",
                '내용': f"This is a sample description for {keyword} related content. Contains various information about the topic searched.",
                '언론사': f"Google Source {i}",
                '날짜': datetime.now().strftime('%Y.%m.%d'),
                '링크': f"https://www.google.com/search?q={keyword.replace(' ', '+')}#{i}"
            })
        # Simulate network delay
        time.sleep(0.5)
        return results

    def get_youtube_videos(keyword, max_pages=1, start_page=1):
        """Placeholder function for YouTube search results"""
        results = []
        # Generate some dummy results
        for i in range(1, random.randint(3, 8)):
            results.append({
                '제목': f"YouTube: {keyword} - Video {i}",
                '내용': f"This is a sample description for {keyword} related YouTube video. Watch this video to learn more about this topic.",
                '언론사': f"YouTube Channel {i}",
                '날짜': datetime.now().strftime('%Y.%m.%d'),
                '링크': f"https://www.youtube.com/results?search_query={keyword.replace(' ', '+')}#{i}"
            })
        # Simulate network delay
        time.sleep(0.5)
        return results
    
    # Define our available sources
    AVAILABLE_SOURCES = {
        "naver_news": {
            "name": "Naver News",
            "icon": "🇰🇷",
            "function": get_naver_news,
            "enabled": True,
            "description": "Official Korean news articles from Naver",
        },
        "google_search": {
            "name": "Google Search",
            "icon": "🔍",
            "function": get_google_search_results,
            "enabled": True,
            "description": "Web search results from Google",
        },
        "youtube": {
            "name": "YouTube",
            "icon": "▶️",
            "function": get_youtube_videos,
            "enabled": True,
            "description": "Video content from YouTube",
        },
    }
    
    def get_source_function(source_key):
        """Get the function for a specific source"""
        if source_key in AVAILABLE_SOURCES and AVAILABLE_SOURCES[source_key]["enabled"]:
            return AVAILABLE_SOURCES[source_key]["function"]
        return None

# Import other pages
try:
    from settings import settings_page, load_settings
    from visualize import visualize_page
except ImportError:
    # Define placeholders if modules don't exist
    def settings_page():
        st.error("Settings module not found")
    
    def visualize_page():
        """Basic visualization page for search results"""
        st.title("📊 Data Visualization")
        
        # Check if we have data from search
        if hasattr(st.session_state, 'visualization_data') and st.session_state.visualization_data is not None:
            df = st.session_state.visualization_data
            keyword = st.session_state.visualization_keyword
            st.subheader(f"Visualizing data for '{keyword}'")
            
            # Overview statistics
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Items", len(df))
            col2.metric("Unique Sources", df['Source'].nunique() if 'Source' in df.columns else 'N/A')
            
            # Date range if available
            if '날짜' in df.columns:
                try:
                    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
                    date_range = (df['날짜'].max() - df['날짜'].min()).days
                    col3.metric("Date Range (days)", date_range)
                except:
                    col3.metric("Date Range", "N/A")
            
            # Source distribution chart
            try:
                if 'Source' in df.columns:
                    st.subheader("Source Distribution")
                    
                    fig, ax = plt.subplots(figsize=(10, 6))
                    source_counts = df['Source'].value_counts()
                    source_counts.plot(kind='bar', ax=ax)
                    plt.title('Source Distribution')
                    plt.ylabel('Count')
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                    # Show source data
                    source_data = df['Source'].value_counts().reset_index()
                    source_data.columns = ['Source', 'Count']
                    source_data['Percentage'] = (source_data['Count'] / source_data['Count'].sum() * 100).round(2)
                    st.dataframe(source_data)
                    
                # Word cloud if content column exists
                content_col = '내용' if '내용' in df.columns else None
                if content_col:
                    try:
                        st.subheader("Word Cloud")
                        from wordcloud import WordCloud
                        
                        # Generate word cloud
                        text = ' '.join(df[content_col].astype(str).tolist())
                        wordcloud = WordCloud(width=800, height=400, background_color='white', 
                                           max_words=100).generate(text)
                        
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.imshow(wordcloud, interpolation='bilinear')
                        ax.axis('off')
                        st.pyplot(fig)
                    except Exception as wc_err:
                        st.error(f"Error generating word cloud: {str(wc_err)}")
                
                # Raw data
                with st.expander("View Raw Data"):
                    st.dataframe(df)
                
            except Exception as viz_error:
                st.error(f"Error creating visualizations: {str(viz_error)}")
        else:
            st.info("Please search for content first to visualize data. Use the Search page to find content, then click 'Visualize These Results'.")
            
            # Example visualization with placeholder data
            st.markdown("### Example Visualization")
            import pandas as pd
            import matplotlib.pyplot as plt
            import random
            
            placeholder_df = pd.DataFrame({
                'Source': ['Naver News', 'Google Search', 'YouTube', 'Twitter/X', 'Medium'] * 5,
                'Date': pd.date_range(start='2023-01-01', periods=25),
                'Content Length': [random.randint(100, 1000) for _ in range(25)]
            })
            
            # Show example
            fig, ax = plt.subplots(figsize=(10, 5))
            placeholder_df['Source'].value_counts().plot(kind='bar', ax=ax)
            plt.title('Example: Source Distribution')
            plt.ylabel('Count')
            plt.tight_layout()
            st.pyplot(fig)
    
    def load_settings():
        return {
            "theme": "dark",
            "display": {"table_height": 600},
            "search": {"default_pages": 5, "max_pages": 20}
        }

# Import the ad creator module
try:
    from sources.ad_creator import create_multi_platform_ads
except ImportError:
    # Define a placeholder if module isn't available
    def create_multi_platform_ads(platforms, ad_data):
        return {p: {"status": "error", "message": "Ad creator module not available"} for p in platforms}

# Import platform detection module if available
try:
    from mobile_config import detect_platform, setup_mobile_ui, create_mobile_navigation, get_mobile_downloads_dir
    MOBILE_SUPPORT_ENABLED = True
except ImportError:
    MOBILE_SUPPORT_ENABLED = False
    
    # Placeholder functions when mobile module isn't available
    def detect_platform():
        return {"is_mobile": False, "is_ios": False, "is_android": False}
        
    def setup_mobile_ui():
        return {
            "use_compact_layout": False,
            "limit_results": 50,
            "table_height": 600,
            "use_pagination": False,
            "disable_visualizations": False
        }
        
    def create_mobile_navigation():
        return False
        
    def get_mobile_downloads_dir():
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")

# Page config
st.set_page_config(page_title="News & Content Downloader", layout="wide", page_icon="📰")

# Load custom CSS
def load_css(css_file):
    with open(css_file, 'r') as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Create CSS file if it doesn't exist
css_path = os.path.join(os.path.dirname(__file__), 'style.css')
if not os.path.exists(css_path):
    with open(css_path, 'w') as f:
        f.write("""/* Base styling */
.stApp {
    background-color: #111111;
    color: #FFFFFF;
}

table {
    border-collapse: collapse;
    width: 100%;
    font-size: 14px;
}

th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}

tr:nth-child(even) {
    background-color: #f2f2f2;
}

tr:nth-child(odd) {
    background-color: #ffffff;
}

th {
    padding-top: 12px;
    padding-bottom: 12px;
    background-color: #4CAF50;
    color: white;
}

td a {
    text-decoration: underline;
    color: #0366d6;
}

td a:hover {
    text-decoration: underline;
    color: #0056b3;
}
</style>

<script>
// Ensure all links in the table open in new tabs
document.addEventListener('DOMContentLoaded', function() {
    var links = document.querySelectorAll('table a');
    for (var i = 0; i < links.length; i++) {
        links[i].setAttribute('target', '_blank');
        links[i].setAttribute('rel', 'noopener noreferrer');
    }
});
</script>
""")

# Load the CSS
load_css(css_path)

# Top navigation bar
def navigation():
    # Check if we should use mobile navigation
    if MOBILE_SUPPORT_ENABLED and create_mobile_navigation():
        # Mobile navigation is already created
        return
    
    # Regular desktop navigation
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
    with col1:
        st.write("## 📰 News & Content Downloader")
    
    # Store page selection in session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'search'
    
    # Navigation buttons
    with col2:
        if st.button("🔍 Search", use_container_width=True, 
                  type="primary" if st.session_state.current_page == 'search' else "secondary",
                  key="nav_search_button"):
            st.session_state.current_page = 'search'
            st.rerun()
    
    with col3:
        if st.button("📊 Visualize", use_container_width=True,
                  type="primary" if st.session_state.current_page == 'visualize' else "secondary",
                  key="nav_visualize_button"):
            st.session_state.current_page = 'visualize'
            st.rerun()
    
    with col4:
        if st.button("📣 Create Ads", use_container_width=True,
                  type="primary" if st.session_state.current_page == 'ads' else "secondary",
                  key="nav_ads_button"):
            st.session_state.current_page = 'ads'
            st.rerun()
            
    with col5:
        if st.button("⚙️ Settings", use_container_width=True,
                  type="primary" if st.session_state.current_page == 'settings' else "secondary",
                  key="nav_settings_button"):
            st.session_state.current_page = 'settings'
            st.rerun()
            
    st.markdown("---")

def make_clickable(link):
    # Returns a clickable link that opens in a new tab
    return f'<a href="{link}" target="_blank" rel="noopener noreferrer">{link}</a>'

def dataframe_with_clickable_links(df):
    # Memory optimization: limit dataframe size for display
    # If dataframe is very large, show only first 100 rows to avoid memory issues
    if len(df) > 100:
        display_df = df.head(100).copy()
        st.warning(f"⚠️ Showing only the first 100 of {len(df)} results to optimize performance. All results will still be included in the Excel download.")
    else:
        display_df = df.copy()
        
    # Convert links to clickable HTML
    df_html = display_df.copy()
    
    # Apply the clickable links to all URL fields
    for col in df_html.columns:
        if col.lower().endswith('url') or col.lower().endswith('link') or col == 'url' or col == 'link':
            df_html[col] = df_html[col].apply(make_clickable)
    
    # Get the styling
    styles = [
        {
            'selector': 'table',
            'props': [
                ('border-collapse', 'collapse'),
                ('width', '100%'),
                ('font-size', '14px'),
                ('text-align', 'left')
            ]
        },
        {
            'selector': 'th',
            'props': [
                ('background-color', '#4CAF50'),
                ('color', 'white'),
                ('font-weight', 'bold'),
                ('border', '1px solid #ddd'),
                ('padding', '8px')
            ]
        },
        {
            'selector': 'td',
            'props': [
                ('border', '1px solid #ddd'),
                ('padding', '8px'),
                ('max-width', '300px'),
                ('overflow', 'hidden'),
                ('text-overflow', 'ellipsis'),
                ('white-space', 'nowrap')
            ]
        },
        {
            'selector': 'tr:nth-child(even)',
            'props': [
                ('background-color', '#f8f8f8')  # Lighter background for even rows
            ]
        },
        {
            'selector': 'tr:hover',
            'props': [
                ('background-color', '#e0f7fa')  # Light blue when hovering
            ]
        },
        {
            'selector': 'a',
            'props': [
                ('color', '#1976D2'),  # Material blue for links
                ('text-decoration', 'none')
            ]
        },
        {
            'selector': 'a:hover',
            'props': [
                ('text-decoration', 'underline'),
                ('color', '#0D47A1')  # Darker blue on hover
            ]
        }
    ]
    
    html = df_html.to_html(escape=False, index=False)
    
    # Add some CSS to make the table look better and ensure links open in new tabs
    html = f"""
    <style>
    {';'.join([f'{style["selector"]} {{ {";".join([f"{prop}: {value}" for prop, value in style["props"]])}' for style in styles])}
    </style>
    <script>
    // Ensure all links in the table open in new tabs
    document.addEventListener('DOMContentLoaded', function() {{
        var links = document.querySelectorAll('table a');
        for (var i = 0; i < links.length; i++) {{
            links[i].setAttribute('target', '_blank');
            links[i].setAttribute('rel', 'noopener noreferrer');
        }}
    }});
    </script>
    {html}
    """
    return html

def save_to_excel(articles, filename):
    """Save results to Excel file"""
    import openpyxl
    from openpyxl import Workbook
    
    # Make sure the downloads directory exists
    # Use mobile-aware path if available
    if MOBILE_SUPPORT_ENABLED:
        downloads_dir = get_mobile_downloads_dir()
        # Make sure filename includes the path
        if not os.path.dirname(filename):
            filename = os.path.join(downloads_dir, os.path.basename(filename))
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
    
    wb = Workbook()
    ws = wb.active
    
    # Get all keys/columns from the articles
    all_keys = set()
    for article in articles:
        all_keys.update(article.keys())
    
    # Order columns - put standard columns first
    standard_columns = ['제목', '내용', '언론사', '날짜', '링크', 'Source']
    columns = []
    for col in standard_columns:
        if col in all_keys:
            columns.append(col)
            all_keys.remove(col)
    # Add any remaining keys
    columns.extend(sorted(all_keys))
    
    # Add header row
    ws.append(columns)
    
    # Add data rows
    for article in articles:
        row = []
        for col in columns:
            row.append(article.get(col, ""))
        ws.append(row)
    
    # Auto-adjust column widths
    for column in ws.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        # Limit width to prevent extremely wide columns
        adjusted_width = min(max_length + 2, 100)
        ws.column_dimensions[column[0].column_letter].width = adjusted_width
    
    # Save file
    wb.save(filename)
    print(f"Data saved to {filename}")
    print(f"File location: {os.path.abspath(filename)}")

# Implement caching for expensive operations
@lru_cache(maxsize=32)
def cached_search(keyword, source_key, max_pages=1, start_page=1):
    """Cached version of source function calls to reduce redundant API calls"""
    try:
        source_function = get_source_function(source_key)
        if source_function:
            return source_function(keyword, max_pages=max_pages, start_page=start_page)
        return []
    except Exception as e:
        st.error(f"Error in cached search for {source_key}: {str(e)}")
        return []

def search_page():
    # Apply mobile UI settings if available
    mobile_settings = setup_mobile_ui() if MOBILE_SUPPORT_ENABLED else {}
    limit_results = mobile_settings.get("limit_results", 50)
    table_height = mobile_settings.get("table_height", 600)
    use_compact_layout = mobile_settings.get("use_compact_layout", False)
    
    # Get settings
    settings = load_settings()
    
    # Simple sidebar for input controls
    with st.sidebar:
        st.sidebar.image("https://raw.githubusercontent.com/streamlit/streamlit/master/examples/data/logo.png", width=100)
        st.sidebar.title("News Search")
        
        # Search keyword with better styling
        st.markdown("""
        <style>
        .search-container {
            background-color: #2E2E2E;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        </style>
        <div class="search-container">
            <h3 style="color: #FFFFFF;">Search Keyword</h3>
        </div>
        """, unsafe_allow_html=True)
        keyword = st.text_input("Search Keyword", placeholder="Enter keyword...", value=keyword if 'keyword' in locals() else "", label_visibility="visible")
        
        # Source selection with icons
        st.markdown("""
        <div class="search-container">
            <h3 style="color: #FFFFFF;">Select Sources</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Create checkboxes for all available sources
        selected_sources = {}
        for source_key, source_info in AVAILABLE_SOURCES.items():
            selected_sources[source_key] = st.checkbox(
                f"{source_info['icon']} {source_info['name']}", 
                value=source_key in ["naver_news", "google_search"],  # Default selected sources
                help=source_info["description"],
                key=f"source_{source_key}"
            )
        
        # Advanced options
        st.markdown("""
        <div class="search-container">
            <h3 style="color: #FFFFFF;">Advanced Options</h3>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("Search Settings"):
            pages = st.number_input("Number of Pages", min_value=1, max_value=settings["search"]["max_pages"], value=settings["search"]["default_pages"])
            max_results = st.slider("Results Limit", min_value=10, max_value=100, value=limit_results, step=10)
        
        # Adjust button size for mobile if needed
        button_style = "height:3rem;font-size:1.1rem;" if use_compact_layout else ""
        
        # Search button with better styling
        st.markdown("<br>", unsafe_allow_html=True)
        search_col1, search_col2 = st.columns([1, 3])
        with search_col2:
            search_button = st.button("🔍 Search", type="primary", use_container_width=True, key="main_search_button")
            if button_style:
                st.markdown(f"""
                <style>
                div[data-testid="stButton"] button {{
                    {button_style}
                }}
                </style>
                """, unsafe_allow_html=True)

    # Main content area
    results_container = st.container()
    progress_container = st.container()

    # Show welcome message when no search is active
    with results_container:
        if not search_button or not keyword:
            # Add a colorful header - simpler for mobile
            if use_compact_layout:
                st.markdown("# 📰 News & Content Downloader")
                st.markdown("Search and download content from multiple sources")
            else:
                # Full desktop version
                st.markdown("""
                <div style="background-color:#1E1E1E; padding:10px; border-radius:10px; margin-bottom:20px">
                    <h1 style="color:#4CAF50; text-align:center">📰 News & Content Downloader</h1>
                    <p style="color:white; text-align:center; font-size:1.2em">Search and download content from multiple sources</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Instructions - responsive version
            if use_compact_layout:
                st.markdown("""
                ### How to use:
                1. Enter your search keyword
                2. Select your sources
                3. Click Search button
                """)
            else:
                # Full desktop version
                st.markdown("""
                <div style="display:flex; justify-content:space-around; margin-bottom:30px">
                    <div style="text-align:center; padding:15px">
                        <h3>👈 Step 1</h3>
                        <p>Enter your search keyword in the sidebar</p>
                    </div>
                    <div style="text-align:center; padding:15px">
                        <h3>🔍 Step 2</h3>
                        <p>Select your sources and options</p>
                    </div>
                    <div style="text-align:center; padding:15px">
                        <h3>📊 Step 3</h3>
                        <p>View and download results</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Example search - responsive for mobile
            st.subheader("Try an example search:")
            
            if use_compact_layout:
                # Single column for mobile
                if st.button("Search for 'AI'", key="example_ai_button", use_container_width=True):
                    st.session_state.example_keyword = "AI"
                    st.session_state.run_example = True
                if st.button("Search for 'Technology'", key="example_tech_button", use_container_width=True):
                    st.session_state.example_keyword = "Technology"
                    st.session_state.run_example = True
                if st.button("Search for 'Health'", key="example_health_button", use_container_width=True):
                    st.session_state.example_keyword = "Health"
                    st.session_state.run_example = True
            else:
                # Multiple columns for desktop
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("Search for 'AI'", key="example_ai_button"):
                        st.session_state.example_keyword = "AI"
                        st.session_state.run_example = True
                with col2:
                    if st.button("Search for 'Technology'", key="example_tech_button"):
                        st.session_state.example_keyword = "Technology"
                        st.session_state.run_example = True
                with col3:
                    if st.button("Search for 'Health'", key="example_health_button"):
                        st.session_state.example_keyword = "Health"
                        st.session_state.run_example = True
                    
            # More detailed instructions
            with st.expander("How to use this app"):
                st.markdown("""
                ### Detailed Instructions:
                1. **Enter your search keyword** in the sidebar search box
                2. **Select which sources** to search from the available options
                3. **Set the number of pages** to fetch in Advanced Options
                4. **Click the Search button** to start the search
                5. **Wait for results** to appear and download them as needed
                
                ### Features:
                - Search multiple sources simultaneously
                - Real-time progress tracking
                - Download results as Excel files
                - Clickable links in the results table
                - Data visualization with the Visualize tab
                - Customizable settings in the Settings tab
                
                ### Available Sources:
                - 🇰🇷 **Naver News** - Korean news articles from Naver
                - 📰 **Daum News** - Korean news articles from Daum
                - 🔍 **Google Search** - Web search results from Google
                - ▶️ **YouTube** - Video content from YouTube
                - 📝 **Medium** - Blog posts from Medium platform
                - 🌐 **WordPress** - Blog posts from WordPress blogs
                - 🐦 **Twitter/X** - Posts from Twitter/X platform
                - 📘 **Naver Blog** - Blog posts from Naver Blog platform
                - ✏️ **Tistory** - Blog posts from Tistory platform
                - 🧵 **Threads** - Posts from Threads platform
                - 📝 **Google Blogger** - Blog posts from Google Blogger platform
                """)

    # Check if we should run an example search
    if hasattr(st.session_state, 'run_example') and st.session_state.run_example:
        # Set the keyword in the sidebar
        keyword = st.session_state.example_keyword
        # Reset flag
        st.session_state.run_example = False
        # Force rerun to trigger the search
        st.experimental_rerun()

    # Display results after search
    if search_button and keyword:
        # Clear any previous errors
        error_placeholder = st.empty()
        
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        # Modify the content function to use caching
        def get_content_with_progress():
            articles = []
            active_sources = []
            
            # Get list of selected sources
            for source_key, is_selected in selected_sources.items():
                if is_selected and source_key in AVAILABLE_SOURCES:
                    active_sources.append(source_key)
            
            if not active_sources:
                status_text.text("Please select at least one source")
                return []
                
            status_text.text(f"Searching for '{keyword}' in {len(active_sources)} sources...")
            
            # Track progress across all selected sources
            total_steps = len(active_sources) * pages
            current_step = 0
            
            # Fetch from each selected source
            for source_key in active_sources:
                source_info = AVAILABLE_SOURCES[source_key]
                source_name = source_info["name"]
                
                # For some sources, limit the number of pages to avoid long searches
                source_pages = min(pages, 3) if source_key in ["google_search", "youtube", "medium", "twitter", "threads"] else pages
                
                for page in range(1, source_pages + 1):
                    current_step += 1
                    current_progress = current_step / total_steps
                    progress_bar.progress(current_progress)
                    status_text.text(f"Fetching {source_name} - page {page}/{source_pages}...")
                    
                    try:
                        # Use the cached search function instead of direct calls
                        page_results = cached_search(keyword, source_key, max_pages=1, start_page=page)
                        
                        # Add source information to results
                        for result in page_results:
                            result['Source'] = source_name
                        
                        articles.extend(page_results)
                        
                        # Limit total results if needed
                        if len(articles) >= max_results:
                            break
                            
                    except Exception as e:
                        st.error(f"Error fetching {source_name} content: {str(e)}")
                        continue
                
                # Check if we've reached the total limit
                if len(articles) >= max_results:
                    break
            
            progress_bar.progress(1.0)
            
            # Limit results to max_results
            if len(articles) > max_results:
                articles = articles[:max_results]
            
            return articles
        
        # Get articles with better error handling
        try:
            articles = get_content_with_progress()
            
            with results_container:
                if articles:
                    # Convert to DataFrame for display
                    df = pd.DataFrame(articles)
                    
                    # Show results
                    st.subheader(f"Found {len(articles)} items for '{keyword}'")
                    
                    # Get table height from settings or mobile config
                    table_height = mobile_settings.get("table_height", settings["display"]["table_height"])
                    
                    # Show source distribution
                    source_counts = df['Source'].value_counts().reset_index()
                    source_counts.columns = ['Source', 'Count']
                    
                    # Display layout based on mobile or desktop
                    if use_compact_layout:
                        # Mobile-friendly layout (single column)
                        st.components.v1.html(dataframe_with_clickable_links(df), height=table_height)
                        st.write("### Source Distribution")
                        for idx, row in source_counts.iterrows():
                            st.metric(row['Source'], row['Count'])
                    else:
                        # Desktop layout (two columns)
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.components.v1.html(dataframe_with_clickable_links(df), height=table_height)
                        with col2:
                            st.write("### Source Distribution")
                            for idx, row in source_counts.iterrows():
                                st.metric(row['Source'], row['Count'])
                    
                    # Create Excel file with error handling
                    today = datetime.now().strftime('%Y%m%d')
                    
                    # Use mobile-aware downloads directory if available
                    if MOBILE_SUPPORT_ENABLED:
                        downloads_dir = get_mobile_downloads_dir()
                    else:
                        downloads_dir = "downloads"
                    
                    os.makedirs(downloads_dir, exist_ok=True)
                    filename = f"{downloads_dir}/{keyword}_results_{today}.xlsx"
                    
                    try:
                        save_to_excel(articles, filename)
                        
                        # Check if download is enabled (may be disabled on some mobile platforms)
                        download_enabled = mobile_settings.get("download_enabled", True) if MOBILE_SUPPORT_ENABLED else True
                        
                        if download_enabled:
                            # Provide download button - fix the error by reading the file first
                            try:
                                with open(filename, "rb") as file:
                                    file_data = file.read()
                                    
                                col1, col2 = st.columns([1, 1])
                                with col1:
                                    st.download_button(
                                        label="Download Excel File",
                                        data=file_data,
                                        file_name=f"{keyword}_results_{today}.xlsx",
                                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                        key="download_results_button"
                                    )
                                with col2:
                                    # Button to visualize results
                                    if st.button("📊 Visualize These Results", use_container_width=True, key="view_results_button"):
                                        st.session_state.current_page = 'visualize'
                                        # Store the current results for visualization
                                        st.session_state.visualization_data = df
                                        st.session_state.visualization_keyword = keyword
                                        st.rerun()
                            except Exception as e:
                                st.error(f"Download button error: {str(e)}")
                                st.write(f"File saved to: {filename}")
                        else:
                            # On platforms where download is disabled, just show the file location
                            st.info(f"Results saved to: {filename}")
                            if st.button("📊 Visualize These Results", use_container_width=True, key="view_results_button"):
                                st.session_state.current_page = 'visualize'
                                st.session_state.visualization_data = df
                                st.session_state.visualization_keyword = keyword
                                st.rerun()
                    except Exception as e:
                        st.error(f"Excel save error: {str(e)}")
                        # Try CSV as fallback
                        try:
                            csv_filename = f"{downloads_dir}/{keyword}_results_{today}.csv"
                            df.to_csv(csv_filename, index=False)
                            st.success(f"Results saved as CSV instead at {csv_filename}")
                            
                            if download_enabled:
                                with open(csv_filename, "rb") as file:
                                    file_data = file.read()
                                    
                                st.download_button(
                                    label="Download CSV File (Excel failed)",
                                    data=file_data,
                                    file_name=f"{keyword}_results_{today}.csv",
                                    mime="text/csv",
                                    key="download_csv_button"
                                )
                        except Exception as csv_err:
                            st.error(f"CSV save error: {str(csv_err)}")
                else:
                    st.markdown("""
                    <div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; text-align: center; margin-top: 50px;">
                        <h2 style="color: #4CAF50;">No results found</h2>
                        <p style="color: #FFFFFF; font-size: 18px;">
                            We couldn't find any content matching your search criteria.
                        </p>
                        <p style="color: #CCCCCC; font-size: 16px;">
                            Try adjusting your search keyword or selecting different sources.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            error_message = str(e)
            error_placeholder.error(f"An error occurred: {error_message}")
            # Log the error for debugging
            print(f"Search error: {error_message}")

# Add the social media ads creation page
def create_ads_page():
    st.title("📣 Social Media Ads Creator")
    
    with st.sidebar:
        st.sidebar.title("Ad Settings")
        
        # Platform selection
        st.subheader("Select Platforms")
        platforms = {
            "facebook": st.checkbox("Facebook", value=True),
            "instagram": st.checkbox("Instagram", value=True),
            "twitter": st.checkbox("X/Twitter"),
            "threads": st.checkbox("Threads"),
            "tistory": st.checkbox("Tistory"),
            "naver_blog": st.checkbox("Naver Blog"),
            "google_blogger": st.checkbox("Google Blogger"),
            "wordpress": st.checkbox("WordPress"),
            "tiktok": st.checkbox("TikTok")
        }
        
        # Ad content settings
        st.subheader("Ad Content")
        ad_title = st.text_input("Ad Title", placeholder="Enter compelling title")
        ad_description = st.text_area("Ad Description", placeholder="Enter ad description")
        ad_url = st.text_input("Target URL", placeholder="https://example.com")
        
        # Image upload
        st.subheader("Ad Media")
        ad_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        
        # Video upload for TikTok and other video platforms
        ad_video = st.file_uploader("Upload Video (For TikTok, Instagram Reels, etc.)", type=["mp4", "mov"], key="video_upload")
        
        # Target audience
        with st.expander("Target Audience"):
            age_min, age_max = st.slider("Age Range", 13, 65, (25, 45))
            gender = st.radio("Gender", ["All", "Male", "Female"])
            location = st.text_input("Location", placeholder="Enter target location")
            
            # More detailed targeting
            st.subheader("Interests & Behaviors")
            interests = st.multiselect("Interests", 
                ["Technology", "Fashion", "Travel", "Food", "Fitness", "Business", "Education", 
                 "Entertainment", "Finance", "Gaming", "Health", "Music", "Politics", "Sports"],
                default=["Technology"])
            
        # Budget & Schedule
        with st.expander("Budget & Schedule"):
            budget = st.number_input("Budget (USD)", min_value=5, value=50)
            start_date = st.date_input("Start Date")
            duration = st.slider("Campaign Duration (days)", 1, 30, 7)
            
        # Create ad button
        create_ad_button = st.button("Create Ad", type="primary", use_container_width=True, key="create_ad_button")
    
    # Main content area
    if not any(platforms.values()):
        st.info("Please select at least one platform to create ads.")
    else:
        selected_platforms = [p for p, selected in platforms.items() if selected]
        
        # Preview section
        st.subheader("Ad Preview")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### Content Preview")
            if ad_title:
                st.markdown(f"**{ad_title}**")
            if ad_description:
                st.markdown(ad_description)
            if ad_image:
                st.image(ad_image, use_column_width=True)
            elif ad_video:
                st.video(ad_video)
            else:
                st.markdown("*Upload an image or video to preview*")
                
        with col2:
            st.markdown("### Selected Platforms")
            for platform in selected_platforms:
                platform_name = platform.replace('_', ' ').title()
                st.markdown(f"✅ {platform_name}")
            
            if 'budget' in locals() and budget:
                st.markdown(f"**Budget:** ${budget}")
            if 'start_date' in locals() and start_date:
                st.markdown(f"**Start Date:** {start_date}")
                
        # Platform-specific settings
        st.subheader("Platform-Specific Settings")
        
        tabs = st.tabs([p.replace('_', ' ').title() for p in selected_platforms])
        
        platform_settings = {}
        
        for i, platform in enumerate(selected_platforms):
            with tabs[i]:
                if platform == "facebook":
                    st.markdown("### Facebook Ad Settings")
                    fb_objective = st.selectbox("Campaign Objective", 
                        ["Brand Awareness", "Traffic", "Engagement", "Lead Generation", "Conversions"], 
                        key="fb_objective")
                    fb_placement = st.multiselect("Ad Placement", 
                        ["Facebook Feed", "Facebook Stories", "Marketplace", "In-Article"], 
                        default=["Facebook Feed"], 
                        key="fb_placement")
                    platform_settings[platform] = {
                        "objective": fb_objective.upper().replace(" ", "_"),
                        "placements": fb_placement
                    }
                
                elif platform == "instagram":
                    st.markdown("### Instagram Ad Settings")
                    ig_format = st.radio("Ad Format", ["Image", "Video", "Carousel", "Stories", "Reels"], key="ig_format")
                    ig_call_to_action = st.selectbox("Call to Action", 
                        ["Learn More", "Shop Now", "Sign Up", "Contact Us"], 
                        key="ig_cta")
                    platform_settings[platform] = {
                        "format": ig_format,
                        "call_to_action": ig_call_to_action
                    }
                
                elif platform == "twitter":
                    st.markdown("### X/Twitter Ad Settings")
                    twitter_objective = st.selectbox("Campaign Objective", 
                        ["Awareness", "Consideration", "Conversion"], 
                        key="twitter_objective")
                    twitter_placement = st.checkbox("Enable Promoted Tweets", value=True, key="twitter_promoted")
                    platform_settings[platform] = {
                        "objective": twitter_objective,
                        "promoted_tweets": twitter_placement
                    }
                
                elif platform == "threads":
                    st.markdown("### Threads Ad Settings")
                    threads_format = st.radio("Ad Format", ["Image", "Video"], key="threads_format")
                    platform_settings[platform] = {
                        "format": threads_format
                    }
                
                elif platform == "tistory":
                    st.markdown("### Tistory Ad Settings")
                    tistory_blog = st.text_input("Tistory Blog URL", 
                        placeholder="https://yourblog.tistory.com", 
                        key="tistory_blog")
                    tistory_category = st.text_input("Category", key="tistory_category")
                    platform_settings[platform] = {
                        "blog_url": tistory_blog,
                        "category": tistory_category
                    }
                
                elif platform == "naver_blog":
                    st.markdown("### Naver Blog Ad Settings")
                    naver_blog_id = st.text_input("Naver Blog ID", key="naver_blog_id")
                    naver_blog_category = st.text_input("Category", key="naver_blog_category")
                    platform_settings[platform] = {
                        "blog_id": naver_blog_id,
                        "category": naver_blog_category
                    }
                
                elif platform == "google_blogger":
                    st.markdown("### Google Blogger Ad Settings")
                    blogger_id = st.text_input("Blogger ID", key="blogger_id")
                    blogger_labels = st.text_input("Labels (comma separated)", key="blogger_labels")
                    platform_settings[platform] = {
                        "blog_id": blogger_id,
                        "labels": blogger_labels.split(",") if blogger_labels else []
                    }
                
                elif platform == "wordpress":
                    st.markdown("### WordPress Ad Settings")
                    wp_site_url = st.text_input("WordPress Site URL", placeholder="https://yoursite.wordpress.com", key="wp_site_url")
                    wp_categories = st.text_input("Categories (comma separated)", key="wp_categories")
                    wp_tags = st.text_input("Tags (comma separated)", key="wp_tags") 
                    wp_post_type = st.radio("Post Type", ["Post", "Sponsored Content", "Page"], key="wp_post_type")
                    platform_settings[platform] = {
                        "site_url": wp_site_url,
                        "categories": wp_categories.split(",") if wp_categories else [],
                        "tags": wp_tags.split(",") if wp_tags else [],
                        "post_type": wp_post_type
                    }
                
                elif platform == "tiktok":
                    st.markdown("### TikTok Ad Settings")
                    tiktok_objective = st.selectbox("Campaign Objective", 
                        ["Traffic", "Conversions", "App Install", "Lead Generation", "Video Views"], 
                        key="tiktok_objective")
                    tiktok_format = st.radio("Ad Format", ["In-Feed", "TopView", "Branded Hashtag Challenge", "Branded Effect"], key="tiktok_format")
                    tiktok_music = st.text_input("Background Music (Optional)", key="tiktok_music")
                    tiktok_hashtags = st.text_input("Hashtags (comma separated)", key="tiktok_hashtags")
                    platform_settings[platform] = {
                        "objective": tiktok_objective,
                        "format": tiktok_format,
                        "music": tiktok_music,
                        "hashtags": tiktok_hashtags.split(",") if tiktok_hashtags else []
                    }
        
        # Results section for ad creation
        results_container = st.container()
        
        # Handle ad creation
        if create_ad_button:
            if not ad_title:
                st.error("Please enter an ad title")
            elif not ad_description:
                st.error("Please enter an ad description")
            elif not (ad_image or ad_video):
                st.error("Please upload either an image or video for your ad")
            else:
                with st.spinner("Creating ads..."):
                    # Save uploaded files temporarily if provided
                    media_paths = {}
                    
                    # Create temp directory if it doesn't exist
                    os.makedirs("temp", exist_ok=True)
                    
                    if ad_image is not None:
                        image_path = os.path.join("temp", ad_image.name)
                        with open(image_path, "wb") as f:
                            f.write(ad_image.getbuffer())
                        media_paths["image"] = image_path
                    
                    if ad_video is not None:
                        video_path = os.path.join("temp", ad_video.name)
                        with open(video_path, "wb") as f:
                            f.write(ad_video.getbuffer())
                        media_paths["video"] = video_path
                    
                    # Prepare ad data
                    ad_data = {
                        "title": ad_title,
                        "description": ad_description,
                        "target_url": ad_url if ad_url else None,
                        "media_paths": media_paths,
                        "target_audience": {
                            "age_min": age_min,
                            "age_max": age_max,
                            "gender": gender,
                            "location": location if location else None,
                            "interests": interests if 'interests' in locals() else []
                        },
                        "budget": budget,
                        "start_date": start_date.isoformat(),
                        "duration": duration
                    }
                    
                    # Add platform-specific settings
                    for platform, settings in platform_settings.items():
                        ad_data[platform] = settings
                    
                    # Create ads on selected platforms
                    results = create_multi_platform_ads(selected_platforms, ad_data)
                    
                    # Show results
                    with results_container:
                        st.subheader("Ad Creation Results")
                        
                        for platform, result in results.items():
                            platform_name = platform.replace('_', ' ').title()
                            
                            if result.get("status") == "success":
                                st.success(f"✅ {platform_name}: {result.get('message')}")
                            elif result.get("status") == "warning":
                                st.warning(f"⚠️ {platform_name}: {result.get('message')}")
                            else:
                                st.error(f"❌ {platform_name}: {result.get('message')}")
                        
                        # Show summary
                        success_count = sum(1 for r in results.values() if r.get("status") == "success")
                        if success_count > 0:
                            st.balloons()
                            st.markdown(f"**Success!** Created ads on {success_count} of {len(selected_platforms)} platforms.")
                            
                            # Clean up temp files
                            for path_type, path in media_paths.items():
                                if os.path.exists(path):
                                    try:
                                        os.remove(path)
                                    except:
                                        pass
        
        # Implementation note
        st.info("Note: This is a prototype interface. In this demo, actual API calls are simulated. To use the real APIs, you would need to add credentials for each platform in the credentials.json file.")

# Main app logic - determine which page to show
def main():
    # Apply mobile UI settings if available
    if MOBILE_SUPPORT_ENABLED:
        setup_mobile_ui()
    
    # Display navigation
    navigation()
    
    # Show the appropriate page
    if st.session_state.current_page == 'search':
        search_page()
    elif st.session_state.current_page == 'visualize':
        visualize_page()
    elif st.session_state.current_page == 'ads':
        create_ads_page()
    elif st.session_state.current_page == 'settings':
        settings_page()
    else:
        search_page()  # Default to search

if __name__ == "__main__":
    main()
