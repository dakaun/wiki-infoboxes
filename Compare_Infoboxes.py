import Extract_Infobox
import pandas as pd
import datetime
import re
import argparse


# get articles (as concatenated string) from the triple file matching with the infobox article name
def get_article_triple_file(article_name, t_file):
    t_file.seek(0)
    article_as_string = ""
    article_name = article_name.replace(' ', '_')
    t_line = t_file.readline()
    while t_line:
        if article_name in t_line:
            article_as_string += t_line
            t_line = t_file.readline()
        elif article_as_string:
            break
        else:
            t_line = t_file.readline()
    return article_as_string


parser = argparse.ArgumentParser(
    description='Extract infoboxes from articles and create csv file with infobox entities '
                'which contain a link + csv file which counts entites')
parser.add_argument('-xml_path', help='Path to xml dump')
parser.add_argument('-info_path', help='Path to infobox file')
parser.add_argument('-wiki_triple', help='Path to wiki_triple file (result from wiki_crawler')
parser.add_argument('-result', help='Path to result file which contains all infobox information')
parser.add_argument('-comp', help='Path to result file which contains all counter information')
args = parser.parse_args()

wikixml_path = args.xml_path
infobox_path = args.info_path
wikitriple_path = args.wiki_triple
result_path = args.result
comp_path = args.comp

# # PATHES: 
# wikixml_path = 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/Second_Task/data/wiki_dump_long.txt'
# infobox_path = 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/Second_Task/wiki-infoboxes/wiki-infoboxes/data/infobox_file/' + str(
#     datetime.datetime.now().month) + str(datetime.datetime.now().day) + 'infobox.txt'
# 
# wikitriple_path = r'C:\Users\danielak\Desktop\Dokumente Daniela\UNI\FIZ\Second_Task\test_wiki_crawler\longer\wiki_triples.txt'
# result_path = 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/Second_Task/wiki-infoboxes/wiki-infoboxes/data/result_infobox/' + str(
#     datetime.datetime.now().month) + str(datetime.datetime.now().day) + '_result_infobox.csv'
# comp_path = 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/Second_Task/wiki-infoboxes/wiki-infoboxes/data/comp_infobox/' + str(
#     datetime.datetime.now().month) + str(datetime.datetime.now().day) + '_comp.csv'

# python Compare_Infoboxes.py -xml_path ../../data/wiki_dump_long.txt -info_path data/infobox_2812.txt -wiki_triple ../../test_wiki_ctawler/longer/wiki_triples.txt -result data/result_infobox/result_infobox_2812.csv -comp data/comp_infobox/comp_2812.csv
df_comp = Extract_Infobox.create_infobox_dic(wikixml_path, infobox_path, comp_path)
# df_comp = pd.read_csv(comp_path, encoding='cp65001')  # TODO fix pandas.errors.ParserError: Error tokenizing data. C error: Expected 1 fields in line 7, saw 2
with open(wikitriple_path) as triple_f:  # , encoding='cp65001'
    with open(infobox_path) as infobox_f:
        df = pd.DataFrame(columns=['Article', 'Infobox_property', 'Entity',
                                   'Sentence'])  # contains articles with infoboxes, and those entities which are links and were found in the article as links
        print('-- Start to compare the Infoboxes')
        # iterate through infoboxes
        infobox_f_line = infobox_f.readline()
        while infobox_f_line:
            article = list(eval(infobox_f_line).keys())[0]  # get first article of the infoboxes
            article_from_triple = get_article_triple_file(article,
                                                          triple_f)  # continue only if article could be found in the triple file
            print('-- Processing infobox: ' + article)
            value_link_match_counter = 0
            if article_from_triple:
                infobox_value_list = list(eval(infobox_f_line)[article])
                while infobox_value_list:
                    plain_infobox_value = eval(infobox_f_line)[article][
                        infobox_value_list[0]]  # first infobox entity value out of list
                    entities_re = re.findall(r'(\[\[.*?\]\])',
                                             plain_infobox_value)  # get entity out of infobox entity value
                    #  if several entities are combined in one infobox entity value
                    for infobox_entity in entities_re:
                        infobox_entity = infobox_entity.replace('[[', '').replace(']]', '')
                        if "|" in infobox_entity:  # if shadowing
                            infobox_entity = re.match(r'(.*?)(\|)', infobox_entity)
                            infobox_entity = infobox_entity.group().replace('|', '')
                        # infobox_entity_undsco = re.sub(r"(.)([A-Z])", r"\1_\2", infobox_entity)
                        infobox_entity_undsco = infobox_entity.replace(' ', '_')
                        match_re = re.search(r'(<.*/' + infobox_entity_undsco + '>).*', article_from_triple,
                                             re.IGNORECASE)
                        if match_re:
                            value_link_match_counter += 1
                            match = match_re.group()
                            df = df.append({'Article': article, 'Infobox_property': infobox_value_list[0],
                                            'Entity': infobox_entity_undsco.replace('_', ' '),
                                            'Sentence': match.replace('>', '/').split('/')[10]},
                                           ignore_index=True)
                    infobox_value_list.pop(0)
            index_co = df_comp.index[df_comp['article'] == article].tolist()[0]
            df_comp.loc[index_co, 'amount_link_article_match'] = value_link_match_counter
            infobox_f_line = infobox_f.readline()
df.to_csv(result_path, sep=';', index=False)
df_comp.to_csv(comp_path, sep=';', index=False)  # todo encoding anpassen
