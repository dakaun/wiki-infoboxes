import re
# from lxml import etree # try to parse
import mwparserfromhell
import datetime
import pandas as pd

# todo insert print statements

def open_wiki_articles(path):
    article = ""
    article_list = []
    with open(path) as articles_raw:
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


def create_infobox_dic(wikiarticle_path, infobox_path, df):
    #wikiarticle_path = 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/Second_Task/data/wiki_dump_long.txt'
    articles = open_wiki_articles(wikiarticle_path)
    entity_list = {}
    infobox_dic = {}
    name = ""
    value = ""
    #infobox_path = 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/Second_Task/infobox_file/' + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + 'infobox.txt'
    with open(infobox_path, 'w+') as infobox_file:
        for article in articles:
            infobox_dic = {}
            link_counter = 0
            amount_info_values = 0
            infobox_value_counter = 0
            infobox = mwparserfromhell.parse(article).filter_templates(matches='Infobox .*')
            # infobox = article.filter_templates(matches='Infobox .*')
            article_title = extract_title(article)
            # create dic with all linked entities from infobox
            if infobox:
                entity_list = {}
                amount_info_values = len(infobox[0].params)
                for i in range(0, amount_info_values):
                    # counts all infobox names with content (not only those which contain a link)
                    if re.match('[^\\n]', str(infobox[0].params[i].value)) is not None : #todo could be enhanced by searching for any charachter except \n, }},|
                        infobox_value_counter += 1
                    if '[[' in infobox[0].params[i].value:
                        link_counter += 1
                        # clear name and value
                        name = str(infobox[0].params[i].name)
                        value = str(infobox[0].params[i].value)
                        name = name.replace('\n', ' ')
                        value = value.replace('\n', ' ')
                        entity_list.update({name: value})
                # infobox_dic = {title: {name:value},...}
                infobox_dic.update({article_title: entity_list})
                infobox_file.write(str(infobox_dic) + '\n')
            df = df.append({'article': article_title, 'amount_values': amount_info_values, 'amount_entities': infobox_value_counter, 'amount_links': link_counter}, ignore_index=True)
    return infobox_path, df


if __name__ == '__main__':
    create_infobox_dic()
