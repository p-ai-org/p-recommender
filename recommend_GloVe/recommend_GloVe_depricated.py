import pickle
from scipy import spatial
import math

with open('description_embeddings.pickle', 'rb') as handle:
    description_embeddings = pickle.load(handle)

def get_course_id_num(course_id):
    return int(re.findall("\d\d*",re.findall("-\d*.?.?-",course_id)[0])[0])


"""course_id1 < course_id2"""
def is_lowerdiv_and_lower_level(course_id1,course_id2):
    
    num1 = get_course_id_num(course_id1)
    num2 = get_course_id_num(course_id2)
    if num < 100:
        return num1 < num2
    else:
        return False

def recommend(course_ids, rec_num = 10, drop_lowerdiv_if_lower_level= False):
    '''
    Recommends courses similar to the ones in course_ids. Returns a list of of recomended course ids and their cosine similarities.
    course_ids: (list[str]) A list of course_ids.
    rec_num: (int) The number of recomendations to return.
    '''
    def similarity(course_id1, course_id2):
        '''similarity(course_id1, course_id2) -> cosine similarity of the course description '''
        return 1 - spatial.distance.cosine(description_embeddings[course_id1.upper()], description_embeddings[course_id2])  

    def closest_courses(course_id):
        '''closest_courses(course_id) -> list of all courses and their cosine simililarity with course_id sorted by cosine similarity'''
        if drop_lowerdiv_if_lower_level:
        unsorted = [ (course, similarity(course_id, course))
                    for course in description_embeddings.keys()]
        return sorted(unsorted, key = lambda w: w[1], reverse = True)

    recs_per_course = math.ceil(rec_num/len(course_ids))
    results = []
    for id in course_ids:
        if id not in description_embeddings:
            raise ValueError("course_ids must contain only valid_ids")
        results += closest_courses(id)[1:recs_per_course+1]

    return sorted(results, key = lambda w: w[1], reverse = True)[:rec_num]

        


# test cases
test_class1 = 'ARBC-140-CM'
linear_algebra = "MATH-073-HM"


print(recommend([test_class1]))
print()
print(recommend([linear_algebra]))
print()
print(recommend([linear_algebra,test_class1]))
print()
print(recommend([linear_algebra],rec_num = 3))
