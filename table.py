import psycopg2
from config import params

db = psycopg2.connect(**params)
cursor = db.cursor()


cursor.execute('''CREATE TABLE scores(
     username   VARCHAR(255),
     record INT NOT NULL,
     latest_score INT NOT NULL
)''')

# drop_table = '''DROP TABLE snake'''
# cursor.execute(drop_table)

cursor.close()
db.commit()
db.close()