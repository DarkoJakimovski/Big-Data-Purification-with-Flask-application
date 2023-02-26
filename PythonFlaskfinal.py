# Flask  апликација со функција за читање податоци од локална SQLite база на податоци што поддржува само GET метод
# и втора функција за запишување податоци во MongoDB што поддржува само POST метод


# Во овој код, дефинираме Flask апликација со единствена рута/компании што поддржува само
# GET метод. Кога ќе се направи барање за GET до оваа крајна точка, се повикува функцијата read_companies().
# Оваа функција отвора врска со SQLite базата на податоци , создава објект на курсорот и извршува
# SQL барање за избор податоците од табелата "companies". Резултатите потоа се претвораат во
# листа на речници, при што секој речник претставува еден ред во табелата.
# Конечно, курсорот и врската со базата се затворени и списокот со речници се враќа
# како JSON одговор.



### Рефакторирана верзија 2 што работи

import sqlite3
import pymongo
from flask import Flask, request, jsonify

app = Flask(__name__)

# API функција што чита од SQLite база на податоци

@app.route("/companies", methods = ["GET"]) #route() функција од Flask класа како декоратор
def read_companies():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM companies LIMIT 5") # SQL query (LIMIT за поконкретно)
    companies = []
    for row in c.fetchall():
        company = {
            "id": row[0],
            "name": row[1],
            "country_iso": row[2],
            "city": row[3],
            "nace": row[4],
            "website": row[5]
        }
        companies.append(company) # изјава во loop со append() метод за листа од речници
    c.close()
    conn.close()
    return jsonify({"companies": companies})


# API функција што запишува податоци во MongoDB

@app.route("/companies", methods=["POST"])
def add_company():
    conn = pymongo.MongoClient()  # конекција со MongoDB
    db = conn["mydatabase"] # селектирање база на податоци
    collection = db["cleaned_companies"] # селектирање колекција
    data = request.get_json()
    result = collection.insert_one(data)

    # JSON одговор кој покажува успех или неуспех
    if result.inserted_id:
        return jsonify({"success": True}), 201
    else:
        return jsonify({"success": False}), 400


if __name__ == "__main__": # Python скрипта како главна програма
    app.run(debug=True)

# Flask апликацијата е хостирана на локален сервер кога ќе ја извршиме со командата app.run(debug=True)
# Методот app.run () започнува локален сервер кој по дифолт е localhost:5000

# Кога е овозможен режимот за дебагирање,Flask апликацијата автоматски ќе се вчита кога ќе се измени кодот
# и исто така ќе обезбеди подетални пораки за грешки во апликацијата.


