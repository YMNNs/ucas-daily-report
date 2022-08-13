# -*- coding: UTF-8 -*-
"""
@Function：json to markdown
@Time ： 2022/6/15 09:45
@Auth ： https://github.com/PolBaladas/torsimany/blob/master/torsimany/torsimany.py
"""
import json


class Json2Markdown(object):
    """
    # json转markdown形式
    """

    def __init__(self):
        self.markdown = ""
        self.tab = "  "
        self.list_tag = '* '
        self.htag = '#'

    def loadJSON(self, file):
        """
        :param file:
        :return:
        """
        with open(file, 'r') as f:
            data = f.read()
        return json.loads(data)

    def parseJSON(self, json_block, depth):
        """
        :param json_block:
        :param depth:
        :return:
        """
        if isinstance(json_block, dict):
            self.parseDict(json_block, depth)
        if isinstance(json_block, list):
            self.parseList(json_block, depth)

    def parseDict(self, d, depth):
        """
        :param d:
        :param depth:
        :return:
        """
        for k in d:
            if isinstance(d[k], (dict, list)):
                self.addHeader(k, depth)
                self.parseJSON(d[k], depth + 1)
            else:
                self.addValue(k, d[k], depth)

    def parseList(self, l, depth):
        """
        :param l:
        :param depth:
        :return:
        """
        for value in l:
            if not isinstance(value, (dict, list)):
                index = l.index(value)
                self.addValue(index, value, depth)
            else:
                self.parseDict(value, depth)

    def buildHeaderChain(self, depth):
        """
        :param depth:
        :return:
        """
        chain = self.list_tag * (bool(depth)) + self.htag * (depth + 1) + \
                ' value ' + (self.htag * (depth + 1) + '\n')
        return chain

    def buildValueChain(self, key, value, depth):
        """
        :param key:
        :param value:
        :param depth:
        :return:
        """
        chain = self.tab * (bool(depth - 1)) + self.list_tag + \
                str(key) + ": " + str(value) + "\n"
        return chain

    def addHeader(self, value, depth):
        """
        :param value:
        :param depth:
        :return:
        """
        chain = self.buildHeaderChain(depth)
        self.markdown += chain.replace('value', value.title())

    def addValue(self, key, value, depth):
        """
        :param key:
        :param value:
        :param depth:
        :return:
        """
        chain = self.buildValueChain(key, value, depth)
        self.markdown += chain

    def json2markdown(self, json_data):
        """
        :param json_data:
        :return:
        """
        depth = 0
        self.parseJSON(json_data, depth)
        self.markdown = self.markdown.replace('#######', '######')
        return self.markdown


if __name__ == '__main__':
    json_data = {}

    # 实例
    json2markdown_ins = Json2Markdown()

    # json转markdown
    markdown_data = json2markdown_ins.json2markdown(json_data)

    print(markdown_data)