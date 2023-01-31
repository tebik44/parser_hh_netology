import lxml as lxml
import json
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from pprint import pprint


def respone(response_text):
    soup = BeautifulSoup(response_text, features='lxml')

    link = soup.find_all(class_="serp-item__title")
    city = soup.find_all(attrs={'class': "bloko-text", 'data-qa': "vacancy-serp__vacancy-address"})
    sallary = soup.find_all(attrs={'data-qa': "vacancy-serp__vacancy-compensation"})
    company = soup.find_all(attrs={'data-qa': "vacancy-serp__vacancy-employer"})

    final_lst = list()
    for (link_,city_,sallary_,company_) in zip(link,city,sallary,company):
        final_lst.append(
            {
                'link' : link_['href'],
                'city' : city_.text,
                'sallary': sallary_.text,
                'company' : company_.text
            }
        )

    return final_lst

if __name__ == "__main__":
    headers = Headers(os="win", headers=True).generate()
    response_text = requests.get(
        'https://spb.hh.ru/search/vacancy?area=1&area=2&search_field=description&only_with_salary=true&text=Python+' \
        'django+flask&from=suggest_post&ored_clusters=true&enable_snippets=true',
        headers=headers).text
    final_lst = respone(response_text)
    with open("data.json", 'w', encoding='utf-8') as file:
        json.dump(final_lst, file, ensure_ascii=False, indent=3)
