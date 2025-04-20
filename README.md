# Moteur de recherche web minimaliste en Python

Un moteur de recherche modulaire développé en Python, utilisant SQLite pour le stockage persistant des données.

## 📋 Aperçu

Ce projet implémente un moteur de recherche complet avec les composants suivants :
- Un crawler web pour collecter les documents
- Un indexeur pour traiter et organiser les données textuelles
- Un moteur de recherche avec algorithme TF-IDF pour le classement des résultats
- Une interface web intuitive développée avec Flask

L'architecture est conçue pour être modulaire, extensible et démontrer les principes fondamentaux des moteurs de recherche.

## 🛠️ Fonctionnalités

- **Crawling web** : Explore le web à partir d'URLs de départ, extrait le contenu textuel et les liens
- **Indexation** : Prétraitement linguistique (tokenisation, suppression des mots vides, stemming) et création d'un index inversé
- **Recherche** : Algorithme TF-IDF pour le classement des résultats par pertinence
- **Persistance** : Stockage efficace des documents et de l'index dans une base de données SQLite
- **Interface web** : Interface utilisateur simple et réactive avec AJAX

## 🔧 Prérequis

- Python 3.7+
- Bibliothèques Python :
  - requests
  - beautifulsoup4
  - nltk
  - flask

## 📥 Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/votrenom/moteur-recherche-python.git
cd moteur-recherche-python
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Téléchargez les ressources NLTK :
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## 🚀 Utilisation

### Structure du projet

```
moteur_recherche/
├── db/
│   └── search_engine.db
├── crawler/
│   ├── __init__.py
│   └── crawler.py
├── indexer/
│   ├── __init__.py
│   └── indexer.py
├── searcher/
│   ├── __init__.py
│   └── searcher.py
├── web_ui/
│   ├── __init__.py
│   ├── app.py
│   └── templates/
│       └── search.html
├── db_manager.py
├── main.py
└── requirements.txt
```

### Commandes

1. **Crawler des sites web** :
```bash
python main.py --crawl --urls https://fr.wikipedia.org/wiki/Python_(langage) --max-pages 20
```

2. **Indexer les documents** :
```bash
python main.py --index
```

3. **Lancer l'interface web** :
```bash
python main.py
```

4. **Exécuter le processus complet** :
```bash
python main.py --crawl --index --urls https://fr.wikipedia.org/wiki/Python_(langage) --max-pages 50
```

Une fois lancé, accédez à l'interface web à l'adresse http://localhost:5000

## 🧮 Aspects mathématiques

Le moteur utilise plusieurs concepts mathématiques :

### TF-IDF (Term Frequency-Inverse Document Frequency)

La formule utilisée pour calculer la pertinence d'un document :

$$\text{Score}(t,d) = \text{TF}(t,d) \times \text{IDF}(t)$$

Où :
- $\text{TF}(t,d) = \frac{\text{nombre d'occurrences de } t \text{ dans } d}{\text{nombre total de termes dans } d}$
- $\text{IDF}(t) = \log\left(\frac{\text{nombre total de documents}}{\text{nombre de documents contenant } t}\right)$

### Modèle vectoriel

Les documents et requêtes sont représentés comme des vecteurs dans un espace multidimensionnel, où chaque dimension correspond à un terme unique.

## 🔍 Fonctionnement détaillé

### DatabaseManager (db_manager.py)
Gère la base de données SQLite, crée les tables et fournit les connexions.

### WebCrawler (crawler/crawler.py)
Explore le web en suivant les liens et stocke les documents dans la base de données.

### Indexer (indexer/indexer.py)
Prétraite le texte des documents et construit l'index inversé.

### SearchEngine (searcher/searcher.py)
Traite les requêtes et renvoie les résultats classés par pertinence.

### WebInterface (web_ui/app.py)
Interface utilisateur pour interagir avec le moteur de recherche.

## 📈 Performances

Sur un corpus de test de 50 pages :
- Temps de crawling : ~2 minutes
- Temps d'indexation : quelques secondes
- Temps de réponse aux requêtes : < 100ms

## 🔄 Amélioration possibles

- Implémentation d'un algorithme PageRank pour améliorer le classement
- Gestion des fautes d'orthographe dans les requêtes
- Analyse sémantique pour mieux comprendre le contexte
- Interface d'administration pour gérer l'indexation
- Parallélisation du crawler pour améliorer les performances

## 📚 Ressources

- [Théorie des moteurs de recherche](https://en.wikipedia.org/wiki/Search_engine_(computing))
- [TF-IDF et recherche d'information](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)
- [Documentation de NLTK](https://www.nltk.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.
