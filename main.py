
import json
import requests
from bs4 import BeautifulSoup
import fake_headers
from pprint import pprint

def gen_headers():
    headers_gen = fake_headers.Headers(os="macos", browser="safari")
    return headers_gen.generate()

main_response = requests.get("https://spb.hh.ru/search/vacancy?L_save_area=true&text=python%2C+django%2C+flask&excluded_text=&area=1&area=2&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=50&hhtmFrom=vacancy_search_filter", headers=gen_headers())
main_html_data = main_response.text
main_soup = BeautifulSoup(main_html_data, "lxml")

vacancy_list_tag = main_soup.find_all(class_="vacancy-serp-item__layout")
parsed_vacancy = []

for vacancy in vacancy_list_tag:
    # title = vacancy.find("span", {"data-qa":"serp-item__title"}).text
    link = vacancy.find("a")["href"]
    salary = vacancy.find("span", {"data-qa":"vacancy-serp__vacancy-compensation"})
    if salary:
        salary = salary.text.strip()
    else:
        salary = 'Не указана'
    company = vacancy.find("a", {"data-qa": "vacancy-serp__vacancy-employer"}).text.strip()
    address = vacancy.find("div", {"data-qa":"vacancy-serp__vacancy-address"}).text
    town = address.split(",")[0]

    parsed_vacancy.append(
        {
        # 'Вакансия': title,
        'Компания': company,
        'Ссылка': link,
        'Зарплата': salary,
        'Город': town
    })

    pprint(parsed_vacancy)

with open("vacancy.json", "w", encoding='utf-8') as file:
    json.dump(parsed_vacancy, file, ensure_ascii=False, indent=4)

