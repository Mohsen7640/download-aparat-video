import json
import requests
import re

from abc import ABC
from bs4 import BeautifulSoup

from exceptions import QualityError


class Crawler(ABC):

    @staticmethod
    def get_request(url, stream=False):
        try:
            response = requests.get(url, stream=stream)
        except requests.HTTPError:
            return None
        return response


class LinkCrawler(Crawler):

    def __init__(self, url, quality):
        self.url = url
        self.quality = quality

    @staticmethod
    def get_list_tags(html_doc):
        """
        Get all li tags with class: menu-item-link link
        :param html_doc:
        :return:
        """
        soup = BeautifulSoup(html_doc, 'html.parser')
        return soup.find_all('li', attrs={'class': 'menu-item-link link'})

    @staticmethod
    def get_links(list_tags):
        """
        Get all links(Nested tags) and store to file
        :param list_tags:
        :return:
        """
        links = list()
        for li in list_tags:
            link = li.find('a').get('href')
            links.append(link)
        LinkCrawler.store('links', links)

    @staticmethod
    def get_qualities(list_tags):
        """
        Get all qualities and store to file
        :param list_tags:
        :return:
        """
        qualities = list()
        for li in list_tags:
            quality = li.find('span').text
            quality = re.findall(pattern='[0-9]+', string=quality)[0]  # clean
            qualities.append(quality)
        LinkCrawler.store('qualities', qualities)

    @staticmethod
    def match_quality_and_link():
        """
        Match quality and link in dictionary
        :return:
        """
        match = dict()

        qualities = LinkCrawler.__load_data('qualities')
        links = LinkCrawler.__load_data('links')

        for quality, link in zip(qualities, links):
            match[quality] = link

        return match

    def get_link(self):
        """
        Get specific link.
        :return:
        """
        match = self.match_quality_and_link()
        if self.quality not in match.keys():
            available_qualities = list(match.keys())
            raise QualityError(
                f'Sorry, this quality is not available\nAvailable qualities are {available_qualities}'
            )
        else:
            return match[self.quality]

    @staticmethod
    def store(filename, data):
        with open(file=f'fixtures/{filename}.json', mode='w') as file_handler:
            file_handler.write(json.dumps(data))

    @staticmethod
    def __load_data(filename):
        with open(file=f'fixtures/{filename}.json', mode='r') as file_handler:
            data = json.loads(file_handler.read())
        return data

    def start(self):
        """
        start Crawl
        :return:
        """
        respond = self.get_request(self.url)
        list_tags = self.get_list_tags(respond.text)
        self.get_links(list_tags)
        self.get_qualities(list_tags)
        link = self.get_link()

        return link
