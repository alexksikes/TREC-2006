import sys, re

def strip_html(text):
    def fixup(m):
        text = m.group(0)
        if text[:1] == "<" or text[:1] == "&" or text[:2] == "&#":
            return ""
        return text
    return re.sub("(?s)<[^>]*>|&#?\w+;", fixup, text)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python strip_html2.py html_file"
    else:
        print strip_html(open(sys.argv[1]).read()),