# app/faq_engine.py
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK data (only needed once)
nltk.download('punkt')
nltk.download('stopwords')

class FAQEngine:
    def __init__(self, dataset_path):
        # Load the dataset
        self.df = pd.read_csv(dataset_path)

        # Validate that the required columns exist
        required_columns = {'Category', 'Question', 'Answer'}
        if not required_columns.issubset(self.df.columns):
            raise ValueError(f"The dataset must contain the following columns: {required_columns}")

        # Extract questions and answers
        self.questions = self.df['Question'].tolist()
        self.answers = self.df['Answer'].tolist()

        # Preprocess questions
        self.processed_questions = [self.preprocess_text(q) for q in self.questions]

    def preprocess_text(self, text):
        """Tokenize, remove stopwords, and lowercase the text."""
        stop_words = set(stopwords.words('english'))
        tokens = word_tokenize(text.lower())
        return ' '.join([word for word in tokens if word.isalnum() and word not in stop_words])

    def get_answer(self, user_question):
        """Find the best matching FAQ question and return its answer."""
        # Preprocess the user question
        processed_user_question = self.preprocess_text(user_question)

        # Combine the user question with the FAQ questions
        all_questions = self.processed_questions + [processed_user_question]

        # Compute TF-IDF vectors
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(all_questions)

        # Compute cosine similarity between the user question and FAQ questions
        similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

        # Find the index of the most similar question
        best_match_index = similarity_scores.argmax()
        best_match_score = similarity_scores[0, best_match_index]

        # Return the answer if the similarity score is above a threshold
        if best_match_score > 0.3:  # Adjust the threshold as needed
            return self.answers[best_match_index]
        else:
            return "Sorry, I couldn't find an answer to your question. Can you rephrase?"
