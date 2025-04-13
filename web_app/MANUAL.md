# Naver News Downloader: User Manual

## Overview

Naver News Downloader is a tool that searches for and downloads news articles from Naver, Korea's most popular search engine. The application collects news articles matching your search keyword and saves them to an Excel file, including:

- Article titles
- Content summaries
- Publisher names
- Publication dates
- Original article links

## Available Versions

The tool is available in multiple formats:

1. **Command Line Version**: Run through a terminal/command prompt
2. **Desktop Application**: Standalone executable for Windows, macOS, and Linux
3. **Web Application**: Browser-based version that works on any device including iPhones

## Quick Start Guide

### Command Line Version

1. Open your terminal/command prompt
2. Run:
   ```
   python naver_news_downloader.py "검색어" -p 5
   ```
3. Replace "검색어" with your search keyword and 5 with the number of pages to crawl
4. The results will be saved in the "downloads" folder

### Desktop Application

1. Launch the NaverNewsDownloader application
2. Enter your search keyword
3. Set the number of pages to crawl (1-20)
4. Click "Start Download"
5. Wait for the search to complete
6. The Excel file will be saved to the selected output directory

### Web Application

1. Start the web app:
   ```
   cd web_app
   streamlit run app.py
   ```
2. Your browser will open to http://localhost:8501
3. Enter your search keyword
4. Set the number of pages to crawl
5. Click "Search"
6. When results appear, click "Download Excel File"

## Detailed Tutorial

### 1. Installation

#### Command Line Version

**Prerequisites**: Python 3.7 or higher, pip

1. Download the repository
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

#### Desktop Application

1. Download the appropriate file for your system:
   - Windows: `NaverNewsDownloader.exe`
   - macOS: `NaverNewsDownloader.app` or `NaverNewsDownloader` binary
   - Linux: `NaverNewsDownloader` binary
2. For macOS/Linux binaries, make executable with:
   ```
   chmod +x NaverNewsDownloader
   ```

#### Web Application

1. Download the `web_app` folder
2. Install dependencies:
   ```
   cd web_app
   pip install -r requirements.txt
   ```
3. Run the setup script (optional):
   ```
   python setup_web_app.py
   ```

### 2. Using the Command Line Version

The command line tool offers several parameters:

```
python naver_news_downloader.py [keyword] [options]
```

**Options:**
- `-p, --pages`: Number of pages to crawl (default: 5)
- `-o, --output`: Custom output filename
- `-d, --dir`: Output directory (default: downloads)
- `-s, --start`: Starting page number (default: 1)

**Examples:**

```
# Basic usage (5 pages of results)
python naver_news_downloader.py "삼성전자"

# Crawl 10 pages of results
python naver_news_downloader.py "LG화학" -p 10

# Save to a custom file
python naver_news_downloader.py "네이버" -o "my_results.xlsx"

# Save to a specific directory
python naver_news_downloader.py "카카오" -d "my_data"

# Start from page 3
python naver_news_downloader.py "현대차" -s 3
```

### 3. Using the Desktop Application

The desktop application provides a graphical user interface for the same functionality:

1. **Launch the Application**:
   - Windows: Double-click the `.exe` file
   - macOS: Open the `.app` or run the binary
   - Linux: Run the binary

2. **Enter Search Information**:
   - Search Keyword: Type the term you want to search for
   - Number of Pages: Set how many pages of search results to crawl (1-20)
   - Output Directory: Choose where to save the Excel file

3. **Start the Search**:
   - Click the "Start Download" button
   - A progress bar will show the search status
   - Status messages appear in the text area

4. **Get Results**:
   - When complete, a message will show the file location
   - The Excel file is named: `keyword_news_YYYYMMDD.xlsx`

### 4. Using the Web Application

The web app is particularly useful for mobile access and remote use:

1. **Start the Web Server**:
   ```
   cd web_app
   streamlit run app.py
   ```

2. **Access the Interface**:
   - On your computer: http://localhost:8501
   - On mobile devices: http://YOUR_COMPUTER_IP:8501

3. **Search for News**:
   - Enter your keyword
   - Set the number of pages
   - Click the "Search" button

4. **View and Download Results**:
   - Results appear in a table on the page
   - Click "Download Excel File" to save the data

5. **Mobile Usage (iPhone)**:
   - Run the server on your computer
   - Find your computer's IP address
   - On your iPhone, open Safari and go to http://YOUR_COMPUTER_IP:8501
   - You can now search and download files from your phone

### 5. Understanding the Output

The Excel file contains the following columns:

1. **제목 (Title)**: The headline of the news article
2. **내용 (Content)**: A brief summary of the article's content
3. **언론사 (Publisher)**: The name of the news organization
4. **날짜 (Date)**: When the article was published (often in relative format like "2일 전" meaning "2 days ago")
5. **링크 (Link)**: URL to the full article

### 6. Cloud Deployment for Mobile Access

For permanent access from any device (including iPhone):

1. Create a GitHub repository with the web_app files
2. Sign up for Streamlit Cloud (https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Deploy the app
5. Access your app from the provided URL on any device

## Troubleshooting

### Common Issues

1. **No Search Results**:
   - Check your internet connection
   - Verify the keyword spelling
   - Try a more common search term

2. **File Permission Errors**:
   - Make sure you have write access to the output directory
   - Run as administrator (Windows) or use sudo (Mac/Linux) if needed

3. **Web App Not Accessible from Mobile**:
   - Ensure your computer and phone are on the same network
   - Check firewall settings
   - Verify the correct IP address is being used

4. **Missing Dependencies**:
   - Run `pip install -r requirements.txt` to install all required packages
   - For the web app, ensure Streamlit is installed: `pip install streamlit`

5. **Desktop App Security Warnings**:
   - On macOS, right-click and select "Open" instead of double-clicking
   - On Windows, click "More info" and "Run anyway"

### Getting Help

If you encounter any issues not covered in this manual:

1. Check the README.md file for additional information
2. Examine the error messages for clues
3. Try running the command-line version for more detailed error output

## Advanced Usage

### Custom Date Ranges

The current version searches all dates by default. To add custom date range:

```python
# Add parameters to the URL:
# &pd=3 (3 days)
# &pd=4 (1 week)
# Or specific dates with &ds=YYYY.MM.DD&de=YYYY.MM.DD
```

### Sorting Options

The default sort is by relevance. To change:

```python
# Add to URL:
# &sort=0 (relevance)
# &sort=1 (recency)
```

## License

This project is open source and available under the MIT License. 