import Extract_Infobox
import pandas as pd
import datetime
import re

infobox_path = Extract_Infobox.create_infobox_dic()
with open(
        r'C:\Users\danielak\Desktop\Dokumente Daniela\UNI\FIZ\Second_Task\test_wiki_crawler\short\wiki_triples(short).txt',
        encoding='cp65001') as triple_f:
    with open(infobox_path) as infobox_f:
        df = pd.DataFrame(columns=['Article', 'Entity',
                                   'Sentence'])  # contains articles with infoboxes, and those entities which are links and were found in the article as links
        infobox_f_line = infobox_f.readline()
        triple_line = triple_f.readline()
        triple_file = triple_f.read()

        df = pd.DataFrame(columns=['Article', 'Entity', 'Sentence'])

        while infobox_f_line and triple_line:
            article = list(eval(infobox_f_line).keys())[0]
            triple_article = triple_line.replace('>', '/').split('/')[4].replace('_', ' ')
            if article == triple_article:
                print('Article match: ', article)
                infobox_entity_list = list(eval(infobox_f_line)[article])
                while article == triple_article:
                    triple_entity = triple_line.replace('>', '/').split('/')[9].replace('_', '')
                    print('Triple Entity: ', triple_entity)
                    print('Infobox Entity: ', eval(infobox_f_line)[article][infobox_entity_list[0]])
                    # check if infobox entity is in triple file, otherwise take next infobox entity
                    entity = re.search(r'/' + triple_entity + '>', triple_file)
                    if entity:
                        if triple_entity in eval(infobox_f_line)[article][infobox_entity_list[0]]:
                            df = df.append({'Article': article, 'Entity': triple_entity,
                                            'Sentence': triple_line.replace('>', '/').split('/')[10]}, ignore_index=True)
                            df.to_csv(
                                r'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/Second_Task/result_match/' + str(
                                    datetime.datetime.now().month) + str(
                                    datetime.datetime.now().day) + 'infobox_matches.csv', index=False)
                            infobox_entity_list.pop(0)
                            triple_line = triple_f.readline()
                        else:
                            triple_line = triple_f.readline()
                        triple_article = triple_line.replace('>', '/').split('/')[4].replace('_', ' ')
                    else:
                        infobox_entity_list.pop(0)
                # back to article rotating
                infobox_f_line = infobox_f.readline()
                triple_line = triple_f.readline()
            else:
                triple_line = triple_f.readline()
print(df)
