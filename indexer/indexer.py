# indexer/indexer.py
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import sqlite3

class Indexer:
    def __init__(self, db_manager, language='french'):
        self.db_manager = db_manager
        
        # Télécharger les ressources NLTK nécessaires
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words(language))
    
    def preprocess_text(self, text):
        # Convertir en minuscules et tokeniser
        tokens = word_tokenize(text.lower())
        
        # Supprimer la ponctuation et les chiffres
        tokens = [re.sub(r'[^\w\s]', '', token) for token in tokens]
        
        # Supprimer les mots vides et appliquer le stemming
        tokens = [self.stemmer.stem(token) for token in tokens 
                 if token and token not in self.stop_words]
        
        return tokens
    
    def index_document(self, doc_id, content):
        tokens = self.preprocess_text(content)
        
        # Calculer la fréquence des termes
        term_freq = {}
        for token in tokens:
            if token in term_freq:
                term_freq[token] += 1
            else:
                term_freq[token] = 1
        
        # Enregistrer dans la base de données
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            for term, freq in term_freq.items():
                try:
                    cursor.execute(
                        "INSERT INTO inverted_index (term, document_id, frequency) VALUES (?, ?, ?)",
                        (term, doc_id, freq)
                    )
                except sqlite3.IntegrityError:
                    # Mettre à jour si l'entrée existe déjà
                    cursor.execute(
                        "UPDATE inverted_index SET frequency = ? WHERE term = ? AND document_id = ?",
                        (freq, term, doc_id)
                    )
            conn.commit()
    
    def build_index(self):
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Récupérer tous les documents non encore indexés
            cursor.execute("""
                SELECT d.id, d.content 
                FROM documents d 
                LEFT JOIN inverted_index i ON d.id = i.document_id 
                WHERE i.id IS NULL
                GROUP BY d.id
            """)
            
            documents = cursor.fetchall()
            
        for doc_id, content in documents:
            print(f"Indexation du document {doc_id}...")
            self.index_document(doc_id, content)
        
        return len(documents)