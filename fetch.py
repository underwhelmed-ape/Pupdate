# imports
import re
from scraper import Pupdate
from csv_handling import CsvWorker
from setup_logger import logger

# get page contents as selector object
pupdate = Pupdate()
request = pupdate.make_request()

# make csv if not already
csv_worker = CsvWorker('seal_counts.csv')
csv_worker.create_csv_if_not_exist()

# list the dates for which data is available to scrape
dates_url = pupdate.dates_available(request)
saved_dates = csv_worker.retrieve_dates_saved_in_csv()


n_paragraphs_w_data = len(pupdate.get_paragraphs_from_data_table(request))
dates_w_data = dates_url[:n_paragraphs_w_data]
dates_w_data.reverse()
for date in dates_w_data:
    if date in saved_dates:
        logger.info(f'Seal counts as at {date} already saved in csv')
    else:
        logger.info(f'Saving Seal counts as at {date}')
        data = pupdate.get_data_for_date(date, request)
        csv_worker.add_new_row_to_csv(data)

