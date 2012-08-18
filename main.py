import liwc
import string

txt_path = 'txt/texts_all.txt'
first_line_as_lable = True
#txt_limit = ['/thing:8917', '/thing:17473']
txt_limit = []
txt_column = 4
tid_column = 1
looks = {
    'posemo':['126'],
    'negemo':['19', '127', '128', '129', '130'],
    }
liwc_path = 'dic/LIWC2007_ENGLISH080730.dic'
show = True
fields = {
    'desc':'4',
    'insc':'5'
    }


cat, dic = liwc.read_liwc(liwc_path)
looks_ws = liwc.get_wordsets(dic, looks)
i = 0
f = open(txt_path, 'r')
r = {}
while 1:
    line = f.readline() 
    if not line: # end of file read
        break
    if first_line_as_lable: # ignore first line if it is lable
        if i == 0: 
            i = i+1
            continue
    txt = line.split('\t')
    tid = txt[tid_column]
    tid = str(tid) # dict needs key to be string, not integer
    if len(txt_limit) != 0: # if only look for specific tid
        if not (tid in txt_limit):
            continue
    r[tid] = {}
    # start to get score
    for field_key in fields:
        field = txt[int(fields[field_key])] # can be loop here
        words_count, score_rs = liwc.score(field, looks, looks_ws, show)
        rs = {'words_count':words_count, 'score':score_rs}
        r[tid][field_key] = rs
    if show:
        print tid, r[tid]
        print '================'
    # now need to print results well, show results in good format, etc
    
    
    
