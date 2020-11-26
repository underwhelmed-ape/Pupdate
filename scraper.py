import requests
import re
from scrapy import Selector
from setup_logger import logger


class Pupdate:
    def __init__(self):
        self.url = 'https://www.lincstrust.org.uk/get-involved/top-reserves/donna-nook/weekly-update'
        self.table_name = 'field field--name-field-section-introduction field--type-text-long field--label-hidden field__items'

    def make_request(self):
        try:
            request = requests.get(self.url)
            logger.info(f'URL request code {request.status_code}')
            pupdate_table = Selector(text=request.text)
            data_table = self._select_data_table_from_page(pupdate_table)
            return data_table
        except:
            logger.error(f'URL request failed')
            pass
    
    def _select_data_table_from_page(self, pupdate_table):
        table_section = pupdate_table.xpath(f'//div[@class="{self.table_name}"]').extract()
        return Selector(text=table_section[0])

    def dates_available(self, page_selection):
        '''return dates available at URL'''
        logger.info('retrieving dates from page')
        dates = [self._date_from_heading(heading) for heading in page_selection.xpath('//h4').extract()]
        logger.info('retrieved dates from page')
        return dates

    def _date_from_heading(self, heading):
        try:
            match = re.search(r'\d{2}/\d{2}/\d{4}', heading).group(0) 
            if match is not None:
                return match
        except:
            logger.warning(f'could not extract date from heading: \n{heading}')
            pass

    def get_headings_from_data_table(self, data_table):
        headings = data_table.xpath('//h4').extract()
        return headings

    def get_paragraphs_from_data_table(self, data_table):
        paragraphs = data_table.xpath('//p').extract()
        return paragraphs

    def get_data_for_date(self, date, data_table):
        '''for a given date, extract the associated paragraph'''
        # loop through each h4 until get to date specified
        headings = self.get_headings_from_data_table(data_table)
        for i, heading in enumerate(headings):
            if self._date_from_heading(heading) == date:
                paragraph = data_table.xpath('//p')[i].extract()
                return self._return_new_data(date, paragraph)


    def _return_new_data(self, date, paragraph):
        if 'first' in paragraph.lower():
            return [date, 1, self._cows_count(paragraph), self._bulls_count(paragraph)]
        else:
            return [date, self._pups_count(paragraph), self._cows_count(paragraph), self._bulls_count(paragraph)]

    def _pups_count(self, paragraph):
        extract = re.search(r'(\d+|\d,\d+)\spup', paragraph).group(1)
        return int(extract.replace(',', ''))

    def _cows_count(self, paragraph):
        extract = re.search(r'(\d+|\d,\d+)\scow', paragraph).group(1)
        return int(extract.replace(',', ''))

    def _bulls_count(self, paragraph):
        extract = re.search(r'(\d+|\d,\d+)\sbull', paragraph).group(1)
        return int(extract.replace(',', ''))
    



if __name__ == "__main__":
    
    r = Pupdate()
    pups = r.make_request()

    print(r.get_paragraph_for_date('20/11/2020', pups))
    print(r.get_paragraph_for_date('13/11/2020', pups))
