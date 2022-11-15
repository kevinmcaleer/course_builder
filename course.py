# Course Builder - course class
# Kevin McAleer
# October 2022

import os
import yaml
import ast

class Course():
    name = ""
    description = ""
    author = ""
    date_created = ""
    date_published = ""
    content = []
    layout = ""
    type = "page"
    links = []
    output = ""
    output_folder = "build"
    course_folder = ""
    content = []
    level = 'beginner'

    def __init__(self, name=None, description=None, author=None, 
                 date_created=None, date_published=None, 
                 content=None, layout=None, type=None, 
                 links=None, output=None, output_folder=None, course_folder=None):
        if name: self.name = name
        if description: self.description = description
        if author: self.author = author
        if date_created: self.date_created = date_created
        if date_published: self.date_published = date_published
        if content: self.content = content
        if layout: self.layout = layout
        if type: self.type = type
        if links: self.links = links
        if output: 
            self.output = output
        else:
            self.output = "nav.html"
        if output_folder: 
            self.output_folder = output_folder
        else:
            self.output_folder = "learn/micropython"
        if course_folder: self.course_folder = course_folder
        
        

    def read_course(self, course_folder):
        self.course_folder = course_folder
        with open(f'{course_folder}/course.yml', 'r') as stream:
            try:
                course=yaml.safe_load(stream)
                print(f'Course manifest loaded')
            except yaml.YAMLError as exc:
                print(exc)
        
        course = course[0]
        self.author = course['author']
        self.name = course['name']
        self.description = course['description']
        self.date_created = course['date_created']
        self.date_published = course['date_published']
        self.content = course['content']
        print(course['content'])
        print(f'found {self.no_of_lessons} lessons')
        return self

    def create_output(self, output_folder=None):
        """ Build the course """
        print(f'Building course: {self.name}')
        
        # Create the course folder
        if output_folder: self.output_folder = output_folder
        print("creating output folder: ", self.output_folder)
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def __str__(self):
        return f'Course name: {self.name}, with {self.no_of_lessons} lessons, layout is: {self.layout}'

    @property
    def no_of_lessons(self):
        # loop through the sections and count the number of lessons within each section
        count = 0
        for i in self.content:
            for _ in i['section']['content']:
                count += 1
        return count

    @staticmethod
    def find_nth(haystack:str, needle:str, n:int)->int:
        start = haystack.find(needle)
        while start >= 0 and n > 1:
            start = haystack.find(needle, start+len(needle))
            n -= 1
        return start

    def update_front_matter(self, lesson_file, front_matter):
        
        # read the lesson file, find the front matter makers and remove them
        lesson_list = lesson_file.split('---', 2) # splits the string into 3 parts

        l = yaml.load(lesson_list[1], Loader=yaml.FullLoader)
        print(f'l is {l}')

        # should now have atleast 3 sections
        # 1 is empty
        # 2 is the front matter
        # 3 is the content

        content = lesson_list[2]
        
        front_matter_list = front_matter.split('---', 2) # splits the string into 3 parts
        f = yaml.load(front_matter_list[1], Loader=yaml.FullLoader)
        print(f'f is: {f}')

        # merge the existing front matter with the new front matter

        merged_frontmatter = f
        merged_frontmatter.update(l)

        merged_frontmatter = yaml.dump(merged_frontmatter, sort_keys=False)

        page = "---\n" + merged_frontmatter + "---\n" + content
        return page

    def build(self):
        """ Build the front matter for each content page, and output to the build folder """

        # Create the front matter that is used to build the page navigation and previous, next buttons
        self.create_output(self.output_folder)
        lesson = ""
        lesson += "<nav>" + "\n"
        if len(self.content) == 0:
            print("no content found")
            return
        for section in self.content:
            # Each section has a name and a content list of items
            print(f'section is: {section}')
            just_item = section['section']

            #  for each item in the content section 
            for item in just_item['content']:
                index = just_item['content'].index(item)
                item_count = len(just_item['content'])
                print(f'item is: {item}, index is {index}, total is {item_count}')
           
                if index == 0:
                    # first item
                    previous = ""
                    if index < item_count-1:
                        next = just_item['content'][index+1]
                    else:
                        next = ""
                    
                if index == item_count-1:
                    # last item
                    next = ""
                    previous = ""
                    if item_count > 0:
                        previous = just_item['content'][index-1]
                    
                
                    front_matter = f'---' + "\n"
                    front_matter += f'layout: {self.layout}' + "\n"
                    front_matter += f'title: {item}' + "\n"
                    front_matter += f'type: {self.type}' + "\n"
                    front_matter += f'previous: {previous}' + "\n"
                    front_matter += f'next: {next}' + "\n"
                    front_matter += f'description: {self.description}' + "\n"
                    front_matter += f'---' + "\n"
                
                    # update front matter
                    lesson_file = f'{self.course_folder}/{item}'
                    with open(lesson_file, 'r') as f:
                        print(f'reading {lesson_file}')
                        lines = f.read()
                        # print(f'lines is: {lines}')
                    page = self.update_front_matter(lesson_file=lines, front_matter=front_matter)

                    print(f'{page}')

                    # write the file
                    print(f'writing file: {self.output_folder}/{item}')
                    with open(f'{self.output_folder}/{item}', 'w') as build_file:
                        build_file.writelines(page)
                    
        return lesson
    def __str__(self):
        """ provide a list of information for to build the courses.yml data file """
        return {'description':self.description,'name':self.name}


class Courses():
    course_list = [Course()]

    def __init__(self, data=None):
        if data: self.course_list = data

    def read_courses(self, course_folder):
        """ Read all the courses in the course folder """

        new_course = Course()
        for course in os.listdir(course_folder):
            if os.path.isdir(os.path.join(course_folder, course)):
                print(f'Found course: {course}')
                new_course.read_course(os.path.join(course_folder, course))
                self.course_list.append(new_course)
        return self

    def output_yml(self, output_folder):
        """ Output the course data to a yml file """

        # check if folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        with open(f'{output_folder}/courses.yml', 'w') as outfile:

            c = []
            for course in self.course_list:
                c.append(course.__str__())

            yaml.safe_dump(c, outfile, default_flow_style=False)
        
    def build(self):
        """ Build the courses """
        
        for course in self.course_list:
            course.build()
    