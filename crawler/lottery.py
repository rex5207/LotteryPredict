import downloader

SELET_NUM = 2

class Lottery:
    def __init__(self, LoType):
        self.lottery_list = []
        self.arrDays = []
        self.history_file = downloader.HISTORY_FILE_DIR + LoType + '.csv'
        if (LoType == downloader.STR_LOT539):
            self.total_num = 39
        else:
            self.total_num = 49

        self.get_data_from_file()

    def get_data_from_file(self):
        print("Read history results from local file...")
        f = open(self.history_file, 'r')
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

    def dfs_all_numbers(self, nums, n_cur):
        if len(nums) < SELET_NUM:
            for i in range(n_cur + 1, self.total_num + 1):
                nums.append(i)
                self.dfs_all_numbers(nums, i)
                nums.pop()
        elif len(nums) == SELET_NUM:
            self.calculate_longest_day(nums)
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
    
    # 最長天數Top5
    def get_days_top5(self, nums, days):
        self.arrDays.append((days, nums.copy()))
        self.arrDays = sorted(self.arrDays, reverse=True)
        if len(self.arrDays) > 5:
            self.arrDays.pop()
    
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


if __name__ == "__main__":
    LoType = downloader.STR_LOT649
    # LoType = downloader.STR_LOT539
    # HisDownloder = downloader.HistoryDownloader(LoType=LoType)
    Lottery = Lottery(LoType)
    Lottery.dfs_all_numbers([], 0)