import re
# from lxml import etree # try to parse
import mwparserfromhell
import datetime
import pandas as pd
import fileinput


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
    amount_info_values = 0
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
    infofile.write(str(infobox_dic) + '\n')
    return title, amount_info_values, infobox_value_counter, link_counter


def create_infobox_dic(wikiarticle_path, infobox_path, df):
    # wikiarticle_path = 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/Second_Task/data/wiki_dump_long.txt'
    # infobox_path = 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/Second_Task/infobox_file/' + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + 'infobox.txt'
    article = ""
    infobox_file = open(infobox_path, 'w+')
    print('-- Extracting infoboxes')
    for line in fileinput.input(wikiarticle_path,
                                openhook=fileinput.hook_compressed):  # hook_compressed hook_encoded('cp65001')
        article += line
        if '</page>' in line:
            # start processing infobox
            infobox = mwparserfromhell.parse(article).filter_templates(matches='Infobox .*')
            article_title = extract_title(article)
            if infobox:
                title, counter1, counter2, counter3 = parse_infobox(infobox, article_title, infobox_file)
                df = df.append(
                    {'article': title, 'amount_properties': counter1,
                     'amount_entities': counter2,
                     'amount_links': counter3}, ignore_index=True)
            # end of processing infobox
            article = ""
    print('-- Infoboxes extracted and saved in infobox_file')
    return infobox_path, df


if __name__ == '__main__':
    df_comp = pd.DataFrame(
        columns=['article', 'amount_properties', 'amount_entities', 'amount_links', 'amount_link_article_match'])
    path, df = create_infobox_dic(
        'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/Second_Task/data/wiki_dump_long.txt',
        'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/Second_Task/infobox_file/' + str(
            datetime.datetime.now().month) + str(datetime.datetime.now().day) + 'infobox.txt', df_comp)
    print(df)
