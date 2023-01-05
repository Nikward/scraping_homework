import requests
from bs4 import BeautifulSoup
import lxml
from fake_headers import Headers
import json
import re
import time

pattern = re.compile('([Dd]jango|[Ff]lask)')

def get_headers():
# Функция генерирует параметры для имитации запроса как у браузера
    return Headers(browser='firefox', os='win').generate()
def get_html(url):
# Функция возвращает html страницу
    req = requests.get(url, headers=get_headers()).text
    return BeautifulSoup(req, 'lxml')
def save_json(name_file, result_dict):
    with open('all_vacans.json', 'a', encoding='utf-8') as file:
        json.dump(result_dict, file, indent=4, ensure_ascii=False)
def get_number_page(url):
# функция возвращает максимальное число страниц
    html = get_html(url)
    return int(html.find('div', class_='pager').find_all('span')[-3].text)


def get_data(soup):
    vacancy_list = soup.find(class_='vacancy-serp-content')
    vacancy_tags = vacancy_list.find_all('div', class_='serp-item')
    result_file = []
    count = 0
    for vac in vacancy_tags:
        vac_href = vac.find(class_='serp-item__title').get('href')
        html_href = get_html(vac_href)
        description_href = html_href.find('div', class_='vacancy-description').text
        if re.search(pattern, description_href):
            name_compeny_vac = vac.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace(' ', ' ')
            vac_city = vac.find('div', class_='vacancy-serp-item__info').find('div', attrs={'data-qa':'vacancy-serp__vacancy-address'}).contents[0]
            try:
                vac_salary = vac.find('span', class_='bloko-header-section-3').text.replace(' ','')
            except:
                vac_salary = ''
            result_file.append({
                'href': vac_href,
                'company': name_compeny_vac,
                'city': vac_city,
                'salary': vac_salary
            })
            count += 1
            print(f"Итерация №{count}")
            time.sleep(3)
    save_json('all_vacancies', result_file)
def start_parsing(number_page=1):
    for page in range(number_page):
        URL = f'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={page}'
        HTML = get_html(URL)
        get_data(HTML)
        print(f'Страница № {page+1} просмотрена')

if __name__ == '__main__':
    start_parsing()