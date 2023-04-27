import requests, os, csv
from dotenv import load_dotenv
import pandas as pd

# Creates list of all course areas offered at the 5Cs

courseareas = requests.get(f'http://jicsweb.pomona.edu/api/courseareas')
coursecodes = []
for codes in courseareas.json():
        coursecodes.append(codes['Code'])


# Generates url for all valid course areas of this semester

def reqCourseInfo(code):
	payload = {}
	load_dotenv()
	api_key = os.environ.get("API_KEY", None)
	payload["api_key"]=api_key
	r = requests.get("https://jicsweb.pomona.edu/api/Courses/2023;FA/" + code, params = payload)
	try:
		return r.json()
	except:
		print(f"No courses offered in course area {code} this semester")



# Calling above function to get all valid course areas this current semester
valid = []
for code in coursecodes:
	if reqCourseInfo(code) is not None:
		valid.append(code)

# Writing data to CSV

header = ['CourseCode', 'Name', 'Description', 'Faculty', 'Campus', 'MeetTime', 'Weekdays']

with open('courses.csv', 'w', encoding='UTF8', newline='') as f:
	writer = csv.writer(f)
	writer.writerow(header)
	for course in valid:
		courseInfo = reqCourseInfo(course)
		for course in courseInfo:
			try:
				CourseCode = course['CourseCode']
				Name = course['Name']
				Description = course['Description']
				Faculty = []
				if len(course['Instructors']) == 1:
					Faculty = course['Instructors'][0]['Name']
					if Faculty == ', taff':
						Faculty = 'Staff'
				else:
					for instructor in course['Instructors']:
						if instructor['Name'] == ', taff':
							Faculty.append('Staff')
						else:
							Faculty.append(instructor['Name'])
				Campus = []
				MeetTime = []
				Weekdays = []
				if len(course['Schedules']) == 1:
					Campus = course['Schedules'][0]['Campus']
					MeetTime = course['Schedules'][0]['MeetTime']
					Weekdays = course['Schedules'][0]['Weekdays']
				else:
					for schedule in course['Schedules']:
						Campus.append(schedule['Campus'])
						MeetTime.append(schedule['MeetTime'])
						Weekdays.append(schedule['Weekdays'])
			except:
				print("Insufficient information on course")
			data = [CourseCode, Name, Description, Faculty, Campus, MeetTime, Weekdays]
			writer.writerow(data)

df = pd.read_csv('courses.csv')
newdf = df.drop_duplicates()
newdf.to_csv('updatedcoursecatalog.csv', index=False)
