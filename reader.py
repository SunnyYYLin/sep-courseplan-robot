import json
import os

class CourseReader:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.index = self.build_index()

    def build_index(self):
        """Build an index of course IDs to their respective JSON files."""
        index = {}
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.data_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for course in data:
                        course_id = course['course_id']
                        index[course_id] = filepath
        return index

    def get_course_by_id(self, course_id):
        """Get course details by course ID."""
        filepath = self.index.get(course_id)
        if filepath:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for course in data:
                    if course['course_id'] == course_id:
                        return course
        return None

    def list_courses(self):
        """Return a list of course IDs and names."""
        course_list = []
        for course_id in self.index:
            course = self.get_course_by_id(course_id)
            if course:
                course_list.append((course_id, course.get('课程名称', 'N/A')))
        return course_list