from bs4 import BeautifulSoup
from lxml import etree
import re
from urllib.request import urlopen
import ssl

STR_LOT649 = 'ltobig'
STR_LOT539 = 'lto539'

HISTORY_FILE_DIR = "../data/"
WEBSITE_PATH = 'https://www.pilio.idv.tw/'
TOTAL_PAGE = 93

class HistoryDownloader:
    def __init__(self, LoType=STR_LOT649):
        self.lottery_list = []
        if (LoType == STR_LOT649):
            self.URL = WEBSITE_PATH + STR_LOT649 + '/list.asp?indexpage='
            self.HISTORY_FILE = HISTORY_FILE_DIR + STR_LOT649 + '.csv'
            self.haveSpeNum = True
        else:
            self.URL = WEBSITE_PATH + STR_LOT539 + '/list.asp?indexpage='
            self.HISTORY_FILE = HISTORY_FILE_DIR + STR_LOT539 + '.csv'
            self.haveSpeNum = False

        self.total_page = self.get_max_pagenum()
        print("self.total_page = %d" % self.total_page)
        self.write_data_to_file()

    # Get total page number
    def get_max_pagenum(self):
        # disable ssl certificate verify
        ssl._create_default_https_context = ssl._create_unverified_context
        response = urlopen(self.URL)
        html = response.read()

        soup = BeautifulSoup(html, "html.parser")
        dom = etree.HTML(str(soup))
        url = dom.xpath('/html/body/div/div/div/a[3]')[0].get('href')
        match = re.search(r'indexpage=(\d+)', url)
        if match:
            return int(match.group(1))
        else:
            return TOTAL_PAGE

    # Get lottery history from website and write to local file
    def write_data_to_file(self):
        for self.total_page in range(1, self.total_page + 1):
            self._get_data_from_webpage(self.total_page)

        print("Write history results to local file...")
        f = open(self.HISTORY_FILE, 'w')
        for lottery in self.lottery_list:
            f.write(lottery["date"] + " ")
            f.writelines(','.join(map(str, lottery["numbers"])))
            f.write('\n')
        f.close
        print("Finish.\n")

    def _get_data_from_webpage(self, page_num):
        print("Get data from website...Page" + str(page_num))
        # disable ssl certificate verify
        ssl._create_default_https_context = ssl._create_unverified_context
        response = urlopen(self.URL + str(page_num))
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all('table', {'class':'auto-style1'})

        for idx, table in enumerate(tables):
            content = table.find_all('td')
            # 將內容改成3-tuple, date/number/space, 並跳過第一欄說明欄
            # [content[3:] => 從第四個元素開始
            # 這個表達式的作用是將 content 列表中每隔三個元素的部分取出來，然後將這些部分重新排列成元組的形式
            if (self.haveSpeNum):
                periodNum = 3
            else:
                periodNum = 2
            if (idx == 0):
                content = zip(*[content[periodNum:][i::periodNum] for i in range(periodNum)])
            else:
                content = zip(*[content[:][i::periodNum] for i in range(periodNum)])

            for result in content:
                date = result[0].text
                numbers = (result[1].text).strip().split(",")
                numbers = list(map(int, numbers))
                if (self.haveSpeNum):
                    spec_num = int(result[2].text)
                    numbers.append(spec_num)
                data = {
                    "date": date[:-3],
                    "numbers": numbers
                }
                self.lottery_list.append(data)