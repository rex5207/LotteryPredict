from bs4 import BeautifulSoup
import time
import re
from urllib.request import urlopen
import ssl
import datetime

HISTORY_FILE = "../data/Superlotto.csv"
URL = "https://www.pilio.idv.tw/lto/list.asp?indexpage="
TOTAL_NUM = 38
SELET_NUM = 2

class Superlotto:

    def __init__(self, result_type = "top"):
        self.lottery_list = []
        self.arrDays = []
        self.arrTimes = []

    def write_data_to_file(self, pagenum):
        for pagenum in range(1, pagenum + 1):
            self.get_data_from_webpage(pagenum)

        print("Write history results to local file...")
        f = open(HISTORY_FILE, 'w')
        for lottery in self.lottery_list:
            f.write(lottery["date"] + " ")
            f.writelines(','.join(map(str, lottery["numbers"])))
            f.write('\n')
        f.close
        print("Finish.\n")

    def get_data_from_file(self):
        print("Read history results from local file...")
        f = open(HISTORY_FILE, 'r')
        for line in f.readlines():
            line = line.strip().split()
            numbers = line[1].split(",")
            numbers = list(map(int, numbers))
            data = {
                "date": line[0],
                "numbers": numbers
            }
            self.lottery_list.append(data)
        print("Finish.\n")
        print("*There are total of %d history data.\n" % len(self.lottery_list))

    def get_data_from_webpage(self, page_num):
        print("Get data from website...Page" + str(page_num))
        # disable ssl certificate verify
        ssl._create_default_https_context = ssl._create_unverified_context
        response = urlopen(URL + str(page_num))
        html = response.read()

        soup = BeautifulSoup(html, "html.parser")
        history = soup.find('table', 'auto-style1')
        content = history.find_all('td')

        # 將內容改成3-tuple, data/number/space, 並跳過第一欄說明欄
        content = zip(*[content[3:][i::3] for i in range(3)])
        for result in content:
            date = result[0].text
            numbers = (result[1].text).strip().split(",")
            numbers = list(map(int, numbers))
            data = {
                "date": date[:-3],
                "numbers": numbers
            }
            self.lottery_list.append(data)

    def dfs_all_numbers(self, nums, n_cur):
        if len(nums) < SELET_NUM:
            for i in range(n_cur + 1, TOTAL_NUM + 1):
                nums.append(i)
                self.dfs_all_numbers(nums, i)
                nums.pop()
        elif len(nums) == SELET_NUM:
            self.calculate_longest_day(nums)
            self.calculate_most_times(nums)
            self.print_result()
    
    # 多久沒有中獎了
    def calculate_longest_day(self, nums):
        days = 0
        for data in self.lottery_list:
            results = data["numbers"]
            if set(nums).issubset(set(results)):
                break
            else:
                days += 1
        self.get_days_top5(nums, days)
    
    # 出現過幾次
    def calculate_most_times(self, nums):
        times = 0
        for data in self.lottery_list:
            results = data["numbers"]
            if set(nums).issubset(set(results)):
                times += 1
        self.get_times_top5(nums, times)

    # 最長天數Top5
    def get_days_top5(self, nums, days):
        self.arrDays.append((days, nums.copy()))
        self.arrDays = sorted(self.arrDays, reverse=True)
        if len(self.arrDays) > 5:
            self.arrDays.pop()

    # 最多次數Top5
    def get_times_top5(self, nums, times):
        self.arrTimes.append((times, nums.copy()))
        self.arrTimes = sorted(self.arrTimes, reverse=True)
        if len(self.arrTimes) > 5:
            self.arrTimes.pop()

    def print_result(self):
        # Clear terminal
        print('\x1b[2J')
        print("============== Top 5 Days================")
        for index, x in enumerate(self.arrDays):
            day = x[0]
            nums = x[1]
            print("Top %d" % (index + 1))
            print("In sequence [%s]" % ','.join(map(str, nums)))
            print("Total: %d days didn't show up." % (day))
        
        print("============== Top 5 Times================")
        for index, x in enumerate(self.arrTimes):
            times = x[0]
            nums = x[1]
            print("Top %d" % (index + 1))
            print("In sequence [%s]" % ','.join(map(str, nums)))
            print("Total: %d times show up." % (times))
