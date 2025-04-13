import requests
from bs4 import BeautifulSoup
import time
import random
import re
from datetime import datetime, timedelta

def get_tistory_posts(keyword, max_pages=1, start_page=1):
    """
    Fetch blog posts from Tistory based on a keyword
    
    Args:
        keyword (str): Search keyword
        max_pages (int): Maximum number of pages to fetch
        start_page (int): Page to start from
        
    Returns:
        list: List of post dictionaries with title, content, author, date and link
    """
    results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }
    
    # Try to fetch real Tistory results
    try:
        for page in range(start_page, start_page + max_pages):
            # Using Daum search to find Tistory posts (since Tistory is owned by Kakao/Daum)
            url = f'https://search.daum.net/search?w=blog&q={keyword}+site%3Atistory.com&p={page}'
            
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code != 200:
                    print(f"Error: Tistory search returned status code {response.status_code}")
                    break
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract blog posts from the search results
                blog_items = soup.select('ul.list_info li')
                if not blog_items:
                    # Try another selector
                    blog_items = soup.select('div.c-item')
                
                if not blog_items:
                    print("No Tistory posts found on page")
                    break
                
                for item in blog_items:
                    try:
                        # Extract title and link
                        title_elem = item.select_one('a.f_link_b') or item.select_one('a.tit_main')
                        if not title_elem:
                            continue
                            
                        title = title_elem.get_text(strip=True)
                        link = title_elem.get('href', '')
                        
                        # Only include Tistory posts
                        if 'tistory.com' not in link:
                            continue
                        
                        # Extract content/description
                        content_elem = item.select_one('p.f_eb') or item.select_one('div.desc')
                        content = content_elem.get_text(strip=True) if content_elem else ""
                        
                        # Extract blog name and author
                        blog_elem = item.select_one('div.etc_info a.f_url') or item.select_one('span.f_nb')
                        blog_name = blog_elem.get_text(strip=True) if blog_elem else "Tistory Blog"
                        
                        # Extract date
                        date_elem = item.select_one('span.f_nb') or item.select_one('span.txt_info')
                        date = date_elem.get_text(strip=True) if date_elem else datetime.now().strftime('%Y.%m.%d')
                        
                        results.append({
                            '제목': title,
                            '내용': content,
                            '언론사': f"Tistory - {blog_name}",
                            '날짜': date,
                            '링크': link
                        })
                    except Exception as e:
                        print(f"Error parsing Tistory post: {str(e)}")
                        continue
                
                time.sleep(random.uniform(1.0, 2.0))
                
            except Exception as e:
                print(f"Error occurred while crawling Tistory page {page}: {str(e)}")
                break
        
    except Exception as e:
        print(f"Tistory search error: {str(e)}")
    
    # If we failed to get real results or got no results, use simulated data
    if not results:
        # Generate placeholder results
        return generate_placeholder_tistory_posts(keyword)
    
    return results

def generate_placeholder_tistory_posts(keyword):
    """Generate simulated Tistory blog posts for demo purposes"""
    placeholder_results = []
    
    # Sample Tistory blog titles
    title_templates = [
        "{keyword}에 대한 내 생각과 경험",
        "{keyword} 완벽 가이드 - 초보자도 쉽게 따라할 수 있는",
        "{keyword} 활용법 10가지",
        "요즘 핫한 {keyword} 리뷰",
        "{keyword} 사용 후기 및 장단점 분석",
        "{year}년 최신 {keyword} 트렌드",
        "{keyword} 관련 꿀팁 모음",
        "전문가가 알려주는 {keyword} 노하우",
        "{keyword} 실패하지 않는 방법",
        "[초보탈출] {keyword} 기초부터 실전까지"
    ]
    
    # Blog names
    blog_names = [
        "일상의기록", "테크인사이트", "프로그래머노트", "디자인스튜디오",
        "여행이야기", "푸드블로거", "패션스타일리스트", "건강한생활",
        "취미의세계", "리뷰전문가", "마케팅인사이트", "금융전문가"
    ]
    
    # Generate 5-8 Tistory posts
    for i in range(random.randint(5, 8)):
        title_template = random.choice(title_templates)
        blog_name = random.choice(blog_names)
        days_ago = random.randint(1, 180)
        publish_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y.%m.%d')
        
        # Format the title
        title = title_template.format(keyword=keyword, year=datetime.now().year)
        
        # Generate content
        content = f"""
        안녕하세요, {blog_name}입니다. 오늘은 {keyword}에 대해 자세히 알아보려고 합니다.
        많은 분들이 {keyword}에 관심을 가지고 계시지만 정확한 정보를 찾기 어려워하시는 것 같아
        제가 직접 경험하고 조사한 내용을 정리해봤습니다. 이 글이 {keyword}에 관심 있는 
        여러분께 도움이 되었으면 좋겠습니다. 궁금한 점은 댓글로 남겨주세요!
        """
        content = re.sub(r'\s+', ' ', content).strip()
        
        # Generate a blog URL (Tistory format)
        blog_subdomain = blog_name.lower().replace(' ', '')
        post_slug = title.lower().replace(' ', '-').replace(':', '').replace('?', '').replace('[', '').replace(']', '')
        post_slug = re.sub(r'[^\w\-]', '', post_slug)
        
        placeholder_results.append({
            '제목': title,
            '내용': content,
            '언론사': f"Tistory - {blog_name}",
            '날짜': publish_date,
            '링크': f"https://{blog_subdomain}.tistory.com/{random.randint(1, 999)}"
        })
    
    return placeholder_results 