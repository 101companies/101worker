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
        for files in os.listdir(path + os.sep + dirs):
            if files.endswith('.html'):
                htmlfiles.append(files)
        data[dirs] = htmlfiles
    updateIndex(path, data)

def updateIndex(path, data):
    if not os.path.isfile(path + os.sep + 'index.html'):
        target = open(path + os.sep + 'index.html', 'w')
    
        
                

def manageLinkFile(moduleName, chartName,mainPath):
    name = moduleName + os.sep + chartName
    data = {"link":[name]}
    if not os.path.isfile(mainPath+os.sep+'links.json'):
        target = os.path.join(mainPath,'links.json')    
    else:
        with open(mainPath+os.sep+'links.json', 'r') as f:
            data=json.load(f)
            if name not in data["link"]:
                data["link"].append(name)
    with open(mainPath+os.sep+'links.json', 'w') as f:
        json.dump(data, f)

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













    

