import sys, re, math

def read(web_term_file):
    n_grams = {}
    f = open(web_term_file, 'r')
    for line in f:
        res = line.split('\t')
        freq = int(res[0])
        # ignore anything with a low frequency
        if freq <= 4:
            break;
        g = res[1][:-1]
        n_grams[g] = freq
    return n_grams
    
p = re.compile('[.,;!#$/:?\'\(\)\[\]_\-\"]')
def remove_punctuation(txt):
    return p.sub(" ", txt).lower()

def overlap(txt, n, n_grams):
    txt = txt.split()
    s = count = score = 0
    for t in txt:
        if s + n > len(txt):
            return (count, score)
        t_gram = []
        for i in range(n):
            t_gram.append(txt[s+i])
        t_gram = " ".join(t_gram)
        # first extra simple score count
        if t_gram in n_grams.keys():
            count +=1
        # takes into account the frequencies
        for g in n_grams:
            if t_gram == g:
                score += math.log(n_grams[g])
        s +=1
    return (count, score)

def compute_overlap(n, web_term_file, txt):
    n_grams = read(web_term_file)
    return overlap(remove_punctuation(txt), n, n_grams)
        
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: python overlap.py nb_grams web_terms text"
    else:
        print compute_overlap(int(sys.argv[1]), sys.argv[2], sys.argv[3])
