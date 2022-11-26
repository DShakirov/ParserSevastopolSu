from time import strftime

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

import os

def parse(parsesite, file_name):

    result_list = {'title': [], 'href': [], 'review': []}
    r = requests.get(parsesite)
    soup = bs(r.text, 'html.parser')
    news_title = soup.find_all('h3', class_='title')
    news_review = soup.find_all('div', class_='review')

    print('Страница загружена.')

    for news, news1 in zip(news_title, news_review):

        result_list['title'].append(news.a['title'])
        result_list['href'].append('http://sevastopol.su'+news.a['href'])
        result_list['review'].append(news1.get_text())


    print('Новости со страницы обработаны')

    df = pd.DataFrame(data=result_list)
    df.to_csv(file_name, mode='a', encoding='cp1251')

    print('Изменения в файл успешно внесены')

    return result_list


if not os.path.exists('results'):
    os.mkdir('results')
unix = str(strftime('[%d-%m-%Y]'))
folder = f'results/{unix}'
if not os.path.exists(folder):
    os.mkdir(folder)

file_name = f'{folder}/sevastopol-su.csv'

if __name__ == '__main__':

    for i in range (4):
        parsesite = 'https://sevastopol.su/all-news/%D0%A1%D0%B5%D0%B2%D0%B0%D1%81%D1%82%D0%BE%D0%BF%D0%BE%D0%BB%D1%8C?page=' + str(i)

        parse(parsesite, file_name)



