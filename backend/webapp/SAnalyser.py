import re
import joblib
from keras.models import load_model
import gensim
from nltk.stem import WordNetLemmatizer 
import nltk
import getpass
import numpy as np

class SAnalysis:
	
	def __init__(self):
		self.model = load_model(f'/home/{getpass.getuser()}/Desktop/FF-Backend/backend/webapp/templates/webapp/sentiment_data/SA.h5')

	def lemmatize(self,text):
		return WordNetLemmatizer().lemmatize(text, pos='v')

	def preprocess(self,raw_text):
		# keep only words
		letters_only_text = re.sub("[^a-zA-Z]", " ", raw_text)
		# convert to lower case and split 
		words = letters_only_text.lower()
		return [self.lemmatize(token) for token in gensim.utils.simple_preprocess(words) ]

	def SentimentAnalyzer(self,doc): 
		doc=' '.join(self.preprocess(doc))
		embedding=[]
		with open(f'/home/{getpass.getuser()}/Desktop/FF-Backend/backend/webapp/templates/webapp/sentiment_data/dict.pkl', 'rb') as handle:
		    corpus_tfidf_vectorizer=joblib.load(handle)
		corpus_vocabulary=corpus_tfidf_vectorizer.vocabulary_
		sent_emb=np.zeros(487)
		j=0
		for w in doc.split():
			try:
				sent_emb[j]=corpus_vocabulary[w]
				j+=1
			except:
				continue
		embedding.append(sent_emb)
		embeddings=np.array(embedding)
		#print(len(embedding))
		return self.model.predict(embeddings)