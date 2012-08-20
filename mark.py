import sqlite3
import json
import call
from main import *

sql_path = 'sql/thingiver.db'
conn = sqlite3.connect(sql_path)

#things = {}

# things
sql_things = 'SELECT id, url, name FROM thing'
def things_sql(things):
    c = conn.cursor()
    sql = sql_things
    c.execute(sql, ())
    for row in c.fetchall():
        thing_id = row[0]
        thing_url = row[1]
        thing_title = row[2]
        if not things.has_key(thing_id):
            things[thing_id] = {}
        things[thing_id]['url'] = thing_url
        things[thing_id]['title'] = thing_title
    return things

# likes
sql_likes = 'SELECT thing_id, COUNT(follower_url) FROM like GROUP BY thing_id'
def likes(things):
    c = conn.cursor()
    sql = sql_likes
    c.execute(sql, ())
    for row in c.fetchall():
        thing_id = row[0]
        thing_likes = row[1]
        if not things.has_key(thing_id):
            things[thing_id] = {}
        things[thing_id]['likes'] = thing_likes
    return things


# likes
sql_mades = '''
SELECT thing.id, COUNT(made_raw.y_url) 
FROM made_raw, thing 
WHERE thing.url = made_raw.x_url
GROUP BY thing.url
'''
def mades(things):
    c = conn.cursor()
    sql = sql_mades
    c.execute(sql, ())
    for row in c.fetchall():
        thing_id = row[0]
        thing_mades = row[1]
        if not things.has_key(thing_id):
            things[thing_id] = {}
        things[thing_id]['mades'] = thing_mades
        #print thing_mades
    return things

def together(r, things):
    for thing_id in things:
        if things[thing_id].has_key('likes'):
            thing_likes = things[thing_id]['likes']
        else:
            thing_likes = 0
        if things[thing_id].has_key('mades'):
            thing_mades = things[thing_id]['mades']
        else:
            thing_mades = 0
        thing_url = things[thing_id]['url'].strip()
        r[thing_url]['likes'] = thing_likes
        r[thing_url]['mades'] = thing_mades
    return r

def output(fields, looks, r, output_result):
    if output_result == True:
        print '**** start to output score ****'
        fs = output_score_open(fields, looks)
        output_score_process(r, fs, fields, looks)
        output_score_close(fs)
        print '**** end of output score ****'

def output_score_open(fields, looks):
    fs = {}
    for field_key in fields:
        f = open('output/mark_%s.txt'%field_key, 'w')
        fs[field_key] = f
        line1 = 'tid \tlikes \tmades \twords_count '
        for look in looks:
            line1 = '%s \t%s'%(line1, str(look))
        line1 = '%s\n'%line1
        f.write(line1)
    return fs
    
def output_score_process(r, fs, fields, looks):
    for tid in r:
        for field_key in fields:
            f = fs[field_key]
            if r[tid].has_key('likes'):
                thing_likes = r[tid]['likes']
            else:
                thing_likes = '0'
            if r[tid].has_key('mades'):
                thing_mades = r[tid]['mades']
            else:
                thing_mades = '0'
            words_count = r[tid][field_key]['words_count']
            scores = r[tid][field_key]['score']
            line = '%s \t%s \t%s \t%s '%(tid, thing_likes, thing_mades, words_count)
            for look in looks:
                score = scores[look]
                line = '%s \t%s'%(line, str(score))
            line = '%s\n'%line
            f.write(line)

def output_score_close(fs):
    for f in fs:
        fs[f].close()
        

if __name__ == '__main__':
    things = {}
    things = things_sql(things)
    things = likes(things)
    things = mades(things)
    r = call.read_main(fields, looks)
    r = together(r, things)
    output(fields, looks, r, output_result)
    #print json.dumps(r, indent=2)
            
    
