import pandas as pd
import argparse

#parser = argparse.ArgumentParser()
#parser.add_argument('-comp_path', help='Path to result file which contains all counter information')
#args = parser.parse_args()
#path = args.comp_path
# path= '../../../comp/1216_info_comp.csv'

data1 = pd.read_csv('../data/comp_infobox/res/124_comp.csv', sep=';')
data2 = pd.read_csv('../data/comp_infobox/res/1801_comp_918596.csv', sep=';')
data3 = pd.read_csv('../data/comp_infobox/res/2012_comp_small.csv', sep=';')

print(data1.shape)
print(data2.shape)
print(data3.shape)

# concat total df
frame  = [data1, data2, data3] # add data
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

print(f'Amount Properties: {amount_properties}')
print(f'Amount Values: {amount_entites}')
print(f'Amount Links: {amount_links}')
print(f'Amount Links which appear in the articles {amount_link_article_match}')

print(f'The Infobox Templates contain {amount_properties} properties')
print(f'{round(amount_entites/amount_properties *100, 2)} % of these properties do have a value. (entities/properties)')
print(f'{round(amount_links/amount_entites *100, 2)} % of those values are links. (links/entities)')
print(f'{round(amount_link_article_match/amount_links *100, 2)} % of those links appear in the article. (match/link)')
print(f'{round(amount_link_article_match/amount_entites*100, 2)} % of all values are links which appear in the article, too. (match/entities)')

#infobox
column_link_match = data_total["amount_link_article_match"]
column_link_match = column_link_match.replace(0, pd.np.nan).dropna()
print("There are " + str(column_link_match) + " infoboxes with links, which appear in the articles too.")
print("Mean: " + str(column_link_match.mean()))

