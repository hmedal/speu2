from objects import experiments, outputtable, computationalresource
import json
import itertools
import copy
import os
import lxml.etree as etree
import sqlite3 as lite
import sys
import subprocess
import datetime
import time

modelsAndAlgorithmNames_global = []
baseParamsDict_global = {}
computationalResource_global = None
outputtable_global = None
outputtable_relerror_global = None
databaseName_global = '../db/facpro-results.db'
databaseTables = {'BaseExpr', 'RelError'}

def remove_old_solution_files():
    dir = "../output/"
    directory = os.listdir(dir)
    for item in directory:
        if item.endswith(".mst") or item.endswith(".sol"):
            os.remove(os.path.join(dir, item))

def setUp(mode = 'debug', resetParams = False):
    if resetParams:
        remove_old_solution_files()
    createOutputTables()
    createDefaultComputationalResource(mode)
    createBaseParamsDict()

def setUpDatabase(dropExisting = False):
    con = None
    try:
        con = lite.connect(databaseName_global)

        c = con.cursor()
        if dropExisting:
            for tableName in databaseTables:
                c.execute('drop table if exists ' + tableName)

        # Create table
        c.execute(getCreateTableString_BaseExpr())
        c.execute(getCreateTableString_RelError())

        con.commit()

    except lite.Error, e:

        if con:
            con.rollback()

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:
        if con:
            con.close()

def getCreateTableString_BaseExpr():
    myDict = json.loads(open('../db/databaseTableColumns.json').read())
    typesDict = myDict['types']
    string =         'CREATE TABLE ' + 'BaseExpr' + '''('''
    for column in myDict['metaColumns']:
        string += column + ' ' + typesDict[column] + ', '
    for dbColCategory in myDict['columnsInAllTables']:
        for dbColName in myDict['columnsInAllTables'][dbColCategory]:
            string += dbColName + ' ' + typesDict[dbColName] + ', '
    for column in myDict['baseTableColumns']:
        string += column + ' ' + typesDict[column] + ', '
    string = string[:-2]
    string += ''');'''
    return string

def getCreateTableString_RelError():
    myDict = json.loads(open('../db/databaseTableColumns.json').read())
    typesDict = myDict['types']
    string = 'CREATE TABLE ' + 'RelError' + '''('''
    for column in myDict['metaColumns']:
        string += column + ' ' + typesDict[column] + ', '
    for dbColCategory in myDict['columnsInAllTables']:
        for dbColName in myDict['columnsInAllTables'][dbColCategory]:
            string += dbColName + ' ' + typesDict[dbColName] + ', '
    for column in myDict['relErrorTableColumns']:
        string += column + ' ' + typesDict[column] + ', '
    string = string[:-2]
    string += ''');'''
    return string

def createOutputTables():
    global outputtable_global, outputtable_relerror_global
    outputtable_global = outputtable.OutputTable(databaseName = databaseName_global, tableName = 'mainTable')
    outputtable_relerror_global = outputtable.OutputTable(databaseName = databaseName_global, tableName='relerrorTable')

def createDefaultComputationalResource(mode = 'debug'):
    global computationalResource_global
    if mode == 'debug':
        computationalResource_global = computationalresource.createComputationalResource('shadow-debug')
    elif mode == 'test':
        computationalResource_global = computationalresource.createComputationalResource('shadow-360746-test')
    else:
        computationalResource_global = computationalresource.createComputationalResource('shadow-360746')

def createBaseParamsDict():
    global baseParamsDict_global
    baseParamsDict_global = json.loads(open('baseExperimentParameters.json').read())

def flatten_two_level_nested_dict(dict):
    newDict = {}
    for key in dict:
        for subkey in dict[key]:
            newDict[subkey] = dict[key][subkey]
    return newDict

