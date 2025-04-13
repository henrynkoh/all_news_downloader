import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from datetime import datetime
import time
import argparse
import os
import sys
import re

def get_naver_news(keyword, max_pages=5, start_page=1):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    articles = []
    
    print(f"Searching for '{keyword}' news...")
    for page in range(start_page, start_page + max_pages):
        url = f'https://search.naver.com/search.naver?where=news&query={keyword}&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&refresh_start=0&related=0&start={((page-1)*10)+1}'
        
        try:
            sys.stdout.write(f"\rFetching page {page}/{start_page + max_pages - 1}...")
            sys.stdout.flush()
            
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            news_items = soup.select('div.news_wrap.api_ani_send')
            
            for item in news_items:
                title = item.select_one('a.news_tit')
                content = item.select_one('div.news_dsc')
                link = title.get('href') if title else None
                
                # Extract publisher
                publisher_elem = item.select_one('a.info.press')
                publisher = publisher_elem.get_text(strip=True) if publisher_elem else "Unknown"
                
                # Extract date
                date_elem = item.select_one('span.info')
                date_text = date_elem.get_text(strip=True) if date_elem else ""
                
                # Naver usually provides date in format like "5시간 전", "3일 전", "2024.04.12." etc.
                # Try to extract structured date or use the original text
                date = date_text
                
                if title and content and link:
                    articles.append({
                        '제목': title.get_text(strip=True),
                        '내용': content.get_text(strip=True),
                        '언론사': publisher,
                        '날짜': date,
                        '링크': link
                    })
            
            time.sleep(1)  # 서버 부하 방지를 위한 딜레이
            
        except Exception as e:
            print(f"\nError occurred while crawling page {page}: {str(e)}")
            continue
    
    print(f"\nTotal articles found: {len(articles)}")
    return articles

def save_to_excel(articles, filename):
    wb = Workbook()
    ws = wb.active
    
    # 헤더 추가
    ws.append(['제목', '내용', '언론사', '날짜', '링크'])
    
    # 데이터 추가
    for article in articles:
        ws.append([
            article['제목'],
            article['내용'],
            article['언론사'],
            article['날짜'],
            article['링크']
        ])
    
    # 열 너비 자동 조정
    for column in ws.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 100)  # Limit width to prevent extremely wide columns
        ws.column_dimensions[column[0].column_letter].width = adjusted_width
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
    
    wb.save(filename)
    print(f"Data saved to {filename}")
    print(f"File location: {os.path.abspath(filename)}")

def main():
    parser = argparse.ArgumentParser(description='Download news articles from Naver Search')
    parser.add_argument('keyword', help='Keyword to search for')
    parser.add_argument('-p', '--pages', type=int, default=5, help='Maximum number of pages to crawl (default: 5)')
    parser.add_argument('-o', '--output', help='Output filename (default: [keyword]_news_[date].xlsx)')
    parser.add_argument('-d', '--dir', default='downloads', help='Directory to save the file (default: downloads)')
    parser.add_argument('-s', '--start', type=int, default=1, help='Start page number (default: 1)')
    
    args = parser.parse_args()
    
    keyword = args.keyword
    max_pages = args.pages
    start_page = args.start
    
    # Create default filename if not provided
    if args.output:
        filename = args.output
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'
    else:
        today = datetime.now().strftime('%Y%m%d')
        filename = f"{args.dir}/{keyword}_news_{today}.xlsx"
    
    # Start crawling
    articles = get_naver_news(keyword, max_pages, start_page)
    
    if articles:
        save_to_excel(articles, filename)
        print(f"Successfully downloaded {len(articles)} articles about '{keyword}'")
    else:
        print("No articles found.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}") 