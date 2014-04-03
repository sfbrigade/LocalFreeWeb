import nltk, logging
from nltk.corpus import wordnet
tokenizer = None
tagger = None

def init_nltk():
    global tokenizer
    global tagger
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')
    tagger = nltk.UnigramTagger(nltk.corpus.brown.tagged_sents())

def tag(text):
    global tokenizer
    global tagger
    if not tokenizer:
        init_nltk()
    tokenized = tokenizer.tokenize(text)
    tagged = tagger.tag(tokenized)
    #tagged.sort(lambda x,y:cmp(x[1],y[1]))
    return tagged


def simple_path(path):
    return [s.lemmas[0].name for s in path]

def nl_process(string, logfile, module_keys):
    logging.info("NLTK starting up with %s." % string)
    string = tag(string)
    location = ""
    search_terms = []
    text = ""
    for word in string:
        if word[1] is None:
            location = word[0]
        elif word[1].find("NN") or word[1].find("WRB") or word[1].find("JJ") or word[1].find("VB"):
            search_terms.append(word[0])
            text += "%s " % word[0]
        else:
            text += "%s " % word[0]
    
    '''logging.info("NLTK found %s" % text)
    if text.find("[0-9]* (.*)"):
        logging.info("found address %s." % text)
        a = text.find("[0-9]* (.*)")
        b = text.rfind("[0-9]* (.*)")
        while a <= b:
            part = text[a]
            a = a + 1
        text = part
    '''
    
    for item in search_terms:
        word = wordnet.synset('%s.n.01' % item)
        paths = word.hypernym_paths()
        for path in paths:
            for line in simple_path(path):
                for key, value in module_keys.items():
                    if line in value.split(", "):
                        module = key
                        break
                else:
                    continue
                break
            else:
                continue
            break
    
    return(location,module,text)
