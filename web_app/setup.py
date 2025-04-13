from setuptools import setup, find_packages

setup(
    name="naver-news-downloader",
    version="0.1.0",
    description="Download news articles from Naver Search",
    author="User",
    py_modules=["naver_news_downloader"],
    install_requires=[
        "requests",
        "beautifulsoup4",
        "openpyxl",
    ],
    entry_points={
        "console_scripts": [
            "naver-news=naver_news_downloader:main",
        ],
    },
) 