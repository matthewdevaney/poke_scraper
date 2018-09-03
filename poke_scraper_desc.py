# import libraries
import os
import requests
from bs4 import BeautifulSoup
import pandas as p

# location of pokemon image assets
url_pokemon_profile = 'https://www.pokemon.com/us/pokedex/'

df = p.read_csv('pokemon_list.csv', header=None)
pokemon_list = df[0].tolist()

# create empty main dictionary
poke_dict = {}

for current_pokemon in pokemon_list:

    print(current_pokemon)

    # get soup object for the pokemon profile website
    r = requests.get(url_pokemon_profile + current_pokemon)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    sub_dict = {}

    # scrape pokemon profile
    poke_id = int(soup.find('div', {'class': 'pokedex-pokemon-pagination-title'}).get_text().strip().split('\n')[1]
                                                                                 .strip().replace('#', '')
                                                                                 .replace('#0', '').replace('#00', ''))
    sub_dict['id'] = poke_id
    sub_dict['name'] = soup.find('div', {'class': 'pokedex-pokemon-pagination-title'}).get_text().strip().split('\n')[0]
    sub_dict['description'] = soup.find_all('div', {'class': 'version-descriptions active'})[0].p.get_text()\
        .replace('\n', ' ').strip().replace('—', '-').replace('é', 'e')

    poke_attributes = soup.find_all('span', {'class': 'attribute-value'})
    sub_dict['height'] = poke_attributes[0].get_text()
    sub_dict['weight'] = poke_attributes[1].get_text()
    sub_dict['category'] = poke_attributes[3].get_text()
    sub_dict['overgrow'] = poke_attributes[4].get_text()

    poke_stats = soup.find_all('li', {'class': 'meter'})
    sub_dict['hp'] = int(poke_stats[0]['data-value'])
    sub_dict['attack'] = int(poke_stats[1]['data-value'])
    sub_dict['defense'] = int(poke_stats[2]['data-value'])
    sub_dict['specattack'] = int(poke_stats[3]['data-value'])
    sub_dict['specdefense'] = int(poke_stats[4]['data-value'])
    sub_dict['speed'] = int(poke_stats[5]['data-value'])

    poke_type = soup.find('div', {'class': 'dtm-type'})
    sub_dict['type'] = [x.get_text() for x in poke_type.find_all('a')]

    poke_weak = soup.find('div', {'class': 'dtm-weaknesses'})
    sub_dict['weakness'] = [x.get_text().strip() for x in poke_weak.find_all('a')]

    poke_dict[poke_id] = sub_dict

poke_df = p.DataFrame.from_dict(poke_dict, orient='index')
poke_df.to_csv('pokemon_data.csv', index=False)
