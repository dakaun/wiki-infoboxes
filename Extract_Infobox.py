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

def extract_title(article):
    re_title = re.search(r'<title>.*?</title>', article)
    group_title = re_title.group()
    title = group_title.replace('<', '>').split('>')
    return title[2]

articles = open_wiki_articles()
entity_dic = {}
infobox_dic = {}
name = ""
value = ""
for text in articles:
    article = mwparserfromhell.parse(text)
    infobox = article.filter_templates(matches='infobox .*')
    article_title = extract_title(text)
    # create dic with all linked entities from infobox
    if infobox:
        for i in range(1, len(infobox[0].params)):
            if '[[' in infobox[0].params[i].value:
                print(infobox[0].params[i].value)
                # clear name and value
                name = str(infobox[0].params[i].name)
                value = str(infobox[0].params[i].value)
                name = name.replace('\n', '').replace(' ', '')
                value = value.replace('\n', '').replace(' ', '')
                entity_dic.update({name: value})
        # infobox_dic = {title: {name:value},...}
        infobox_dic.update({article_title: entity_dic})
        entity_dic = {}
print(infobox_dic)



