import os
import json
import csv
import shutil


def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def write_csv(target,csvData,name):
    d = os.path.join(target, name + '.csv')
    with open(d, 'w') as f:
        wr = csv.writer(f)
        for item in csvData:
            wr.writerow(item)
    return name + '.csv'

def create_piechart(name,moduleName,xName,yName,xValues,yValues,path):
    dataPath = os.path.join(path,moduleName)
    check_path(dataPath)
    templateName = "pie"
    csvData = []
    labels = ['age','population']
    csvData.append(labels)
    for x,y in zip(xValues,yValues): 
        csvData.append([x,y])
    csvname = write_csv(dataPath,csvData, name)
    copyTemplateToTarget(path,name,moduleName, csvname,templateName)
    folderIterator(path)


def folderIterator(path):
    data = {}
    for dirs in os.listdir(path):
        htmlfiles = []
        if dirs.endswith('index.html'):
            continue
        for files in os.listdir(path + os.sep + dirs):
            if files.endswith('.html'):
                htmlfiles.append(files)
        data[dirs] = htmlfiles
    updateIndex(path, data)

def updateIndex(path, data):

    targetpath = path + os.sep + 'index.html'
    templatepath = os.path.join('templates','index.html')
    shutil.copyfile(templatepath, targetpath)
    for key in data.keys():
        skiplines = False
        inputfile = open(targetpath, 'r')
        tempfile = open(path + os.sep + 'temp', 'w')
        keyfound = False
		
        for line in inputfile:
            if line.find('<!--'+ key + '-->') != -1:
                skiplines = True
                keyfound = True
                tempfile.writelines(line)
            if line.find('<!--'+key+'-END-->') != -1:
                skiplines = False
                line = ""
            if not skiplines:
                tempfile.writelines(line)

        if not keyfound:
            os.remove(path + os.sep + 'temp')
            inputfile = open(path + os.sep + 'index.html', 'r')
            tempfile = open(path + os.sep + 'temp', 'w')
            for line in inputfile:
                if line.find('<!-- xxx -->') != -1:
                    line = '<!--'+ key + '-->' + "\n" + '<!--'+key+'-END-->' + "\n<!-- xxx -->\n"
                tempfile.writelines(line)
        tempfile = open(path + os.sep + 'temp', 'r')
        inputfile = open(path + os.sep + 'index.html', 'w')
        for line in tempfile:
            if line.find('<!--'+ key + '-->') != -1:
                line = createHtmlTag(key, data[key])
            inputfile.writelines(line)
        os.remove(path + os.sep + 'temp')

def createHtmlTag(key, array):
    htmlNote = '<!--'+ key + '-->' + "\n"
    header = "<details>\n<summary>"+key+"</summary>\n<ul>\n"
    fullCode = htmlNote + header
    for item in array:
        linkperitem = "<li><a href="+key+os.sep+item+" target=\'content_frame\'>"+item+"</a></li>\n"
        fullCode = fullCode + linkperitem
    endNode = "\n</ul>\n</details>\n"+"<!--"+key+"-END--> \n"
    fullcode = fullCode + endNode
    return fullcode

def copyTemplateToTarget(path,name,moduleName, dataname, templateName):
    #hard-code template folder path??
    templatePath = os.path.join('templates',templateName+'.html')
    targetPath = os.path.join(path,moduleName, name + '.html')
    insertTemplate(templatePath, targetPath, dataname)

def insertTemplate(template, targetpath, dataname):
    inputfile = open(template)
    outputfile = open(targetpath, 'w')

    for line in inputfile:
        if line.find('enterDataHere'):
            line = line.replace('enterDataHere', dataname)
        outputfile.writelines(line)


#################
# Google Charts #
#################

# barChart
def create_googleChart_bar(moduleName, fileName, options, data, path):
    sourcePath = os.path.join('templates', 'googleCharts', 'barChart.html')
    targetFolder = os.path.join(path, moduleName)
    targetPath = os.path.join(path, moduleName, fileName + '.html')
    inputFile = open(sourcePath)
    check_path(targetFolder)
    outputFile = open(targetPath, 'w')
    for line in inputFile:
        if line.find('INSERT_DATA'):
            line = line.replace('INSERT_DATA', str(data))
        if line.find('INSERT_OPTIONS'):
            line = line.replace('INSERT_OPTIONS', options)
# pieChart
def create_googleChart_pie(moduleName, fileName, options, data, path): 
    sourcePath = os.path.join('templates', 'googleCharts', 'pieChart.html')
    targetFolder = os.path.join(path, moduleName)
    targetPath = os.path.join(path, moduleName, fileName + '.html')
    inputFile = open(sourcePath)
    check_path(targetFolder)
    outputFile = open(targetPath, 'w')
    for line in inputFile:
        if line.find('INSERT_DATA'):
            line = line.replace('INSERT_DATA', str(data))
        if line.find('INSERT_OPTIONS'):
            line = line.replace('INSERT_OPTIONS', options)
        outputFile.writelines(line)












    

