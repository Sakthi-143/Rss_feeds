# Rss_feeds
: Build an application that collects news articles from various RSS feeds (e.g: listed below), stores them in a database, and categorizes them into predefined categories.
# 📡 RSS Feed Processor and Classifier

## 📚 Table of Contents
1. [Introduction](#-introduction)
2. [System Architecture](#-system-architecture)
3. [Installation and Setup](#-installation-and-setup)
4. [Code Structure](#-code-structure)
5. [Key Components](#-key-components)
6. [Running the Application](#-running-the-application)
7. [Maintenance and Troubleshooting](#-maintenance-and-troubleshooting)
8. [Future Enhancements](#-future-enhancements)
9. [Conclusion](#-conclusion)

---

## 1. 📘 Introduction

### Project Objectives
The **RSS Feed Processor and Classifier** is a Python-based application designed to:
- Collect news articles from multiple RSS feeds.
- Store article data in a structured database.
- Categorize articles into predefined categories using machine learning.
- Process articles asynchronously for improved performance.
- Provide a scalable and maintainable solution.

### Technology Stack
- **Python 3.8+**
- **MySQL** for database management
- **SQLAlchemy** as the Object Relational Mapper (ORM)
- **Celery** for task queue handling
- **Redis** as the message broker
- **Scikit-learn** for machine learning
- **NLTK** for natural language processing

## 2. 🏛️ System Architecture

The application follows a modular architecture, consisting of:
1. **RSS Feed Parser**: Fetches and parses RSS feeds.
2. **Database Layer**: Manages data storage and retrieval.
3. **Task Queue**: Handles asynchronous processing of articles.
4. **Classification Engine**: Categorizes articles using machine learning techniques.

**Flow:** 
```
[RSS Feeds] -> [Feed Parser] -> [Database] <- [Task Queue] <- [Classification Engine]
```

## 3. ⚙️ Installation and Setup

### 3.1 Prerequisites
- **Python 3.8** or higher
- **MySQL Server**
- **Redis Server**

### 3.2 Environment Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv rss_env
   source rss_env/bin/activate  # On Windows: rss_env\Scripts\activate
   ```

2. **Install required packages:**
   ```bash
   pip install feedparser sqlalchemy mysql-connector-python celery redis scikit-learn nltk
   ```

### 3.3 Database Setup
1. **Create a MySQL database:**
   ```sql
   CREATE DATABASE rss_processor;
   ```

2. **Update the `DB_URL` in `main.py` with your database credentials:**
   ```python
   DB_URL = "mysql+mysqlconnector://username:password@localhost/rss_processor"
   ```

### 3.4 Redis Setup
- Ensure Redis is installed and running on the default port (**6379**).

## 4. 📂 Code Structure

The main application script (`main.py`) consists of:
- Imports and configuration
- Database model definition
- Celery task queue setup
- RSS feed parsing function
- Article processing task
- Classification logic
- Main execution function

## 5. 🔑 Key Components

### 5.1 Database Model
Defines the schema for storing articles in the database:
```python
class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    content = Column(Text)
    pub_date = Column(DateTime)
    source_url = Column(String(255), unique=True)
    category = Column(String(50))
```

### 5.2 RSS Feed Parsing
The `parse_feed` function fetches and processes RSS feeds:
```python
def parse_feed(feed_url):
    # Fetch and parse feed
    # Store new articles in database
    # Queue articles for processing
```

### 5.3 Asynchronous Processing
Celery is used for asynchronous article processing:
```python
@app.task(bind=True, default_retry_delay=300, max_retries=5)
def process_article(self, article_id):
    # Retrieve article from database
    # Classify article
    # Update database with classification
```

### 5.4 Classification Engine
A **scikit-learn** pipeline is used for article classification:
```python
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words=stopwords.words('english'))),
    ('clf', MultinomialNB()),
])
```

## 6. 🚀 Running the Application

1. **Start the Celery worker:**
   ```bash
   celery -A main worker --loglevel=info
   ```

2. **Run the main script in a separate terminal:**
   ```bash
   python main.py
   ```

The application will start processing RSS feeds, storing articles, and classifying them asynchronously.

## 7. 🛠️ Maintenance and Troubleshooting

### 7.1 Logging
The application uses Python's logging module, with logs written to `app.log`:
```python
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
```

### 7.2 Common Issues
1. **Database Connection Errors**: Ensure that MySQL is running and credentials are correctly set.
2. **Celery Worker Not Starting**: Check if Redis is running and accessible.
3. **Classification Errors**: Verify that the **NLTK** data is downloaded properly.

## 8. 🔧 Future Enhancements

- **Web Interface**: Implement a web UI for monitoring and management.
- **Enhanced Classification**: Use a larger, domain-specific dataset to improve accuracy.
- **Full-text Article Extraction**: Extend support for extracting full article content.
- **Periodic Scheduling**: Add support for automatic RSS feed updates.
- **Test Suite Development**: Create a comprehensive test suite for better reliability.

## 9. 📈 Conclusion

The **RSS Feed Processor and Classifier** provides a scalable solution for automating the collection and categorization of news articles. By leveraging asynchronous processing and machine learning, the application efficiently handles large volumes of data from various sources.

