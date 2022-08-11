from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import csv



base_urls = 'https://nambafood.kg/cafe'

def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    return soup



def get_list_cafe_urls():
    list_cafe = []
    cafe = get_soup(base_urls).findAll('a', class_="cafe-item")
    for el in cafe:
        cafe_url = el.get("href")
        list_cafe.append(urljoin(base_urls,cafe_url))
    return list_cafe




def get_list_dict_food():
    list_dict_food = []

    for el_cafe in get_list_cafe_urls():
        for el in get_soup(el_cafe).findAll("span", class_="section--container"):

            for item in el.findAll('div',class_="card--item"):
                dict_food = {}
                try:
                    dict_food['Категория'] = ' '.join(el.find('h2', ).text.split())
                    dict_food['Фото'] = urljoin(el_cafe,item.find('img').get('src'))
                    dict_food['Имя'] = ' '.join(item.find('div', class_="card--item--title").text.split())
                    dict_food['Описание'] = ' '.join(item.find('div', class_="card--item--description").text.split())
                    dict_food['Цена'] = ' '.join(item.find('div', class_="price").text.split())
                    list_dict_food.append(dict_food)
                except AttributeError:
                    break
    return list_dict_food

#s = get_list_dict_food()
#print(1)

with open('food.csv', 'w', newline='') as csvfile:
    fieldnames = ['Имя', 'Описание', 'Категория', 'Цена', 'Фото']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for el in get_list_dict_food():
        try:
            writer.writerow(el)
        except UnicodeEncodeError:
            print(el)