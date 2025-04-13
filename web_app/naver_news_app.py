import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from datetime import datetime
import sys
import queue

# Import our crawler functionality
from naver_news_downloader import get_naver_news, save_to_excel

class NaverNewsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Naver News Downloader")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 12))
        self.style.configure('TLabel', font=('Arial', 12))
        self.style.configure('TEntry', font=('Arial', 12))
        
        # Create message queue for thread-safe UI updates
        self.msg_queue = queue.Queue()
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Naver News Downloader", font=('Arial', 18, 'bold'))
        title_label.pack(pady=10)
        
        # Create input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        # Keyword input
        keyword_label = ttk.Label(input_frame, text="Search Keyword:")
        keyword_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.keyword_var = tk.StringVar()
        keyword_entry = ttk.Entry(input_frame, textvariable=self.keyword_var, width=30)
        keyword_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Page count input
        pages_label = ttk.Label(input_frame, text="Number of Pages:")
        pages_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.pages_var = tk.IntVar(value=5)
        pages_spinbox = ttk.Spinbox(input_frame, from_=1, to=20, textvariable=self.pages_var, width=5)
        pages_spinbox.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Output directory
        output_label = ttk.Label(input_frame, text="Output Directory:")
        output_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.output_dir_var = tk.StringVar(value="downloads")
        output_entry = ttk.Entry(input_frame, textvariable=self.output_dir_var, width=30)
        output_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        browse_button = ttk.Button(input_frame, text="Browse...", command=self.browse_directory)
        browse_button.grid(row=2, column=2, padx=5, pady=5)
        
        # Start button
        start_button = ttk.Button(main_frame, text="Start Download", command=self.start_download)
        start_button.pack(pady=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=10)
        
        # Status text
        self.status_text = tk.Text(main_frame, height=10, wrap=tk.WORD)
        self.status_text.pack(fill=tk.BOTH, expand=True, pady=10)
        self.status_text.config(state=tk.DISABLED)
        
        # Bind keyboard shortcuts
        self.root.bind('<Return>', lambda event: self.start_download())
        
        # Start message checking
        self.check_queue()
    
    def browse_directory(self):
        """Open directory browser dialog"""
        directory = filedialog.askdirectory(initialdir=os.getcwd())
        if directory:
            self.output_dir_var.set(directory)
    
    def update_status(self, message):
        """Add message to queue for thread-safe UI updates"""
        self.msg_queue.put(message)
    
    def check_queue(self):
        """Check for messages in the queue and update UI"""
        try:
            while True:
                message = self.msg_queue.get_nowait()
                self.status_text.config(state=tk.NORMAL)
                self.status_text.insert(tk.END, message + "\n")
                self.status_text.see(tk.END)
                self.status_text.config(state=tk.DISABLED)
                self.msg_queue.task_done()
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)
    
    def start_download(self):
        """Start the download process in a separate thread"""
        keyword = self.keyword_var.get().strip()
        if not keyword:
            messagebox.showerror("Error", "Please enter a search keyword.")
            return
        
        # Reset UI
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.progress_var.set(0)
        
        # Start thread
        threading.Thread(target=self._download_thread, daemon=True).start()
    
    def _download_thread(self):
        """Run the download process (in a separate thread)"""
        try:
            # Get input values
            keyword = self.keyword_var.get().strip()
            pages = self.pages_var.get()
            output_dir = self.output_dir_var.get().strip()
            
            # Make sure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Create output filename
            today = datetime.now().strftime('%Y%m%d')
            filename = f"{output_dir}/{keyword}_news_{today}.xlsx"
            
            # Redirect print output to our status text
            def custom_print(message):
                self.update_status(message)
            
            # Start crawling
            self.update_status(f"Searching for '{keyword}' news...")
            
            # Create a local subclass of get_naver_news that can update our progress bar
            def get_news_with_progress():
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                articles = []
                
                for page in range(1, pages + 1):
                    # Update progress bar
                    progress = (page - 1) / pages * 100
                    self.progress_var.set(progress)
                    
                    self.update_status(f"Fetching page {page}/{pages}...")
                    
                    # Same logic as in get_naver_news
                    url = f'https://search.naver.com/search.naver?where=news&query={keyword}&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&refresh_start=0&related=0&start={((page-1)*10)+1}'
                    
                    try:
                        import requests
                        from bs4 import BeautifulSoup
                        
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
                            date = date_text
                            
                            if title and content and link:
                                articles.append({
                                    '제목': title.get_text(strip=True),
                                    '내용': content.get_text(strip=True),
                                    '언론사': publisher,
                                    '날짜': date,
                                    '링크': link
                                })
                        
                        # Add delay to avoid overloading server
                        import time
                        time.sleep(1)
                        
                    except Exception as e:
                        self.update_status(f"Error on page {page}: {str(e)}")
                        continue
                
                self.progress_var.set(100)
                self.update_status(f"Total articles found: {len(articles)}")
                return articles
            
            # Get articles with progress updates
            articles = get_news_with_progress()
            
            if articles:
                # Save to Excel
                save_to_excel(articles, filename)
                self.update_status(f"Data saved to {filename}")
                self.update_status(f"File location: {os.path.abspath(filename)}")
                self.update_status(f"Successfully downloaded {len(articles)} articles about '{keyword}'")
                
                # Show completion message
                messagebox.showinfo("Download Complete", 
                                   f"Successfully downloaded {len(articles)} articles.\nSaved to {os.path.abspath(filename)}")
            else:
                self.update_status("No articles found.")
                messagebox.showinfo("No Results", "No articles found for the given keyword.")
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create executable
def main():
    root = tk.Tk()
    app = NaverNewsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 