def cardProductOfDictionaries(paramsDict):
    for key in paramsDict:
        if not isinstance(paramsDict[key], list):
            paramsDict[key] = [paramsDict[key]]
    return list(dict(itertools.izip(paramsDict, x)) for x in itertools.product(*paramsDict.itervalues()))

def createParamsDictsForExprmnts(baseParamsDict, rangesOfParametersToVary, group_def = None):
    ''' returns a list of dictonaries, one for each experiment'''
    if group_def is not None:
        baseParamsDict = flatten_two_level_nested_dict(baseParamsDict)
    newParamsDict = copy.deepcopy(baseParamsDict)
    for paramName in rangesOfParametersToVary.keys():
        newParamsDict[paramName] = rangesOfParametersToVary[paramName]
    list_of_flattened_dicts = cardProductOfDictionaries(newParamsDict)
    list_of_unflattened_dicts = []
    for flattened_dict in list_of_flattened_dicts:
        unflattened_dict = {}
        for key in group_def:
            unflattened_dict[key] = {}
            for subkey in group_def[key]:
                unflattened_dict[key][subkey] = flattened_dict[subkey]
        list_of_unflattened_dicts.append(unflattened_dict)
    return list_of_unflattened_dicts

def getFilenameForExprParamsDict(rangesOfParametersToVary, paramsDict):
    paramsToVary = rangesOfParametersToVary.keys()
    stringToAdd = ''
    for paramName in paramsToVary:
        stringToAdd += '_' + paramName + '-' + paramsDict[paramName]
    return '../exprFiles/ExprParams_base' + stringToAdd + '.json'

def runExperimentsForExperimentBatch(ranges_of_params_to_vary, experimentName,
                                     modelsAndAlgs = modelsAndAlgorithmNames_global, baseParamsDict = None,
                                     runTheExperiments = False, localMode = False):
    group_def = json.loads(open('../db/databaseTableColumns.json').read())['columnsInAllTables']
    if baseParamsDict is None:
        params_dicts_for_exprs = createParamsDictsForExprmnts(baseParamsDict_global,
                                                              ranges_of_params_to_vary, group_def)
    else:
        params_dicts_for_exprs = createParamsDictsForExprmnts(baseParamsDict, ranges_of_params_to_vary, group_def)
    print "paramsDictsForExperiments", params_dicts_for_exprs
    exprBatch = experiments.OptimizationExperimentBatch(computationalResource_global,
                                            '../exprBatchScripts/run_experiments_for_' + experimentName + '.sh')
    for paramsDict in params_dicts_for_exprs:
        for infModelName in modelsAndAlgs:
            scriptCall = 'python ' + '../src/models/run_facpro.py'
            exprBatch.addOptimizationExperiment(experiments.OptimizationExperiment(scriptCall,
                            computationalResource_global, outputtable_global, experimentName,
                            parametersDictionary = paramsDict, paramsThatChanged = ranges_of_params_to_vary.keys()))
    exprBatch.writeBatchScript()
    if not localMode:
        print "syncing files"
        os.system('rsync -av --exclude ~/PycharmProjects/wnopt_cavs3/exprBatchScripts/rsync-exclude-list.txt '
                  '~/PycharmProjects/wnopt_cavs3 hmedal@shadow-login:/work/hmedal/code/')
        os.system('ssh hmedal@shadow-login chmod a+x /work/hmedal/code/wnopt_cavs3/exprBatchScripts/*.sh')
        result = subprocess.check_output('ssh hmedal@shadow-login "cd /work/hmedal/code/wnopt_cavs3/exprBatchScripts; '
                  './run_experiments_for_Test.sh"', shell = True)  # note to self: output appears in exprBatchScripts
        print "result ", result
        with open('../log/jobs_scheduled.log', 'a') as f:
            ts = time.time()
            f.write(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') + '\n')
            f.write(result + '\n')  # python will convert \n to os.linesep
            f.close()  # you can omit in most cases as the destructor will call it


def run_experiments_for_RunTime_Table(runTheExperiments = False):
    rangesOfParametersToVary = {'datasetName': ['grid-7x7',
                            'berkeley', 'grid-8x8', 'grid-9x9'], 'numChannels' : [1,2], 'jamBudget' : [1,3]}
    runExperimentsForExperimentBatch(rangesOfParametersToVary, 'RunTime',
                                     modelsAndAlgs=modelsAndAlgorithmNames_global,
                                     runTheExperiments = runTheExperiments)
    if runTheExperiments:
        os.system('ssh hmedal@shadow-login "cd /work/hmedal/code/wnopt_cavs/exprBatchScripts; '
                  './run_experiments_for_RunTime.sh"')

def run_experiments_for_HeatMap_Figure(runTheExperiments = False):
    rangesOfParametersToVary = {'dataset': ['grid-7x7', 'berkeley'], 'numChannels': [1, 2], 'numJammers': [1, 3]}
    paramsDictsForExperiments = createParamsDictsForExprmnts(baseParamsDict_global, rangesOfParametersToVary)
    exprBatch = experiments.OptimizationExperimentBatch(computationalResource_global,
                                                        '../exprBatchScripts/run_experiments_for_HeatMap_Figure.sh')
    for paramsDict in paramsDictsForExperiments:
        for infModelName in ['none', 'semi-additive', 'capture', 'protocol', 'interferenceRangeA',
                             'interferenceRangeB']:
            paramsDict['interferenceApproximateModel'] = infModelName
            paramsDict['interferenceTrueModel'] = 'additive'
            scriptCall = 'python ' + '../src/models/relerror.py'
            exprBatch.addOptimizationExperiment(experiments.OptimizationExperiment(scriptCall,
                        computationalResource_global, outputtable_global, 'HeatMap', parametersDictionary=paramsDict))

def run_experiments_for_NumNodes_Table():
    rangesOfParametersToVary = {'dataset': ['grid-7x7', 'berkeley', 'grid-8x8', 'grid-9x9']}
    runExperimentsForExperimentBatch(rangesOfParametersToVary, 'NumNodes')

def run_experiments_for_NumChannels_Table():
    rangesOfParametersToVary = {'dataset': ['grid-7x7', 'berkeley'], 'numChannels' : [1,2,3]}
    runExperimentsForExperimentBatch(rangesOfParametersToVary, 'NumChannels')

def run_experiments_for_NumJammerLocations_Table_2D():
    rangesOfParametersToVary = {'dataset': ['grid-7x7', 'berkeley'], 'numJammerLocations': [9, 16, 25]}
    runExperimentsForExperimentBatch(rangesOfParametersToVary, 'NumJammerLocations_2D')

def run_experiments_for_NumJammerLocations_Table_3D():
    rangesOfParametersToVary = {'dataset': ['grid_5x5x5', 'berkeley_3d'], 'numJammerLocations': [27, 64, 125]}
    runExperimentsForExperimentBatch(rangesOfParametersToVary, 'NumJammerLocations_3D')

def run_experiments_for_NumJammerLocations_Table():
    run_experiments_for_NumJammerLocations_Table_2D()
    run_experiments_for_NumJammerLocations_Table_3D()

def run_experiments_for_NumJammers_Table():
    rangesOfParametersToVary = {'dataset': ['grid-7x7', 'berkeley'], 'numJammers': [1,2,3,4,5]}
    runExperimentsForExperimentBatch(rangesOfParametersToVary, 'NumJammers')

if __name__ == "__main__":
    setUpDB = False
    setUp()
    if setUpDB:
        setUpDatabase()
    run_experiments_for_RunTime_Table()
    run_experiments_for_HeatMap_Figure()
    run_experiments_for_NumNodes_Table()
    run_experiments_for_NumChannels_Table()
    run_experiments_for_NumJammerLocations_Table()
    run_experiments_for_NumJammers_Table()