import pickle
from scipy import spatial
import math
import json
import re

with open("./static/courses.json", "r") as courses_file:
    courses = json.load(courses_file)

folder = "recommend_GloVe/"
with open(folder+'desc embed unweighted.pickle', 'rb') as handle:
    compatible_courses = [x["identifier"] for x in courses]
    description_embeddings = pickle.load(handle)
    description_embeddings = {key : value for key, value in description_embeddings.items() if key in compatible_courses}

with open(folder+'id_to_title.pickle', 'rb') as handle:
    id_to_course_title = pickle.load(handle)

with open(folder+'title_to_ids.pickle', 'rb') as handle:
    title_to_ids = pickle.load(handle)




def get_course_id_num(course_id):
    return int(re.findall("\d\d*",re.findall("-\d*.?.?-",course_id)[0])[0])

def get_average_course_id_num(course_id_list):
    return sum([get_course_id_num(course_id) for course_id in course_id_list])/len(course_id_list)


def get_lowerdiv_and_lower_level_course_ids(course_list, reference_num):
    '''
    Returns all of the course_ids that are less than a refference number and less than 100.
    '''
    return list(filter(lambda course_id:  get_course_id_num(course_id) < min(100,reference_num), course_list ))

# computers the average vector
def recommend(course_ids, rec_num = 10, blacklist_lowerlevel = True):
    '''
    Recommends courses similar to the ones in course_ids. Returns a list of of recomended course ids and their cosine similarities.
    Unlike the previous recomendation function, this one computes the average vector of the course_ids.
    course_ids: (list[str]) A list of course_ids.
    rec_num: (int) The number of recomendations to return.
    '''

    
    blacklisted = [] + course_ids
    for ci in course_ids:
        title = id_to_course_title[ci]
        course_ids_with_same_title = title_to_ids[title]
        blacklisted = blacklisted + course_ids_with_same_title


    if blacklist_lowerlevel:
        ref_num = get_average_course_id_num(course_ids)
        all_course_ids = description_embeddings.keys()
        blacklisted += get_lowerdiv_and_lower_level_course_ids(all_course_ids,ref_num )
        
    
    def similarity(vec1, vec2):
        '''similarity(vec1, vec2) -> cosine similarity of vectors'''
        return 1 - spatial.distance.cosine(vec1,vec2)

    def closest_courses(vec):
        '''closest_courses(course_id) -> list of all courses and their cosine simililarity with course_id sorted by cosine similarity'''
        unsorted = [(course, round(similarity(vec, description_embeddings[course]),2)  ,
                     [x for x in courses if x["identifier"] == course][0])
                     for course in description_embeddings.keys()
                    if course not in blacklisted]
        return sorted(unsorted, key = lambda w: w[1], reverse = True)

    def get_average_descripton_vec(course_ids):
        return sum([description_embeddings[c_id] for c_id in course_ids])/len(course_ids)
    
    average_vec =  get_average_descripton_vec(course_ids)
    return closest_courses(average_vec)[:rec_num+1]

        

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
