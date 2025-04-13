import requests
import random
import re
from datetime import datetime, timedelta
import json
import time

def get_threads_posts(keyword, max_pages=1, start_page=1):
    """
    Fetch posts from Threads platform based on a keyword
    
    Args:
        keyword (str): Search keyword
        max_pages (int): Maximum number of pages to fetch
        start_page (int): Page to start from
        
    Returns:
        list: List of post dictionaries with content, author, date and link
    """
    # Note: Threads currently doesn't have a public API or search functionality
    # This is a placeholder implementation that generates simulated results
    return generate_placeholder_threads_posts(keyword, count=max_pages)

def generate_placeholder_threads_posts(keyword, count=1):
    """Generate simulated Threads posts for demo purposes"""
    results = []
    max_results = count * 10  # Approximate threads per page
    
    # Threads handle patterns
    handle_prefixes = ['real', 'the', 'official', 'mr', 'ms', 'dr', 'prof', 'its', 'im', 'just', 'my']
    handle_suffixes = ['official', 'real', 'original', 'actual', 'account', 'verified', '123', 'xyz']
    
    # Common hashtags based on the keyword
    keyword_hashtag = '#' + keyword.replace(' ', '')
    related_hashtags = [
        '#trending', '#viral', '#threads', '#instagram', 
        '#community', '#thoughts', '#discussion', '#ideas', 
        '#today', '#share', '#connect', '#explore'
    ]
    
    # Thread templates
    thread_templates = [
        "Just posted about {keyword}. What do you all think? {hashtags}",
        "Has anyone else been following the latest on {keyword}? Thoughts? {hashtags}",
        "{keyword} is changing everything. Here's my take: {hashtags}",
        "My perspective on {keyword}: It's more complex than people think. {hashtags}",
        "Curious what others think about {keyword}? Let's discuss. {hashtags}",
        "New thread on {keyword}. Join the conversation! {hashtags}",
        "I've been exploring {keyword} for {months} months now. Here's what I've found: {hashtags}",
        "Hot take: {keyword} isn't what everyone thinks it is. {hashtags}",
        "Question for my followers: How are you engaging with {keyword}? {hashtags}",
        "The conversation around {keyword} is missing some key points: {hashtags}"
    ]
    
    # Generate threads
    for i in range(random.randint(max_results - 2, max_results + 3)):
        # Create handle
        if random.random() < 0.7:  # 70% chance of having prefix + name
            handle = f"{random.choice(handle_prefixes)}{keyword.replace(' ', '')}"
        else:
            name_part = keyword.split(' ')[0] if ' ' in keyword else keyword
            handle = f"{name_part.lower()}{random.choice(handle_suffixes)}"
        
        # Make handle Threads-like
        handle = re.sub(r'[^\w]', '', handle)[:15]  # Handles limited to 15 chars
        
        # Create display name
        display_name = ' '.join(word.capitalize() for word in handle.split('_'))
        
        # Generate post time (last 7 days)
        hours_ago = random.randint(1, 168)  # Up to 7 days ago
        mins_ago = random.randint(0, 59)
        post_time = datetime.now() - timedelta(hours=hours_ago, minutes=mins_ago)
        date_str = post_time.strftime('%Y-%m-%d')
        time_str = post_time.strftime('%H:%M')
        
        # Format relative time for display
        if hours_ago < 24:
            relative_time = f"{hours_ago}h"
        else:
            relative_time = f"{hours_ago // 24}d"
        
        # Select random thread template and format it
        template = random.choice(thread_templates)
        months = random.randint(1, 12)
        
        # Select 1-3 random hashtags plus the keyword hashtag
        selected_hashtags = random.sample(related_hashtags, random.randint(1, 3))
        if random.random() < 0.8:  # 80% chance to include keyword hashtag
            selected_hashtags.append(keyword_hashtag)
        hashtag_str = ' '.join(selected_hashtags)
        
        # Format the thread content
        content = template.format(
            keyword=keyword, 
            hashtags=hashtag_str,
            months=months
        )
        
        # Add engagement metrics
        likes = random.randint(5, 10000)
        replies = int(likes * random.uniform(0.01, 0.1))
        reposts = int(likes * random.uniform(0.01, 0.05))
        
        # Format engagement for display in content
        engagement = f"❤️ {likes} • 💬 {replies} • 🔄 {reposts}"
        
        # Generate unique thread ID
        thread_id = ''.join(random.choice('0123456789abcdef') for _ in range(16))
        
        results.append({
            '제목': f"@{handle}: {content[:50]}..." if len(content) > 50 else f"@{handle}: {content}",
            '내용': f"{content}\n\n{engagement} • {relative_time}",
            '언론사': f"Threads - @{handle}",
            '날짜': f"{date_str} {time_str}",
            '링크': f"https://threads.net/@{handle}/post/{thread_id}"
        })
    
    # Add a short delay to simulate network latency
    time.sleep(0.5)
    
    return results 