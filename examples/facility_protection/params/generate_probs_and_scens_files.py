import numpy as np
from scipy import stats
import json
import itertools
import examples.facility_protection.facpro

def getProbabilityFromAllocation(allocation, numAllocLevels):
    return min(1.0, allocation/(numAllocLevels + 0.0))

def getProbabilityFromAllocationAndHazardLevel(allocation, numAllocLevels, hazardLevel, numHazardLevels):
    return getProbabilityFromAllocation(allocation, numAllocLevels)**(hazardLevel/(numHazardLevels + 0.0))

def get_params_string_probs(num_alloc_levels, num_states):
    return "k_" + str(num_alloc_levels) + "_l_" + str(num_states)

def get_params_string_scens(num_facs, num_states):
    return "j_" + str(num_facs) + "_l_" + str(num_states)

def generate_probs(alloc_levels, num_external_states, num_states):
    probs = {}
    for alloc_level in range(alloc_levels):
        probs[alloc_level] = {}
        probs[alloc_level]['cost'] = alloc_level
        for external_state in range(num_external_states):
            probs[alloc_level][external_state] = {}
            for state in range(num_states):
                p = getProbabilityFromAllocationAndHazardLevel(alloc_level, alloc_levels, external_state,
                                                               num_external_states)
                probs[alloc_level][external_state][state] = stats.binom.pmf(state, num_states - 1, p)
    with open('fac_pro_probs_and_costs_' + get_params_string_probs(alloc_levels, num_states) + '.json', 'w') as outfile:
        json.dump(probs, outfile, indent=4)

def generate_scens(params_file, world_states_file = None):
    params_dict = json.loads(open(params_file).read())
    num_facs = params_dict['num_facs']
    num_states = params_dict['num_cap_levels']
    scens = {}
    second_stage_prob = examples.facility_protection.facpro.SecondStageProblem(params_file)
    if world_states_file is None:
        world_states = {}
        world_states[0] = {}
        world_states[0]['probability'] = 1.0
        world_states[0]['exposures'] = [1]*num_facs

    scens = {}
    count = 0
    for world_state in world_states:
        for states_vector in itertools.product(range(num_states), repeat=num_facs):
            scens[count] = {}
            scens[count]['component_states'] = states_vector
            scens[count]['exposures'] = world_states[world_state]['exposures']
            scens[count]['prob_of_world_state'] = world_states[world_state]['probability']
            scens[count]['objective_value'] = second_stage_prob.computeSecondStageUtility(states_vector)
            count += 1

    with open('fac_pro_scens_' + get_params_string_scens(num_facs, num_states) + '.json', 'w') as outfile:
        json.dump(scens, outfile, indent=2)

if __name__ == "__main__": #TODO IOError: [Errno 2] No such file or directory: 'params_Daskin_j3_k3_l3.json
    num_allocation_levels = 3
    num_facs = 3
    num_hazard_states = 3
    num_states = 3
    params_file = 'params_Daskin_j' + str(num_facs) + '_k' + str(num_allocation_levels) + '_l' + str(num_states) + '.json'
    generate_probs(num_allocation_levels, num_hazard_states, num_states)
    generate_scens(params_file)