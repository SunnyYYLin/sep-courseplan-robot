from crawler import CourseCrawler
from reader import CourseReader
from viewer import HtmlViewer
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    # crawler = CourseCrawler('config.json', batch_size=200)eb
    # start_id = 0
    # end_id = 999999
    # crawler.crawl(start_id, end_id)
    app = QApplication(sys.argv)
    reader = CourseReader(data_dir='data')
    viewer = HtmlViewer(course_reader=reader)
    viewer.show()
    sys.exit(app.exec_())