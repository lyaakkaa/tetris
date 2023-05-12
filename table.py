import psycopg2
from config import params

db = psycopg2.connect(**params)
cursor = db.cursor()


cursor.execute('''CREATE TABLE tetris(
    username VARCHAR(255),
    high_score INT NOT NULL,
);''')

# drop_table = '''DROP TABLE snake'''
# cursor.execute(drop_table)

cursor.close()
db.commit()
db.close()