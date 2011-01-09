# TODO: use a parser ratrher than regex, for example before missed <a <space> href>

# We have internal links if the form <a href="#tags">anchored_text</a>
# We get the following stats:
# tags (exist_in_article_count, total_count)
# anchored_text (exist_in_article_count, total_count)
# coo_tags_anchored_text (tags, anchored_text, count)
# article_size (article, number_of_char)
# tags_article (tags, article)
# anchored_text article (anchored_text, article)
# jrl_art_count (journal_name, number_articles)

import sys, glob, os, zipfile, re, sets

tags = {}
text = {}
coo_tags_text = {}

ind_tags_pmid = {}
ind_text_pmid = {}

art_size = {}
jrl_art_count = {}
    
def update_tbl(tbl, key, found):
    if tbl.has_key(key):
        if key not in found:
            tbl[key][0] +=1
            found.add(key)
        tbl[key][1] +=1
    else:
        tbl[key] = [1, 1]
    return True
        
def update_tbl2(ind, key, stuff):
    if ind.has_key(key):
        ind[key].append(stuff)
    else:
        ind[key] = [stuff]

def init_tbl():
    global tags, text, coo_tags_text, ind_tags_pmid, ind_text_pmid, art_size, jrl_art_count
    tags = {}
    text = {}
    coo_tags_text = {}
    
    ind_tags_pmid = {}
    ind_text_pmid = {}
    
    art_size = {}
    jrl_art_count = {}
            
p = re.compile('<a\s+href\s*=\s*"#(.*?)">(.*?)</a>', re.I)
def update(html, pmid):
    found_tag = sets.Set()
    found_txt = sets.Set()
    found_coo = sets.Set()
    matches = p.findall(html)
    for match in matches:
        tag = match[0].lower()
        txt = strip_html(match[1].lower())
        update_tbl(tags, tag, found_tag)
        update_tbl(text, txt, found_txt)
        update_tbl(coo_tags_text, (tag, txt), found_coo)
        update_tbl2(ind_tags_pmid, pmid, tag)
        update_tbl2(ind_text_pmid, pmid, txt)
        
def strip_html(text):
    def fixup(m):
        text = m.group(0)
        if text[:1] == "<" or text[:1] == "&" or text[:2] == "&#":
            return ""
        return text
    return re.sub("(?s)<[^>]*>|&#?\w+;", fixup, text)

def write_tbl(tbl, o):
    for t in tbl:
        s = str(t)
        for v in tbl[t]:
            s += "%s%s" % (delim, v)
        o.write(s + "\n")

def write_files(out_name, path):
    ext = {'.tag':tags, '.txt':text, '.coo':coo_tags_text, '.itag':ind_tags_pmid
            , '.itxt':ind_text_pmid, '.asize':art_size, '.acount':jrl_art_count}
    for e in ext:
        o = file(os.path.join(path, out_name) + e, 'w')
        write_tbl(ext[e], o)
        o.close()
        
def run(path, journals):
    nb_journals = len(journals)
    count_j = 0
    for journal in journals:
        count_j +=1
        print "=================== %s/%s ===================" % (count_j, nb_journals)
        stats(journal, count_j, path)
        init_tbl()
    
def stats(journal, count_j, path):
    journal_name = re.sub('.zip', '', os.path.split(journal)[1])
    print journal_name
    z = zipfile.ZipFile(journal, "r")
    articles = z.namelist()
    nb_articles = len(articles)
    update_tbl2(jrl_art_count, journal_name, nb_articles)
    count_a = 0
    for article in articles:
        count_a +=1
        print "------------------ %s | %s/%s ------------------" % (count_j, count_a, nb_articles)
        pmid = re.sub('.html|.htm', '', article.split('/')[-1])
        print pmid
        html = z.read(article)
        html = re.sub("\r|\n", "", html)
        update(html, pmid)
        update_tbl2(art_size, pmid, len(html))
    z.close()
    write_files(journal_name, path)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python stats.py output_name zipfiles"
    else:
        run(sys.argv[1], sys.argv[2:])
