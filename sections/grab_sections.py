import os, re, sys, glob

p = re.compile('<\s*section\s*id\s*=\s*"(.*)"\s*>')
def get_sections(text):
    return "\n".join(p.findall(text))

def run(data_path):
    articles = glob.glob(os.path.join(data_path, '*.xml'))
    nb_articles = len(articles)
    count_a = 0
    for article in articles:
        count_a +=1
        pmid = article.split('/')[-1]
        print "----- %s ----- %s/%s --" % (pmid, count_a, nb_articles)
        text = open(article, 'r').read()
        print get_sections(text)
        
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python grab_sections.py xml_data"
    else:
        run(sys.argv[1])
