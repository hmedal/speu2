import itertools
import json
import os

from scipy import stats

import examples.facility_protection.src.facpro


def getProbabilityFromAllocation(allocation, numAllocLevels):
    return min(1.0, allocation/(numAllocLevels + 0.0))

def getProbabilityFromAllocationAndHazardLevel(allocation, numAllocLevels, hazardLevel, numHazardLevels):
    return getProbabilityFromAllocation(allocation, numAllocLevels)**(hazardLevel/(numHazardLevels + 0.0))

def get_params_string_probs(num_alloc_levels, num_states):
    return "k_" + str(num_alloc_levels) + "_l_" + str(num_states)

def get_params_string_scens(num_facs, num_states):
    return "j_" + str(num_facs) + "_l_" + str(num_states)

def get_params_string_params(num_facs, num_alloc_levels, num_states):
    return "j" + str(num_facs) + "_k" + str(num_alloc_levels) + "_l" + str(num_states)

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

def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z

def generate_scens(static_params_file, changing_params_dict, world_states_file = None):
    params_dict = json.loads(open(static_params_file).read())
    num_facs = changing_params_dict['num_facs']
    num_states = changing_params_dict['num_states']
    scens = {}
    second_stage_prob = examples.facility_protection.src.facpro.SecondStageProblem(
        merge_two_dicts(params_dict, changing_params_dict))
    if world_states_file is None:
        world_states = {}
        world_states[0] = {}
        world_states[0]['probability'] = 1.0
        world_states[0]['exposures'] = [0] * num_facs
    else:
        world_states = json.loads(open(world_states_file).read())
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

if __name__ == "__main__":
    print "cwd", os.getcwd()
    changing_params_dict = {"num_allocation_levels" : 3, "num_facs" : 2, "num_hazard_states" : 2, "num_states" : 2,
                            "exposure_type" : 'allFullyExposedAlways', "num_hazard_states" : 2,
                            "datasetName" : "Daskin49"}
    exposure_type = changing_params_dict['exposure_type']
    if changing_params_dict['exposure_type'] != '':
        exposure_type_print = "_" + exposure_type
    else:
        exposure_type_print = exposure_type
    static_params_file = 'static_params.json'
    generate_probs(changing_params_dict['num_allocation_levels'], changing_params_dict['num_hazard_states'],
                   changing_params_dict['num_states'])
    world_states_file = '../dat/daskin_data/Hazards/hazardsDef_custom_facs' + str(changing_params_dict['num_facs']) \
                        + "_levels" \
                        + str(changing_params_dict['num_hazard_states'])+ exposure_type_print + '.json'
    generate_scens(static_params_file, changing_params_dict, world_states_file)