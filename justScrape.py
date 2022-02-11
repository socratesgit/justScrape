from bs4 import BeautifulSoup
import requests
import time
import json

with open("queries.json","r") as f:
    queries = json.load(f)

session = requests.Session()

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
 'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
 'Accept':'text/html,application/xhtml+xml,application/xml;'
 'q=0.9,image/webp,*/*;q=0.8'}

url_just_eat = "https://www.justeat.it"

list_restaurant = list()
id_set = set()

for town,url in queries.items():
    time.sleep(5)
    html = session.get("https://www.justeat.it/area/{}".format(url),headers=headers)
    soup = BeautifulSoup(html.text,features="html.parser")
    canonical = soup.find("link",{"rel":"canonical"})

    for restaurant_info in soup.find_all("section", {"data-test-id" : "restaurant"}):
        
        num_id = restaurant_info["data-restaurant-id"]
        if num_id in id_set:
            break
        else:
            id_set.add(num_id)
        name = restaurant_info.find("h3",{"data-test-id" : "restaurant_name"}).get_text().strip()
        print("processing: ("+str(num_id)+"), "+name)
        url_menu = restaurant_info.a["href"]
        menu_raw = session.get(url_just_eat+restaurant_info.a["href"],headers=headers)
        menu_clean = BeautifulSoup(menu_raw.text,features="html.parser")

        dishes = list()

        for dish in menu_clean.find_all("div",{"class":"c-menuItems-content"}):
            name_dish_tag = dish.find("h3",{"data-test-id":"menu-item-name"})
            if name_dish_tag:
                name_dish = name_dish_tag.get_text().strip()
            else:
                name_dish = "NULL"
            price_tag = dish.find("p",{"class":"c-menuItems-price notranslate"})
            if price_tag:
                price = price_tag.get_text().strip().replace("&nbsp;"," ").replace("u20ac","")
            else:
                price = "NULL"
            ingredients_tag = dish.find("p",{"data-test-id":"menu-item-description"})
            if ingredients_tag:
                ingredients = ingredients_tag.get_text().strip()
            else:
                ingredients = "NULL"
            dishes.append({
                'name' : name_dish,
                'price'  : price,
                'ingredients' : ingredients
            })
        
        list_restaurant.append({
            'num_id' : num_id,
            'name' : name,
            'town' : town,
            'url_menu' : url_menu,
            'list_dish' : dishes
        }) 


with open('data.json', 'a', encoding='utf-8') as f:
    json.dump(list_restaurant, f,ensure_ascii=True,indent=4)

    






