from __future__ import division
import fnmatch
import os
from gensim import corpora, models, similarities
import simplejson as json
import logging
import nltk
import math
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
                    if "/method/" in fragment:
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
                filePath = os.path.join("http://101companies.org/resources", filename[len(const101.tRoot) + 1:])[:-len(".refinedTokens.json")]+"?format=html"
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

    return index, model, freqDictionary



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

    if not resultCount:
        resultCount = len(index.index)

    for i in range(resultCount):
        result[names[sims[i][0]]] = sims[i][1]

    return result


def computeCosineDistance(vec1, vec2):
    scalarProduct = 0
    vectLength1 = 0
    vectLength2 = 0

    for i in range(len(vec1)):
        vectLength1 += vec1[i] * vec1[i]
        vectLength2 += vec2[i] * vec2[i]
        scalarProduct += vec1[i] * vec2[i]

    return scalarProduct / (math.sqrt(vectLength1) * math.sqrt(vectLength2))


def queryIndexESA(resource, index, model, freqDict, names, stopWords=None, resultCount=None):

    new_bag = createBag(resource, stopWords, stemmer=nltk.stem.SnowballStemmer('english'))
    new_bow = freqDict.doc2bow(new_bag)
    new_vec = model[new_bow]

    sims = index[new_vec]
    docScores = dict()

    for i, doc in enumerate(index.index):
        docScores[names[i]] = computeCosineDistance(index[doc], sims)

    result = dict()

    if not resultCount:
        resultCount = len(index.index)

    for i, doc in enumerate(sorted(docScores, key=docScores.get, reverse=True)):
        result[doc] = docScores[doc]
        if i > resultCount:
            break

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


def createLsaFileDump(suffix):
    stopWords = ["import", "java", "org", "softlang"]
    names, texts = createFileDocuments(suffix, stopWords)
    index, model, tfidf, freqDict = generateLsaIndex(texts)
    simDump = dict()

    for i, sims in enumerate(index):
        simDict = dict()
        for j, value in sorted(enumerate(sims), key=lambda item: -item[1])[:11]:
            if not i==j:
                simDict[names[j]] = str(value)
        top10 = OrderedDict(sorted(simDict.items(), key=lambda t: -float(t[1])))
        simDump[names[i]] = [top10]

    json.dump(simDump, open(os.path.join(const101.dumps, "similarities_lsa.json"), 'w'))


def createFragmentDump(suffix):
    stopWords = ["import", "java", "org", "softlang"]
    names, texts = createFragmentDocuments(suffix, stopWords)
    index, model, tfidf, freqDict = generateLsaIndex(texts)
    simDump = dict()

    for i, sims in enumerate(index):
        simDict = dict()
        for j, value in sorted(enumerate(sims), key=lambda item: -item[1])[:11]:
            if not i==j:
                simDict[names[j]] = str(value)
        top10 = OrderedDict(sorted(simDict.items(), key=lambda t: -float(t[1])))
        simDump[names[i]] = [top10]

    json.dump(simDump, open(os.path.join(const101.dumps, "similarities_fragments_lsa.json"), 'w'))

