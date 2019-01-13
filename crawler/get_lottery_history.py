from daily539 import Daily539
from happy39M5 import Happy39

if __name__ == "__main__":
    # daily539 = Daily539("top")
    # daily539.read_numbers_to_file()
    # daily539.dfs_all_numbers(0)

    happy39 = Happy39()
    # happy39.write_numbers_to_file(36)
    happy39.read_numbers_to_file()
    happy39.dfs_all_numbers(0)
    happy39.show_top5()
