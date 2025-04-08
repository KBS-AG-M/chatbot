# app/faq_engine.py
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class FAQEngine:
    def __init__(self, dataset_path='data/faq_dataset.csv'):
        self.df = pd.read_csv(dataset_path)
        self.vectorizer = TfidfVectorizer()
        self.questions = self.df['question'].tolist()
        self.answers = self.df['answer'].tolist()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.questions)

    def get_answer(self, query):
        query_vec = self.vectorizer.transform([query])
        similarity = cosine_similarity(query_vec, self.tfidf_matrix)
        index = similarity.argmax()
        return self.answers[index]
