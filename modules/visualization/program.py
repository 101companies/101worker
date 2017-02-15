import os
import json
import csv
import shutil


'''
write functions
'''

def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def write_csv(target,csvData):
    d = os.path.join(target, 'data.csv')
    with open(d, 'w') as f:
        wr = csv.writer(f)
        for item in csvData:
            wr.writerow(item)

def assemble_piechart(endFolderName,xName,yName,xValues,yValues, moduleName, env):
    dataPath = os.path.join(env.get_env('views101dir'),moduleName,endFolderName)
    mainPath = os.path.join(env.get_env('views101dir'),moduleName)
    check_path(dataPath)
    chartName = "pie"
    csvData = []
    labels = ['age','population']
    csvData.append(labels)
    for x,y in zip(xValues,yValues): 
        csvData.append([x,y])
    write_csv(dataPath,csvData)
    copyTemplateToTarget(moduleName,endFolderName,chartName,env)
    manageLinkFile(endFolderName,mainPath)

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

def copyTemplateToTarget(moduleName,endFolderName,chartName,env):
    shutil.copyfile(env.get_env('modules101dir')+os.sep+'visualization'+os.sep+'template'+os.sep+chartName+'.html',env.get_env('views101dir')+os.sep+moduleName+os.sep+endFolderName+os.sep+'chart.html')
	
'''
program
'''

def run(env, res):

    # modules
    from .module.locPerContribution import run as runLocPerContribution
    runLocPerContribution(env, res)
