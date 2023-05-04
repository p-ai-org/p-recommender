# this file only needs to be run once to generate the tfidf vectors and save them to a pickle file

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import re

data = pd.read_csv('course/courses.csv')
data = data.dropna(subset=['CourseCode', 'Course Description'])
data = data[~data['Course Description'].str.contains(r'^[^\w]*$', flags=re.IGNORECASE)]

# Combine 'Description', 'CourseCode', 'Name', and 'Faculty' into a single entry
data['combined'] = data.apply(lambda row: ' '.join([str(row['Course Description']), str(row['CourseCode']), str(row['Name']), str(row['Faculty']), str(row['Campus']), str(row['Prerequisites'])]), axis=1)
course_descriptions = data["combined"].tolist()
course_titles = data["CourseCode"].tolist()

tfidfvectorizer = TfidfVectorizer(analyzer='word', stop_words= 'english', ngram_range=(2, 5))
vectors = tfidfvectorizer.fit_transform(course_descriptions)

print("Length of course_titles:", len(course_titles))
print("Length of vectors:", len(vectors.toarray()))

with open("recommend_tfidf/vectorizer.pkl", "wb") as f:
    pickle.dump(tfidfvectorizer, f)

# Include "Name" and "Description" in the course_data DataFrame
course_data = pd.DataFrame({"course_title": course_titles, "vector": list(vectors.toarray()), "Name": data["Name"], "Description": data["Course Description"], "Instructor": data["Faculty"], "Location": data["Campus"], "Prerequisites": data["Prerequisites"], "GE(s) Satisfied": data["Course Area(s)"]})
print("course_data =", course_data)

course_data.to_pickle("recommend_tfidf/course_data.pkl")
