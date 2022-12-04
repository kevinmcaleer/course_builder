import yaml
from course_builder.course import Course, Courses
import os
import json

c = Course()
c.read_course('source/micropython')

navigation = c.build_navigation()

print(navigation)

