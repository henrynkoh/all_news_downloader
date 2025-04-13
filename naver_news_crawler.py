import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from datetime import datetime
import time

def get_naver_news(keyword, max_pages=5):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    articles = []
    
    for page in range(1, max_pages + 1):
        url = f'https://search.naver.com/search.naver?where=news&query={keyword}&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&refresh_start=0&related=0&start={((page-1)*10)+1}'
        
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            news_items = soup.select('div.news_wrap.api_ani_send')
            
            for item in news_items:
                title = item.select_one('a.news_tit')
                content = item.select_one('div.news_dsc')
                link = title.get('href') if title else None
                
                if title and content and link:
                    articles.append({
                        '제목': title.get_text(strip=True),
                        '내용': content.get_text(strip=True),
                        '링크': link
                    })
            
            time.sleep(1)  # 서버 부하 방지를 위한 딜레이
            
        except Exception as e:
            print(f"Error occurred while crawling page {page}: {str(e)}")
            continue
    
    return articles

def save_to_excel(articles, filename):
    wb = Workbook()
    ws = wb.active
    
    # 헤더 추가
    ws.append(['제목', '내용', '링크'])
    
    # 데이터 추가
    for article in articles:
        ws.append([
            article['제목'],
            article['내용'],
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
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column[0].column_letter].width = adjusted_width
    
    wb.save(filename)
    print(f"데이터가 {filename}에 저장되었습니다.")

def main():
    keyword = "코미팜"
    max_pages = 5
    filename = f"코미팜_뉴스_{datetime.now().strftime('%Y%m%d')}.xlsx"
    
    print(f"'{keyword}' 관련 뉴스를 크롤링합니다...")
    articles = get_naver_news(keyword, max_pages)
    
    if articles:
        save_to_excel(articles, filename)
        print(f"총 {len(articles)}개의 기사가 수집되었습니다.")
    else:
        print("수집된 기사가 없습니다.")

if __name__ == "__main__":
    main() 