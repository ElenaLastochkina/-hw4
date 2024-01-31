import requests
from lxml import etree
import csv
 
url = 'http://books.toscrape.com/'
 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}
 
try:
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        parser = etree.HTMLParser()
        tree = etree.fromstring(response.content, parser)
        
        rows = tree.xpath('//table[@class="table table-striped"]//tr')
        
        with open('book_data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            for row in rows:
                data = row.xpath('.//text()')
                data = [item.strip() for item in data if item.strip()]
                
                if len(data) >= 3:
                    writer.writerow(data)
                    
        print('Данные успешно сохранены в CSV-файл.')
    else:
        print('Ошибка запроса: код состояния', response.status_code)
        
except requests.exceptions.RequestException as e:
    print('Ошибка при отправке HTTP запроса:', e)
except (etree.ParserError, etree.XPathError) as e:
    print('Ошибка при парсинге HTML:', e)
except (IOError, csv.Error) as e:
    print('Ошибка ввода-вывода или CSV:', e)