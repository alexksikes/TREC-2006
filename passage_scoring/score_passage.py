import sys, os, math
from overlap import *

WEB_TERMS = "/projects/bebop/trec/trec2006/nakov/web_terms"

def score(q_id, text_span):
    total = 0
    
    web_verb = os.path.join(WEB_TERMS, "%s_web_v.txt" % q_id)
    
    (count, score) = compute_overlap(1, web_verb, text_span)
    boosted = math.exp(2) * score
#    print "verbs : freq = %s \t sum(log(freq)) = %s \t v-boosted = %s" % (count, score, boosted)
    total += boosted 
    
    for n in range(6)[1:]:
        web_term_file = os.path.join(WEB_TERMS, "%s_web_%s.txt" % (q_id, n))
        (count, score) = compute_overlap(n, web_term_file, text_span)
        boosted = math.exp(2*n) * score
#        print "%s-gram : freq = %s \t sum(log(freq)) = %s \t n-boosted = %s" % (n, count, score, boosted)
        total += boosted
     
#    print "total score of span = sum(n-boosted) = %s" % total
    return total
        
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: python score_passage.py question_id text_span"
    else:
        score(int(sys.argv[1]), sys.argv[2])
