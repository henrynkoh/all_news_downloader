# News & Content Downloader Web Application

A powerful application for searching, collecting, analyzing, and visualizing content from multiple sources including news sites, search engines, social media platforms, and blogs.

## Features

- **Multi-source search**: Search across multiple content platforms simultaneously
- **Real-time progress tracking**: Watch as your searches progress across different sources
- **Data visualization**: Analyze your search results with built-in visualization tools
- **Excel export**: Download your results in Excel format for further analysis
- **Clickable links**: All links in search results open in new tabs for easy browsing

## Usage

1. Enter your search keywords in the search bar
2. Select the source(s) you want to search
3. Set the number of pages to fetch
4. Click the 🔍 Search button
5. View your results in a table with clickable links
6. Download the results as an Excel file

## Directories

- **downloads/**: Excel files are saved here with names like "keyword_news_date.xlsx"
- **sources/**: Contains modules for different content sources

## Running the Application

```bash
streamlit run app.py
```

The application will be available at http://localhost:8501 (or another port if 8501 is in use).
