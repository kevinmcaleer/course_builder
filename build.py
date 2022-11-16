# Course Builder
# Kevin McAleer
# October 2022

import yaml
from course import Course, Courses
import os

# copy the build files to the /learn folder for Jekyll to build

courses = Courses()
courses.read_courses('source')
print(courses.output_yml('data'))

courses.build()
