import Extract_Infobox
import pandas as pd

infobox_path = Extract_Infobox.create_infobox_dic()
with open(
        r'C:\Users\danielak\Desktop\Dokumente Daniela\UNI\FIZ\Second_Task\test_wiki_crawler\short\wiki_triples(short).txt',
        encoding='cp65001') as triple_f:
    with open(infobox_path) as infobox_f:
        df = pd.DataFrame(columns=['Article', 'Entity',
                                   'Sentence'])  # contains articles with infoboxes, and those entities which are links and were found in the article as links
        infobox_f_line = infobox_f.readline()
        #article = list(infobox_f_line.keys())[0]
        triple_line = triple_f.readline()
        #triple_article = triple_line.replace('>', '/').split('/')[4].replace('_', ' ')


        while infobox_f_line and triple_line:
            #print(infobox_f_line)
            article = list(eval(infobox_f_line).keys())[0]
            #print(article)
            triple_article = triple_line.replace('>', '/').split('/')[4].replace('_', ' ')
            if article == triple_article:
                print('Article match: ', article)
                #while article == triple_article:
                #    entity = eval(infobox_f_line)
                #    print(entity)
                 #   triple_entity = triple_line.replace('>', '/').split('/')[9].replace('_', '')
                #    if triple_entity == entity:
                #        print('nothing')


                infobox_f_line = infobox_f.readline()
                triple_line = triple_f.readline()
            else:
                triple_line = triple_f.readline()




        # while infobox_f_line:
        #     article = list(eval(infobox_f_line).keys())[0]
        #     triple_article = triple_line.replace('>', '/').split('/')[4].replace('_', ' ')
        #     print(article)
        #     if article == triple_article:
        #         print('Article: ', article)
        #     infobox_f_line = infobox_f.readline()
        #     print(infobox_f_line)
        #     triple_line = triple_f.readline()



        #triple_line = triple_f.readline()
        #triple_article = triple_line.replace('>', '/').split('/')[4].replace('_', ' ')

    # while triple_line:
    #     triple_article = triple_line.replace('>', '/').split('/')[4].replace('_', ' ')
    #     for article in entity_dic:
    #         while article == triple_article:
    #             print('Article :', article)
    # for entity in entity_dic[article]:
    # print('Entity: ', entity)
# article = ""
# triple_line = triple_line = triple_f.readline()
# triple_article = triple_line.replace('>', '/').split('/')[4].replace('_', ' ')
# for article in entity_dic:
#     while article == triple_article:
#         print('Article ', article)                triple_line = triple_line = triple_f.readline()
#         triple_article = triple_line.replace('>', '/').split('/')[4].replace('_', ' ')
# triple_entity = triple_line.replace('>', '/').split('/')[9].replace('_', '')
# for entity in entity_dic[article]:
# if triple_entity in entity_dic[article][entity]:


# endlosscheife
# for article, entity in entity_dic.items():
#     print('Article: ', article)
#     print('Entity: ', entity)

# for entity in entity_dic[article]:
#    print('Entity ', entity)
# while article == triple_article:
# print(article, ': Artikel gefunden')
# triple_line = triple_line = triple_f.readline()
# triple_article = triple_line.replace('>', '/').split('/')[4].replace('_', ' ')
# break

#     while triple_line:
#         for article in entity_dic:
#             #triple_line = triple_f.readline()
#             triple_article = triple_line.replace('>', '/').split('/')[4].replace('_', ' ')
#             while article == triple_article: # if article == triple_article:
#                 print(article, ': Artikel gefunden')
#                 triple_entity = triple_line.replace('>', '/').split('/')[9].replace('_', '')
#                 for entity in entity_dic[article]:
#                     if triple_entity in entity_dic[article][entity]:
#                         print(triple_entity, ': Entity gefunden ')
#                         df = df.append({'Article': article, 'Entity': triple_entity,
#                                         'Sentence': triple_line.replace('>', '/').split('/')[10]}, ignore_index=True)
#                     triple_line = triple_f.readline()
#                     triple_entity = triple_line.replace('>', '/').split('/')[9].replace('_', '')
#                 break
# print(df)
#
# for line in triple_file:
#     for article in entity_dic:
#         print(article)
