import json
import os
from typing import List

class CourseReader:
    def __init__(self, data_dir="data", index_dir="index"):
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), data_dir)
        self.index_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), index_dir)
        self.course_index_file = os.path.join(self.index_dir, 'course_index.json')
        self.file_index_file = os.path.join(self.index_dir, 'file_index.json')
        self.course_index = {}
        self.file_index = {}
        self.load_indexes()

    def build_indexes(self) -> None:
        """Build and save course and file indexes."""
        course_index = {}
        file_index = {}
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.data_dir, filename)
                batch_number = int(filename.split('_')[-1].split('.')[0])
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data:
                        start_id = data[0]['course_id']
                        end_id = data[-1]['course_id']
                        file_index[batch_number] = {'start_id': start_id, 'end_id': end_id}
                        for course in data:
                            course_id = course['course_id']
                            course_code = course.get('课程编码', 'N/A')
                            course_name = course.get('课程名称', 'N/A')
                            course_index[course_id] = (course_code, course_name)
        # Sort indexes
        self.course_index = dict(sorted(course_index.items(), key=lambda item: item[0], reverse=True))
        self.file_index = dict(sorted(file_index.items(), key=lambda item: item[0], reverse=True))
        self.save_indexes()

    def save_indexes(self) -> None:
        """Save indexes to files."""
        os.makedirs(self.index_dir, exist_ok=True)
        with open(self.course_index_file, 'w', encoding='utf-8') as f:
            json.dump(self.course_index, f, ensure_ascii=False, indent=4)
        with open(self.file_index_file, 'w', encoding='utf-8') as f:
            json.dump(self.file_index, f, ensure_ascii=False, indent=4)
        print("Indexes saved.")

    def load_indexes(self) -> None:
        """Load indexes from files."""
        if os.path.exists(self.course_index_file):
            with open(self.course_index_file, 'r', encoding='utf-8') as f:
                self.course_index = json.load(f)
        else:
            self.build_indexes()
        print(f"{len(self.course_index)} courses loaded.")
        if os.path.exists(self.file_index_file):
            with open(self.file_index_file, 'r', encoding='utf-8') as f:
                self.file_index = json.load(f)
        else:
            self.build_indexes()
        print("Indexes loaded.")

    def get_course_by_id(self, course_id:int) -> dict|None:
        """Get course details by course ID."""
        for batch_number, id_range in self.file_index.items():
            if int(id_range['start_id']) <= int(course_id) <= int(id_range['end_id']):
                filepath = os.path.join(self.data_dir, f'course_plans_batch_{batch_number}.json')
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for course in data:
                        if course['course_id'] == course_id:
                            return course
        print(f"Course {course_id} not found.")
        return None

    def list_courses(self) -> List[tuple[int, str, str]]:
        """Return a list of course IDs and names."""
        return [(course_id, course[0], course[1]) for course_id, course in self.course_index.items()]
