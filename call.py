import liwc
import string
import pprint
import json

## method to get score for each field in your txt files
def get_scores(liwc_path, txt_path, first_line_as_lable, tid_column, tid_limit, fields, looks, show):
    print '**** start to calculate the score ****'
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
    print 'end of start to calculate the score ****'
    return r


## output process results into a local txt file. 
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
    
def read_main(fields, looks):
    r = {}
    for field_key in fields:
        f = open('output/%s.txt'%field_key, 'r')
        i = 0
        while 1:
            i = i + 1
            line = f.readline()
            if not line:
                break
            if i == 1:
                continue # the first line is a lable
            line = line.strip()
            scores = line.split('\t')
            if len(scores) < 2:
                continue
            tid = scores[0].strip()
            if not r.has_key(tid):
                r[tid] = {}
            if not r[tid].has_key(field_key):
                r[tid][field_key] = {}
            words_count = scores[1].strip()
            if not r[tid][field_key].has_key('words_count'):
                r[tid][field_key]['words_count'] = words_count
            if not r[tid][field_key].has_key('score'):
                r[tid][field_key]['score'] = {}
            j = 2
            for look in looks:
                score = scores[j].strip()
                if not r[tid][field_key]['score'].has_key(look):
                    r[tid][field_key]['score'][look] = score
                j = j + 1
        f.close()
    return r

## pair: bounday crossing
def pair(pair_file_path, fields, looks, r, first_line_as_label_pair):
    print '**** start to pair ****'
    i = 0
    f = open(pair_file_path, 'r')
    lines_out = {}
    line_one = ''
    for field_key in fields:
        line_one = '%s \t%s_words_count '%(line_one, field_key)
        for look in looks:
            line_one = '%s \t%s_%s '%(line_one, field_key, look)
    line_one = 'objectA %s \tobjectB %s '%(line_one, line_one)
    while 1:
        i = i+1
        #print i
        line = f.readline()
        #print line
        if not line:
            break
        if first_line_as_label_pair:
            if i == 1:
                line_one = '%s \t%s \n'%(line_one, line.strip())
                continue
        line = line.strip()
        txt = line.split('\t')
        #tid = txt[i]
        a = txt[0].strip() # from a -> b
        b = txt[1].strip()
        line_out = ''
        ## for object a
        tid = '/thing:%s'%(str(a))
        line_out = '%s '%(tid)
        if not r.has_key(tid):
            for field_key in fields:
                words_count = 'None'
                line_out = '%s \t%s '%(line_out, words_count)
                for look in looks:
                    score = 'None'
                    line_out = '%s \t%s '%(line_out, str(score))
        else:
            for field_key in fields:
                words_count = r[tid][field_key]['words_count']
                scores = r[tid][field_key]['score']
                line_out = '%s \t%s '%(line_out, words_count)
                for look in looks:
                    score = scores[look]
                    line_out = '%s \t%s '%(line_out, str(score))
        ## for object b
        tid = '/thing:%s'%(str(b))
        line_out = '%s \t%s'%(line_out, tid)
        if not r.has_key(tid):
            for field_key in fields:
                words_count = 'None'
                line_out = '%s \t%s '%(line_out, words_count)
                for look in looks:
                    score = 'None'
                    line_out = '%s \t%s '%(line_out, str(score))
        else:
            for field_key in fields:
                tid = '/thing:%s'%(str(b))
                words_count = r[tid][field_key]['words_count']
                scores = r[tid][field_key]['score']
                line_out = '%s \t%s '%(line_out, words_count)
                for look in looks:
                    score = scores[look]
                    line_out = '%s \t%s'%(line_out, str(score))
        ## append rest existing info
        line_out = '%s \t%s \n'%(line_out, line.strip())
        lines_out[i] = line_out
        lines_out[0] = line_one
    print '**** end of pare ****'
    return lines_out

def pair_output(lines_out, pair_file_path, pair_show):
    print '**** start to output pair ****'
    line_one = ''
    f_out_name = pair_file_path.replace('/', '')
    f_out = 'output/pair_%s'%f_out_name
    f = open(f_out, 'w')
    for i in lines_out:
        line = '%s \t%s'%(str(i), lines_out[i])
        if pair_show:
            print line
        f.write(line)
    f.close()
    print '**** end of output pair ****'
    
    
