import re
# from lxml import etree # try to parse
import mwparserfromhell


def open_wiki_articles():
    article = ""
    article_list = []
    with open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/Second_Task/data/wiki_dump_short.txt',
              encoding='cp65001') as articles_raw:
        articles_line = articles_raw.readline()
        while articles_line:
            article += articles_line
            if '</page>' in articles_line:
                article_list.append(article)
                article = ""
            articles_line = articles_raw.readline()
    return article_list

articles = open_wiki_articles()
for text in articles:
    article = mwparserfromhell.parse(text)
    #print(article)
    infobox = article.filter_templates(matches='infobox .*')
    #print(infobox)
    if infobox:
        print('Name ', infobox[0].params[0].name)
        print('Value ', infobox[0].params[0].value)


