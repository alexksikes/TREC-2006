# TODO: use a parser, too many exceptins, for example in a space space href

import sys, glob, os, zipfile, re

def strip_html(text):
    def fixup(m):
        text = m.group(0)
        if text[:1] == "<" or text[:1] == "&" or text[:2] == "&#":
            return ""
        return text
    return re.sub("(?s)<[^>]*>|&#?\w+;", fixup, text)

p = re.compile('<a\s+href\s*=\s*"#(.*?)">(.*?)</a>', re.I)
ref = {}
txt = {}
def count(html):
    matches = p.findall(html)
    for match in matches:
        r = match[0].lower()
        t = strip_html(match[1].lower())
        if ref.has_key(r):
            ref[r] +=1
        else:
            ref[r] = 1
        if txt.has_key(t):
            txt[t] +=1
        else:
            txt[t] = 1

ref_j = {}
txt_j = {}
def count_per_journal(html, journal_name):
    matches = p.findall(html)
    for match in matches:
        r = match[0].lower()
        t = strip_html(match[1].lower())
        
        if ref_j.has_key(r):
            ref_j[r][journal_name] +=1
        else:
            ref_j[r] = {}
            ref_j[r][journal_name] = 1
        
        if txt_j.has_key(t):
            txt_j[t][journal_name] +=1
        else:
            txt_j[t] = {}
            txt_j[t][journal_name] = 1
                
def write_files(out_name):
    oref = file(out_name+'.ref', 'w')
    otxt = file(out_name+'.txt', 'w')
    for t in ref:
        oref.write("%s : %s\n" % (t, ref[t]))
    for t in txt:
        otxt.write("%s : %s\n" % (t, txt[t]))
    oref.close()
    otxt.close()
    
# at each (tag, journal) put count
def write_table(out_name):
    oref = file(out_name+'.ref', 'w')
    otxt = file(out_name+'.txt', 'w')
    
    oref.write('* |')
    otxt.write('* |')
    print journals
    for journal in journals:
        oref.write("%s | " % journal_name)
        oref.write("%s | " % journal_name)
    oref.write("\n")
    otxt.write("\n")
    
    for tag_name in ref_j:
        oref.write(tag_name + " : ")
        for journal_name in ref_j[tag_name]:
            oref.write("%s | " % (ref_j[tag_name][journal_name]))
        oref.write("\n")
            
    for txt_name in txt_j:
        oref.write(txt_name + " : ")
        for journal_name in txt_j[txt_name]:
            otxt.write("%s | " % (txt_j[txt_name][journal_name]))
        otxt.write("\n")
    
    oref.close()
    otxt.close()

journals = []
def run(journals_dir, out_name):
    journals = glob.glob(os.path.join(journals_dir, '*.zip'))
    nb_journals = len(journals)
    count_j = 0
    for journal in journals:
        count_j +=1
        print "=================== %s/%s ===================" % (count_j, nb_journals)
        journal_name = re.sub('.zip', '', os.path.split(journal)[1])
        print journal_name
        
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
            html = re.sub("\r|\n", "", html)
            #count(html)
            count_per_journal(html, journal_name)
        z.close()
    #write_files(out_name)
    write_table(out_name)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: python internal_links.py journals_dir out_name"
    else:
        run(sys.argv[1], sys.argv[2])
