from bs4 import BeautifulSoup
import time
import re
from urllib.request import urlopen
import ssl
import datetime

class Daily539:

    def __init__(self, result_type = "top"):
        self.lottery_list = []
        self.rate5 = []
        self.top5 = []
        self.suck5 = []
        self.temp = []
        self.result_type = result_type


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
        print("*There are total of %d history data.\n" % len(self.lottery_list))


    def get_rewards_from_rules(self, n_win):
        if(n_win < 2):
            return 0
        elif(n_win == 2):
            return 50
        elif(n_win == 3):
            return 300
        elif(n_win == 4):
            return 20000
        elif(n_win == 5):
            return 8000000


    def get_rewards_from_history_data(self, mynumbers):
        final_reward = 0
        final_wins = 0
        for data in self.lottery_list:
            results = data["numbers"]
            n_win = 0
            for num in mynumbers:
                if(num in results):
                    n_win += 1
            if(n_win == 5):
                return -1, 0
            final_reward += self.get_rewards_from_rules(n_win)
            if(n_win >= 2):
                final_wins += 1
        return final_reward, final_wins


    def dfs_all_numbers(self, n_cur):
        if(len(self.temp) < 5):
            for i in range(n_cur + 1, 40, 1):
                self.temp.append(i)
                self.dfs_all_numbers(i)
            if(len(self.temp) > 0):
                self.temp.pop()
        else:
            self.show_results(self.temp)
            self.temp.pop()

    def show_results(self, mynumbers):
        final_reward, final_wins = self.get_rewards_from_history_data(
            mynumbers)
        if(final_reward is not -1):
            if(self.result_type == "top"):
                self.get_top5(final_reward, mynumbers)
            elif(self.result_type == "suck"):
                self.get_suck5(final_reward, mynumbers)
            else:
                self.get_rate5(final_wins, mynumbers)


    def get_rate5(self, final_wins, mynumbers):
        if(len(self.rate5) < 5):
            self.rate5.append((final_wins, mynumbers.copy()))
            self.rate5 = sorted(self.rate5, reverse=True)
            self.show_rate5()
        else:
            min_reward = self.rate5[4][0]
            if(final_wins > min_reward):
                self.rate5.pop()
                self.rate5.append((final_wins, mynumbers.copy()))
                self.rate5 = sorted(self.rate5, reverse=True)
                self.show_rate5()


    def get_top5(self, final_reward, mynumbers):
        if(len(self.top5) < 5):
            self.top5.append((final_reward, mynumbers.copy()))
            self.top5 = sorted(self.top5, reverse=True)
            self.show_top5()
        else:
            min_reward = self.top5[4][0]
            if(final_reward > min_reward):
                self.top5.pop()
                self.top5.append((final_reward, mynumbers.copy()))
                self.top5 = sorted(self.top5, reverse=True)
                self.show_top5()


    def get_suck5(self, final_reward, mynumbers):
        if(len(self.suck5) < 5):
            self.suck5.append((final_reward, mynumbers.copy()))
            self.suck5 = sorted(self.suck5, reverse=False)
            self.show_suck5()
        else:
            min_reward = self.suck5[4][0]
            if(final_reward < min_reward):
                self.suck5.pop()
                self.suck5.append((final_reward, mynumbers.copy()))
                self.suck5 = sorted(self.suck5, reverse=False)
                self.show_suck5()

    def show_rate5(self):
        # Clear terminal
        print('\x1b[2J')
        print(datetime.datetime.now())
        print("In %d history datas." % len(self.lottery_list))
        print("============== Rate 5 ================")
        for index, x in enumerate(self.rate5):
            final_reward = x[0]
            top_numbers = x[1]
            print("Top %d" % (index + 1))
            print("In sequence [%s]" % ','.join(map(str, top_numbers)))
            print("Total: Win %d times." % (final_reward))
            print("Average: Win %.2f times.\n" %
                  (final_reward/len(self.lottery_list)))


    def show_top5(self):
        # Clear terminal
        print('\x1b[2J')
        print("============== Top 5 ================")
        for index, x in enumerate(self.top5):
            final_reward = x[0]
            top_numbers = x[1]
            print("Top %d" % (index + 1))
            print("In sequence [%s]" % ','.join(map(str, top_numbers)))
            print("Total: You can win %d dollars." % (final_reward))
            print("Average: You can get %.2f dollars.\n" %
                  (final_reward/len(self.lottery_list)))


    def show_suck5(self):
        # Clear terminal
        print('\x1b[2J')
        print("============== Suck 5 ================")
        for index, x in enumerate(self.suck5):
            final_reward = x[0]
            top_numbers = x[1]
            print("Top %d" % (index + 1))
            print("In sequence [%s]" % ','.join(map(str, top_numbers)))
            print("Total: You can win %d dollars." % (final_reward))
            print("Average: You can get %.2f dollars.\n" %
                  (final_reward/len(self.lottery_list)))
