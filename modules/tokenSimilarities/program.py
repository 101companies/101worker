import fnmatch
import os
from gensim import corpora, models, similarities
import simplejson as json
import logging
import nltk
from collections import OrderedDict
import sys
sys.path.append('../../libraries/101meta')
import const101

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)


def createBag(tokens, stopWords=None, stemmer=None):
    bag = []
    for token, occs in tokens.iteritems():
        if len(token) >= 2:
            word = token.lower()
            if stemmer:
                word = stemmer.stem(word)
            if word not in stopWords:
                bag += occs*[word]
    return bag


def createFragmentDocuments(suffix, stopWords, stemming=True):

    if stemming:
        stemmer = nltk.stem.SnowballStemmer('english')
    else:
        stemmer = None

    texts = []
    fragmentTokens = []
    fragments = []
    for root, dirs, files in os.walk(const101.tRoot, followlinks=True):
        for basename in fnmatch.filter(files, "*.fragments.refinedTokens.json"):
            filename = os.path.join(root, basename)
            if filename[:-len(".fragments.refinedTokens.json")].endswith(suffix):
                fragmentsDict = json.load(open(filename))
                hostfile = os.path.join(const101.sRoot, filename[len(const101.tRoot) + 1:])[:-len(".fragments.refinedTokens.json")]
                for fragment, tokens in fragmentsDict.iteritems():
                    if not "/method/" in fragment:
                        continue
                    fragmentTokens.append(tokens)
                    fragments.append(os.path.join(hostfile, fragment))

    for token in fragmentTokens:
        bag = createBag(token, stopWords, stemmer)
        texts.append(bag)

    return fragments, texts


def createFileDocuments(suffix, stopWords, stemming=True):

    if stemming:
        stemmer = nltk.stem.SnowballStemmer('english')
    else:
        stemmer = None

    texts = []
    tokenfiles = []
    tokens = []


    for root, dirs, files in os.walk(const101.tRoot, followlinks=True):
        for basename in fnmatch.filter(files, "*.refinedTokens.json"):
            filename = os.path.join(root, basename)
            if filename[:-len(".refinedTokens.json")].endswith(suffix) and not filename[:-len(".refinedTokens.json")].endswith(".fragments"):
                tokens.append(json.load(open(filename)))
                filePath = os.path.join(const101.sRoot, filename[len(const101.tRoot) + 1:])[:-len(".refinedTokens.json")]
                tokenfiles.append(filePath)

    for token in tokens:
        bag = createBag(token, stopWords, stemmer)
        texts.append(bag)

    return tokenfiles, texts


def generateIndex(texts, no_below=None, no_above=None, keep_n=None):

    freqDictionary = corpora.Dictionary(texts)

    if no_above:
        freqDictionary.filter_extremes(no_above=no_above)
    if no_below:
        freqDictionary.filter_extremes(no_below=no_below)
    if keep_n:
        freqDictionary.filter_extremes(keep_n=keep_n)
        print '\n' + "---------Most frequent Tokens---------" + '\n'
        for id in freqDictionary:
            print freqDictionary[id]

    corpus = [freqDictionary.doc2bow(text) for text in texts]
    model = models.TfidfModel(corpus, id2word=freqDictionary)
    index = similarities.MatrixSimilarity(model[corpus])

    return index, model, freqDictionary,



def queryIndex(resource, index, model, freqDict, names, stopWords=None, resultCount=None):

    new_bag = createBag(resource, stopWords, stemmer=nltk.stem.SnowballStemmer('english'))
    new_bow = freqDict.doc2bow(new_bag)
    new_vec = model[new_bow]

    print '\n' + "---------New Instance Vector---------" + '\n'
    for tuple in new_vec:
        print freqDict.get(tuple[0]) + " : " + str(tuple[1])
    print '\n' + "-------------------------------------" + '\n'

    sims = index[new_vec]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])

    result = dict()

    if resultCount:
        for i in range(resultCount):
            result[names[sims[i][0]]] = sims[i][1]

    return result

