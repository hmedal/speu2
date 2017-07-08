import numpy as np
from scipy import stats
import json
import itertools

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
        for external_state in range(num_external_states):
            probs[alloc_level][external_state] = {}
            for state in range(num_states):
                p = getProbabilityFromAllocationAndHazardLevel(alloc_level, alloc_levels, external_state,
                                                               num_external_states)
                probs[alloc_level][external_state][state] = stats.binom.pmf(state, num_states - 1, p)
    with open('fac_pro_probs_' + get_params_string_probs(alloc_levels, num_states) + '.json', 'w') as outfile:
        json.dump(probs, outfile, indent=4)


def generate_scens(num_facs, num_states, world_states_file = None):
    scens = {}

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
            scens[count]['objective_value'] = 10.0 #TODO implement this
            count += 1

    with open('fac_pro_scens_' + get_params_string_scens(num_facs, num_states) + '.json', 'w') as outfile:
        json.dump(scens, outfile, indent=2)

if __name__ == "__main__":
    num_facs = 3
    num_hazard_states = 3
    num_states = 3
    generate_probs(num_facs, num_hazard_states, num_states)
    generate_scens(num_facs, num_states)