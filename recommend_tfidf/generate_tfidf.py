# this file only needs to be run once to generate the tfidf vectors and save them to a pickle file

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import re

DATA_FILE = 'coursecatalog.csv'
data = pd.read_csv(DATA_FILE)
data = data.dropna(subset=['CourseCode', 'Description'])
data = data[~data['Description'].str.contains(r'^[^\w]*$', flags=re.IGNORECASE)]

# Combine 'Description', 'CourseCode', 'Name', and 'Faculty' into a single entry
data['combined'] = data.apply(lambda row: ' '.join([str(row['Description']), str(row['CourseCode']), str(row['Name']), str(row['Faculty'])]), axis=1)
course_descriptions = data["combined"].tolist()
course_titles = data["CourseCode"].tolist()

tfidfvectorizer = TfidfVectorizer(analyzer='word', stop_words= 'english', ngram_range=(2, 5))
vectors = tfidfvectorizer.fit_transform(course_descriptions)

print("Length of course_titles:", len(course_titles))
print("Length of vectors:", len(vectors.toarray()))

with open("recommend_tfidf/vectorizer.pkl", "wb") as f:
    pickle.dump(tfidfvectorizer, f)

# Include "Name" and "Description" in the course_data DataFrame
course_data = pd.DataFrame({"course_title": course_titles, "vector": list(vectors.toarray()), "Name": data["Name"], "Description": data["Description"]})
course_data.to_pickle("recommend_tfidf/course_data.pkl")