# Installation Guide for News & Content Downloader

This guide provides detailed instructions for installing and running the News & Content Downloader application on various platforms, including PC/Mac desktops and iPhone.

## Desktop Installation (Windows & macOS)

### Method 1: Using the Standalone Application (Recommended)

This is the easiest method as it doesn't require Python or any dependencies to be installed.

#### Windows
1. Download the `News_Content_Downloader_Windows.zip` file
2. Extract the ZIP file to a location on your computer
3. Double-click the `Run_News_Downloader.bat` file
4. The application will start and open in your default web browser

#### macOS
1. Download the `News_Content_Downloader_macOS.zip` file
2. Extract the ZIP file to a location on your computer
3. Right-click on `News_Content_Downloader.app` and select "Open"
   - You may need to bypass macOS security by going to System Preferences > Security & Privacy and clicking "Open Anyway"
4. The application will start and open in your default web browser

### Method 2: Running from Source Code

If you prefer to run the application from source code, or if you want to modify it, follow these steps:

#### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

#### Steps
1. Download the `News_Content_Downloader_Source.zip` file
2. Extract the ZIP file to a location on your computer
3. Open a terminal or command prompt
4. Navigate to the extracted folder:
   ```
   cd path/to/extracted/folder
   ```
5. Create a virtual environment (optional but recommended):
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```
6. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
7. Run the application:
   ```
   cd web_app
   streamlit run app.py
   ```
8. The application will start and open in your default web browser

## iPhone/iPad Installation

Due to iOS limitations, installing Python applications directly on iOS devices requires some workarounds. Here are the available methods:

### Method 1: Using Pythonista (Recommended)

[Pythonista](https://apps.apple.com/us/app/pythonista-3/id1085978097) is a full Python IDE for iOS that allows you to run Python scripts directly on your device.

1. Purchase and install Pythonista 3 from the App Store
2. Download the `News_Content_Downloader_iOS.zip` file to your iPhone
3. Extract the ZIP file
4. Open Pythonista
5. Import the files:
   - Tap the "+" button in the top left
   - Select "Import File..."
   - Navigate to the extracted files and select all of them
   - Alternately, you can use the "Open in..." option from your file manager to open the files in Pythonista
6. Install required packages using StaSh (Pythonista package manager):
   - Run the following command in Pythonista's console to install StaSh:
     ```python
     import requests as r; exec(r.get('https://bit.ly/get-stash').text)
     ```
   - Once StaSh is installed, run the following commands to install the required packages:
     ```
     pip install streamlit
     pip install pandas
     pip install openpyxl
     pip install beautifulsoup4
     pip install requests
     ```
7. Run the application by opening `app.py` and tapping the "Run" button

### Method 2: Using Pyto

[Pyto](https://apps.apple.com/us/app/pyto-python-3/id1436650069) is another Python IDE for iOS.

1. Purchase and install Pyto from the App Store
2. Download the `News_Content_Downloader_iOS.zip` file to your iPhone
3. Extract the ZIP file
4. Open Pyto
5. Import the files using the "+" button and selecting "Import from Files..."
6. Install required packages by running the following commands in Pyto's console:
   ```
   pip install streamlit
   pip install pandas
   pip install openpyxl
   pip install beautifulsoup4
   pip install requests
   ```
7. Run the application by opening `app.py` and tapping the "Run" button

### Method 3: Using a Web-Based Solution (Streamlit Cloud)

For the simplest experience with minimal setup, you can access the web-hosted version of the application:

1. Open your web browser on your iPhone
2. Navigate to: [https://news-content-downloader.streamlit.app](https://news-content-downloader.streamlit.app) (example link - actual link may differ)
3. The application will run in your browser with no installation required

This method does not require any installation but does require an internet connection to use the application.

## Troubleshooting

### Common Issues on Desktop

1. **Application won't start**
   - Ensure you have administrative privileges
   - Try running from a different location (e.g., Desktop)
   - Check that your antivirus isn't blocking the application

2. **"Python not found" error when running from source**
   - Make sure Python is installed and added to your PATH
   - Try using the full path to the Python executable

3. **Missing dependencies**
   - Run `pip install -r requirements.txt` again
   - Check for error messages during installation

### Common Issues on iOS

1. **Unable to install packages in Pythonista/Pyto**
   - Some packages may not be compatible with iOS
   - Try using the simplified version of the app with fewer dependencies

2. **App crashes on startup**
   - Check if you have enough free space on your device
   - Close other applications to free up memory

3. **Unable to save files**
   - Make sure the app has permission to access Files
   - Try saving to a different location within the app's sandbox

## Getting Updates

To get the latest updates for the application:

1. Visit the GitHub repository: [https://github.com/yourusername/news-content-downloader](https://github.com/yourusername/news-content-downloader)
2. Download the latest release
3. Follow the installation instructions for your platform

## Support and Contact

If you encounter any issues or have questions about the application, please create an issue on the GitHub repository or contact the developer at [your.email@example.com](mailto:your.email@example.com). 