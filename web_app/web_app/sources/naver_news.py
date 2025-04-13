"""
Naver News source module for News & Content Downloader.

This module provides functionality to search and extract news articles from Naver.
"""

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

def get_naver_news(keyword, max_pages=5, start_page=1):
    """
    Fetch news articles from Naver based on a keyword search.
    
    Args:
        keyword (str): The search term to look for
        max_pages (int, optional): Maximum number of pages to fetch. Defaults to 5.
        start_page (int, optional): Page to start from. Defaults to 1.
        
    Returns:
        list: List of dictionaries containing article data
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    articles = []
    
    end_page = start_page + max_pages if max_pages > 0 else start_page + 1
    
    for page in range(start_page, end_page):
        url = f'https://search.naver.com/search.naver?where=news&query={keyword}&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&refresh_start=0&related=0&start={((page-1)*10)+1}'
        
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            news_items = soup.select('div.news_wrap.api_ani_send')
            
            if not news_items:
                print(f"No articles found on page {page}")
                break
                
            print(f"Total articles found: {len(news_items)}")
            
            for item in news_items:
                title_elem = item.select_one('a.news_tit')
                content_elem = item.select_one('div.news_dsc')
                info_elem = item.select_one('div.info_group')
                
                if title_elem and content_elem:
                    title = title_elem.get_text(strip=True)
                    content = content_elem.get_text(strip=True)
                    link = title_elem.get('href')
                    
                    # Extract publisher and date if available
                    publisher = ""
                    date = ""
                    
                    if info_elem:
                        publisher_elem = info_elem.select_one('a.info.press')
                        if publisher_elem:
                            publisher = publisher_elem.get_text(strip=True)
                            
                        date_elem = info_elem.select_one('span.info')
                        if date_elem:
                            date = date_elem.get_text(strip=True)
                    
                    article = {
                        '제목': title,
                        '내용': content,
                        '언론사': publisher,
                        '날짜': date,
                        '링크': link
                    }
                    
                    articles.append(article)
            
            # Sleep to avoid being blocked
            time.sleep(1)
            
        except Exception as e:
            print(f"Error occurred while crawling page {page}: {str(e)}")
            continue
    
    return articles

if __name__ == "__main__":
    # Test the module
    keyword = "AI"
    print(f"Searching for '{keyword}' news...")
    
    articles = get_naver_news(keyword, max_pages=1)
    
    for i, article in enumerate(articles[:3]):
        print(f"\nArticle {i+1}:")
        print(f"Title: {article['제목']}")
        print(f"Content: {article['내용'][:100]}...")
        print(f"Publisher: {article['언론사']}")
        print(f"Date: {article['날짜']}")
        print(f"Link: {article['링크']}")
    
    print(f"\nTotal articles found: {len(articles)}") 