import requests
from bs4 import BeautifulSoup
import json
import re

def get_csgo_items():
    with open("output.txt", "w") as file:
        # Чтение значений из файла config.txt
        with open("config.txt", "r") as config_file:
            config_data = json.load(config_file)
            parse_count = config_data["parse count"]
            minimal_wear_range = config_data["minimal wear"]
            factory_new_range = config_data["factory new"]
            well_worn_range = config_data["well-worn"]
            field_tested_range = config_data["field-tested"]
            battle_scared_range = config_data["battle_scared"]
            min_price_for_skins = config_data["min_price_for_skins"]
            max_price_for_skins = config_data["max_price_for_skins"]
            min_lots = config_data["min_lots"]

        for i in range(1, int(parse_count)):
            url = f"https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=tag_normal&category_730_Quality%5B%5D=tag_strange&category_730_Quality%5B%5D=tag_unusual&category_730_Quality%5B%5D=tag_unusual_strange&category_730_Rarity%5B%5D=tag_Rarity_Rare_Weapon&category_730_Rarity%5B%5D=tag_Rarity_Common_Weapon&category_730_Rarity%5B%5D=tag_Rarity_Mythical_Weapon&category_730_Rarity%5B%5D=tag_Rarity_Uncommon_Weapon&category_730_Rarity%5B%5D=tag_Rarity_Legendary_Weapon&category_730_Rarity%5B%5D=tag_Rarity_Ancient_Weapon&appid=730#p{i}_popular_desc"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            listings = soup.find_all("a", class_="market_listing_row_link")
            for item in listings:
                name = item.find("span", class_="market_listing_item_name").text
                quantity = item.find("span", class_="market_listing_num_listings_qty").text
                price = item.find("span", class_='normal_price').text.split()[2].replace('$', '') # Получение первого значения цены
                quality = re.search(r"\((.*?)\)", name).group(1)  # Извлечение значения из скобок
                quantity = int(quantity.replace(",", ""))
                item_link = soup.find("a", class_='market_listing_row_link').get('href')
                if quantity > min_lots:
                    item_link = item.get("href")
                    if item_link and float(price) < int(max_price_for_skins) and float(price) > int(min_price_for_skins):
                        if quality == 'Factory New':
                            output = f"{factory_new_range} {item_link}"
                            file.write(output + "\n")
                        elif quality == 'Well-Worn':
                            output = f"{well_worn_range} {item_link}"
                            file.write(output + "\n")
                        elif quality == 'Field-Tested':
                            output = f"{field_tested_range} {item_link}"
                            file.write(output + "\n")
                        elif quality == 'Battle-Scarred':
                            output = f"{battle_scared_range} {item_link}"
                            file.write(output + "\n")
                        elif quality == 'Minimal Wear':
                            output = f"{minimal_wear_range} {item_link}"
                            file.write(output + "\n")
                        else:
                            output = f"{item_link}"
                            file.write(output + "\n")




get_csgo_items()