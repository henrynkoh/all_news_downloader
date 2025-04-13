import requests
import random
import re
from datetime import datetime, timedelta
import json

def get_twitter_posts(keyword, max_pages=1, start_page=1):
    """
    Fetch tweets from Twitter/X based on a keyword
    
    Args:
        keyword (str): Search keyword
        max_pages (int): Maximum number of pages to fetch
        start_page (int): Page to start from
        
    Returns:
        list: List of tweet dictionaries with content, author, date and link
    """
    # Note: Twitter/X API requires OAuth authentication and has rate limits
    # For demonstration purposes, we'll use a placeholder implementation
    return generate_placeholder_twitter_posts(keyword, max_pages)

def generate_placeholder_twitter_posts(keyword, count=1):
    """Generate simulated Twitter/X posts for demo purposes"""
    results = []
    max_results = count * 10  # Approximate tweets per page
    
    # Twitter handle patterns
    handle_prefixes = ['tech', 'real', 'the', 'digital', 'ai', 'dev', 'data', 'official', 'mr', 'ms', 'dr', 'prof']
    handle_suffixes = ['guru', 'expert', 'pro', 'fan', 'lover', 'enthusiast', 'geek', 'nerd', '123', 'xyz', 'official']
    
    # Common Twitter hashtags based on the keyword
    keyword_hashtag = '#' + keyword.replace(' ', '')
    related_hashtags = [
        '#tech', '#innovation', '#digital', '#future', 
        '#AI', '#ML', '#data', '#trends', '#business', 
        '#startup', '#technology', '#news'
    ]
    
    # Tweet templates
    tweet_templates = [
        "Just published a new article about {keyword}. Check it out! {link} {hashtags}",
        "Has anyone else been following the latest developments in {keyword}? Thoughts? {hashtags}",
        "{keyword} is going to change everything. Here's why: {link} {hashtags}",
        "My take on {keyword}: It's not just hype, it's the future. {hashtags}",
        "5 reasons why {keyword} matters in {year}: {link} {hashtags}",
        "Breaking: Major announcement about {keyword} coming soon! Stay tuned. {hashtags}",
        "I've been working with {keyword} for {months} months now. Here's what I've learned: {link}",
        "Hot take: {keyword} isn't what everyone thinks it is. Here's the reality: {hashtags}",
        "Question for my followers: How are you using {keyword} in your work? {hashtags}",
        "The problem with most {keyword} discussions is that they miss this key point: {link} {hashtags}"
    ]
    
    # Verification badges for some users
    verification = [True, False, False, False, False]  # 20% chance of being verified
    
    # Generate tweets
    for i in range(random.randint(max_results - 2, max_results + 3)):
        # Create Twitter handle
        if random.random() < 0.7:  # 70% chance of having prefix + name
            handle = f"{random.choice(handle_prefixes)}{keyword.replace(' ', '')}"
        else:
            name_part = keyword.split(' ')[0] if ' ' in keyword else keyword
            handle = f"{name_part.lower()}{random.choice(handle_suffixes)}"
        
        # Make handle Twitter-like
        handle = re.sub(r'[^\w]', '', handle)[:15]  # Twitter handles limited to 15 chars
        
        # Create display name
        display_name = ' '.join(word.capitalize() for word in handle.split('_'))
        
        # Add verification for some users
        is_verified = random.choice(verification)
        if is_verified:
            display_name += " ✓"
        
        # Generate tweet time (last 48 hours)
        hours_ago = random.randint(1, 48)
        mins_ago = random.randint(0, 59)
        tweet_time = datetime.now() - timedelta(hours=hours_ago, minutes=mins_ago)
        date_str = tweet_time.strftime('%Y-%m-%d')
        time_str = tweet_time.strftime('%H:%M')
        
        # Format relative time for display
        if hours_ago < 24:
            relative_time = f"{hours_ago}h"
        else:
            relative_time = f"{hours_ago // 24}d"
        
        # Select random tweet template and format it
        template = random.choice(tweet_templates)
        months = random.randint(1, 18)
        year = datetime.now().year
        
        # Generate a short URL
        short_domain = random.choice(['bit.ly', 't.co', 'tiny.url', 'ow.ly'])
        short_code = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=7))
        link = f"https://{short_domain}/{short_code}"
        
        # Select 1-3 random hashtags plus the keyword hashtag
        selected_hashtags = random.sample(related_hashtags, random.randint(1, 3))
        if random.random() < 0.8:  # 80% chance to include keyword hashtag
            selected_hashtags.append(keyword_hashtag)
        hashtag_str = ' '.join(selected_hashtags)
        
        # Format the tweet content
        content = template.format(
            keyword=keyword, 
            link=link, 
            hashtags=hashtag_str,
            year=year,
            months=months
        )
        
        # Add engagement metrics
        likes = random.randint(0, 1000)
        retweets = int(likes * random.uniform(0.05, 0.3))
        comments = int(likes * random.uniform(0.02, 0.15))
        
        # Format engagement for display in content
        engagement = f"🔄 {retweets} 💬 {comments} ❤️ {likes}"
        
        # Generate unique tweet ID
        tweet_id = ''.join(random.choices('0123456789', k=19))
        
        results.append({
            '제목': f"@{handle}: {content[:50]}...",  # Use first part of content as title
            '내용': f"{content}\n\n{engagement} • {relative_time}",
            '언론사': f"Twitter/X - @{handle}",
            '날짜': f"{date_str} {time_str}",
            '링크': f"https://twitter.com/{handle}/status/{tweet_id}"
        })
    
    return results 