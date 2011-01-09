def vector(txt):
    v = {}
    tokens = txt.split()
    for t in tokens:
        if v.has_key(t):
            v[t] +=1
        else:
            v[t] = 1
    return v

def dot(v1, v2):
    count = 0
    for a in v1:
        if v2.has_key(a):
            count +=1
    return count
    
def score(txt1, txt2):
    return dot(vector(str1), vector(str2))

def most_similar(txt1, txt_list):
    v1 = vector(txt1)
    best_txt = ""
    best_score = -1
    for txt in txt_list:
        v2 = vector(txt)
        score = dot(v1, v2)
        if score > best_score:
            best_score = score
            best_txt = txt
    return best_txt
    
def most_similar2(txt1, txt_list):
    v1 = vector(txt1)
    best_txt = ""
    best_score = -1
    i = 0
    for txt in txt_list:
        v2 = vector(txt)
        score = dot(v1, v2)
        if score > best_score:
            best_score = score
            best_i = i
        i +=1
    return best_i
    