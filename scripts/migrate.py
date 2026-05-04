import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
from os import getenv   

# Functions Nettoyage données format object
def clean_strings(df):
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.strip().str.title()
    return df

#Fonctions Nettoyage données format numérique et date
def clean_data(df):
    
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce').astype('Int64')
    df['Billing Amount'] = pd.to_numeric(df['Billing Amount'],errors='coerce').round(2)
    df['Date of Admission'] = pd.to_datetime(df['Date of Admission'], errors='coerce')
    df['Discharge Date'] = pd.to_datetime(df['Discharge Date'], errors='coerce')
    df['Room Number'] = pd.to_numeric(df['Room Number'], errors='coerce').astype('Int64')
    return df
#Fonction Validation données
def validate_data(df):
    if ((df['Age'] > 0) & (df['Age'] < 150)).all():
        print ("✅ Age is valid ")
    else: 
        print ("❌ Age is invalid")
    if ((df['Gender'] == 'Male') | (df['Gender'] == 'Female')).all():
        print ("✅ Gender is valid ")
    else:
        print ("❌ Gender is invalid")
    if (df['Blood Type'].isin(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'])).all():
        print ("✅ Blood Type is valid ")
    else:
        print ("❌ Blood Type is invalid")
    if ((df['Date of Admission']) < (df['Discharge Date'])).all():
        print ("✅ Dates are valid ")
    else:
        print ("❌ Dates are invalid")
    if df['Billing Amount'].notna().all():
        print ("✅ Billing Amount is valid ")
    else:
        print ("❌ Billing Amount is invalid")
    if (df['Room Number'] > 0 ).all():
        print ("✅ Room Number is valid ")
    else:
        print ("❌ Room Number is invalid")

#Fonction de migration vers Mongo DB
def migrate(df, collection):
    collection.delete_many({}) #supprimme les doublons avant migration
    for col in df.columns:
        if (df[col].dtype == 'datetime64[ns]'):
            df[col] = df[col].dt.apply(lambda x: x.to_pydatetime())
    records = df.to_dict(orient='records')
    collection.insert_many(records)
    collection.create_index("Name")
    collection.create_index("Date of Admission")
    collection.create_index("Doctor")
    collection.create_index("Hospital")
    collection.create_index("Admission Type")
    print(f"✅ {len(records)} records migrated successfully!")

#Execution du script
if __name__ == "__main__":
    #Load .env
    load_dotenv()

    # Load data
    df = pd.read_csv('data/healthcare_dataset.csv')
    
    # Clean and validate data
    df = clean_strings(df)
    df = clean_data(df)
    validate_data(df)

    # Connect to MongoDB
    uri = getenv("MONGODB_URI")
    client = MongoClient(uri, tlsAllowInvalidCertificates=True)
    db = client['healthcare']
    collection = db['patients']

    # Migrate data
    migrate(df, collection)
    
    # Validate data in MongoDB
    records_mongo = list(collection.find({}, {'_id': 0}))
    df_mongo = pd.DataFrame(records_mongo)
    validate_data(df_mongo)

    