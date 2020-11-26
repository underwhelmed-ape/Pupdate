import pandas as pd
import os
import csv
from setup_logger import logger

class CsvWorker:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def create_csv_if_not_exist(self):
        if not self._check_csv_exists():
            logger.info(f'{self.csv_path} does not exist. Creating file')
            with open(self.csv_path, 'w') as wf:
                writer = csv.writer(wf)
                writer.writerow(['date', 'pups', 'cows', 'bulls'])
            logger.info(f'{self.csv_path} file created')
        else:
            logger.info(f'{self.csv_path} already exists')
    
    def _check_csv_exists(self):
        return os.path.exists(self.csv_path)

    def retrieve_dates_saved_in_csv(self):
        '''returns a list of dates as str (16/10/2020) in csv'''
        with open(self.csv_path, 'r') as rf:
            reader = csv.reader(rf)
            next(reader)
            saved_dates = [row[0] for row in reader]
        return saved_dates

    def add_new_row_to_csv(self, data):
        '''new data -> ['date', 'pups_no', 'cows_no', 'bulls_no']'''
        with open(self.csv_path, 'a') as af:
            writer = csv.writer(af)
            writer.writerow(data)

    def __str__(self):
        return '''Set of methods for working with csvs'''



if __name__ == "__main__":
    
    csv_worker = CsvWorker('test.csv')
    
    print(csv_worker.retrieve_dates_saved_in_csv())

    csv_worker.add_new_row_to_csv(['28/09/2021','6470','9550','2000'])


