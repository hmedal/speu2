'''
Created on Jul 11, 2016

@author: hmedal
'''
import os
import platform
import multiprocessing
import lxml.etree as etree
import unittest
import getpass

class Cluster(object):
    
    def __init__(self, filename = None, institution = None, name = None, processorsPerNode = None, serverName = None,
                 codePathOnCluster = '~/code/src/python/'):
        if filename is not None:
            ''' reads in XML file'''
            d = etree.parse(open(filename))
            institution = str(d.xpath('//info/institution[1]/text()')[0])
            name = str(d.xpath('//info/clusterName[1]/text()')[0])
            processorsPerNode = str(d.xpath('//info/processorsPerNode[1]/text()')[0])
            serverName = str(d.xpath('//info/serverName[1]/text()')[0])
        self.createCluster(institution, name, processorsPerNode, serverName)
        self.codePathOnCluster = codePathOnCluster
        
    def createCluster(self, institution, name, processorsPerNode, serverName):
        self.institution = institution
        self.name = name
        self.processorsPerNode = processorsPerNode
        self.serverName = serverName
        
    def syncProjectFiles(self, sourcePath):
        destFullPath = self.serverName + ':' + self.codePathOnCluster
        rsyncStr = 'rsync -av ' + sourcePath + ' ' + destFullPath
        print rsyncStr
        os.system(rsyncStr)
        
class Queue(object):
    
    def __init__(self, filename = None, cluster = None, name = None, maxProcessors = None, maxtime = None):
        ''' reads in XML file'''
        if filename is not None:
            cluster = Cluster(filename)
            d = etree.parse(open(filename))
            name = str(d.xpath('//info/queuename[1]/text()')[0])
            maxProcessors = str(d.xpath('//info/maxProcessors[1]/text()')[0])
            maxtime = str(d.xpath('//info/maxtime[1]/text()')[0]) # in hours
        else:
            cluster = cluster
        self.createQueue(cluster, name, maxProcessors, maxtime)
        
    def createQueue(self, cluster, name, maxProcessors, maxtime):
        self.cluster = cluster
        self.name = name
        self.maxProcessors = maxProcessors
        self.maxtime = maxtime
    
class ComputationalResource(object):
    '''
    classdocs
    '''
    
    def __init__(self, filename = None, queue = None, numThreadsToUse = None, programToExecuteWith = None,
                 exeStatement = None, orgFund = 'unsponsored', type = 'remote'):
        self.schedulerCommand = '/usr/local/torque/bin/qsub'
        self.type = type
        self.orgFund = orgFund
        if filename is not None:
            self.queue = Queue(filename)
            d = etree.parse(open(filename))
            self.numThreadsToUse = str(d.xpath('//info/numThreadsToUse[1]/text()')[0])
            self.programToExecuteWith = str(d.xpath('//info/numThreadsToUse[1]/text()')[0])
        else:
            self.queue = queue
            self.numThreadsToUse = numThreadsToUse
            self.programToExecuteWith = programToExecuteWith
            self.exeStatement = exeStatement
        
    def getInfo(self):
        procInfo = os.popen("cat /proc/cpuinfo | grep 'model name' | uniq").read()
        return [self.queue.cluster.institution, self.queue.cluster.name, platform.machine(), platform.processor(),
                platform.system(), platform.python_version(), platform.node(), procInfo, multiprocessing.cpu_count()]
    
def createComputationalResource(name):
    if name == 'shadow2':
        serverName = 'shadow-login.hpc.msstate.edu'
        if getpass.getuser() == 'hm568':
            serverName = 'hmedal@shadow-login.hpc.msstate.edu'
        cluster = Cluster(institution= 'msu', name = 'shadow2', processorsPerNode= 20, serverName = serverName)
        queue = Queue(cluster = cluster, name = 'qdasi200p48h', maxProcessors = 200, maxtime = 48)
        myCompResource = ComputationalResource(queue = queue, numThreadsToUse = 20, programToExecuteWith = 'python',
                                               exeStatement = '~/code/src/python/wnopt/src/runScripts/execute.py')
    elif name == 'shadow-unsponsored':
        serverName = 'shadow-login.hpc.msstate.edu'
        if getpass.getuser() == 'hm568':
            serverName = 'hmedal@shadow-login.hpc.msstate.edu'
        cluster = Cluster(institution= 'msu', name = 'shadow', processorsPerNode= 20, serverName = serverName)
        queue = Queue(cluster = cluster, name = 'q200p48h', maxProcessors = 200, maxtime = 0.6)
        myCompResource = ComputationalResource(queue = queue, numThreadsToUse = 20, programToExecuteWith = 'python',
                            exeStatement = '~/code/src/python/wnopt/src/runScripts/execute.py',
                            orgFund = 'unsponsored')
    elif name == 'shadow-debug':
        serverName = 'shadow-login.hpc.msstate.edu'
        if getpass.getuser() == 'hm568':
            serverName = 'hmedal@shadow-login.hpc.msstate.edu'
        cluster = Cluster(institution= 'msu', name = 'shadow', processorsPerNode= 20, serverName = serverName)
        queue = Queue(cluster = cluster, name = 'q200p48h', maxProcessors = 200, maxtime = 0.1)
        myCompResource = ComputationalResource(queue = queue, numThreadsToUse = 20, programToExecuteWith = 'python',
                            exeStatement = '~/code/src/python/wnopt/src/runScripts/execute.py',
                            orgFund = 'unsponsored')
    elif name == 'shadow-360746':
        serverName = 'shadow-login.hpc.msstate.edu'
        if getpass.getuser() == 'hm568':
            serverName = 'hmedal@shadow-login.hpc.msstate.edu'
        cluster = Cluster(institution= 'msu', name = 'shadow', processorsPerNode= 20, serverName = serverName)
        queue = Queue(cluster = cluster, name = 'q200p48h', maxProcessors = 200, maxtime = 48)
        myCompResource = ComputationalResource(queue = queue, numThreadsToUse = 20, programToExecuteWith = 'python',
                            exeStatement = '~/code/src/python/wnopt/src/runScripts/execute.py',
                            orgFund = '060803-360746')
    elif name == 'shadow-360746-debug':
        serverName = 'shadow-login.hpc.msstate.edu'
        if getpass.getuser() == 'hm568':
            serverName = 'hmedal@shadow-login.hpc.msstate.edu'
        cluster = Cluster(institution= 'msu', name = 'shadow', processorsPerNode= 20, serverName = serverName)
        queue = Queue(cluster = cluster, name = 'q200p48h', maxProcessors = 200, maxtime = 0.1)
        myCompResource = ComputationalResource(queue = queue, numThreadsToUse = 20, programToExecuteWith = 'python',
                            exeStatement = '~/code/src/python/wnopt/src/runScripts/execute.py',
                            orgFund = '060803-360746')
    elif name == 'shadow-360746-test':
        serverName = 'shadow-login.hpc.msstate.edu'
        if getpass.getuser() == 'hm568':
            serverName = 'hmedal@shadow-login.hpc.msstate.edu'
        cluster = Cluster(institution= 'msu', name = 'shadow', processorsPerNode= 20, serverName = serverName)
        queue = Queue(cluster = cluster, name = 'q200p48h', maxProcessors = 200, maxtime = 1)
        myCompResource = ComputationalResource(queue = queue, numThreadsToUse = 20, programToExecuteWith = 'python',
                            exeStatement = '~/code/src/python/wnopt/src/runScripts/execute.py',
                            orgFund = '060803-360746')
    return myCompResource