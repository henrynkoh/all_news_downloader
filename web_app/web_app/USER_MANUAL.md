# News & Content Downloader - User Manual

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Main Features](#main-features)
   - [Search](#search)
   - [Visualization](#visualization)
   - [Social Media Ads](#social-media-ads)
   - [Settings](#settings)
5. [Mobile Use](#mobile-use)
6. [Advanced Features](#advanced-features)
7. [Troubleshooting](#troubleshooting)
8. [FAQs](#faqs)

## Introduction

News & Content Downloader is a powerful application that lets you search, collect, analyze, and visualize content from multiple sources including news sites, search engines, social media platforms, and blogs. This versatile tool helps you gather information efficiently and create social media advertisements across various platforms.

The application is available for multiple platforms including Windows, macOS, and iOS devices, with a responsive design that adapts to different screen sizes.

## Installation

### Desktop Installation (Windows & macOS)

#### Windows
1. Download the `News_Content_Downloader_Windows.zip` file
2. Extract the ZIP file to a location on your computer
3. Double-click the `Run_News_Downloader.bat` file
4. The application will open in your default web browser

#### macOS
1. Download the `News_Content_Downloader_macOS.zip` file
2. Extract the ZIP file
3. Right-click on `News_Content_Downloader.app` and select "Open"
4. The application will open in your default web browser

### iOS Installation (iPhone & iPad)
1. Install [Pythonista](https://apps.apple.com/us/app/pythonista-3/id1085978097) from the App Store
2. Download the `News_Content_Downloader_iOS.zip` file
3. Extract the ZIP file and import the files into Pythonista
4. Follow the detailed instructions in the included iOS_README.md file

For more detailed installation instructions, refer to [INSTALL_GUIDE.md](INSTALL_GUIDE.md).

## Getting Started

When you first launch the application, you'll see the main search interface with the following components:

- **Navigation Bar** at the top with tabs for Search, Visualize, Create Ads, and Settings
- **Sidebar** on the left with search options and filters
- **Main Content Area** in the center showing instructions or search results

### Quick Search Guide
1. Enter a keyword in the search box on the left sidebar
2. Select which sources to include in your search
3. Adjust any search parameters as needed
4. Click the "Search" button
5. View your results in the table display
6. Download results as Excel or CSV file

## Main Features

### Search

The search feature is the core functionality of the application:

#### Search Options
- **Keyword**: Enter the term you want to search for
- **Sources**: Select which content sources to include:
  - Naver News
  - Google Search
  - YouTube
  - Medium
  - Twitter/X
  - Naver Blog
  - Tistory
  - Threads
  - Google Blogger
  - And more...
- **Number of Pages**: How many pages of results to fetch from each source
- **Results Limit**: Maximum number of results to display

#### Search Results
- Results appear in a table with clickable links
- Column headers can be clicked to sort results
- Links open in new tabs when clicked
- Source distribution is shown on the right side

#### Downloading Results
1. After a search completes, an Excel file is automatically saved to the downloads folder
2. Use the "Download Excel File" button to save the file to your preferred location
3. If Excel format fails, a CSV format will be used as fallback

### Visualization

The visualization feature helps you analyze your search results:

1. After completing a search, click "Visualize These Results" or select the Visualize tab
2. The visualization page includes:
   - **Source Distribution**: Pie chart showing the proportion of results from each source
   - **Word Cloud**: Visual representation of the most common words in your results
   - **Content Analysis**: Frequency analysis of topics and terms
   - **Time Analysis**: Timeline of content publication dates (when available)

### Social Media Ads

The social media ad creation feature allows you to create and manage advertisements across multiple platforms:

1. Click the "Create Ads" tab in the navigation bar
2. Select the platforms you want to create ads for:
   - Facebook
   - Instagram
   - X/Twitter
   - Threads
   - Tistory
   - Naver Blog
   - Google Blogger
3. Enter your ad content:
   - Ad title
   - Ad description
   - Target URL
   - Upload an image
4. Configure targeting options:
   - Age range
   - Gender
   - Location
5. Set budget and schedule:
   - Budget amount
   - Start date
   - Campaign duration
6. Configure platform-specific settings in each platform's tab
7. Click "Create Ad" to publish your advertisements

### Settings

The Settings page allows you to customize the application:

#### Display Settings
- Table height
- Maximum results to display
- Light/dark theme toggle
- Font size

#### Search Settings
- Default pages to search
- Maximum searchable pages
- Request delay (to prevent rate limiting)

#### Advanced Settings
- Request timeout
- Cache expiry time
- Experimental features

## Mobile Use

The application has been optimized for mobile devices with:

- **Responsive Design**: Adapts to screen size automatically
- **Touch-Friendly Controls**: Larger buttons and input fields
- **Simplified Navigation**: Dropdown menu instead of tabs on small screens
- **Optimized Tables**: Horizontal scrolling for tables that exceed screen width
- **Reduced Data Usage**: Smaller result sets on mobile by default

## Advanced Features

### Keyboard Shortcuts
- **Ctrl+Enter** (or **Cmd+Enter** on Mac): Execute search
- **Ctrl+D** (or **Cmd+D** on Mac): Download results
- **Ctrl+V** (or **Cmd+V** on Mac): Switch to visualization
- **Ctrl+S** (or **Cmd+S** on Mac): Open settings

### Command Line Options
When running from source code, you can use these command line options:

```bash
streamlit run app.py -- --theme dark --max_pages 10 --cache_ttl 3600
```

Available options:
- `--theme`: Set the theme (dark/light)
- `--max_pages`: Set maximum searchable pages
- `--cache_ttl`: Set cache expiry time in seconds
- `--debug`: Enable debug logging

### Custom Source Integration
Advanced users can create custom source modules to integrate additional content sources:

1. Create a new Python file in the `sources` directory
2. Implement the required functions following the template in the documentation
3. Add the source to the sources configuration

## Troubleshooting

### Common Issues and Solutions

#### No Search Results
- Verify your internet connection
- Try a different keyword
- Select additional sources
- Check if sources are accessible from your location

#### Download Errors
- Ensure the downloads directory exists
- Check if you have write permissions
- Verify enough disk space is available
- Try downloading as CSV instead

#### Application Won't Start
- Verify Python is installed (if running from source)
- Check if all dependencies are installed
- Try running as administrator
- Clear browser cache

#### Mobile-Specific Issues
- Enable JavaScript in your mobile browser
- Ensure sufficient device storage space
- Try closing other apps to free up memory
- Use Safari on iOS for best compatibility

## FAQs

**Q: Is an internet connection required?**
A: Yes, the application needs internet access to search for content across various platforms.

**Q: How many results can I download at once?**
A: The default limit is 50 results, but you can increase this up to 100 in the settings.

**Q: Can I use the application offline?**
A: The desktop version can run offline, but you won't be able to fetch new content without an internet connection.

**Q: How do I add a new content source?**
A: Advanced users can create custom source modules. See the "Advanced Features" section for details.

**Q: Are my searches private?**
A: Your searches are not stored on any external servers, but the sources you search (e.g., Google) may log your search queries according to their own policies.

**Q: Can I schedule automatic searches?**
A: This feature is not currently available in the base application, but you can use the command line version with external scheduling tools.

**Q: How can I get help if I encounter issues?**
A: Check the troubleshooting section of this manual first. If your issue persists, refer to the support information in the README file. 