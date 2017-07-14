'''
Created on Aug 23, 2013

@author: hmedal
'''

import numpy as np
from scipy import stats
import gurobipy
import logging
import time
from multiprocessing import Pool
import lxml.etree as etree
import ast
import itertools
import json
import argparse

class Dataset(object):
    '''
    classdocs
    '''

    def __init__(self, dataFilePath):
        self.readInDataset(dataFilePath)

    def readInDataset(self, path):
        # print "path: ", path
        # global numFacs, demPtWts, numDemPts, capacities, pairsDistMatrix
        d = etree.parse(open(path))
        # facility information

        self.facXVals = [float(i) for i in d.xpath('//fac/@x')]
        self.facYVals = [float(i) for i in d.xpath('//fac/@y')]
        self.coor = [[self.facXVals[i], self.facYVals[i]] for i in range(len(self.facXVals))]
        facNames = d.xpath('//fac/@name')

        self.numFacs = len(self.facXVals)
        self.facIDs = [int(i) for i in d.xpath('//fac/@id')]
        # demand point information
        demPtXVals = [float(i) for i in d.xpath('//demPt/@x')]
        demPtYVals = [float(i) for i in d.xpath('//demPt/@y')]
        demPtIDs = [int(i) for i in d.xpath('//demPt/@id')]
        demPtNames = d.xpath('//demPt/@name')
        self.demPtWts = [float(i) for i in d.xpath('//demPt/@wt')]
        self.numDemPts = len(demPtXVals)
        # sumDemand = sum(self.demPtWts)
        # capacities = [(sumDemand/((1-excess_capacity)*numFacs)) for i in range(numFacs)]
        # pairs info
        pairsDist = d.xpath('//pair/@dist')
        # pairsDistFloats = [float(value) for value in pairsDist]
        self.pairsDistMatrix = [[float(pairsDist[i * self.numFacs + j]) for j in range(self.numFacs)] for i in
                                range(self.numDemPts)]

class ProblemInstance(object):
    '''
    classdocs
    '''

    utility_dissipation_constant = 3
    distance_rate = 100.0  # miles per hour perhaps (traveling by plane)

    def __init__(self, params_file):
        if isinstance(params_file, dict):
            params_dict = params_file
        else:
            params_dict = json.loads(open(params_file).read())
        self.readInExperimentData(params_dict)
        dataset_name = params_dict['datasetName']
        num_facs = params_dict['num_facs']
        dataFilePath = params_dict['data_file_path']
        self.createInstance(Dataset(dataFilePath))

    def time_from_distance(self, distance):
        return distance / self.distance_rate

    def utility(self, distance, maxDistance):
        time = self.time_from_distance(distance)
        maxTime = self.time_from_distance(maxDistance)
        return self.utility_dissipation_constant * np.ma.core.exp(
            -self.utility_dissipation_constant * time / (maxTime + 0.0))

    def readInExperimentData(self, params_dict):
        print "params dict", params_dict
        self.excess_capacity = params_dict['excess_capacity']
        self.penaltyMultiplier = params_dict['penalty_multiplier']
        self.numAllocLevels = params_dict['num_allocation_levels']
        self.numCapLevels = params_dict['num_states']
        #self.budgetMultiplier = params_dict['budget_multiplier']

    def createInstance(self, dataset):
        self.facIDs = dataset.facIDs
        self.numFacs = dataset.numFacs
        self.demPtWts = dataset.demPtWts
        self.numDemPts = dataset.numDemPts
        self.sumDemand = sum(self.demPtWts)
        self.capacities = [(self.sumDemand / ((1 - self.excess_capacity) * self.numFacs)) for i in range(self.numFacs)]
        pairsDistMatrix = dataset.pairsDistMatrix
        maxDist = max([max(pairsDistMatrix[i]) for i in range(self.numFacs)])
        # print "maxDist", maxDist, self.utility(self.penaltyMultiplier * maxDist)

        self.pairsUtilityMatrix = [
            [self.utility(pairsDistMatrix[i][j], self.penaltyMultiplier * maxDist) for j in range(self.numFacs)] for i
            in range(self.numDemPts)]
        for i in range(self.numDemPts):
            self.pairsUtilityMatrix[i].append(
                self.utility(self.penaltyMultiplier * maxDist, self.penaltyMultiplier * maxDist))
        # print "utilMatrix", self.pairsUtilityMatrix
        #print "budget (without round): ", self.budgetMultiplier * self.numFacs * (self.numAllocLevels - 1)
        #self.budget = round(self.budgetMultiplier * self.numFacs * (self.numAllocLevels - 1))
        #print "self.budget: ", self.budget

