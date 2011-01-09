import os, re, sys, glob, zipfile

#BASE_DIR = '/home/alex/trec/ir.ohsu.edu/genomics/data/2006/'
#BASE_DIR = '/home/alex/trec/ir.ohsu.edu/genomics/data/2006/subset2/'
BASE_DIR = '/home/alex/trec/ir.ohsu.edu/genomics/data/2006/subset/'

p_cite = re.compile('access_num=(\d+)')

def run(journals_dir, citation_file):
    journals = glob.glob(os.path.join(journals_dir, '*.zip'))
    nb_journals = len(journals)
    count_j = 0
    for journal in journals:
        count_j +=1
        print "=================== %s/%s ===================" % (count_j, nb_journals)
        print os.path.split(journal)[1]
        z = zipfile.ZipFile(journal, "r")
        articles = z.namelist()
        nb_articles = len(articles)
        count_a = 0
        for article in articles:
            count_a +=1
            print "------------------ %s | %s/%s ------------------" % (count_j, count_a, nb_articles)
            pmid = re.sub('.html|.htm', '', article.split('/')[-1])
            print pmid
            html = z.read(article)
            matches = p_cite.findall(html)
            for match in matches:
                c_file.write("%s %s\n" % (pmid, match))
        z.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: python trec_index.py journals_dir citation_file"
    else:
        journals_dir = sys.argv[1]
        c_file = file(sys.argv[2], 'w')
        run(journals_dir, c_file)