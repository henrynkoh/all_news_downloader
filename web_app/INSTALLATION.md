# Naver News Downloader - Installation Guide

This guide explains how to install and use the Naver News Downloader on different platforms.

## Desktop Application

### Windows

1. Download the `NaverNewsDownloader.exe` file
2. Double-click to run the application
3. You may see a security warning - click "More info" and then "Run anyway"

### macOS

1. Download the `NaverNewsDownloader.app` file or the `NaverNewsDownloader` binary
2. If using the .app:
   - Move it to your Applications folder
   - Right-click and select "Open" (needed first time on macOS)
3. If using the binary:
   - Open Terminal
   - Navigate to the directory containing the file
   - Run `chmod +x NaverNewsDownloader` to make it executable
   - Run `./NaverNewsDownloader` to start the application

### Linux

1. Download the `NaverNewsDownloader` binary
2. Open Terminal
3. Navigate to the directory containing the file
4. Run `chmod +x NaverNewsDownloader` to make it executable
5. Run `./NaverNewsDownloader` to start the application

## Web Application (For all platforms)

The web application provides a browser-based interface that works on any device, including iPhones and other mobile devices.

### Prerequisites

- Python 3.7 or newer
- pip (Python package installer)

### Installation

1. Download the `web_app` folder
2. Open Terminal/Command Prompt
3. Navigate to the `web_app` directory
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the application:
   ```
   streamlit run app.py
   ```
6. Your browser will automatically open to `http://localhost:8501`

### Mobile Access

To access the web app from your iPhone or other mobile devices:

1. Run the web app on your computer as described above
2. Find your computer's IP address (run `ipconfig` on Windows or `ifconfig` on Mac/Linux)
3. On your mobile device, open a browser and navigate to: `http://YOUR_COMPUTER_IP:8501`
4. You can now use the app on your mobile device while the server runs on your computer

## Cloud Deployment (For Mobile/iPhone Use)

For a more permanent solution that allows you to access the app from anywhere:

1. Deploy the web app to a cloud service like Streamlit Cloud, Heroku, or AWS
2. Instructions for Streamlit Cloud:
   - Create an account at [https://streamlit.io/cloud](https://streamlit.io/cloud)
   - Connect your GitHub account
   - Upload the web_app files to a GitHub repository
   - Deploy the app on Streamlit Cloud by selecting your repository
3. Once deployed, you'll get a public URL that you can access from any device including your iPhone

## Usage

1. Enter your search keyword in the search box
2. Specify the number of pages to crawl (more pages = more results)
3. Click the "Search" or "Start Download" button
4. Wait for the search to complete
5. Save or download the Excel file with the results
6. The Excel file will contain news article titles, content summaries, publishers, dates, and links

## Troubleshooting

If you encounter any issues:

1. Make sure you have an active internet connection
2. Check that you have the necessary permissions to write files to the download directory
3. If using the web app, ensure all dependencies are correctly installed
4. For desktop app security warnings, you may need to adjust your security settings 