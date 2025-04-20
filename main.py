# main.py
import argparse
import os
from db_manager import DatabaseManager
from crawler.crawler import WebCrawler
from indexer.indexer import Indexer
from searcher.searcher import SearchEngine
from web_ui.app import WebInterface

def main():
    parser = argparse.ArgumentParser(description='Moteur de recherche')
    parser.add_argument('--crawl', action='store_true', help='Lancer le crawler')
    parser.add_argument('--index', action='store_true', help='Lancer l\'indexation')
    parser.add_argument('--urls', nargs='+', help='URLs de départ pour le crawler')
    parser.add_argument('--max-pages', type=int, default=50, help='Nombre maximum de pages à crawler')
    parser.add_argument('--port', type=int, default=5000, help='Port pour l\'interface web')
    args = parser.parse_args()
    
    # Initialiser le gestionnaire de base de données
    db_manager = DatabaseManager()
    
    # Crawler
    if args.crawl:
        if not args.urls:
            print("Erreur: Veuillez spécifier au moins une URL de départ avec --urls")
            return
        
        crawler = WebCrawler(db_manager, args.urls, args.max_pages)
        print(f"Démarrage du crawling depuis {args.urls}...")
        documents_count = crawler.crawl()
        print(f"Crawling terminé. {documents_count} nouveaux documents collectés.")
    
    # Indexer
    if args.index:
        indexer = Indexer(db_manager)
        print("Indexation des documents...")
        indexed_count = indexer.build_index()
        print(f"Indexation terminée. {indexed_count} documents indexés.")
    
    # Moteur de recherche
    search_engine = SearchEngine(db_manager)
    
    # Interface web
    web_interface = WebInterface(search_engine)
    print(f"Démarrage de l'interface web sur le port {args.port}...")
    web_interface.run(port=args.port)

if __name__ == "__main__":
    main()