def contrDetectionSamples():
    # contribution detection
    testResource = const101.tRoot+"/contributions/gwtTree/src/org/softlang/client/guiinfos/tree/comparators/DepComparator.java.refinedTokens.json"
    #testResource = const101.tRoot+"/contributions/mobileAndroid/src/org/softlang/company/mobileAndroid/CompanyWidget.java.refinedTokens.json"
    #testResource = const101.tRoot+"/contributions/jena/org/softlang/jena/rdf/Containment.java.refinedTokens.json"
    #testResource = const101.tRoot+"/contributions/atlTotalPlugin/src/ATL_ComputeTotalPlugin/Activator.java.refinedTokens.json"
    #testResource = const101.tRoot+"/contributions/strutsAnnotation/src/main/java/org/softlang/actions/CompanyAction.java.refinedTokens.json"
    #testResource = const101.tRoot+"/contributions/jsf/jsf/src/java/company/classes/Department.java.refinedTokens.json"
    #testResource = const101.tRoot+"/contributions/jgralab/src/de/uni_koblenz/oneoonecompanies/CompanyServices.java.refinedTokens.json"
    #testResource = const101.tRoot+"/contributions/jdbc/org/softlang/features/Cut.java.refinedTokens.json"
    stopWords = ["import", "java", "org", "softlang"]
    names, texts = createFileDocuments(".java", stopWords)
    index, model, freqDict = generateIndex(texts)
    resourceContent = json.load(open(testResource))
    queryResult = queryIndex(resourceContent, index, model, freqDict, names, stopWords=stopWords, resultCount=50)
    for key, value in sorted(queryResult.iteritems(), key=lambda (k, v): (-v, k)):
        if not key == testResource:
            print "%s : %s" % (value, key)

    print "-----------------------------------------------------------------------------------below"

    queryResult2 = queryIndexESA(resourceContent, index, model, freqDict, names, stopWords=stopWords, resultCount=50)
    for key, value in sorted(queryResult2.iteritems(), key=lambda (k, v): (-v, k)):
        if not key == testResource:
            print "%s : %s" % (value, key)



def fragmentDetectionSamples():

    # fragment detection
    #testResource = const101.tRoot+"/contributions/hibernate/org/softlang/company/Company.java/class/Company/method/setId"
    #testResource = const101.tRoot+"/contributions/jsf/jsf/src/java/company/classes/Company.java/class/Company/method/getDepartments"
    #testResource = const101.tRoot+"/contributions/jdbc/org/softlang/features/Depth.java/class/Depth/method/depth/1"
    testResource = const101.tRoot+"/contributions/jena/org/softlang/jena/rdf/Containment.java/class/Containment/method/checkContainment"
    #testResource = const101.tRoot+"/contributions/antlrLexer/src/main/java/org/softlang/company/features/Parsing.java/class/Parsing/method/parse"

    suffix = ".java"
    filename, fragmentname = testResource.split(suffix+"/")
    tokenFile = json.load(open(os.path.join(filename+suffix+".fragments.refinedTokens.json")))
    resourceContent = tokenFile[fragmentname]

    stopWords = ["import", "java", "org", "softlang"]
    names, texts = createFragmentDocuments(suffix, stopWords)
    index, model, freqDict = generateIndex(texts)
    queryResult = queryIndex(resourceContent, index, model, freqDict, names, stopWords=stopWords, resultCount=30)
    for key, value in sorted(queryResult.iteritems(), key=lambda (k, v): (-v, k)):
        if not key == testResource:
            print "%s : %s" % (value, key)

    print "ESA RESULTS--------------------------------------------------------------------------------------------------"

    queryResultESA = queryIndexESA(resourceContent, index, model, freqDict, names, stopWords=stopWords, resultCount=30)
    for key, value in sorted(queryResultESA.iteritems(), key=lambda (k, v): (-v, k)):
        if not key == testResource:
            print "%s : %s" % (value, key)


def getMostImportantTokens(suffix):
    stopWords = ["import", "java", "org", "softlang"]
    names, texts = createFileDocuments(suffix, stopWords)
    index, model, freqDict = generateIndex(texts)

    cDict = dict()

    for text in texts:
        for tuple in model[freqDict.doc2bow(text)]:
            key = freqDict[tuple[0]]
            #sys.stdout.write("("+str(key)+","+str(tuple[1])+")")
            if key not in cDict:
                cDict[key] = tuple[1]
            else:
                cDict[key] += tuple[1]
        #print ""


    #for k,v in sorted(cDict.iteritems(), key=lambda item: -item[1]):
    #    print str(k)+","+str(v)

    for k,v in sorted(freqDict.iteritems(), key=lambda pair: -freqDict.dfs[pair[0]]):
        print str(v)+","+str(freqDict.dfs[k])


