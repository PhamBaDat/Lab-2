import csv
import json
import xml.etree.ElementTree as ET
import random
import pandas as pd

# with open("memes_dataset.csv", encoding = "utf-8") as fh:
#     fh.seek(0)
#     title = next(fh)
#     title = title.split(",")
#     title = [col.strip() for col in title]

#     print(title)

# while True:
#     next(fh)
#     print(fh.readline())

DATASET_PATH2 = "currency.xml"
DATASET_PATH = "books-en.csv"
OUT_PATH1 = "библиографические ссылки для 20 случайных записей.json"
OUT_PATH2 = "Извлечение данных.json"
OUT_PATH3 = "Перечень издательств без повторений."

dataset = open("books-en.csv")

def get_title(dataset):
    dataset.seek(0) 
    title = next(dataset)
    title = title.split(";")
    title = [col.strip() for col in title]

    return title

def get_object(line, title):
    fields = []
    value = ""

    for char in line:
        if char != ";":
            value += char
        else:
            fields.append(value)
            value = ""

    fields.append(value.strip())
    result = {col: f for col, f in zip(title, fields)}
    return result   

def filter_year (dataset, title, year):
    filtered = []

    for line in dataset:
        obj = get_object(line, title)
        year_value = obj["Year-Of-Publication"]

        if year_value == str(year):
            filtered += [obj]

    dataset.seek(0)
    return filtered

def count_title(dataset, title):
    filter = []
    count = 0

    for line in dataset:
        obj = get_object(line, title)
        book_name = obj['Book-Title']

        if len(book_name) > 30:
            count += 1
            # print(f'{count}. {book_name}')
    
    dataset.seek(0)
    return count

def filter_author(dataset, title, author):
    filter = []

    for line in dataset:
        obj = get_object(line, title)
        author_name = obj['Book-Author']
        price = obj['Price'].replace(',', '.')

        if author_name == author and float(price) >= 200:
            filter += [obj]

    dataset.seek(0)
    return filter

def get_object_advance(line, title, i):
    fields = []
    obj = get_object(line, title)

    for col in obj:
        if col == 'Book-Title' or col == 'Book-Author' or col == 'Year-Of-Publication':
            fields.append(obj[col])
            
    result = f'{i}. {fields[1]}.{fields[0]} - {fields[2]}'
    return result   

def filter_title(dataset, title):
    filter = []
    i=0
    
    num_sample = 20
    random_lines = []
     
    for line in dataset:
        if len(random_lines) <= num_sample:
            random_lines.append(line)
        else:
            idx = random.randint(0, len(random_lines) - 1)
            if random.random() < num_sample / (num_sample) + 1:
                random_lines[idx] = line

    for line in random_lines:
        obj = get_object_advance(line, title, i)
        filter += [obj]

        i+=1

    dataset.seek(0)
    return filter

def most_popular(data):
    ...
                    
def get_data():
    xml_data = file.read()
    num = []
    char = []
    fields = []     

    root = ET.fromstring(xml_data)

    valutes = root.findall('Valute')
    print(f'Amount of Valute: {len(valutes)}')

    for valute in valutes:
        id_value = valute.attrib['ID']
        num_code = valute.find('NumCode').text
        char_code = valute.find('CharCode').text
        nominal = valute.find('Nominal').text
        name = valute.find('Name').text
        value = valute.find('Value').text
        Vunit_rate = valute.find('VunitRate').text

        # line = f'Valute ID: {id_value}, NumCode: {num_code}, CharCode: {char_code}, Nominal: {nominal}, Name: {name}, Value: {value}, VunitRate: {Vunit_rate}'
        line = f'NumCode: {num_code} - CharCode: {char_code}'
        fields.append(line)
        # num.append(num_code)
        # char.append(char_code)

    return fields

def get_publisher(dataset, title):
    fields = []

    for line in dataset:
        obj = get_object(line, title)
        for col in obj:
            c=0
            if col == 'Publisher':
                for a in fields:
                    if obj[col] == a:
                        c=1
                if c == 0:
                    fields.append(obj[col])
    
    return fields


if __name__ == "__main__":
    with open(DATASET_PATH, encoding = "utf-8") as fh:
        title = get_title(dataset)
        print(f'Количество записей, у которых в поле Название строка длиннее 30 символов: {count_title(dataset, title)}')
        print()
   
        # name = input("Author name: ")
        name = 'Amy Tan'
        print(f'List of books priced over 200 rubles - Author name = {name}')
        res1 = (filter_author(dataset, title, name))
        print (f'Количество записей: {len(res1)}')
        for r in res1:
            print(r)
        print()

        res2 = (filter_title(dataset, title))
        res2 = json.dumps(res2, indent = 4)
        with open(OUT_PATH1, "w") as out:
                out.write(res2)
        print()

    with open (DATASET_PATH2, 'r', encoding = 'windows-1251') as file:       
        print("Извлечь данные из файла currency.xml: ")
        res3 = get_data()
        for r in res3:
            print(r)
        print()
        # res3 = json.dumps(res3, indent = 4)
        # with open (OUT_PATH2, "w") as out:
        #     out.write(res3)
        
    
    res4 =  get_publisher(dataset, title)
    res4 = json.dumps(res4, indent = 4)
    with open (OUT_PATH3, "w") as out:
        out.write(res4)

    

        