import pandas as pd
import argparse

parser = argparse.ArgumentParser()
#todo implement argparse

data = pd.read_csv('../../../comp/1216_info_comp.csv', sep=';')
sum_amount_values = data['amount_values'].sum(0)
sum_amount_entities = data['amount_entities'].sum(0)
sum_amount_links = data['amount_links'].sum(0)
sum_amount_link_article_match = data['amount_link_article_match'].sum(0)
print(f'Sum of all given entities in the infoboxes: {sum_amount_values} (included those, which are given by the template, but are not used)')
print(f'Sum of all values: {sum_amount_entities}')
print(f'Sum of all values, which contain a link: {sum_amount_links}')
print(f'Sum of all values, which links also appear in the article as link: {sum_amount_link_article_match}')
print(f'{(sum_amount_entities/sum_amount_values)*100} % of all given infobox entites contain a value.')
# based on sum_amount_entities - only those entites which contain something
print(f'{(sum_amount_links/sum_amount_entities)*100} % of all infobox values contain a link.')
print(f'{(sum_amount_link_article_match/sum_amount_entities)*100} % of the infobox values are links which appear in the article .')
print(f'{(sum_amount_link_article_match/sum_amount_links)*100} % of all links appear in the article')