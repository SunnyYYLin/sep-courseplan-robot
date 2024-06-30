from crawler import CourseCrawler
from reader import CourseReader
from viewer import HtmlViewer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
import sys
import json
import os

if __name__ == '__main__':
    work_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(work_dir, 'config.json')
    with open(config_dir, 'r') as f:
        config = json.load(f)
        
    if config['mode'] == 'crawl':
        crawler = CourseCrawler('config.json')
        crawler.crawl()
    elif config['mode'] == 'query':
        app = QApplication(sys.argv)
        font = QFont()
        font.setPointSize(config['font_size'])
        app.setFont(font)
        reader = CourseReader()
        viewer = HtmlViewer(course_reader=reader)
        viewer.show()
        sys.exit(app.exec_())
    else:
        print("Invalid mode in config.json.")