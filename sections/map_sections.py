import sys
from quick_categorize import *

sections = {}
def load(section_spans):
    f = open(section_spans, 'r')
    for line in f:
        (pmid, sect_name, start, end) = line.split('\t')
        [pmid, start, end] = map(int, [pmid, start, end])
        if len(sect_name) < 50:
            if sections.has_key(pmid):
                sections[pmid].append((sect_name, start, end))
            else:
                sections[pmid] = [(sect_name, start, end)]

def run(span_ids, section_spans):
    load(section_spans)
    f = open(span_ids, 'r')
    for line in f:
        (span_id, pmid, start, length) = line.split('\t')
        [pmid, start, length] = map(int, [pmid, start, length])
        sect_names = which_sections(start, length, pmid)
        for sect_n in sect_names:
            category = which_category_id(sect_n[0])
            if category:
#                print "%s\t%s\t%s\t'%s'" % (pmid, span_id, category, sect_n)
#            print "%s\t%s\t%s\t'%s'" % (pmid, span_id, which_category_id(sect_n), sect_n)
                print "%s\t%s\t%s\t%s\t%s\t%s\t%s" % (pmid, span_id, sect_n[0], start, start+length, sect_n[1], sect_n[2])

def which_sections(span_s, span_l, pmid):
    sect_name = []
    if sections.has_key(pmid):
        for section in sections[pmid]:
            (sect_n, sect_s, sect_e) = (section[0], section[1], section[2])
            span_e = span_s + span_l
            if span_e < sect_s:
                break;
            if span_s <= sect_e:
                sect_name.append((sect_n, sect_s, sect_e))
#                sect_name.append(sect_n)
            if span_e < sect_e:
                break;
    return sect_name

#def which_section(span_s, span_l, pmid):
#    if sections.has_key(pmid):
#        for section in sections[pmid]:
#            (sect_n, sect_s, sect_e) = (section[0], section[1], section[2])
#            if (span_s >= sect_s) and ((span_s + span_l) <= sect_e):
#                return (sect_n, sect_s, sect_e)
#    return (None, None, None)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: python map_sections.py span_ids section_spans"
    else:
        run(sys.argv[1], sys.argv[2])
