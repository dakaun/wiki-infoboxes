import re
# from lxml import etree # try to parse
import mwparserfromhell

with open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/Second_Task/data/wiki_dump_short.txt',
          encoding='cp65001') as articles_raw:
    articles = articles_raw.read()
    #article = mwparserfromhell.parse(articles)
    #print(article)
    #infobox =  article.filter_templates(matches='infobox .*')

    # -----REGEX
    infobox = re.findall(r'{{Infobox .*?}}', articles, re.DOTALL)
    print(infobox)
