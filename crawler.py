import requests
from bs4 import BeautifulSoup
import time
import csv
import json
import os
from tqdm import tqdm

class CourseCrawler:
    def __init__(self, config_path, batch_size=100):
        self.config = self.load_config(config_path)
        self.base_url = "https://xkcts.ucas.ac.cn:8443/course/courseplan/"
        self.login_url = "https://sep.ucas.ac.cn"
        self.session = requests.Session()
        self.batch_size = self.config['batch_size']
        self.range = (self.config['start'], self.config['end'])
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def load_config(self, path):
        with open(path, 'r') as f:
            config = json.load(f)
        return config

    def login(self):
        login_data = {
            'username': self.config['username'],
            'password': self.config['password'],
        }
        response = self.session.post(self.login_url, data=login_data)
        print(f"Login status code: {response.status_code}")
        if response.status_code == 200:
            print("Login successful.")
        else:
            print("Login failed.")
            exit()

    def fetch_course(self, course_id):
        url = self.base_url + str(course_id)
        try:
            response = self.session.get(url, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                mc_body = soup.find('div', {'class': 'mc-body'})
                if mc_body:
                    course_info = {'course_id': course_id, 'url': url}

                    # 提取课程名称
                    title_tag = mc_body.find('h4').find('p').find('strong')
                    course_info['课程名称'] = title_tag.text if title_tag else 'N/A'

                    # 提取课程编码、英文名称、课时、学分、课程属性、主讲教师
                    info_paragraph = mc_body.find_all('p')[1]
                    spans = info_paragraph.find_all('span')
                    for span in spans:
                        strong_tag = span.find('strong')
                        if strong_tag:
                            key = strong_tag.text.strip().replace('：', '')
                            value = span.text.replace(strong_tag.text, '').strip()
                            course_info[key] = value

                    # 提取 mc_body 内的所有 HTML 内容
                    course_info['详细内容'] = str(mc_body)

                    return course_info
        except requests.RequestException as e:
            print(f"Error fetching course {course_id}: {e}")
        return None

    def save_batch(self, batch, batch_number):
        filename = os.path.join(self.data_dir, f'course_plans_batch_{batch_number}.json')
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(batch, jsonfile, ensure_ascii=False, indent=4)

    def crawl(self):
        self.login()
        course_plans = []
        batch_number = 0

        for course_id in tqdm(range(self.range[0], self.range[1] + 1)):
            course_plan = self.fetch_course(course_id)
            if course_plan:
                course_plans.append(course_plan)

            if len(course_plans) >= self.batch_size:
                batch_number += 1
                self.save_batch(course_plans, batch_number)
                course_plans = []

        if course_plans:
            batch_number += 1
            self.save_batch(course_plans, batch_number)

        print("Crawling and storing completed.")
    