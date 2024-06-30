import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QLineEdit, QLabel, QHBoxLayout, QSplitter
from PyQt5.QtCore import Qt
from reader import CourseReader
from typing import List

class HtmlViewer(QMainWindow):
    def __init__(self, course_reader: CourseReader) -> None:
        super().__init__()
        self.course_reader = course_reader
        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle('Course Reader')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Search boxes
        self.code_search_box = QLineEdit()
        self.code_search_box.setPlaceholderText('Search by Course Code')
        self.code_search_box.textChanged.connect(self.filter_courses)

        self.name_search_box = QLineEdit()
        self.name_search_box.setPlaceholderText('Search by Course Name')
        self.name_search_box.textChanged.connect(self.filter_courses)

        self.search_layout = QHBoxLayout()
        self.search_layout.addWidget(QLabel("Search by Code:"))
        self.search_layout.addWidget(self.code_search_box)
        self.search_layout.addWidget(QLabel("Search by Name:"))
        self.search_layout.addWidget(self.name_search_box)
        self.layout.addLayout(self.search_layout)

        # Course list
        self.course_list = QListWidget()
        self.course_list.itemClicked.connect(self.display_course)

        # HTML viewer
        self.html_viewer = QTextEdit()
        self.html_viewer.setReadOnly(True)

        # Splitter to make course list and HTML viewer adjustable
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.course_list)
        self.splitter.addWidget(self.html_viewer)

        self.layout.addWidget(self.splitter)

        self.load_courses()

    def load_courses(self) -> None:
        self.courses = self.course_reader.list_courses()
        self.display_courses(self.courses)

    def display_courses(self, courses: List[tuple[int, str, str]]) -> None:
        self.course_list.clear()
        for course_id, course_code, course_name in courses:
            item = QListWidgetItem(f"{course_id} - {course_code} - {course_name}")
            item.setData(Qt.UserRole, course_id)
            self.course_list.addItem(item)

    def filter_courses(self) -> None:
        code_search_text = self.code_search_box.text().strip().lower()
        name_search_text = self.name_search_box.text().strip().lower()

        filtered_courses = []
        for course_id, course_code, course_name in self.courses:
            if code_search_text in course_code.lower() and name_search_text in course_name.lower():
                filtered_courses.append((course_id, course_code, course_name))
        self.display_courses(filtered_courses)

    def display_course(self, item) -> None:
        course_id = int(item.data(Qt.UserRole))
        course = self.course_reader.get_course_by_id(course_id)
        if course:
            self.html_viewer.setHtml(course.get('详细内容', '内容未找到'))