def createFileDump(suffix):
    stopWords = ["import", "java", "org", "softlang"]
    names, texts = createFileDocuments(suffix, stopWords)
    index, model, freqDict = generateIndex(texts)
    simDump = dict()

    for i, sims in enumerate(index):
        simDict = dict()
        for j, value in sorted(enumerate(sims), key=lambda item: -item[1])[:11]:
            if not i==j:
                simDict[names[j]] = str(value)
        top10 = OrderedDict(sorted(simDict.items(), key=lambda t: -float(t[1])))
        simDump[names[i]] = [top10]

    json.dump(simDump, open(os.path.join(const101.dumps, "similarities.json"), 'w'))


def createFragmentDump(suffix):
    stopWords = ["import", "java", "org", "softlang"]
    names, texts = createFragmentDocuments(suffix, stopWords)
    index, model, freqDict = generateIndex(texts)
    simDump = dict()

    for i, sims in enumerate(index):
        simDict = dict()
        for j, value in sorted(enumerate(sims), key=lambda item: -item[1])[:11]:
            if not i==j:
                simDict[names[j]] = str(value)
        top10 = OrderedDict(sorted(simDict.items(), key=lambda t: -float(t[1])))
        simDump[names[i]] = [top10]

    json.dump(simDump, open(os.path.join(const101.dumps, "similarities_fragments.json"), 'w'))


def contrDetectionSamples():
    # contribution detection
    #testResource = const101.tRoot+"/contributions/gwtTree/src/org/softlang/client/guiinfos/tree/comparators/DepComparator.java.refinedTokens.json"
    #testResource = const101.tRoot+"/contributions/mobileAndroid/src/org/softlang/company/mobileAndroid/CompanyWidget.java.refinedTokens.json"
    #testResource = const101.tRoot+"/contributions/jena/org/softlang/jena/rdf/Containment.java.refinedTokens.json"
    #testResource = const101.tRoot+"/contributions/atlTotalPlugin/src/ATL_ComputeTotalPlugin/Activator.java.refinedTokens.json"
    #testResource = const101.tRoot+"/contributions/strutsAnnotation/src/main/java/org/softlang/actions/CompanyAction.java.refinedTokens.json"
    testResource = const101.tRoot+"/contributions/jsf/jsf/src/java/company/classes/Department.java.refinedTokens.json"
    #testResource = const101.tRoot+"/contributions/jgralab/src/de/uni_koblenz/oneoonecompanies/CompanyServices.java.refinedTokens.json"
    #testResource = const101.tRoot+"/contributions/jdbc/org/softlang/features/Cut.java.refinedTokens.json"
    stopWords = ["import", "java", "org", "softlang"]
    names, texts = createFileDocuments(".java", stopWords)
    index, model, freqDict = generateIndex(texts)
    resourceContent = json.load(open(testResource))
    queryResult = queryIndex(resourceContent, index, model, freqDict, names, stopWords=stopWords, resultCount=11)
    for key, value in sorted(queryResult.iteritems(), key=lambda (k, v): (-v, k)):
        if not key == testResource:
            print "%s : %s" % (value, key)



def fragmentDetectionSamples():

    # fragment detection
    #testResource = const101.tRoot+"/contributions/hibernate/org/softlang/company/Company.java/class/Company/method/setId"
    testResource = const101.tRoot+"/contributions/jsf/jsf/src/java/company/classes/Company.java/class/Company/method/getDepartments"
    #testResource = const101.tRoot+"/contributions/jdbc/org/softlang/features/Depth.java/class/Depth/method/depth/1"
    #testResource = const101.tRoot+"/contributions/jena/org/softlang/jena/rdf/Containment.java/class/Containment/method/checkContainment"
    #testResource = const101.tRoot+"/contributions/antlrLexer/src/main/java/org/softlang/company/features/Parsing.java/class/Parsing/method/parse"

    suffix = ".java"
    filename, fragmentname = testResource.split(suffix+"/")
    tokenFile = json.load(open(os.path.join(filename+suffix+".fragments.refinedTokens.json")))
    resourceContent = tokenFile[fragmentname]

    stopWords = ["import", "java", "org", "softlang"]
    names, texts = createFragmentDocuments(suffix, stopWords)
    index, model, freqDict = generateIndex(texts)
    queryResult = queryIndex(resourceContent, index, model, freqDict, names, stopWords=stopWords, resultCount=11)
    for key, value in sorted(queryResult.iteritems(), key=lambda (k, v): (-v, k)):
        if not key == testResource:
            print "%s : %s" % (value, key)


createFileDump(".java")
createFragmentDump(".java")
