from fastapi import FastAPI
from psycopg2._psycopg import cursor
from pydantic import BaseModel
import psycopg2

# Création de l'application FastAPI
app = FastAPI()

# Vérification de la connexion à la base de données postgreSQL

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

# Class pour inscription

class inscription(BaseModel):
    name: str
    surname: str
    phone_number: str
    national_card:str
    account_type:str
    password:str


# Route inscription

@app.post("/inscription")
def inscription(data: inscription):

# Vérification de la connexion à la base de données

    connection = get_connection()
    if connection is None:
        return {"message": "Erreur de connexion"}
    cursor = connection.cursor()

# Vérification du numéro de téléphone avant création du nouvel utilisateur

    cursor.execute('SELECT*FROM "USERS" WHERE phone_number = %s', (data.phone_number,))
    result = cursor.fetchone()
    if result is not None:
        return{"message":"Ce numéro est déjà utilisé"}

# Création du nouvel utilisateur et récupérateur de l'id pour la création automatique du wallet

    cursor.execute(
        'INSERT INTO "USERS" (name,surname,phone_number,national_card,account_type,password) VALUES (%s,%s,%s,%s,%s,%s) RETURNING id_users',
        (data.name,data.surname,data.phone_number,data.national_card,data.account_type,data.password)
    )

# Récupération de l'id du nouvel utilisateur et création automatique de son portefeuille (wallet)

    user_id = cursor.fetchone()[0]
    cursor.execute('INSERT INTO "WALLETS" (balance,id_users) VALUES (0,%s)', (user_id,))

    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Compte créé avec succès"}

# Class connexion

class connexion(BaseModel):
    phone_number: str
    password: str

@app.post("/connexion")
def connexion(data: connexion):
    connection = get_connection()
    if connection is None:
        return {"message": "Erreur de connexion"}
    cursor = connection.cursor()
    cursor.execute('SELECT*FROM "USERS" WHERE phone_number = %s', (data.phone_number,))
    result = cursor.fetchone()
    if result is None:
        return {"message":'Numéro incorrect'}
    elif result[6] != data.password:
        cursor.execute('INSERT INTO "AUDIT_LOGS" (action_type,id_user) VALUES (%s,%s)', ('mauvais mot de passe',result[0]))
        connection.commit()
        return {"message":'mot de passe incorrect'}
    else:
        cursor.execute('INSERT INTO "AUDIT_LOGS" (action_type,id_user) VALUES (%s,%s)', ('connexion',result[0]))
        connection.commit()
        return {'message': "Vous êtes connectés", "id_users": result[0], "name": result[1], "surname": result[2]}
    cursor.close()
    connection.close()


class transfer_sender(BaseModel):
    balance:float
    id_wallet_sender: int
    phone_number_receiver:str
    
    
@app.post("/transfer_sender")
def transfer_sender(data: transfer_sender):
    connection = get_connection()
    if connection is None:
        return{"message": "Erreur de connexion"}
    cursor = connection.cursor()
    cursor.execute('SELECT*FROM "WALLETS" WHERE id_wallets = %s)', (data.id_wallet_sender,))
    wallet_sender = cursor.fetchone()
    if wallet_sender is None:
        return {"message": "Portefeuille émetteur introuvable"}

    cursor.execute('SELECT*FROM "USERS" WHERE phone_number = %s', (data.phone_number_receiver,))
    user_receiver = cursor.fetchone()
    if user_receiver is None:
        return {"message":"Numéro introuvable. Veuillez réessayer"}

    cursor.execute('SELECT*FROM "WALLETS" WHERE id_users = %s)', (user_receiver[0],))
    wallet_receiver = cursor.fetchone()
    if wallet_receiver is None:
        return {"message": "Portefeuille de dépôt introuvable"}


    if wallet_sender[1] < data.balance:
        return {"message": "Montant insuffisant"}
    elif data.balance > wallet_sender[3]:
        return {"message": "Attention. Plafond journalier atteint"}



    cursor.execute('UPDATE "WALLETS SET balance = balance -%s WHERE id_wallets = %s' , (data.balance,data.id_wallet_sender))
    cursor.execute('UPDATE "WALLETS" SET balance = balance + %s WHERE id_wallets = %s', (data.balance,wallet_receiver[0]))







    

        



