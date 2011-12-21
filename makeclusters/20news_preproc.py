import os
import re, string

pattern = re.compile('[\d\W_]+')

direc = "20news-18828"
stopwords_f = "stop_english.dat"

f = open(stopwords_f, 'r')
stopwords = f.read().split()
f.close()

def process_line(s):
    """
    remove non alpha, remove strings <= 3 characters in length, remove stop list words, strip extra whitespace, 
    make lower case
    """
    words = map(string.lower, re.sub("\\b[\\w']{1,3}\\b", "", pattern.sub(' ', s)).split())
    return ' '.join([item for item in words if not item in stopwords])
    # if char other than '>','"','''
    # return " ".join(i for i in s if (ord(i)<128 and ord(i)>31 and ord(i) != 62 and ord(i) != )

for dirname, dirnames, filenames in os.walk(direc):
    for idx, filename in enumerate(filenames):
        f = open(os.path.join(dirname, filename), 'r')
        fs = f.read()
        print os.path.join(dirname, filename)
        fs = process_line(fs)
        # for i in fs:
        #     if not ((ord(i)<128 and ord(i)>31) or ord(i)==10):
        #     print "%d: '%s'" % (ord(i), 0)
        f.close
        f = open(os.path.join(dirname, filename), 'w')
        f.write(fs)
        f.close()
