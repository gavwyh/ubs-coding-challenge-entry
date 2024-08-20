"""
Assumptions: 
1. If a student has the same weightage score to any schools, the student will be allocated to the smallest indexed school
2. Sorting takes place in O(1) memory, which is better than heap construction O(students) memory due to O(n^2) time bottleneck of checking each student
"""
import json
import sys
from enum import Enum

class School:
    def __init__(self, name, location, maxAllocation):
        self.name = name
        self.location = location
        self.maxAllocation = maxAllocation

class Student:
    def __init__(self, id, homeLocation, alumni=None, volunteer=None):
        self.id = id
        self.homeLocation = homeLocation
        self.alumni = alumni
        self.volunteer = volunteer

class WeightageCriteria(Enum):
    DISTANCE = 0.5
    ALUMNI = 0.3
    VOLUNTEER = 0.2

if len(sys.argv) != 2:
    raise ValueError("Invalid argument length, ensure command syntax is as follows: <path to python bin> main.py input.json")

filename = sys.argv[1]
if filename != "input.json":
    raise ValueError("Invalid file name, ensure filename is of input.json, got=" + filename)

with open(filename, 'r') as file:
    jsonData = json.load(file)
    schools = []
    students = []

    for school in jsonData["schools"]:
        schools.append(School(school["name"], school["location"], school["maxAllocation"]))
    
    for student in jsonData["students"]:
        students.append(Student(student["id"], student["homeLocation"], student.get("alumni"), student.get("volunteer")))
    
    allocated = set()
    output = []

    for school in schools:
        weightageScores = []
        allocations = {}

        for student in students:
            id = student.id
            # skip students alr enrolled into a school
            if id in allocated:
                continue

            weightageScore = 0.0
            # calculate score based on euclidean distance + alumni + volunteer
            weightageScore += (((student.homeLocation[0] - school.location[0]) ** 2) + ((student.homeLocation[1] - school.location[1]) ** 2) ** 0.5) * WeightageCriteria.DISTANCE.value
            weightageScore += WeightageCriteria.ALUMNI.value if student.alumni == school.name else 0.0
            weightageScore += WeightageCriteria.VOLUNTEER.value if student.volunteer == school.name else 0.0

            weightageScores.append((weightageScore, id))

        weightageScores.sort(key= lambda x:(x[0], x[1]))

        allocatedStudents = []
        for i in range(school.maxAllocation):
            allocatedStudents.append(weightageScores[i][1])
            allocated.add(weightageScores[i][1])

        allocations[school.name] = allocatedStudents
        output.append(allocations)

    with open("output.json", 'w') as outputFile:
        json.dump(output, outputFile)
