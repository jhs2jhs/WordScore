## configuration ##
base_lines = 50


##### do not edit bellow this line ####

import liwc
import string
import pprint
import json
from datetime import datetime
from main import *

def get_time(liwc_path, txt_path, first_line_as_lable, tid_column, tid_limit, fields, looks, show):
    t1 = datetime.now()
    t2 = datetime.now()
    t3 = datetime.now()
    print '**** read first %s ****'%(str(base_lines))
    t1 = datetime.now()
    cat, dic = liwc.read_liwc(liwc_path)
    looks_ws = liwc.get_wordsets(dic, looks)
    i = 0
    f = open(txt_path, 'r')
    r = {}
    while 1:
        i = i + 1
        line = f.readline() 
        if not line: # end of file read
            break
        if first_line_as_lable: # ignore first line if it is lable
            if i == 1: 
                i = i+1
                continue
        if i == base_lines:
                t2 = datetime.now()
        if i > base_lines:
            continue
        txt = line.split('\t')
        tid = txt[tid_column].strip()
        tid = str(tid) # dict needs key to be string, not integer
        if len(tid_limit) != 0: # if only look for specific tid
            flag = True
            for l in tid_limit:
                if tid == l.strip():
                    flag = False
            if flag == True:
                continue
        r[tid] = {}
        # start to get score
        for field_key in fields:
            field = txt[int(fields[field_key])].strip() # can be loop here
            words_count, score_rs = liwc.score(field, looks, looks_ws, show)
            rs = {'words_count':words_count, 'score':score_rs}
            r[tid][field_key] = rs
        if show:
            print tid
            print json.dumps(r[tid], sort_keys=True, indent=2) # pretty print data
            print '================'
        # now need to print results well, show results in good format, etc
    f.close()
    print '**** end of calculate the score ****'
    t3 = datetime.now()
    t = (t2-t1).seconds
    td = (i*1.0/base_lines)*(t*1.0)*3
    td = int(td)
    mins = td/60
    seconds = (td - mins*60)
    print 
    print "============================="
    print "== Time estimate: %s minutes =="%(str(mins))
    print "============================="
    print 

if __name__ == '__main__':
    get_time(liwc_path, txt_path, first_line_as_lable, tid_column, tid_limit, fields, looks, show)

