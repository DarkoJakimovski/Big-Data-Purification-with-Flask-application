# Рефакторирана верзија 3 со точен клуч и вредности

import requests
import re
from cleanco import cleanco


# Дефинирање на Flask API endpoint
GET_URL = "http://localhost:5000/companies"
POST_URL = "http://localhost:5000/companies"

# Исчитување на имињата на компаниите од локалната SQLite база на податоци со GET request
response = requests.get(GET_URL)
companies = response.json()["companies"]

# Процесирање и прочистување на имиња на компании
cleaned_companies = {}
for company in companies:
    # Отстранување на запирките и целиот текст по запирките
    name = re.sub(r',.*', '', company["name"])

    # Отстранување на заградите и текстот во нив
    name = re.sub(r'\(.*\)', '', name)

    # Отстранување на наводниците
    name = re.sub(r'\"', '', name)

    # Отстранување на цртичките кога тоа не е дел од името на компанијата
    name = re.sub(r'\s-\s', ' ', name)

    # Прочистување на името на компанијата да биде без легален ентитет
    name = cleanco(name).clean_name()

# Нормализирање на името на компанијата

    # Името да биде само со почетни големи буѕкви
    name = name.title()

    # Акроними со големи букви
    name = re.sub(r'\b([A-Z]+)\b', lambda match: match.group(1).upper(), name)

    # Прочистеното име како клуч, а останатите атрибути како вредности
    cleaned_companies = {
        name: {
        "country_iso": company["country_iso"],
        "city": company["city"],
        "nace": company["nace"],
        "website": company["website"]
        }
    }

    # # Додавање со инкрементација во еден документ со име како клуч + останати атрибути како вредности
    #    cleaned_companies[name] = {
    #        "country_iso": company["country_iso"],
    #        "city": company["city"],
    #        "nace": company["nace"],
    #        "website": company["website"]
    #    }

    # Запишување на резултатот со POST request до Mongo базата на податоци
    response = requests.post(POST_URL, json=cleaned_companies)

    # Проверка дали барањето е успешно
    if response.json()["success"]:
        print(f"Successfully added {cleaned_companies} to MongoDB!")
    else:
        print(f"Failed to add {cleaned_companies} to MongoDB.")
    if response.status_code != 201:
        print(f"Error: {response.content}")
    else:
        print(f"{name} added to the database.")

print("THE PROJECT IS SUCCESSFULLY FINISHED")
