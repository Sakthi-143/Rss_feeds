#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('pip install feedparser')


# In[4]:


get_ipython().system('pip install celery')


# In[6]:


get_ipython().system('pip install mysql-connector-python')


# In[ ]:





# In[8]:


import feedparser
from datetime import datetime
import logging
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from celery import Celery
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import nltk
from nltk.corpus import stopwords
import pickle
import os

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize SQLAlchemy
Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    content = Column(Text)
    pub_date = Column(DateTime)
    source_url = Column(String(255), unique=True)
    category = Column(String(50))

# Database connection
DB_URL = "mysql+mysqlconnector://username:mysql.sys@localhost/dbname"
engine = create_engine(DB_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Celery configuration
app = Celery('tasks', broker='redis://localhost:6379')
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# List of RSS feeds
RSS_FEEDS = [
    'http://rss.cnn.com/rss/cnn_topstories.rss',
    'http://qz.com/feed',
    'http://feeds.foxnews.com/foxnews/politics',
    'http://feeds.reuters.com/reuters/businessNews',
    'http://feeds.feedburner.com/NewshourWorld',
    'https://feeds.bbci.co.uk/news/world/asia/india/rss.xml'
]

# Load or train the classifier
CLASSIFIER_FILE = 'classifier.pkl'

def train_classifier():
    # This is a placeholder. In a real scenario, you'd have a labeled dataset.
    X = ["Terrorists attacked the city center", 
         "New breakthrough in cancer research brings hope",
         "Earthquake devastates coastal town",
         "Stock market reaches new heights"]
    y = ["Terrorism / protest / political unrest / riot",
         "Positive/Uplifting",
         "Natural Disasters",
         "Others"]
    
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words=stopwords.words('english'))),
        ('clf', MultinomialNB()),
    ])
    
    pipeline.fit(X, y)
    
    with open(CLASSIFIER_FILE, 'wb') as f:
        pickle.dump(pipeline, f)
    
    return pipeline

def load_classifier():
    if os.path.exists(CLASSIFIER_FILE):
        with open(CLASSIFIER_FILE, 'rb') as f:
            return pickle.load(f)
    else:
        return train_classifier()

classifier = load_classifier()

def parse_feed(feed_url):
    try:
        feed = feedparser.parse(feed_url)
        session = Session()

        for entry in feed.entries:
            try:
                existing_article = session.query(Article).filter_by(source_url=entry.link).first()
                if not existing_article:
                    article = Article(
                        title=entry.title,
                        content=entry.summary,
                        pub_date=datetime(*entry.published_parsed[:6]),
                        source_url=entry.link
                    )
                    session.add(article)
                    session.commit()
                    process_article.delay(article.id)
            except Exception as e:
                logger.error(f"Error processing entry from {feed_url}: {str(e)}")
                session.rollback()

        session.close()
    except Exception as e:
        logger.error(f"Error parsing feed {feed_url}: {str(e)}")

@app.task(bind=True, default_retry_delay=300, max_retries=5)
def process_article(self, article_id):
    try:
        session = Session()
        article = session.query(Article).get(article_id)
        
        if article:
            category = classifier.predict([article.content])[0]
            article.category = category
            session.commit()
        
        session.close()
    except Exception as e:
        logger.error(f"Error processing article {article_id}: {str(e)}")
        raise self.retry(exc=e)

def main():
    for feed in RSS_FEEDS:
        parse_feed(feed)

if __name__ == "__main__":
    main()


# In[ ]:




