import sys, re

def fix_xml(text):
    def fixup(m):
        text = m.group(0)
        if text[:1] == "&" or text[:2] == "&#":
            return ""
        return text
    return re.sub("&#?\w+;?", fixup, text)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python fix_xml.py xml_file"
    else:
        print fix_xml(open(sys.argv[1]).read()),
