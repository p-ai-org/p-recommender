import pickle
from scipy.spatial.distance import cosine
import numpy as np
import pandas as pd
import re

with open("recommend_tfidf/vectorizer.pkl", "rb") as f:
    loaded_vectorizer = pickle.load(f)

with open("recommend_tfidf/course_data.pkl", "rb") as f:
    loaded_course_data = pd.read_pickle(f)

loaded_course_vectors = np.array(loaded_course_data["vector"].tolist())

def similarity(vec1, vec2):
    '''similarity(vec1, vec2) -> cosine similarity of vectors'''
    return 1 - cosine(vec1, vec2)

def recommend(user_input, rec_num=10, upperlvl=False, cmc=True, pomona=True, hmc=True, scripps=True, pitzer=True, other=True):
    query_vector = loaded_vectorizer.transform([user_input]).toarray().ravel()
    similarities = []
    for i in range(loaded_course_vectors.shape[0]):
        similarities.append(similarity(query_vector, loaded_course_vectors[i]))

    # get the indices of the most similar courses
    indices = np.argsort(similarities)[::-1]

    recommendations = []

    # create the table with the most similar courses and their details
    permited_colleges = []
    default_colleges = ["CM", "PO", "HM", "SC", "PZ"]
    if cmc:
        permited_colleges.append("CM")
    if pomona:
        permited_colleges.append("PO")
    if hmc:
        permited_colleges.append("HM")
    if scripps:
        permited_colleges.append("SC")
    if pitzer:
        permited_colleges.append("PZ")
    if other:
        permited_colleges.append("JP")
        permited_colleges.append("KS")
        permited_colleges.append("JM")
        permited_colleges.append("CH")
        permited_colleges.append("PPO")
        permited_colleges.append("AF")

    num_added_classes = 0
    for index in indices:
        course_code = loaded_course_data.iloc[index]["course_title"]
        course_college = re.search(r"(\w+)-", course_code).group(1)
        if (course_college not in permited_colleges):
            continue
        course_lvl = re.search(r"\d+", course_code).group(0)
        if (upperlvl and int(course_lvl) < 100):
            continue
        if(num_added_classes >= rec_num):
            break
        num_added_classes += 1
        similarity_score = similarities[index]
        course_details = {
            "title": loaded_course_data.iloc[index]["Name"],
            "description": loaded_course_data.iloc[index]["Description"],
            "prerequisites": "None",
            "instructor": "",
            "location": ""
        }
        recommendations.append((course_code, similarity_score, course_details))

    return recommendations

# table = recommend("machine")
# for row in table:
#     print(row)
