import pandas as pd
import nltk
import pickle
import random
import numpy as np
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

class ChatbotModel:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.tfidf_vectorizer = TfidfVectorizer()
        self.questions = []
        self.answers = []
        self.tfidf_matrix = None
        self.greeting_inputs = ["hello", "hi", "greetings", "hey", "what's up", "howdy"]
        self.greeting_responses = [
            "Hello, how can I help you with blood donation today?",
            "Hi there! What would you like to know about blood donation?",
            "Hey! I'm here to answer your blood donation questions.",
            "Greetings! How can I assist you with blood donation information?"
        ]
        
    def load_data(self, csv_file):
        """Load and preprocess the dataset"""
        try:
            data = pd.read_csv(csv_file)
            self.questions = data['Question'].tolist()
            self.answers = data['Answer'].tolist()
            
            # Preprocess questions for TF-IDF
            processed_questions = [self.preprocess_text(q) for q in self.questions]
            
            # Create TF-IDF matrix
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(processed_questions)
            
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def preprocess_text(self, text):
        """Clean and preprocess text by removing punctuation, lemmatizing, etc."""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        
        # Tokenize and lemmatize
        tokens = nltk.word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens if word not in self.stop_words]
        
        return ' '.join(tokens)
    
    def get_response(self, user_input):
        """Generate a response to user input"""
        # Check for greetings
        user_input = user_input.lower()
        if user_input in self.greeting_inputs:
            return random.choice(self.greeting_responses)
        
        # Preprocess the user's query
        processed_query = self.preprocess_text(user_input)
        
        # Transform user query using the same vectorizer
        query_vector = self.tfidf_vectorizer.transform([processed_query])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_vector, self.tfidf_matrix)[0]
        
        # If no good match found (threshold can be adjusted)
        if np.max(similarities) < 0.3:
            return "I'm sorry, I don't have enough information about that. Could you ask something else about blood donation?"
        
        # Get index of most similar question
        closest_match_idx = np.argmax(similarities)
        
        # Return corresponding answer
        return self.answers[closest_match_idx]
    
    def save_model(self, filename):
        """Save the trained model to a file"""
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def load_model(filename):
        """Load a trained model from a file"""
        with open(filename, 'rb') as f:
            return pickle.load(f)

def train_and_save_model(csv_file, model_file):
    """Train a new chatbot model and save it"""
    chatbot = ChatbotModel()
    success = chatbot.load_data(csv_file)
    if success:
        chatbot.save_model(model_file)
        print(f"Model trained and saved to {model_file}")
    else:
        print("Failed to train model")

def handle_chat_query(user_input, model_file='chat_model.pkl'):
    """Function to be called from the web app to get responses"""
    try:
        chatbot = ChatbotModel.load_model(model_file)
        return chatbot.get_response(user_input)
    except Exception as e:
        print(f"Error handling query: {e}")
        return "Sorry, I'm having trouble processing your request."

# This section would be used to train the model initially
if __name__ == "__main__":
    train_and_save_model('dataset.csv', 'chat_model.pkl')