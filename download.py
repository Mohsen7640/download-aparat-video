from time import sleep
from tqdm import tqdm
from math import floor, log

from crawl import Crawler, LinkCrawler


class Download(Crawler):

    def __init__(self, url, quality):
        self.url = url
        self.quality = quality
        self.link = LinkCrawler(self.url, self.quality).start()

    @property
    def get_name(self):
        return self.link.split('/')[-1]

    @staticmethod
    def is_downloadable(response):
        content_type = response.headers['Content-Type'].lower()
        if ('text' in content_type) or ('html' in content_type):
            return False
        return True

    @staticmethod
    def change_scale(response, unit_size=1024):
        total_bit = int(response.headers.get('Content-Length', 0))

        if total_bit != 0:
            scale = floor(log(total_bit, unit_size))
            total_bit = (total_bit / pow(unit_size, scale)) * pow(1000, scale)

            return total_bit, scale
        return total_bit, 1

    def download(self, response):
        unit_size = 1024
        total_bit, scale = self.change_scale(response)

        progress_bar = tqdm(total=total_bit, unit_scale=True, unit='B')

        with open(file=f'download/{self.get_name}', mode='wb') as file_handler:
            for chunk in response.iter_content(chunk_size=unit_size):
                size = (len(chunk) / pow(unit_size, scale)) * pow(1000, scale)
                progress_bar.update(size)
                file_handler.write(chunk)

        progress_bar.close()

    def start(self):
        respond = self.get_request(url=self.link, stream=True)

        if self.is_downloadable(respond):
            print('Downloading ...')
            sleep(1)

            self.download(respond)

            sleep(1)
            print('File download completed ...')
        else:
            print('The file is not downloadable ...')
