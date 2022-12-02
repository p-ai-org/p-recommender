import pickle
from scipy import spatial
import math
import json

with open('description_embeddings.pickle', 'rb') as handle:
    description_embeddings = pickle.load(handle)

with open('id_to_title.pickle', 'rb') as handle:
    id_to_course_title = pickle.load(handle)

with open('title_to_ids.pickle', 'rb') as handle:
    title_to_ids = pickle.load(handle)

with open("./static/courses.json", "r") as courses_file:
    courses = json.load(courses_file)

# computers the average vector
def recommend(course_ids, rec_num = 10):
    '''
    Recommends courses similar to the ones in course_ids. Returns a list of of recomended course ids and their cosine similarities. Unlike the previous recomendation function, this one computes the average vector of the course_ids.
    course_ids: (list[str]) A list of course_ids.
    rec_num: (int) The number of recomendations to return.
    '''

    
    blacklisted = [] + course_ids
    for ci in course_ids:
        title = id_to_course_title[ci]
        course_ids_with_same_title = title_to_ids[title]
        blacklisted = blacklisted + course_ids_with_same_title

    
    def similarity(vec1, vec2):
        '''similarity(vec1, vec2) -> cosine similarity of vectors'''
        return 1 - spatial.distance.cosine(vec1,vec2)

    def closest_courses(vec):
        '''closest_courses(course_id) -> list of all courses and their cosine simililarity with course_id sorted by cosine similarity'''
        
        unsorted = [(course, similarity(vec, description_embeddings[course]),
                     [x for x in courses if x["identifier"] == course][0])
                     for course in description_embeddings.keys()
                    if course not in blacklisted]
        return sorted(unsorted, key = lambda w: w[1], reverse = True)

    def get_average_descripton_vec(course_ids):
        return sum([description_embeddings[c_id] for c_id in course_ids])/len(course_ids)
    
    average_vec =  get_average_descripton_vec(course_ids)
    return closest_courses(average_vec)[1:rec_num+1]

        

"""
# test cases
test_class1 = 'ARBC-140-CM'
linear_algebra = "MATH-073-HM"

wood = "ART-027-PO" 
phys = "PHYS-128-PO"

print(recommend([test_class1]))
print()
print(recommend([linear_algebra]))
print()
print(recommend([linear_algebra,test_class1]))
print()
print(recommend([linear_algebra],rec_num = 3))
print()
print(recommend([wood,phys],rec_num = 5))
"""
