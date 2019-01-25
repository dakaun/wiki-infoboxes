import pandas as pd
import argparse

#parser = argparse.ArgumentParser()
#parser.add_argument('-comp_path', help='Path to result file which contains all counter information')
#args = parser.parse_args()
#path = args.comp_path
# path= '../../../comp/1216_info_comp.csv'

data1 = pd.read_csv('../../../infoboxes/comp_infoboxes/res/1801_comp_918596.csv', sep=';')
data2 = pd.read_csv('../../../infboxes/comp_infoboxes/res/2012_comp_small.csv', sep=';')
# data3 = pd.read_csv('../data/comp_infobox/res/2012_comp_small.csv', sep=';')

print(data1.shape)
print(data2.shape)
# print(data3.shape)

# concat total df
frame  = [data1, data2] # add data
data_total = pd.concat(frame, axis=0, ignore_index=True)

print("TOTAL DATA SHAPE: " + data1.shape)
# data_total:
print("There are " + str(data_total['article'].nunique()) +" unique articles.")
data_total = data_total[data_total['article'].duplicated()!=True] # todo how many infoboxes are there

amount_entites = data_total['amount_entities'].sum()
amount_link_article_match = data_total['amount_link_article_match'].sum()
amount_links = data_total['amount_links'].sum()
amount_properties = data_total['amount_properties'].sum()
#amount_values = data_total['amount_values'].sum()

print('Amount Properties: {}'.format(amount_properties))
print('Amount Values: {}'.format(amount_entites))
print('Amount Links: {}'.format(amount_links))
print('Amount Links which appear in the articles {}'.format(amount_link_article_match))

print('The Infobox Templates contain {} properties'.format(amount_properties))
print('{} % of these properties do have a value. (entities/properties))'.format(round(amount_entites/amount_properties *100, 2)))
print('{} % of those values are links. (links/entities)'.format(round(amount_links/amount_entites *100, 2)))
print('{} % of those links appear in the article. (match/link)'.format(round(amount_link_article_match/amount_links *100, 2)))
print('{} % of all values are links which appear in the article, too. (match/entities)'.format(round(amount_link_article_match/amount_entites*100, 2)))

#infobox
column_link_match = data_total["amount_link_article_match"]
column_link_match = column_link_match.replace(0, pd.np.nan).dropna()
print("There are " + str(column_link_match.shape) + " infoboxes with links, which appear in the articles too.")
print("Mean: " + str(column_link_match.mean()))

