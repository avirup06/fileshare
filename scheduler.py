import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import os
import time

path = "D:\storage"
username="postgres"
password="root"
host="localhost"
port="5432"
database_name="fileshare_db"
encoded_password = urllib.parse.quote(password)


DATABASE_URL: str = f"postgresql+psycopg2://{username}:{encoded_password}@{host}:{port}/{database_name}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

while True:
    query = text("SELECT * FROM public.files where is_auto_deleted = true and is_deleted = false")
    res = db.execute(query)
    file_list = [[row[0], f'{path}\{row[2]}.{(row[1]).rsplit(".", 1)[1]}'] for row in res]

    for file in file_list:
        if os.path.exists(file[1]):
            os.remove(file[1])
        else:
            pass
    
        update_query = text(f"UPDATE public.files SET is_deleted = true WHERE id = '{file[0]}'")
        db.execute(update_query)
    
    print("completed")
    time.sleep(30)