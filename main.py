
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



# метод find_all() отобразит список всех articles(статей) и мы можем по этому списку итерироваться
# for vacancy_tag in vacancy_list_tag.find_all("serp-item serp-item_link"):
#     h3_tag = vacancy_tag.find("h3 data-qa", class_="bloko-header-section-3")
#     # a2_tag = h2_tag.find("a", class_="tm-title__link")
#     # time_tag = article_tag.find("time")
#
#     header = h3_tag.text.strip()

    # link_relative = a2_tag['href']
    # link_absolute = f'https://habr.com{link_relative}'
    # publication_time = time_tag['datetime']

    # full_article_response = requests.get(link_absolute, headers=gen_headers())
    # full_article_html_data = full_article_response.text
    # full_article_soup = BeautifulSoup(full_article_html_data, "lxml")
    # full_article_tag = full_article_soup.find("div", id="post-content-body")
    # full_article_text = full_article_tag.text.strip()

    # parsed_data = ({
    #     "header": header,
    # #     "link": link_absolute,
    # #     "pub_time": publication_time,
    # #     "text": full_article_text[:100]
    #     }
    # )
    # print(parsed_data)
