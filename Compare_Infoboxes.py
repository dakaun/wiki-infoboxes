import Extract_Infobox
import pandas as pd


def open_triple_file():
    with open(
            r'C:\Users\danielak\Desktop\Dokumente Daniela\UNI\FIZ\Second_Task\test_wiki_crawler\short\wiki_triples(short).txt',
            encoding='cp65001') as triple_f:
        return triple_f


entity_dic = Extract_Infobox.create_infobox_dic()
with open(
        r'C:\Users\danielak\Desktop\Dokumente Daniela\UNI\FIZ\Second_Task\test_wiki_crawler\short\wiki_triples(short).txt',
        encoding='cp65001') as triple_f:
    triple_line = ""
    df = pd.DataFrame(columns=['Article', 'Entity', 'Sentence'])  # contains articles with infoboxes, and those entities which are links and were found in the article as links
    for article in entity_dic:
        triple_line = triple_f.readline()
        while (triple_line):
            triple_article = triple_line.replace('>', '/').split('/')[4].replace('_', ' ')
            if article == triple_article:
                print(article, ': Artikel gefunden')
                triple_entity = triple_line.replace('>', '/').split('/')[9].replace('_', '')
                for entity in entity_dic[article]:
                    if triple_entity in entity_dic[article][entity]:
                        print(triple_entity, ': Entity gefunden ')
                        df = df.append({'Article': article, 'Entity': triple_entity, 'Sentence': triple_line.replace('>', '/').split('/')[10]}, ignore_index=True)
                break
            break
print(df)
#
# for line in triple_file:
#     for article in entity_dic:
#         print(article)
