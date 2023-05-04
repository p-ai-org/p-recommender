import requests, os, csv
from dotenv import load_dotenv
import pandas as pd

# Creates list of all course areas offered at the 5Cs

courseareas = requests.get(f'http://jicsweb.pomona.edu/api/courseareas')
coursedict = {}
for codes in courseareas.json():
	coursedict.update({codes['Code']: codes['Description']})


# Generates url for all valid course areas of this semester and returns json

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
valid = {}
for code in coursedict.keys():
	if reqCourseInfo(code) is not None:
		valid[code] = coursedict[code]


# Writing data to CSV

header = ['Course Area', 'CourseCode', 'Name', 'Course Description', 'Faculty', 'Campus', 'MeetTime', 'Weekdays', 'Prerequisites']

with open('courses.csv', 'w', encoding='UTF8', newline='') as f:
	writer = csv.writer(f)
	writer.writerow(header)
	for current in valid:
		for course in reqCourseInfo(current):
			try:
				CourseArea = valid[current]
				CourseCode = course['CourseCode']
				Name = course['Name']
				Description = course['Description']
				Faculty = []
				reqs = Description.find("Prerequisite:")
				reqs1 = Description.find("Prerequisites:")
				if reqs != -1:
					Prerequisites = Description[reqs + len("Prerequisite:"):]
				elif reqs1 != -1:
					Prerequisites = Description[reqs1 + len("Prerequisites:"):]
				else:
					Prerequisites = 'None'
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
			data = [CourseArea, CourseCode, Name, Description, Faculty, Campus, MeetTime, Weekdays, Prerequisites]
			writer.writerow(data)

df = pd.read_csv('courses.csv')
duplicates = df.loc[df.duplicated(subset=['CourseCode'], keep=False), :]
print("duplicates=", duplicates)
for idx, row in duplicates.groupby('CourseCode')['Course Area']:
    concat = ', '.join(row.values)
    df.loc[df['CourseCode'] == idx, 'Course Area(s)'] = concat
    df.drop_duplicates(subset=['CourseCode'], keep='first', inplace=True)

df.drop('Course Area', axis=1, inplace=True)
df.to_csv('courses.csv', index=False)
