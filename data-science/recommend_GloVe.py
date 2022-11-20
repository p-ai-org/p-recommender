import pickle
from scipy import spatial

with open('C:\Users\Sophia Ristuben\Documents\GitHub\p-recommender\data-science\description_embeddings.pickle', 'rb') as handle:
    description_embeddings = pickle.load(handle)

# recommend(user_input) -> return [{id, sim}]
# user_input can be an id or list of ids 


def recommend(user_input):
    def similarity(user_input, reference):
        return 1 - spatial.distance.cosine(description_embeddings[user_input.upper()], description_embeddings[reference])  

    def closest_courses(user_input):
        unsorted = [ (course, similarity(user_input, course))
                    for course in description_embeddings.keys()]
        return sorted(unsorted, key = lambda w: w[1], reverse = True)
    
    if type(user_input) == str:
        if not (user_input in description_embeddings):
            raise ValueError("user_input must be a valid id")
        return closest_courses(user_input)[1:11]
    elif type(user_input) == list:
        unsorted = []
        for ui in user_input:
            if ui in description_embeddings:
                unsorted += closest_courses(ui)[1:6]

        if len(unsorted) < 2:
            raise ValueError("At least two id in user_input must be valid id")
        return sorted(unsorted, key = lambda w: w[1], reverse = True)[:10]
    else:
    	raise ValueError("user_input must be a string or list of strings")

# test cases
test_class1 = 'ARBC-140-CM'
linear_algebra = "MATH-073-HM"


print(recommend(test_class1))
print()
print(recommend(linear_algebra))
print()
print(recommend([linear_algebra,test_class1]))