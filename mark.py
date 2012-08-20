import sqlite3

sql_path = 'sql/thingiver.db'
conn = sqlite3.connect(sql_path)

things = {}

# likes, and mades
def likes():
    c = conn.cursor()
    sql = sql_like
    c.execute(sql, ())
    for row in c.fetchall():
        thing_id = row[0]
        thing_likes = row[1]
        if not things.has_key():
            
    
