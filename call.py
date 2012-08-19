import liwc
import string
import pprint
import json

## method to get score for each field in your txt files
def get_scores(liwc_path, txt_path, first_line_as_lable, tid_column, tid_limit, fields, looks, show):
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
        if len(tid_limit) != 0: # if only look for specific tid
            if not (tid in tid_limit):
                continue
        r[tid] = {}
        # start to get score
        for field_key in fields:
            field = txt[int(fields[field_key])] # can be loop here
            words_count, score_rs = liwc.score(field, looks, looks_ws, show)
            rs = {'words_count':words_count, 'score':score_rs}
            r[tid][field_key] = rs
        if show:
            print tid
            print json.dumps(r[tid], sort_keys=True, indent=2) # pretty print data
            print '================'
        # now need to print results well, show results in good format, etc
    return r


## output process results into a local txt file. 
def output(fields, looks, r, output_result):
    if output_result == True:
        fs = output_score_open(fields, looks)
        output_score_process(r, fs, fields, looks)
        output_score_close(fs)

def output_score_open(fields, looks):
    fs = {}
    for field_key in fields:
        f = open('output/%s.txt'%field_key, 'w')
        fs[field_key] = f
        line1 = 'tid \twords_count '
        for look in looks:
            line1 = '%s \t%s'%(line1, str(look))
        line1 = '%s\n'%line1
        f.write(line1)
    return fs
    
def output_score_process(r, fs, fields, looks):
    for tid in r:
        for field_key in fields:
            f = fs[field_key]
            words_count = r[tid][field_key]['words_count']
            scores = r[tid][field_key]['score']
            line = '%s \t%s '%(tid, words_count)
            for look in looks:
                score = scores[look]
                line = '%s \t%s'%(line, str(score))
            line = '%s\n'%line
            f.write(line)

def output_score_close(fs):
    for f in fs:
        fs[f].close()
    
    
    
