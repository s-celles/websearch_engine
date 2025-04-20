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
        # Supprimer le fragment de l'URL (tout ce qui est après #)
        parsed = urlparse(url)
        url_without_fragment = parsed._replace(fragment='').geturl()
        
        # Vérifier si l'URL sans fragment a déjà été visitée
        if url_without_fragment in self.visited_urls:
            return False
        
        # Vérifications standards
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
                # Supprimer le fragment avant de l'ajouter aux URLs visitées
                parsed = urlparse(row[0])
                url_without_fragment = parsed._replace(fragment='').geturl()
                self.visited_urls.add(url_without_fragment)
        
        while urls_to_visit and len(self.visited_urls) < self.max_pages:
            current_url = urls_to_visit.pop(0)
            
            # Supprimer le fragment avant de vérifier si l'URL a été visitée
            parsed = urlparse(current_url)
            current_url_without_fragment = parsed._replace(fragment='').geturl()
            
            if current_url_without_fragment in self.visited_urls:
                continue
            
            try:
                print(f"Crawling: {current_url}")
                response = requests.get(current_url, timeout=5)
                
                if response.status_code == 200:
                    self.visited_urls.add(current_url_without_fragment)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extraire le contenu textuel
                    text = soup.get_text(separator=' ', strip=True)
                    title = soup.title.string if soup.title else current_url
                    
                    # Sauvegarder le document (utiliser l'URL originale pour le stockage)
                    doc_id = self.save_document(current_url, title, text)
                    if doc_id:
                        documents_count += 1
                    
                    # Trouver les liens
                    for link in soup.find_all('a', href=True):
                        new_url = urljoin(current_url, link['href'])
                        
                        # Vérifier si l'URL sans fragment a déjà été visitée
                        parsed_new_url = urlparse(new_url)
                        new_url_without_fragment = parsed_new_url._replace(fragment='').geturl()
                        
                        if new_url_without_fragment not in self.visited_urls and self.is_valid_url(new_url):
                            urls_to_visit.append(new_url)
                
                # Politesse envers les serveurs
                time.sleep(1)
                
            except Exception as e:
                print(f"Erreur lors du crawl de {current_url}: {e}")
        
        return documents_count