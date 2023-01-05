import requests
from bs4 import BeautifulSoup
import lxml
from fake_headers import Headers
import json
import re

URL = r'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
pattern = re.compile('([Dd]jango|[Ff]lask)')

def get_headers():
# Функция генерирует параметры для имитации браузера
    return Headers(browser='firefox', os='win').generate()




def get_data(url):
    req = requests.get(url, headers=get_headers()).text
    soup = BeautifulSoup(req, 'lxml')
    vacancy_list = soup.find(class_='vacancy-serp-content')
    vacancy_tags = vacancy_list.find_all('div', class_='serp-item')
    result_dict = []
    for vac in vacancy_tags:
        vac_href = vac.find(class_='serp-item__title').get('href')
        req_href = requests.get(vac_href, headers=get_headers()).text
        html_href = BeautifulSoup(req_href, 'lxml')
        description_href = html_href.find('div', class_='vacancy-description').text
        if re.search(pattern, description_href):
            name_compeny_vac = vac.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace(' ', ' ')
            vac_city = vac.find('div', class_='vacancy-serp-item__info').find('div', attrs={'data-qa':'vacancy-serp__vacancy-address'}).contents[0]
            try:
                vac_salary = vac.find('span', class_='bloko-header-section-3').text.replace(' ','')
            except:
                vac_salary = ''
            result_dict.append({
                'href': vac_href,
                'company': name_compeny_vac,
                'city': vac_city,
                'salary': vac_salary
            })

    with open('all_vacans.json','w', encoding='utf-8') as file:
        json.dump(result_dict, file, indent=4, ensure_ascii=False)




if __name__ == '__main__':

    get_data(URL)