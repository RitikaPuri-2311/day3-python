# Group By Field
from itertools import groupby

Student = [
    {"name": "Riti", "dept": "Engineering"},
    {"name": "Tara", "dept": "MBA"},
    {"name": "Eshave", "dept": "Farmer"},
    {"name": "Salro", "dept": "Biker"},
    {"name": "Madhu", "dept": "BDE"},
]


def get_dept(student):
    return student["dept"]


Student.sort(key=get_dept)

grouped_Student = groupby(Student, key=get_dept)

for dept, group in grouped_Student:
    print(f"{dept}:")
    for person in group:
        print(f"  - {person['name']}")