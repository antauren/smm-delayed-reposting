# extracturl-1.0.1.tar.gz from https://pypi.org/project/extracturl/#files

import re
import string


def extract(text: str) -> list:
    url = r"""((?:(?:https|ftp|http)?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|org|uk)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|uk|ac)\b/?(?!@)))"""
    urls = re.findall(url, text)

    url_list = [''.join(x for x in url if x in string.printable) for url in urls]

    return url_list
