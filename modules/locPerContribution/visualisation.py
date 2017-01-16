import numpy
import matplotlib.pyplot as plotting
import os

def createImage(env,workerlibEnv):
    data = env.read_dump('locPerContribution')
    contributions = []
    loc = []    
    for contribution in data.keys():
        contributions.append(contribution)
        loc.append(data[contribution])
    plotting.bar(numpy.arange(len(contributions)),loc,0.35, color = 'b')
    plotting.xlabel("Contribution")
    plotting.ylabel("Lines of Code")
    plotting.xticks(numpy.arange(len(contributions))+0.35/2., contributions)
    plotting.title("LocPerContribution")

    ### check if path exists, else create it ###
    if not os.path.exists(workerlibEnv['views101dir']):
        os.mkdir(workerlibEnv['views101dir'])
    path = workerlibEnv['views101dir']+'/locPerContribution'
    if not os.path.exists(path):
        os.mkdir(path)
    ############################################

    plotting.savefig(path+'/chart.png')

