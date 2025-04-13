# Naver News Downloader: Step-by-Step Tutorial

This tutorial guides you through the process of using the Naver News Downloader to search for and download news articles from Naver.

## Using the Command Line Version

### Step 1: Install the Required Dependencies

Before using the tool, make sure you have the required Python packages:

```bash
pip install requests beautifulsoup4 openpyxl
```

### Step 2: Run the Command Line Tool

Open your terminal or command prompt and run:

```bash
python naver_news_downloader.py "검색어" -p 5
```

Replace "검색어" with your desired search term, and 5 with the number of pages you want to search.

You should see output similar to:
```
Searching for '검색어' news...
Fetching page 1/5...
Total articles found: 50
Data saved to downloads/검색어_news_YYYYMMDD.xlsx
File location: /path/to/downloads/검색어_news_YYYYMMDD.xlsx
Successfully downloaded 50 articles about '검색어'
```

### Step 3: Locate and Open the Excel File

Find the Excel file in the "downloads" folder. Open it with Microsoft Excel, LibreOffice Calc, or any spreadsheet program.

The file will contain 5 columns:
- 제목 (Title)
- 내용 (Content)
- 언론사 (Publisher)
- 날짜 (Date)
- 링크 (Link)

## Using the Web Application (iPhone-Compatible)

### Step 1: Start the Web App Server

1. Navigate to the web_app directory:
   ```bash
   cd web_app
   ```

2. Run the setup script (optional, handles dependencies):
   ```bash
   python setup_web_app.py
   ```

3. Or start the app directly if dependencies are installed:
   ```bash
   streamlit run app.py
   ```

### Step 2: Access the Web Interface

For computer access:
1. Open your browser to http://localhost:8501
2. You should see the Naver News Downloader interface

For iPhone/mobile access:
1. Find your computer's IP address:
   - Windows: Run `ipconfig` in Command Prompt
   - macOS: Run `ifconfig | grep inet` in Terminal
   - Linux: Run `hostname -I` in Terminal

2. On your iPhone, open Safari and go to:
   ```
   http://YOUR_COMPUTER_IP:8501
   ```

### Step 3: Search for News

1. In the search field, type your keyword
2. Set the number of pages (1-20)
3. Click the "Search" button
4. Wait for the search to complete

### Step 4: View and Download Results

1. After searching, you'll see a table with all found articles
2. Click the "Download Excel File" button to save the data to your device
3. On iPhone, the file will download to your Downloads folder

## Using the Desktop Application

### Step 1: Download and Run the Application

1. Get the appropriate file for your system from the "dist" folder:
   - Windows: NaverNewsDownloader.exe
   - macOS: NaverNewsDownloader.app
   - Linux: NaverNewsDownloader

2. Run the application:
   - Windows: Double-click the .exe file
   - macOS: Open the .app file or run the binary in Terminal
   - Linux: Run the binary in Terminal

### Step 2: Enter Search Parameters

1. In the "Search Keyword" field, enter the term you want to search for
2. Use the spinbox to set the number of pages (1-20)
3. Choose your output directory (default is "downloads")

### Step 3: Start the Search

1. Click the "Start Download" button
2. Watch the progress bar for status updates
3. The status area will show details as pages are crawled

### Step 4: Get Your Results

1. When the search completes, a message will appear
2. Open the Excel file from the specified location
3. The file will be named: keyword_news_YYYYMMDD.xlsx

## Cloud Deployment for Permanent Mobile Access

If you want to access the app from your iPhone anytime, without running a server on your computer:

### Step 1: Create a GitHub Repository

1. Sign up for GitHub if you don't have an account
2. Create a new repository
3. Upload the contents of the web_app folder

### Step 2: Deploy on Streamlit Cloud

1. Sign up at [Streamlit Cloud](https://streamlit.io/cloud)
2. Connect your GitHub account
3. Select your repository
4. Deploy the app

### Step 3: Access from Anywhere

Once deployed, you'll get a public URL you can access from any device, including your iPhone.

## Next Steps

- Try searching for different Korean keywords
- Experiment with the number of pages to get more or fewer results
- Analyze the data in Excel by sorting, filtering, or creating charts
- Set up a scheduled task to run the search automatically at regular intervals 