import requests
from lxml import etree
import csv
 
url = 'https://www.fifa.com/fifa-world-ranking/'
 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}
 
try:
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        parser = etree.HTMLParser()
        tree = etree.fromstring(response.content, parser)
        
        # Найдем таблицу с данными с помощью XPath
        table = tree.xpath('//table[@class="table tbl-ranking"]')[0]
        
        # Извлечем заголовки таблицы
        headers = [th.text for th in table.xpath('.//th')]
        
        # Извлечем данные из строк таблицы
        rows = table.xpath('.//tr')
        
        data = []
        for row in rows:
            row_data = [td.text.strip() for td in row.xpath('.//td')]
            data.append(row_data)
        
        with open('fifa_ranking_data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)
        
        print('Данные успешно сохранены в CSV-файл.')
    else:
        print('Ошибка запроса: код состояния', response.status_code)
        
except requests.exceptions.RequestException as e:
    print('Ошибка при отправке HTTP запроса:', e)
except (etree.ParserError, etree.XPathError) as e:
    print('Ошибка при парсинге HTML:', e)
except (IOError, csv.Error) as e:
    print('Ошибка ввода-вывода или CSV:', e)