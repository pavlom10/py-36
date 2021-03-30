import requests
from bs4 import BeautifulSoup

# определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']
URL = 'https://habr.com/ru/all'

if __name__ == '__main__':
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')

    for article in articles:
        title_element = article.find('a', class_='post__title_link')
        title_text = title_element.text.strip()
        title_link = title_element.attrs.get('href')
        title_date = article.find(class_='post__time').text

        preview_text = article.text.lower()

        response = requests.get(title_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.find('article').text.lower()

        for word in KEYWORDS:
            if word in preview_text or word in text:
                print(title_date, '-', title_text, '-', title_link)
                break