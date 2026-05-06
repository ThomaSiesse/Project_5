from pymongo import MongoClient
import bcrypt
from os import getenv
from dotenv import load_dotenv

# Fonction pour créer l'utilisateur
def create_user(username):
    # Collecte des informations de l'utilisateur
    password = input("Entrez le mot de passe : ")
    role = input("Entrez le rôle (admin/developer/doctor/medical staff):")

    # Hash du mot de passe
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Stockage dans MongoDB
    db = get_db()
    users_collection = db['users']
    users_collection.insert_one({'username': username, 'password': hashed_password, 'role' : role})

    print("✅ User created successfully!")

def login(username):
    # Collecte des informations de l'utilisateur
    password = input("Entrez votre mot de passe : ")

    # Récupération de l'utilisateur depuis MongoDB
    db = get_db()
    users_collection = db['users']
    user = users_collection.find_one({'username': username})
    #vérifie si l'utilisateur existe et si le mot de passe correspond
    while True:
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            print(f"✅ Login successful! Welcome {username} with role {user['role']}.")
            return user['role']
        else:
            print("❌ Invalid username or password.")
            return None
#Fonction de vérification des permissions
def check_permissions(role,action):
    #permission
    permission = { 'admin': ['create', 'read', 'update'],
                   'doctor': ['create', 'read', 'update'],
                   'medical_staff': ['read'],
                   'developer' : ['create', 'read', 'update', 'delete']
                   }
    if role in permission and action in permission[role]:
        return True
    else:
        return False
#connection MongoDB
def get_db():
    uri = getenv("MONGODB_URI")
    client = MongoClient(uri, tlsAllowInvalidCertificates=True)
    return client['healthcare']
#Execution du script
if __name__ == "__main__":
    load_dotenv() #charge les données
    db = get_db() #connection à la base de données
    users_collection = db['users'] #accès à la collection des utilisateurs
    username = input("Entrez votre nom d'utilisateur: ") 
    user = users_collection.find_one({'username': username})
    print(user)
    if user:
        print("✅ Utilisateur trouvé - login")
        role = login(username)
    else:
        print("❌ Utilisateur non trouvé - création")
        create_user(username)
        role = login(username)
        if role:
            check_permissions(role, 'read')