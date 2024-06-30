from crawler import CourseCrawler
from reader import CourseReader
from viewer import HtmlViewer
from PyQt5.QtWidgets import QApplication
import sys
import json

if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)
        
    if config['mode'] == 'crawl':
        crawler = CourseCrawler('config.json')
        crawler.crawl()
    elif config['mode'] == 'query':
        app = QApplication(sys.argv)
        reader = CourseReader(data_dir='data')
        viewer = HtmlViewer(course_reader=reader)
        viewer.show()
        sys.exit(app.exec_())
    else:
        print("Invalid mode in config.json.")