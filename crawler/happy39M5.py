from bs4 import BeautifulSoup
import time
import re
from urllib.request import urlopen
import ssl
import datetime


class Happy39:

    def __init__(self):
        self.lottery_list = []
        self.top5 = []
        self.temp = []

    def get_history_from_page(self, indexpage):
            # disable ssl certificate verify
        ssl._create_default_https_context = ssl._create_unverified_context
        url = 'https://www.lotto-8.com/server/lto539/serverD/listlto539.asp?indexpage=' + \
            str(indexpage) + '&orderby=old'
        response = urlopen(url)
        html = response.read()

        soup = BeautifulSoup(html, "html.parser")
        history = soup.find('table', 'auto-style4')
        content = history.find_all('td')

        # 將內容改成3-tuple, data/number/space, 並跳過第一欄說明欄
        content = zip(*[content[3:][i::3] for i in range(3)])
        for result in content:
            date = result[0].text
            numbers = (result[1].text).strip().split(",")
            numbers = list(map(int, numbers))
            data = {
                "date": date,
                "numbers": numbers
            }
            self.lottery_list.append(data)

    def write_numbers_to_file(self, pagenum):
        print("\nGet data from website...")
        for pagenum in range(1, pagenum + 1):
            self.get_history_from_page(pagenum)
        print("\nWrite history results to local file...")
        f = open("lottery_numbers.txt", 'w')
        for lottery in self.lottery_list:
            f.write(lottery["date"] + " ")
            f.writelines(','.join(map(str, lottery["numbers"])))
            f.write('\n')
        f.close
        print("Finish.\n")

    def read_numbers_to_file(self):
        print("\nRead history results from local file...")
        f = open("lottery_numbers.txt", 'r')
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
        print("*There are total of %d history data.\n" %
              len(self.lottery_list))

    def dfs_all_numbers(self, n_cur):
        if(len(self.temp) < 3):
            for i in range(n_cur + 1, 40, 1):
                self.temp.append(i)
                self.dfs_all_numbers(i)
            if(len(self.temp) > 0):
                self.temp.pop()
        else:
            fail_times = self.check_fail_times(self.temp)
            win_times = self.check_win_times(self.temp)
            self.get_top5(fail_times, win_times, self.temp)
            self.temp.pop()

    # 找出已經幾次沒中獎了
    def check_fail_times(self, mynum):
        fail_times = 0
        for data in reversed(self.lottery_list):
            history_num = data["numbers"]
            if(self.isWin(mynum, history_num) is True):
                return fail_times
            else:
                fail_times += 1
        return fail_times

    # 找出從以前到現在總共中獎幾次
    def check_win_times(self, mynum):
        win_times = 0
        for data in self.lottery_list:
            history_num = data["numbers"]
            if(self.isWin(mynum, history_num) is True):
                win_times += 1
        return win_times

    def isWin(self, mynum, history_num):
        n = 0
        for num in mynum:
            if(num in history_num):
                n += 1
        return (n >= 2)

    def get_top5(self, fail_times, win_times, mynumbers):
        if(len(self.top5) < 5):
            self.top5.append((fail_times, win_times, mynumbers.copy()))
            self.top5 = sorted(self.top5, reverse=True)
        else:
            min_reward = self.top5[4][0]
            if(fail_times > min_reward):
                self.top5.pop()
                self.top5.append((fail_times, win_times, mynumbers.copy()))
                self.top5 = sorted(self.top5, reverse=True)

    
    def show_top5(self):
        print("============== Top 5 ================")
        for index, x in enumerate(self.top5):
            fail_times = x[0]
            win_times = x[1]
            top_numbers = x[2]
            print("Top %d" % (index + 1))
            print("In sequence [%s]" % ','.join(map(str, top_numbers)))
            print("Total: There are totally %d failed times." % (fail_times))
            print("Average: It will win in every %d times." %
                  (len(self.lottery_list)/win_times))
