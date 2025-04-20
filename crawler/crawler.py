import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import sqlite3

class WebCrawler:
    def __init__(self, db_manager, start_urls, max_pages=100):
        self.db_manager = db_manager
        self.start_urls = start_urls
        self.max_pages = max_pages
        self.visited_urls = set()
    
    def is_valid_url(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
    
    def save_document(self, url, title, content):
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO documents (url, title, content) VALUES (?, ?, ?)",
                    (url, title, content)
                )
                conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                # URL existe déjà
                return None
    
    def crawl(self):
        urls_to_visit = self.start_urls.copy()
        documents_count = 0
        
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            # Récupérer les URLs déjà visitées de la base de données
            cursor.execute("SELECT url FROM documents")
            for row in cursor.fetchall():
                self.visited_urls.add(row[0])
        
        while urls_to_visit and len(self.visited_urls) < self.max_pages:
            current_url = urls_to_visit.pop(0)
            
            if current_url in self.visited_urls:
                continue
            
            try:
                print(f"Crawling: {current_url}")
                response = requests.get(current_url, timeout=5)
                
                if response.status_code == 200:
                    self.visited_urls.add(current_url)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extraire le contenu textuel
                    text = soup.get_text(separator=' ', strip=True)
                    title = soup.title.string if soup.title else current_url
                    
                    # Sauvegarder le document
                    doc_id = self.save_document(current_url, title, text)
                    if doc_id:
                        documents_count += 1
                    
                    # Trouver les liens
                    for link in soup.find_all('a', href=True):
                        new_url = urljoin(current_url, link['href'])
                        if self.is_valid_url(new_url) and new_url not in self.visited_urls:
                            urls_to_visit.append(new_url)
                
                # Politesse envers les serveurs
                time.sleep(1)
                
            except Exception as e:
                print(f"Erreur lors du crawl de {current_url}: {e}")
        
        return documents_count