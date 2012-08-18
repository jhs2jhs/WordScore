import string 

def read_liwc(filename):
    liwc_data = open(filename, 'r')
    
    mode = 0
    cat = {}
    dic = {}

    for line in liwc_data:
        line = line.strip('\r\n')
        if line == '%':
            mode += 1
            continue
        elif mode == 1: # cat
            chunks = line.split('\t')
            cat[chunks[0]] = chunks[1]
        elif mode == 2: # dic
            chunks = line.split('\t')
            word = chunks.pop(0)
            dic[word] = chunks
    return (cat, dic)


def get_wordsets(dic, looks):
    rs = {}
    for key in looks:
        rs[key] = {}
    for word in dic:
        for (key, value) in looks.items():# for each filed, I need to look at
            for cat in dic[word]:
                if cat in value: # if find right cat
                    rs[key][word] = dic[word]
                    continue
    return rs
                    
def score(txt, looks, looks_ws, show=False):
    txt = txt.lower()
    words = txt.split(' ')
    words_count = len(words)
    rs = {}
    for key in looks:
        rs[key] = 0
    for word in words:
        if len(word) == 0 or word[0] == '@': # empty word, or this word is name
            continue 
        word = word.translate(None, string.punctuation)
        for key in looks:
            wordsets = looks_ws[key] # get complete set for individual target
            for wordset in wordsets:
                if matches(wordset, word): # check for value, can improve accuracy here
                    if show: # print corps
                        print wordset, ' = ', key 
                    rs[key] = rs[key]+1
    return (words_count, rs)


#### needs to update here for complex matches
def matches(liwc_word, txt):
    if liwc_word[-1] == '*':
        return txt.startswith(liwc_word[:-1])
    else:
        return txt == liwc_word
                
