import os
import requests
import json
from bs4 import BeautifulSoup
os.system("clear")


# Получения HTML
def get_html(url, header):
    responce = requests.get(url, headers=header)

    if responce.status_code != 200:
        return f"Error: {responce.status_code}"
    else:
        return responce.text 
    


# data = get("")
# with open ('index.html', 'w', encoding='utf-8') as file:
#     file.write(data)


# Обработка  HTML

def proccessing(html):
    soup = BeautifulSoup(html, "lxml").find('div', {'class':'product-grid'})
    products = soup.find_all('div', {'class': 'product-card'})


    data = []
    for product in products:
        a = product.find('a')
        product_url = 'https://www.lcwaikiki.kz' + a.get('href')
        product_id = a.get('data_optionid') # это класс
        product_title = a.get('title')

        product_price = a.find('div', {'class':'product-price'}).find(  # Это параметр
        'span', {'class': 'product-price__price'}).text
        
        data.append({
            'product_url': product_url,
            'product_id' : product_id,
            'product_title': product_title,
            'product_price': product_price.replace(' ', ' ') #\xa0
        })

    return data 


# Запуск кода (Уникальна)

def main():
    header = {
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0"
    }
    data = []
    for page in range(1, 10):

        url = f"https://www.lcwaikiki.kz/ru-RU/KZ/tag/tshirt-7-5?PageIndex={page}"

        if page <2:
                url = 'https://www.lcwaikiki.kz/ru-RU/KZ/tag/tshirt-7-5'

        html = get_html(url, header)
        soup = proccessing(html)

        data.extend(soup)
        print(f"Page: {page} | {url[0:len(url)//2]}...")


    with open ('data.json', 'w') as file:
        json.dump(soup, file, indent=4, ensure_ascii=False)


main()

    

