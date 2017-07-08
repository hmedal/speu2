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
        params_dict = json.loads(open(params_file).read())
        self.readInExperimentData(params_dict)
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
        self.excess_capacity = params_dict['excess_capacity']
        self.penaltyMultiplier = params_dict['penalty_multiplier']
        self.numAllocLevels = params_dict['num_allocation_levels']
        self.numCapLevels = params_dict['num_cap_levels']
        self.budgetMultiplier = params_dict['budget_multiplier']

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
        print "budget (without round): ", self.budgetMultiplier * self.numFacs * (self.numAllocLevels - 1)
        self.budget = round(self.budgetMultiplier * self.numFacs * (self.numAllocLevels - 1))
        print "self.budget: ", self.budget

class SecondStageProblem(object):

    def __init__(self, params_file, debug = False):
        params_dict = json.loads(open(params_file).read())
        self.instance = ProblemInstance(params_file)
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