import sys
import os
from datetime import datetime
from repository.repository_builder import find_repository_by_name
from repository.writer import repository_write_file



def create_filename(dir, filename):
    return os.path.join(dir, filename)

def main(source, stock, date_start, date_end, directory):
    repository = find_repository_by_name(source)
    data = repository.get(stock, date_start, date_end)

    filename = create_filename(directory, stock)
    repository_write_file(data, filename)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("It required more params")
        print("python downloader.py SOURCE STOCK DATE_START DATE_END FOLDER_SAVE")
        print("example")
        print("python downloader.py yahoo MSFT 2020-01-01 2020-03-31 ./data")
    else:
        source = sys.argv[1]
        stock = sys.argv[2]
        start = datetime.strptime(sys.argv[3], "%Y-%m-%d")
        end = datetime.strptime(sys.argv[4], "%Y-%m-%d")
        directory = sys.argv[5]

        main(source, stock, start, end, directory)