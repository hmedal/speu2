'''
Created on Jul 11, 2016

@author: hmedal
'''

import os
import xml.etree.cElementTree as ET
import unittest
import json
from src.objects import computationalresource, outputtable


def convertHoursToTimeString(hours):
    seconds = hours * 3600
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

def get_params_string_name(parametersDictionary, paramsThatChanged = None):
    paramsString = ''
    shortNamesDict = json.loads(open('../expr_scripts_for_paper/params_shortNames.json').read())
    if paramsThatChanged is None or len(paramsThatChanged) == 0:
        paramsString = 'base'
    else:
        for paramName in paramsThatChanged:
            paramsString += '_' + shortNamesDict[paramName] + '-' + str(parametersDictionary[paramName])
    return paramsString

def get_filename_from_params_dict(parametersDictionary, paramsThatChanged=None):
    infModelName = parametersDictionary['signal']['infModelName']
    return infModelName + "_" + get_params_string_name(parametersDictionary, paramsThatChanged = None)

def createOutputFileNameFromParamsDict(parametersDictionary, exprBatchName, paramsThatChanged = None):
    return '../output/' + get_filename_from_params_dict(parametersDictionary, paramsThatChanged) + '.out'

def createExprFileFromParamsDict(paramsDict, exprBatchName, paramsThatChanged = None):
    print "paramsDict before write", paramsDict
    exprFileName = '../exprFiles/' + get_filename_from_params_dict(paramsDict, paramsThatChanged) + '.json'
    with open(exprFileName, 'w') as exprFileObject:
        json.dump(paramsDict, exprFileObject, indent=4, sort_keys=True)
    return exprFileName

class OptimizationExperiment(object):
    '''
    For the purpose of printing out output
    '''

    def __init__(self, scriptCall, computationalResource, outputTable, exprName, parametersDictionary = None,
                 paramsThatChanged = None, outputFileName = None, exprFile = None):
        '''
        Constructor
        '''
        self.scriptCall = scriptCall
        self.compResource = computationalResource
        self.outputTable = outputTable
        self.exprName = exprName
        if outputFileName is None:
            if parametersDictionary is None:
                raise Exception("parametersDictionary may not be None if outputFileName is None")
            self.outputFileName = createOutputFileNameFromParamsDict(parametersDictionary, exprName, paramsThatChanged)
        else:
            self.outputFileName = outputFileName
        if exprFile is None:
            if parametersDictionary is None:
                raise Exception("parametersDictionary may not be None if exprFile is None")
            self.exprFile = createExprFileFromParamsDict(parametersDictionary, exprName, paramsThatChanged)
        else:
            self.exprFile = exprFile
        self.schedulerCommandFileOutputFilePath = '../runFiles/' + \
                                                  get_filename_from_params_dict(parametersDictionary,
                                                                                paramsThatChanged) + '.pbs'
        self.saveSchedulerCommandFile(self.schedulerCommandFileOutputFilePath)
        
    def saveSchedulerCommandFile(self, schedulerCommandFileOutputFilePath, isLastJob = False, fileType = 'pbs'):
        if fileType is 'pbs':
            print "printing to ", schedulerCommandFileOutputFilePath, " ", self.compResource.orgFund
            f = open(schedulerCommandFileOutputFilePath, 'w')
            myStr = ""
            if self.compResource.orgFund != 'unsponsored':
                myStr += "#PBS -A " + self.compResource.orgFund + "\n"
            myStr += "#PBS -N " + self.exprName + "\n"
            myStr += "#PBS -q " + self.compResource.queue.name + "\n"
            myStr += "\n"
            myStr += "#PBS -j oe\n"
            myStr += "\n"
            myStr += "#PBS -M hugh.medal@msstate.edu\n" # send me email when job aborts (with an error)
            if isLastJob:
                myStr += "#PBS -m ae\n"
            else:
                myStr += "#PBS -m a\n"
            myStr += "#PBS -o " + self.exprName +".$PBS_JOBID\n"
            myStr += "#PBS -l nodes=1:ppn=" + str(self.compResource.numThreadsToUse) + "\n"
            myStr += "#PBS -l walltime=" + str(convertHoursToTimeString(self.compResource.queue.maxtime)) + "\n"
            myStr += "\n"
            myStr += "cd $PBS_O_WORKDIR\n"
            myStr += 'export PYTHONPATH="$PYTHONPATH:/work/hmedal/code/wnopt_cavs3"' + "\n"
            myStr += self.scriptCall + " -e " + self.exprFile + " > " + self.outputFileName
            f.write(myStr)
        else:
            raise Exception('invalid type')
        
class OptimizationExperimentBatch(object):
    ''''''

    def __init__(self, computationalResource, filepathForBatch):
        self.computationalResource = computationalResource
        self.experimentsList = []
        self.filepathForBatch = filepathForBatch
    
    def addOptimizationExperiment(self, experiment):
        self.experimentsList.append(experiment)
        
    def writeBatchScript(self):
        if self.computationalResource.type is 'local':
            self.writeBatchScript_Local()
        elif self.computationalResource.type is 'remote':
            self.writeBatchScript_Remote()
        else:
            raise Exception('type is unknown')
        
    def writeBatchScript_Local(self):
        f = open(self.filepathForBatch, 'w')
        myStr = "#!/bin/bash\n"
        for experiment in self.experimentsList:
            myStr += experiment.schedulerCommandFileOutputFilePath + "\n"
        f.write(myStr)
        os.system("chmod a+x " + self.filepathForBatch)
        
    def writeBatchScript_Remote(self):
        f = open(self.filepathForBatch, 'w')
        myStr = "#!/bin/sh\n"
        myStr += ". ~/.bashrc"
        myStr += "\n"
        print "printing " + str(len(self.experimentsList)) + " experiments in batch script"
        for experiment in self.experimentsList:
            print "experiment", experiment, experiment.compResource
            myStr += experiment.compResource.schedulerCommand + " " + \
                     experiment.schedulerCommandFileOutputFilePath + "\n"
        print "writing to file"
        f.write(myStr)
    
    def runBatchScript(self):
        print "running batch script..."
        os.system('ssh hmedal@shadow-login.hpc.msstate.edu "cd /work/hmedal/code/wnopt_cavs/exprBatchScripts; '
                  + self.filepathForBatch)
        print "...batch script ran"

    def writeAndRun(self):
        print "printing batch script..."
        self.writeBatchScript()
        print "...batch script printed"
        self.runBatchScript()