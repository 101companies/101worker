import os
import json
import csv
import shutil


def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def write_csv(target,csvData):
    d = os.path.join(target, 'data.csv')
    with open(d, 'w') as f:
        wr = csv.writer(f)
        for item in csvData:
            wr.writerow(item)

def create_piechart(name,xName,yName,xValues,yValues,path):
    dataPath = os.path.join(path,name)
    check_path(dataPath)
    templateName = "pie"
    csvData = []
    labels = ['age','population']
    csvData.append(labels)
    for x,y in zip(xValues,yValues): 
        csvData.append([x,y])
    write_csv(dataPath,csvData)
    copyTemplateToTarget(path,name,templateName)
    manageLinkFile(name,path)

def manageLinkFile(endFolderName,mainPath):
    data = {"link":[endFolderName]}
    if not os.path.isfile(mainPath+os.sep+'links.json'):
        target = os.path.join(mainPath,'links.json')    
    else:
        with open(mainPath+os.sep+'links.json', 'r') as f:
            data=json.load(f)
            if endFolderName not in data["link"]:
                data["link"].append(endFolderName)
    with open(mainPath+os.sep+'links.json', 'w') as f:
        json.dump(data, f)

def copyTemplateToTarget(path,name,templateName):
    #hard-code template folder path??
    templatePath = os.path.join('template',templateName+'.html')
    targetPath = os.path.join(path,name,'chart.html')
    shutil.copyfile(templatePath,targetPath)

