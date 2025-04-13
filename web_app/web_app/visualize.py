import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
from wordcloud import WordCloud
import numpy as np
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go
import re
from datetime import datetime

# Set style for plots
plt.style.use('dark_background')
sns.set_style("darkgrid")

def load_excel_files():
    """Load all Excel files from the downloads directory"""
    downloads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
    if not os.path.exists(downloads_dir):
        return None, "Downloads directory does not exist. Please run a search first."
    
    excel_files = glob.glob(os.path.join(downloads_dir, '*.xlsx'))
    if not excel_files:
        return None, "No Excel files found. Please run a search first."
    
    # Sort by modification time (newest first)
    excel_files.sort(key=os.path.getmtime, reverse=True)
    return excel_files, None

def get_file_info(file_path):
    """Extract info from filename and get modification time"""
    filename = os.path.basename(file_path)
    # Remove extension
    name_without_ext = os.path.splitext(filename)[0]
    # Split by underscore
    parts = name_without_ext.split('_')
    
    # Extract keyword and date if possible
    if len(parts) >= 3:
        keyword = '_'.join(parts[:-2])  # Everything before the last two elements
        date = parts[-2]  # Second to last element is date
    else:
        keyword = name_without_ext
        date = "Unknown"
    
    # Get file modification time
    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
    mod_time_str = mod_time.strftime('%Y-%m-%d %H:%M:%S')
    
    # Get file size
    size_bytes = os.path.getsize(file_path)
    size_kb = size_bytes / 1024
    
    return {
        'filename': filename,
        'keyword': keyword,
        'date': date,
        'modified': mod_time_str,
        'size_kb': f"{size_kb:.1f} KB",
        'path': file_path
    }

def load_data(file_path):
    """Load data from Excel file"""
    try:
        df = pd.read_excel(file_path)
        return df, None
    except Exception as e:
        return None, f"Error loading file: {str(e)}"

def clean_text(text):
    """Clean text for word cloud and analysis"""
    if not isinstance(text, str):
        return ""
    # Remove URLs, special characters, and extra spaces
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def generate_wordcloud(text_data):
    """Generate a word cloud from text data"""
    if not text_data or text_data.isspace():
        return "Not enough text data for word cloud"
    
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='#111',
        colormap='viridis',
        max_words=200
    ).generate(text_data)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    return plt

def count_sources(df):
    """Count articles by source"""
    if 'Source' not in df.columns and '언론사' in df.columns:
        source_col = '언론사'
    else:
        source_col = 'Source'
    
    if source_col in df.columns:
        source_counts = df[source_col].value_counts()
        return source_counts
    return None

def visualize_page():
    """Main visualization page"""
    st.title("Data Visualization")
    st.write("Analyze and visualize your search results")
    
    # Load Excel files
    excel_files, error = load_excel_files()
    
    if error:
        st.error(error)
        return
    
    # Convert files to info dictionaries
    file_infos = [get_file_info(file) for file in excel_files]
    
    # Create a DataFrame for file selection
    files_df = pd.DataFrame(file_infos)
    
    # File selector
    st.subheader("Select Data File")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_file = st.selectbox(
            "Choose a file to visualize:",
            options=files_df['path'].tolist(),
            format_func=lambda x: f"{os.path.basename(x)} ({files_df.loc[files_df['path'] == x, 'keyword'].iloc[0]})"
        )
    
    # Show file info
    selected_info = files_df[files_df['path'] == selected_file].iloc[0]
    with col2:
        st.info(f"**File Info:**\n"
                f"- Keyword: {selected_info['keyword']}\n"
                f"- Date: {selected_info['date']}\n"
                f"- Size: {selected_info['size_kb']}")
    
    # Load data
    df, error = load_data(selected_file)
    if error:
        st.error(error)
        return
    
    # Show basic stats
    st.subheader("Data Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Articles", len(df))
    with col2:
        if 'Source' in df.columns:
            sources = len(df['Source'].unique())
        elif '언론사' in df.columns:
            sources = len(df['언론사'].unique())
        else:
            sources = "N/A"
        st.metric("Unique Sources", sources)
    with col3:
        if '날짜' in df.columns:
            dates = len(df['날짜'].unique())
            st.metric("Date Range", dates)
        else:
            st.metric("Date Range", "N/A")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["Word Cloud", "Source Analysis", "Content Length", "Raw Data"])
    
    with tab1:
        st.subheader("Word Cloud Visualization")
        # Combine title and content text
        if '제목' in df.columns and '내용' in df.columns:
            combined_text = ' '.join(df['제목'].astype(str) + ' ' + df['내용'].astype(str))
            combined_text = clean_text(combined_text)
            
            if combined_text:
                wordcloud_plt = generate_wordcloud(combined_text)
                st.pyplot(wordcloud_plt)
            else:
                st.warning("Not enough text data for word cloud")
        else:
            st.warning("Required columns not found for word cloud")
    
    with tab2:
        st.subheader("Source Analysis")
        source_counts = count_sources(df)
        
        if source_counts is not None and not source_counts.empty:
            # Plot with Plotly for interactive charts
            fig = px.bar(
                x=source_counts.index, 
                y=source_counts.values,
                labels={'x': 'Source', 'y': 'Article Count'},
                title='Article Count by Source',
                color=source_counts.values,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(
                plot_bgcolor='rgba(17,17,17,0.8)',
                paper_bgcolor='rgba(17,17,17,0.8)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Pie chart
            fig = px.pie(
                values=source_counts.values, 
                names=source_counts.index,
                title='Source Distribution',
                hole=0.4
            )
            fig.update_layout(
                plot_bgcolor='rgba(17,17,17,0.8)',
                paper_bgcolor='rgba(17,17,17,0.8)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Source information not available")
    
    with tab3:
        st.subheader("Content Length Analysis")
        if '내용' in df.columns:
            # Calculate content lengths
            df['content_length'] = df['내용'].astype(str).apply(len)
            
            # Histogram
            fig = px.histogram(
                df, 
                x='content_length',
                nbins=20,
                title='Distribution of Content Length',
                labels={'content_length': 'Content Length (characters)', 'count': 'Number of Articles'},
                color_discrete_sequence=['#4CAF50']
            )
            fig.update_layout(
                plot_bgcolor='rgba(17,17,17,0.8)',
                paper_bgcolor='rgba(17,17,17,0.8)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Show stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Length", f"{df['content_length'].mean():.0f} chars")
            with col2:
                st.metric("Shortest", f"{df['content_length'].min()} chars")
            with col3:
                st.metric("Longest", f"{df['content_length'].max()} chars")
        else:
            st.warning("Content column not found")
    
    with tab4:
        st.subheader("Raw Data")
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    st.set_page_config(page_title="Data Visualization", layout="wide", page_icon="📊")
    visualize_page() 