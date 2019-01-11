import re
# from lxml import etree # try to parse
import mwparserfromhell
import datetime
import pandas as pd
import fileinput
from multiprocessing import cpu_count, Pool


# todo insert print statements

def open_wiki_articles(input_path):
    article = ""
    article_list = []
    input = fileinput.FileInput(input_path)
    for line in input:
        while line:
            article += line
            if '</page>' in line:
                article_list.append(article)
                article = ""
    return article_list


def extract_title(article):
    re_title = re.search(r'<title>.*?</title>', article)
    group_title = re_title.group()
    title = group_title.replace('<', '>').split('>')
    return title[2]


def parse_infobox(infobox, title, infofile):
    infobox_value_counter = 0
    link_counter = 0
    entity_list = {}
    infobox_dic = {}
    name = ""
    value = ""

    print('-- Processing article : ' + title)
    amount_info_values = len(infobox[0].params)
    for i in range(0, amount_info_values):
        # counts all infobox names with content (not only those which contain a link)
        if re.match('[^\\n]', str(infobox[0].params[
                                      i].value)) is not None:  # todo could be enhanced by searching for any charachter except \n, }},|
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
    infobox_dic.update({title: entity_list})
    infofile.write(str(infobox_dic) + '\n') # check ob das mit multiprocessing funtkioniert, oder ob das file immer wieder überschrieben wird...
    #infoboxdic_line = str(infobox_dic) + '\n'
    return amount_info_values, infobox_value_counter, link_counter


def pages_from(input):
    article = ""
    title = None

    for line in input:
        article += line
        re_title = re.search(r'<title>.*?</title>', line)
        if '</page>\n' in line:
            yield (article, title)
            article = ""
            title = None
        if not re_title:
            continue
        title = re_title.group().replace('<', '>').split('>')[2]


def create_infobox_dic(wikiarticle_path, infobox_path, df):
    # wikiarticle_path = 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/Second_Task/data/wiki_dump_long.txt'
    # infobox_path = 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/Second_Task/infobox_file/' + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + 'infobox.txt'
    df = pd.DataFrame(columns=['article', 'amount_properties', 'amount_entities', 'amount_links', 'amount_link_article_match'])

    infobox_file = open(infobox_path, 'w+')

    print('-- Extracting infoboxes')
    input = fileinput.FileInput(wikiarticle_path, openhook=fileinput.hook_encoded('cp65001'))  # hook_compressed hook_encoded('cp65001')

    # TODO next try: try to implement Queue as in WikiExtractor


    for page_data in pages_from(input):
        page, title = page_data
        # start processing infobox
        infobox = mwparserfromhell.parse(page).filter_templates(matches='Infobox .*')

        if infobox:
            counter1, counter2, counter3 = parse_infobox(infobox, title, infobox_file)
            df = df.append(
                    {'article': title, 'amount_properties': counter1,
                     'amount_entities': counter2,
                     'amount_links': counter3}, ignore_index=True)
                # end of processing infobox
        page = None
    print('-- Infoboxes extracted and saved in infobox_file')
    return df # Todo write df to file?


if __name__ == '__main__':
    df_comp = pd.DataFrame(
        columns=['article', 'amount_properties', 'amount_entities', 'amount_links', 'amount_link_article_match'])
    path, df = create_infobox_dic(
        r'C:\Users\danielak\Desktop\Dokumente Daniela\UNI\FIZ\Second_Task\data\wiki_dump_long_withoutsiteinfo.txt',
        'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/Second_Task/infobox_file/' + str(
            datetime.datetime.now().month) + str(datetime.datetime.now().day) + 'infobox.txt', df_comp)
    print(df)
    #wikiarticlepath #'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/Second_Task/data/wiki_dump_long.txt',
