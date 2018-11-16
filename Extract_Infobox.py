import re
# from lxml import etree # try to parse
import mwparserfromhell
import datetime


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


def create_infobox_dic():
    articles = open_wiki_articles()
    entity_dic = {}
    infobox_dic = {}
    name = ""
    value = ""
    path = 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/Second_Task/infobox_file/' + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + 'infobox.txt'
    with open(path, 'w+') as infobox_file:
        for text in articles:
            infobox_dic = {}
            article = mwparserfromhell.parse(text)
            infobox = article.filter_templates(matches='infobox .*')
            article_title = extract_title(text)
            # create dic with all linked entities from infobox
            if infobox:
                entity_dic = {}
                for i in range(1, len(infobox[0].params)):
                    if '[[' in infobox[0].params[i].value:
                        # clear name and value
                        name = str(infobox[0].params[i].name)
                        value = str(infobox[0].params[i].value)
                        name = name.replace('\n', '').replace(' ', '')
                        value = value.replace('\n', '').replace(' ', '')
                        entity_dic.update({name: value})
                # infobox_dic = {title: {name:value},...}
                infobox_dic.update({article_title: entity_dic})
                infobox_file.write(str(infobox_dic) + '\n')
                entity_dic = {}
    return path


if __name__ == '__main__':
    create_infobox_dic()
