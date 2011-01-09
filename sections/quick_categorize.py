import os, re, sys, glob

categories_match = {0:['title'], 
              1:['references', 'literature cited'], 
              2:['abstract', 'summary'], 
              3:['abbreviations'],
              4:['conclusion', 'conclusions', 'concluding remarks', 'concluding comments'], 
              5:['discussion', 'discussions', 'results', 'study limitations'], 
              6:['introduction', 'overview'], 
              7:['method', 'methods', 'experimental procedure', 'methodology', 'study design'], 
              8:['footnotes'], 
              9:['acknowledgments', 'acknowledgements'],
              10:['appendix', 'glossary', 'supplementary materials', 'supplementary data'], 
              11:['future', 'outlook'], 
              12:['case'],
              13:['grants'],
              14:['main text']
              }

categories_id = {0:'title', 
              1:'references', 
              2:'abstract',
              3:'abbreviations',
              4:'conclusions', 
              5:'results', 
              6:'introduction', 
              7:'methods', 
              8:'footnotes', 
              9:'acknowledgments',
              10:'appendix', 
              11:'future', 
              12:'cases',
              13:'grants',
              14:'main'
              }

def which_category(str):
    for c in categories_match:
        for c_sub in categories_match[c]:
            if (str.count(c_sub) or c_sub.count(str)) and len(str):
                return c
    return -1

MAX_SIZE = 60
def which_category_id(str):
    if len(str) and len(str) < MAX_SIZE:
        for c in categories_match:
            for c_sub in categories_match[c]:
                if (str.count(c_sub) or c_sub.count(str)):
                    return categories_id[c]
#    return 'nc'

p = re.compile('\s+([0-9]+)\s(.*)')
def run(sections):
    line_no = 0
    lines = open(sections, 'r').readlines()
    for line in lines:
        m = p.match(line)
        if m:
            sec = m.group(2)
            print "%s\t%s\t++%s++" % (m.group(1), sec, which_category(sec))
            
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python quick_categorize.py sections_clustered"
    else:
        run(sys.argv[1])