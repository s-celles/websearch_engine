import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path='db/search_engine.db'):
        # Créer le répertoire de la base de données s'il n'existe pas
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_path = db_path
        self.create_tables()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def create_tables(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Table des documents
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                title TEXT,
                content TEXT,
                crawl_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Table de l'index inversé
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS inverted_index (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                term TEXT,
                document_id INTEGER,
                frequency INTEGER,
                FOREIGN KEY (document_id) REFERENCES documents (id),
                UNIQUE(term, document_id)
            )
            ''')
            
            # Index pour accélérer les recherches
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_term ON inverted_index (term)')
            
            conn.commit()