def plotTopics(no_below=None, no_above=None, keep_n=None):

    names, texts = createFileDocuments(".java", ["import", "java", "org", "softlang"])
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
    tfidf = models.TfidfModel(corpus, id2word=freqDictionary)
    corpus_idf = tfidf[corpus]

    lsi = models.LsiModel(corpus_idf, id2word=freqDictionary, num_topics=3) # initialize an LSI transformation
    lsi.print_topics(3,300)
    corpus_lsi = lsi[corpus_idf]

    xs = []
    ys = []
    zs = []

    contrPoints = dict()

    for i, doc in enumerate(corpus_lsi):
        contr = names[i].split("contributions/")[1].split("/")[0]
        if not contrPoints.has_key(contr):
            contrPoints[contr] = dict()
            contrPoints[contr]["xs"] = []
            contrPoints[contr]["ys"] = []
            contrPoints[contr]["zs"] = []

        contrPoints[contr]["xs"].append(doc[0][1])
        contrPoints[contr]["ys"].append(doc[1][1])
        contrPoints[contr]["zs"].append(doc[2][1])



    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import numpy as np
    import matplotlib.cm as cm

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    colors = cm.rainbow(np.linspace(0, 1, len(contrPoints)))
    i = 0

    for contr, values in contrPoints.iteritems():

        ax.scatter(values["xs"], values["ys"], values["zs"], c=colors[i])
        i+=1

    plt.legend(contrPoints.keys())
    plt.show()


def labelClusters(lsi):
    topics = dict()
    avg = dict()

    for i in range(lsi.num_topics):
        topics[i] = dict()
        for termTuple in lsi.show_topic(i, 100):
            if termTuple[0] > 0:
                topics[i][termTuple[1]] = termTuple[0]

                if not avg.has_key(termTuple[1]):
                    avg[termTuple[1]] = termTuple[0]
                else:
                    avg[termTuple[1]] = avg[termTuple[1]] + termTuple[0]


    for topic, termDict in topics.iteritems():
        for term, score in termDict.iteritems():
            topics[topic][term] = score - (avg[term]/lsi.num_topics)

    for topic, termDict in topics.iteritems():
        print "------------------------------------------------------------------------------------------"
        print "Topic = "+str(topic)+" Label= "
        for term in sorted(termDict, key=termDict.get, reverse=True):
            print term+" "+str(termDict[term])


def generateLsaIndex(texts, topics=10, no_below=None, no_above=None, keep_n=None):

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
    tfidf = models.TfidfModel(corpus, id2word=freqDictionary)
    lsi = models.LsiModel(tfidf[corpus], id2word=freqDictionary, num_topics=topics) # initialize an LSI transformation
    index = similarities.MatrixSimilarity(lsi[corpus])

    labelClusters(lsi)

    return index, lsi, tfidf, freqDictionary


def queryLsaIndex(resource, index, lsi, tfidf, freqDict, names, stopWords=None, resultCount=None):

    new_bag = createBag(resource, stopWords, stemmer=nltk.stem.SnowballStemmer('english'))
    new_bow = freqDict.doc2bow(new_bag)
    new_vec = lsi[tfidf[new_bow]]

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


def compareLsaToTfidf():

    createFileDump(".java")
    createLsaFileDump(".java")


    lsaDump = json.load(open(os.path.join(const101.dumps, "similarities_lsa.json"), 'r'))
    tfidfDump = json.load(open(os.path.join(const101.dumps, "similarities.json"), 'r'))

    pos=0
    neg=0

    for resource, lsaSims in lsaDump.iteritems():
        tfidfSims = tfidfDump[resource]
        pos += len(set(lsaSims[0].keys()).intersection(set(tfidfSims[0].keys())))


    print "pos="+str(float(pos)/(10*len(lsaDump)))


#createFileDump(".java")
#contrDetectionSamples()
createFragmentDump(".java")
fragmentDetectionSamples()
