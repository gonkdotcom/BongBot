from html.parser import HTMLParser
import requests


class Bongard(HTMLParser):
    def __init__(self):
        super().__init__()
        self.img = None

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.img = attrs[0][1].split(',')[1]
        # pass


class Solution(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = None
        self.flag = False

    def handle_starttag(self, tag, attrs):
        if tag == "td" and len(attrs) == 2 and attrs[0][1] == "top" and attrs[0][0] == "valign" and attrs[1][
            1] == "left" and attrs[1][0] == "align":
            self.flag = True

    def handle_data(self, data):
        if self.flag:
            self.text = data
            self.flag = False
