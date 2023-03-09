from textblob import TextBlob
def spellcheck(a):
    b = TextBlob(a)
    crt=str(b.correct())
    if(a==crt):
        return ""
    else:
        return crt