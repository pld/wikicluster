def log(note, string):
    print "[LOG] %s: %s" % (note, string)

def error(string):
    print "[ERROR] %s" % string

def list_as_dec_str(l):
    return " ".join(map(lambda x: "%0.5f" % x, l))

