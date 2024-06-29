import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt

class HtmlViewer(QMainWindow):
    def __init__(self, course_reader):
        super().__init__()
        self.course_reader = course_reader

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Course Reader')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.course_list = QListWidget()
        self.course_list.itemClicked.connect(self.display_course)
        self.layout.addWidget(self.course_list)

        self.html_viewer = QTextEdit()
        self.html_viewer.setReadOnly(True)
        self.layout.addWidget(self.html_viewer)

        self.load_courses()

    def load_courses(self):
        courses = self.course_reader.list_courses()
        for course_id, course_name in courses:
            item = QListWidgetItem(f"{course_id} - {course_name}")
            item.setData(Qt.UserRole, course_id)
            self.course_list.addItem(item)

    def display_course(self, item):
        course_id = item.data(Qt.UserRole)
        course = self.course_reader.get_course_by_id(course_id)
        if course:
            self.html_viewer.setHtml(course.get('详细内容', '内容未找到'))