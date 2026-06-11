from fastapi import FastAPI
from psycopg2._psycopg import cursor
from pydantic import BaseModel
import psycopg2


app = FastAPI()


def get_connection():
    try:
        connect_db = psycopg2.connect(
        dbname="KongoPay",
        user="postgres",
        password="postgres123",
        host="localhost",
        port=5432
        )
        print("Connexion réussie!")
        return connect_db

    except Exception as error:
     print(f"Erreur de connexion à la base de données: {error}")
     return None

class inscription(BaseModel):
    name: str
    surname: str
    phone_number: str
    national_card:str
    account_type:str
    password:str


@app.post("/inscription")
def inscription(data: inscription):
    connection = get_connection()
    if connection is None:
        return {"message": "Erreur de connexion"}
    cursor = connection.cursor()
    cursor.execute('SELECT*FROM "USERS" WHERE phone_number = %s', (data.phone_number,))
    result = cursor.fetchone()
    if result is not None:
        return{"message":"Ce numéro est déjà utilisé"}
    cursor.execute(
        'INSERT INTO "USERS" (name,surname,phone_number,national_card,account_type,password) VALUES (%s,%s,%s,%s,%s,%s) RETURNING id_users',
        (data.name,data.surname,data.phone_number,data.national_card,data.account_type,data.password)
    )

    user_id = cursor.fetchone()[0]
    cursor.execute('INSERT INTO "WALLETS" (balance,id_users) VALUES (0,%s)', (user_id,))



    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Compte créé avec succès"}