class SecondStageProblem(object):

    def __init__(self, params_file, debug = False):
        if isinstance(params_file, dict):
            params_dict = params_file
        else:
            params_dict = json.loads(open(params_file).read())
        self.instance = ProblemInstance(params_dict)
        self.num_cap_levels = self.instance.numCapLevels
        self.debug = debug
        self.createModelGurobi()

    def createModelGurobi(self):
        self.gurobiModel = gurobipy.Model("myLP")
        try:
            # Create variables)
            self.assignVars = [
                [self.gurobiModel.addVar(0, 1, vtype=gurobipy.GRB.CONTINUOUS, name="x_" + str(i) + "," + str(j)) for j in
                 range(self.instance.numFacs + 1)] for i in range(self.instance.numDemPts)]
            # Integrate new variables
            self.gurobiModel.update()
            # Set objective
            self.gurobiModel.setObjective(sum(
                [self.instance.demPtWts[i] * self.instance.pairsUtilityMatrix[i][j] * self.assignVars[i][j] for j in
                 range(self.instance.numFacs + 1) for i in range(self.instance.numDemPts)]), gurobipy.GRB.MAXIMIZE)
            self.gurobiModel.update()
            self.capacityConstraints = [self.gurobiModel.addConstr(
                sum([self.instance.demPtWts[i] * self.assignVars[i][j] for i in range(self.instance.numDemPts)]) <=
                self.instance.capacities[j], "capacity_" + str(j)) for j in range(self.instance.numFacs)]
            for i in range(self.instance.numDemPts):
                self.gurobiModel.addConstr(sum([self.assignVars[i][j] for j in range(self.instance.numFacs + 1)]) == 1,
                                      "demand_met" + str(i))
            self.gurobiModel.update()
            self.gurobiModel.setParam('OutputFlag', False)

        except gurobipy.GurobiError as e:
            print 'createTransportationModelGurobi: Gurobi Error reported' + str(e)
            # logging.error('Error reported')

    def resetRHSCapacities(self, cap_levels_for_facs):
        for fac in range(self.instance.numFacs):
            self.capacityConstraints[fac].setAttr("rhs", (cap_levels_for_facs[fac] / float(self.num_cap_levels - 1)) *
                                                  float(self.instance.capacities[fac]))
        self.gurobiModel.update()

    def computeSecondStageUtility(self, cap_levels_for_facs):
        self.resetRHSCapacities(cap_levels_for_facs)
        self.gurobiModel.optimize()
        return self.gurobiModel.objVal

def generate_scens_dict(params_dict, world_states_file=None, states_vector_list=None):
    num_facs = params_dict['num_facs']
    num_states = params_dict['num_states']
    scens = {}
    second_stage_prob = SecondStageProblem(params_dict)
    if world_states_file is None:
        world_states = {}
        world_states[0] = {}
        world_states[0]['probability'] = 1.0
        world_states[0]['exposures'] = [0] * num_facs
    else:
        world_states = json.loads(open(world_states_file).read())
    scens = {}
    count = 0
    if states_vector_list is None:
        states_vector_list = itertools.product(range(num_states), repeat=num_facs)
    for world_state in world_states:
        for states_vector in states_vector_list:
            scens[count] = {}
            scens[count]['component_states'] = states_vector
            scens[count]['exposures'] = world_states[world_state]['exposures']
            scens[count]['prob_of_world_state'] = world_states[world_state]['probability']
            scens[count]['objective_value'] = second_stage_prob.computeSecondStageUtility(states_vector)
            count += 1
    return scens

def get_params_string_scens(num_facs, num_states):
    return "j_" + str(num_facs) + "_l_" + str(num_states)

def get_scen_sample_dict(sample_size, params_dict, world_states_dict, allocation_dict = None):
    num_facs = params_dict['num_facs']
    num_states = params_dict['num_states']
    second_stage_prob = SecondStageProblem(params_dict)
    world_states_probs = [world_states_dict[str(key)]['probability'] for key in range(len(world_states_dict))]
    world_states_values = range(len(world_states_dict))
    scens = {}
    for iteration in range(sample_size):
        scens[iteration] = {}
        world_state = np.random.choice(world_states_values, 1, p=world_states_probs)[0]
        scens[iteration]['exposures'] = world_states_dict[str(world_state)]['exposures']
        if allocation_dict is None:
            states = list(np.random.randint(num_states, size=num_facs))
        else:
            state_values = range(num_states)
            states = []
            for fac in range(num_facs):
                exposure = world_states_dict[str(world_state)]['exposures'][fac]
                probs = [allocation_dict[str(fac)]['state_probs'][str(exposure)][str(state)] for state in state_values]
                states.append(np.random.choice(state_values, 1, p = probs)[0])
        scens[iteration]['component_states'] = states
        scens[iteration]['objective_value'] = second_stage_prob.computeSecondStageUtility(states)
    return scens

def generate_scens_saa_second_stage(params_dict, allocation_dict, saa_params_dict, world_states_file = None):
    second_stage_samples = saa_params_dict['saa_second_stage_samples']
    num_facs = params_dict['num_facs']
    num_states = params_dict['num_states']
    if world_states_file is None:
        world_states = {}
        world_states[0] = {}
        world_states[0]['probability'] = 1.0
        world_states[0]['exposures'] = [0] * num_facs
    else:
        world_states = json.loads(open(world_states_file).read())
    scens = get_scen_sample_dict(second_stage_samples, params_dict, world_states, allocation_dict)
    with open('params/scens_saa_secondStage.json', 'w') as outfile:
        json.dump(scens, outfile, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read a filename.')
    parser.add_argument('-a', '--allocfile', help='the state probabilities file', default="alloc.json")
    parser.add_argument('-d', '--debug', help='run in debug mode', action='store_false')
    parser.add_argument('-e', '--exprfile', help='experiment parameters file', default="exprFile.json")
    parser.add_argument('-w', '--worldstates', help='world states file', default="worldstates.json")
    args = parser.parse_args()
    params_dict = json.loads(open(args.exprfile).read())
    allocation_dict = json.loads(open(args.allocfile).read())
    saa_params_dict = json.loads(open(args.exprfile).read())
    generate_scens_saa_second_stage(params_dict, allocation_dict, saa_params_dict, args.worldstates)