from superlotto import Superlotto

if __name__ == "__main__":
    lotto = Superlotto()
    # lotto.write_data_to_file(62)
    lotto.get_data_from_file()
    lotto.dfs_all_numbers([], 0)
    # daily539 = Daily539("top")
    # daily539.read_numbers_to_file()
    # daily539.dfs_all_numbers(0)