# News & Content Downloader

A powerful web application for searching, collecting, and analyzing news and content from multiple sources including Naver News, Google Search, YouTube, blogs, and social media platforms.

![Application Screenshot](https://raw.githubusercontent.com/streamlit/streamlit/master/examples/data/logo.png)

## Features

- **Multi-source search**: Search across multiple content platforms simultaneously
- **Real-time progress tracking**: Watch as your searches progress across different sources
- **Data visualization**: Analyze your search results with built-in visualization tools
- **Excel/CSV export**: Download your results in common formats for further analysis
- **Clickable links**: All links in search results open in new tabs for easy browsing
- **Customizable settings**: Adjust display preferences, search parameters, and more
- **Social media ad creation**: Create and manage advertisements across multiple social platforms
- **Multiple platforms**: Available as a web app, desktop application, and mobile app
- **Responsive design**: Optimized for both desktop and mobile devices

## Available Platforms

The News & Content Downloader is available on multiple platforms:

### Web Application
- Run in any modern web browser
- No installation required
- Hosted version available at [news-content-downloader.streamlit.app](https://news-content-downloader.streamlit.app)

### Desktop Application
- **Windows**: Standalone executable (no Python installation required)
- **macOS**: Native macOS application
- Offline functionality
- Better performance than web version

### Mobile Applications
- **iOS**: Compatible with Pythonista and Pyto on iPhone and iPad
- **Android**: Compatible with Pydroid and Termux
- Mobile-optimized interface
- Touch-friendly controls

## Available Sources

The application currently supports the following content sources:

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

## Installation

### Quick Install

#### Desktop (Windows & macOS)
1. Download the appropriate package for your operating system:
   - [Windows Installer](https://github.com/yourusername/news-content-downloader/releases/latest/download/News_Content_Downloader_Windows.zip)
   - [macOS App](https://github.com/yourusername/news-content-downloader/releases/latest/download/News_Content_Downloader_macOS.zip)
2. Extract the ZIP file
3. Run the application (`.exe` on Windows, `.app` on macOS)

#### iOS (iPhone & iPad)
1. Install [Pythonista](https://apps.apple.com/us/app/pythonista-3/id1085978097) from the App Store
2. Download the [iOS Package](https://github.com/yourusername/news-content-downloader/releases/latest/download/News_Content_Downloader_iOS.zip)
3. Follow the instructions in `iOS_README.md` included in the package

For detailed installation instructions, see [INSTALL_GUIDE.md](INSTALL_GUIDE.md).

### Manual Installation (Source Code)

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone the repository

```bash
git clone https://github.com/yourusername/news-content-downloader.git
cd news-content-downloader
```

### Step 2: Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate the virtual environment:

- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the application

```bash
cd web_app
streamlit run app.py
```

The application will start and should automatically open in your default web browser. If not, you can access it at http://localhost:8501.

## User Guide

### Basic Search

1. **Enter a search keyword** in the search box on the left sidebar
2. **Select which sources** to include in your search (default: Naver News and Google Search)
3. **Adjust search parameters** if needed (pages to search, results limit)
4. **Click the Search button** to start the search process
5. **View results** in the table display with clickable links
6. **Download results** as Excel or CSV file for further analysis

### Social Media Ad Creation

1. **Navigate to the Create Ads tab** in the top navigation bar
2. **Select which platforms** you want to create ads on
3. **Enter your ad title and description**
4. **Upload an image** for your ad
5. **Configure target audience** including age range, gender, and location
6. **Set your budget and campaign duration**
7. **Customize platform-specific settings** in each platform's tab
8. **Click Create Ad** to publish your advertisements

### Advanced Features

#### Visualization

After completing a search, you can visualize your results by clicking the "Visualize These Results" button or by selecting the Visualize tab from the top navigation bar.

The visualization page provides:
- Source distribution analysis
- Word cloud of content
- Basic statistics about your search results

#### Settings

Customize the application behavior through the Settings tab:

**Display Settings:**
- Adjust table height
- Set maximum results to display
- Toggle source distribution display
- Choose between dark and light theme

**Search Settings:**
- Set default pages to search
- Configure maximum searchable pages
- Adjust request delay to prevent rate limiting

**Advanced Settings:**
- Configure request timeout
- Enable/disable result caching
- Set cache expiry time
- Access experimental features like parallel requests

## Troubleshooting

### Common Issues

1. **Search returns no results**
   - Try a different keyword
   - Select additional sources
   - Check your internet connection

2. **Download button not working**
   - Check if downloads folder exists (created automatically in most cases)
   - Verify you have write permissions to the application directory
   - Look for error messages in the terminal window

3. **Slow performance**
   - Reduce the number of sources selected
   - Reduce the number of pages to search
   - Increase request delay in settings

### Error Messages

- **"Error in cached search for [source]"**: The application failed to search this particular source. Try again or exclude this source.
- **"Excel save error"**: Problem saving the Excel file. The application will automatically try to save as CSV instead.
- **"No results found"**: Your search query didn't return any results from the selected sources.

## Development

### Project Structure

```
news-content-downloader/
├── web_app/                  # Main application files
│   ├── app.py                # Core application file
│   ├── settings.py           # Settings management
│   ├── style.css             # Custom CSS styling
│   ├── mobile_config.py      # Mobile device configuration
│   ├── package_app.py        # Packaging script for various platforms
│   ├── app_icon.svg          # Application icon
│   ├── sources/              # Source modules
│   │   ├── __init__.py       # Source configuration
│   │   ├── naver_news.py     # Naver News source
│   │   ├── google_search.py  # Google Search source
│   │   ├── ad_creator.py     # Social media ad creation module
│   │   └── ...               # Other source modules
│   └── downloads/            # Downloaded files (created at runtime)
├── dist/                     # Packaged applications (created by package_app.py)
│   ├── desktop/              # Desktop application packages
│   └── mobile/               # Mobile application packages
└── requirements.txt          # Python dependencies
```

### Building for Multiple Platforms

To package the application for different platforms, use the `package_app.py` script:

```bash
# Package for all platforms
python package_app.py

# Package for specific platform
python package_app.py --platform desktop
python package_app.py --platform ios
python package_app.py --platform cloud
```

Each platform package will be created in the `dist` directory.

### Mobile Development

The application uses responsive design to adapt to different screen sizes. Mobile-specific code is contained in `mobile_config.py`. Key features include:

- Automatic platform detection (iOS, Android, desktop)
- Touch-friendly UI elements
- Simplified navigation on small screens
- Optimized file handling for mobile OS limitations

### Custom UI Development

To modify the application appearance:

1. Edit `style.css` for basic styling
2. Update `mobile_config.py` for mobile-specific UI changes 
3. Update theme settings in `.streamlit/config.toml`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/) - The web framework used
- [Pandas](https://pandas.pydata.org/) - For data manipulation
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - For web scraping
- [OpenPyXL](https://openpyxl.readthedocs.io/) - For Excel file generation
- [WordCloud](https://github.com/amueller/word_cloud) - For word cloud visualization

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Contact

For support or feature requests, please open an issue on GitHub.
