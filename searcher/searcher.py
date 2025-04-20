# searcher/searcher.py
import math
from collections import defaultdict
import nltk


class SearchEngine:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        # Créer un indexeur pour prétraiter les requêtes
        from indexer.indexer import Indexer

        self.query_processor = Indexer(db_manager)

    def get_total_documents(self):
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM documents")
            return cursor.fetchone()[0]

    def search(self, query, top_k=10):
        # Prétraiter la requête
        query_terms = self.query_processor.preprocess_text(query)

        if not query_terms:
            return []

        total_documents = self.get_total_documents()
        if total_documents == 0:
            return []

        # Calculer les scores TF-IDF
        scores = defaultdict(float)

        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()

            for term in query_terms:
                # Trouver les documents contenant ce terme
                cursor.execute(
                    """
                    SELECT document_id, frequency, 
                           (SELECT COUNT(*) FROM documents) as total_docs,
                           (SELECT COUNT(*) FROM inverted_index WHERE term = ?) as term_docs
                    FROM inverted_index 
                    WHERE term = ?
                """,
                    (term, term),
                )

                results = cursor.fetchall()

                if results:
                    # Pour chaque document contenant le terme
                    for doc_id, term_freq, total_docs, term_docs in results:
                        # Calculer IDF (Inverse Document Frequency)
                        idf = math.log(total_docs / term_docs) if term_docs > 0 else 0

                        # Pour calculer TF, nous avons besoin de la longueur du document
                        cursor.execute(
                            """
                            SELECT LENGTH(content) 
                            FROM documents 
                            WHERE id = ?
                        """,
                            (doc_id,),
                        )

                        doc_length = cursor.fetchone()[0]
                        if doc_length > 0:
                            # Calculer TF (Term Frequency)
                            tf = term_freq / doc_length
                            # Ajouter le score TF-IDF
                            scores[doc_id] += tf * idf

            # Récupérer les informations sur les documents avec les meilleurs scores
            ranked_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)[
                :top_k
            ]

            results = []
            for doc_id, score in ranked_results:
                cursor.execute(
                    "SELECT url, title FROM documents WHERE id = ?", (doc_id,)
                )
                url, title = cursor.fetchone()

                results.append(
                    {"id": doc_id, "url": url, "title": title, "score": score}
                )

        return results
