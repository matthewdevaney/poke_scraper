# import libraries
import os
import requests
from bs4 import BeautifulSoup


# location of pokemon image assets
#domain_pokemon_img = 'https://assets.pokemon.com/assets/cms2/img/pokedex/detail/'
domain_pokemon_img = 'https://cdn.bulbagarden.net/upload/e/ec/'
file_type_pokemon_img = 'png'

# create a list of three digit pokemon numbers
start_range = 1
end_range = 151

current_number = start_range
pokemon_id_list = []


while True:
    pokemon_id_list.append((3 - len(str(current_number))) * '0' + str(current_number))
    if end_range == current_number:
        break
    current_number += 1


# build a list of urls for pokemon images
pokemon_image_urls = []

for pokemon_id in pokemon_id_list:
    pokemon_image_urls.append(domain_pokemon_img + pokemon_id + 'MS.' + file_type_pokemon_img)


for n, url in enumerate(pokemon_image_urls):
    r = requests.get(url)
    r.raise_for_status()
    with open(os.getcwd() + '\\img\\' + str(n+1) + '_icon.png', 'wb') as f:
        f.write(r.content)
