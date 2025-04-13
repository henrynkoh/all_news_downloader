import os
import platform
import subprocess
import shutil

def build_desktop_app():
    """Build standalone desktop application using PyInstaller"""
    
    # Create directories
    os.makedirs("dist", exist_ok=True)
    os.makedirs("build", exist_ok=True)
    
    # Determine platform
    system = platform.system()
    
    print(f"Building for {system}...")
    
    # Define PyInstaller command
    if system == "Windows":
        cmd = [
            "pyinstaller",
            "--name=NaverNewsDownloader",
            "--onefile",
            "--windowed",
            "--icon=app_icon.ico",
            "--add-data=README.md;.",
            "naver_news_downloader.py"
        ]
    elif system == "Darwin":  # macOS
        cmd = [
            "pyinstaller",
            "--name=NaverNewsDownloader",
            "--onefile",
            "--windowed",
            "--add-data=README.md:.",
            "naver_news_downloader.py"
        ]
    else:  # Linux
        cmd = [
            "pyinstaller",
            "--name=NaverNewsDownloader",
            "--onefile",
            "--add-data=README.md:.",
            "naver_news_downloader.py"
        ]
    
    # Run PyInstaller
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Error building executable:")
        print(result.stderr)
        return False
    
    print(f"Build successful! Executable is in dist/ directory")
    return True

def create_web_app():
    """Create a simple web application package for deployment"""
    
    # Create web app directory
    web_dir = "web_app"
    os.makedirs(web_dir, exist_ok=True)
    
    # Copy necessary files
    shutil.copy("naver_news_downloader.py", f"{web_dir}/")
    shutil.copy("requirements.txt", f"{web_dir}/")
    
    # Create app.py for web interface
    with open(f"{web_dir}/app.py", "w") as f:
        f.write("""
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from naver_news_downloader import get_naver_news, save_to_excel

st.set_page_config(page_title="Naver News Downloader", layout="wide")

st.title("Naver News Downloader")

with st.form("search_form"):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        keyword = st.text_input("Search Keyword", placeholder="Enter keyword...")
    
    with col2:
        pages = st.number_input("Number of Pages", min_value=1, max_value=20, value=5)
    
    submitted = st.form_submit_button("Search")
    
    if submitted and keyword:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Create a custom function to handle progress updates
        def get_news_with_progress():
            articles = []
            status_text.text(f"Searching for '{keyword}' news...")
            
            for page in range(1, pages + 1):
                progress = (page - 1) / pages
                progress_bar.progress(progress)
                status_text.text(f"Fetching page {page}/{pages}...")
                
                # Call the original function but with our specific page
                page_articles = get_naver_news(keyword, max_pages=1, start_page=page)
                articles.extend(page_articles)
            
            progress_bar.progress(1.0)
            return articles
        
        # Get articles
        try:
            articles = get_news_with_progress()
            
            if articles:
                # Convert to DataFrame for display
                df = pd.DataFrame(articles)
                
                # Show results
                status_text.text(f"Found {len(articles)} articles")
                st.dataframe(df)
                
                # Create Excel file
                today = datetime.now().strftime('%Y%m%d')
                filename = f"downloads/{keyword}_news_{today}.xlsx"
                os.makedirs("downloads", exist_ok=True)
                
                save_to_excel(articles, filename)
                
                # Provide download button
                with open(filename, "rb") as file:
                    st.download_button(
                        label="Download Excel File",
                        data=file,
                        file_name=f"{keyword}_news_{today}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                status_text.text("No articles found.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
""")
    
    # Create requirements.txt for web app
    with open(f"{web_dir}/requirements.txt", "w") as f:
        f.write("""
streamlit>=1.10.0
pandas>=1.3.0
requests>=2.25.1
beautifulsoup4>=4.9.3
openpyxl>=3.0.7
""")
    
    # Create README for web app
    with open(f"{web_dir}/README.md", "w") as f:
        f.write("""# Naver News Downloader Web App

A web-based interface for downloading news articles from Naver Search.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

Then open your browser to http://localhost:8501
""")
    
    print("Web app created in web_app/ directory")
    return True

if __name__ == "__main__":
    print("Building Naver News Downloader apps...")
    print("\n1. Building desktop application...")
    build_desktop_app()
    
    print("\n2. Creating web application package...")
    create_web_app()
    
    print("\nBuild process complete!")
    print("Executables are in the dist/ directory")
    print("Web app is in the web_app/ directory") 