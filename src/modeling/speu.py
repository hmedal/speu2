import argparse
import json
import gurobipy as gp
import csv
import operator
import os
import numpy as np
from scipy.stats import t as tDist

FUZZ = 0.0000001
alpha = 0.05

def create_model_object(maximize, params_file, scenarios_file, probabilities_file, debug):
    params_dict = json.loads(open(params_file).read())
    if params_dict["solution_method"] == "deterministic-equivalent":
        return SPEU_Stochastic_Program(maximize, params_file, scenarios_file, probabilities_file, debug)
    elif params_dict["solution_method"] == "saa":
        return SPEU_SAA_Algorithm(maximize, params_file, scenarios_file, probabilities_file, debug)

class SPEU_Stochastic_Program():

    def __init__(self, maximize, params_file, scenarios_file, probabilities_file, debug):
        '''
        Constructor
        '''
        if maximize:
            self.obj_sense = gp.GRB.MAXIMIZE
        else:
            self.obj_sense = gp.GRB.MINIMIZE
        self.params_dict = json.loads(open(params_file).read())
        self.solution_method = self.params_dict['solution_method']
        self.read_scens_file(scenarios_file)
        self.read_probabilities_file(probabilities_file)
        budgetMultiplier = self.params_dict['budget_multiplier']
        self.params_dict['budget'] = round(budgetMultiplier * self.num_components * (self.num_alloc_levels - 1))
        self.debug = debug
        self.create_model()

    def read_scens_file(self, scenarios_file):
        if isinstance(scenarios_file, dict):
            self.scenarios = scenarios_file
        else:
            self.scenarios = json.loads(open(scenarios_file).read())
        first_key = self.scenarios.keys()[0]
        self.num_components = len(self.scenarios[first_key]['component_states'])
        self.num_scenarios = len(self.scenarios)

    def read_probabilities_file(self, probabilities_and_costs_file):
        self.probabilities_and_costs = json.loads(open(probabilities_and_costs_file).read())
        self.num_alloc_levels = len(self.probabilities_and_costs)

    def create_model(self):
        self.model = gp.Model()
        self.create_variables()
        self.model.update()
        self.set_objective()
        self.create_constraints()
        if self.debug:
            self.model.write("./output/speu_model.lp")

    def create_variables(self):
        self.alloc_var = {}
        for component in range(self.num_components):
            self.alloc_var[component] = {}
            for alloc_level in range(self.num_alloc_levels):
                self.alloc_var[component][alloc_level] = self.model.addVar(0, 1, vtype = gp.GRB.BINARY,
                                  name="allocVar_j_" + str(component) + "_k_" + str(alloc_level))
        self.cum_prob_var = {}
        for component in range(self.num_components):
            self.cum_prob_var[component] = {}
            for alloc_level in range(self.num_alloc_levels):
                self.cum_prob_var[component][alloc_level] = {}
                for scen in self.scenarios:
                    self.cum_prob_var[component][alloc_level][scen] = self.model.addVar(0,gp.GRB.INFINITY,
                        name="cum_prob_j_" + str(component) + "_k_" + str(alloc_level) + "_s_" + str(scen))

    def create_constraints(self):
        self.create_prob_chain_first_component()
        self.create_prob_chain_constraints()
        self.create_vub_constraints()
        self.create_multiple_choice_constraint()
        self.create_budget_constraint()

    def create_prob_chain_first_component(self):
        # constraints for first component
        for scen in self.scenarios:
            for alloc_level in range(self.num_alloc_levels):
                component_state = self.scenarios[str(scen)]['component_states'][0]  # first component state
                component_exposure = self.scenarios[str(scen)]['exposures'][0]  # first component exposure
                prob_of_state = self.probabilities_and_costs[str(alloc_level)][str(component_exposure)][
                    str(component_state)]
                #if prob_of_state > FUZZ:
                second_stage_obj_val = self.scenarios[str(scen)]['objective_value']
                self.model.addConstr(self.cum_prob_var[0][alloc_level][scen] ==
                                     second_stage_obj_val * prob_of_state * self.alloc_var[0][alloc_level],
                                     "first_component_s_" + str(scen) + "_k_" + str(alloc_level))
                #else:
                #    print "constraint not added", scen, alloc_level, prob_of_state

    def create_prob_chain_constraints(self):
        # constraints for other components
        for scen in self.scenarios:
            # print "scen", scen
            for component in range(1, self.num_components):
                # print "component", component
                left_sum = 0
                for alloc_level1 in range(self.num_alloc_levels):
                    component_state = self.scenarios[str(scen)]['component_states'][component - 1]
                    component_exposure = self.scenarios[str(scen)]['exposures'][component - 1]
                    prob_of_state = self.probabilities_and_costs[str(alloc_level1)][str(component_exposure)][
                        str(component_state)]
                    # print "prob_of_state left sum", alloc_level1, prob_of_state
                    #if prob_of_state > FUZZ:
                    left_sum += self.cum_prob_var[component - 1][alloc_level1][scen]
                    #else:
                    #    print "term not added to lhs", scen, component, alloc_level1
                right_sum = 0
                for alloc_level2 in range(self.num_alloc_levels):
                    component_state = self.scenarios[str(scen)]['component_states'][component]
                    component_exposure = self.scenarios[str(scen)]['exposures'][component]
                    prob_of_state = self.probabilities_and_costs[str(alloc_level2)][str(component_exposure)][
                        str(component_state)]
                    # print "prob_of_state right sum", alloc_level2, prob_of_state
                    if prob_of_state > FUZZ:
                        right_sum += (1 / prob_of_state) * self.cum_prob_var[component][alloc_level2][scen]
                    else:
                        right_sum += (1 / FUZZ) * self.cum_prob_var[component][alloc_level2][scen]
                self.model.addConstr(left_sum == right_sum, "prob_chain_j_" + str(component) + "_s_" + str(scen))

    def create_vub_constraints(self):
        # variable upper bound (VUB) constraints
        for scen in self.scenarios:
            second_stage_obj_val = self.scenarios[str(scen)]['objective_value']
            for component in range(self.num_components):
                for alloc_level in range(self.num_alloc_levels):
                    self.model.addConstr(self.cum_prob_var[component][alloc_level][scen] <=
                                         second_stage_obj_val * self.alloc_var[component][alloc_level],
                                         "VUB_j_" + str(component) + "_k_" + str(alloc_level) + "_s_" + str(scen))

    def create_multiple_choice_constraint(self):
        # multiple choice constraints
        for component in range(self.num_components):
            vars_sum = 0
            for alloc_level in range(self.num_alloc_levels):
                vars_sum += self.alloc_var[component][alloc_level]
            self.model.addConstr(vars_sum == 1, "multiple_choic_j_" + str(component))

    def create_budget_constraint(self):
        cost_sum = 0
        for component in range(self.num_components):
            for alloc_level in range(self.num_alloc_levels):
                cost_sum += self.probabilities_and_costs[str(alloc_level)]['cost'] * \
                            self.alloc_var[component][alloc_level]
        self.model.addConstr(cost_sum <= self.params_dict['budget'], "budget")

    def set_objective(self):
        objective_sum = 0
        for scen in self.scenarios:
            objective_sum += self.scenarios[scen]['prob_of_world_state']*\
                             sum([self.cum_prob_var[self.num_components - 1][alloc_level][scen]
                                  for alloc_level in range(self.num_alloc_levels)])
        self.model.setObjective(objective_sum, gp.GRB.MAXIMIZE)

    def solve(self):
        self.model.optimize()
        self.soln_file = "./output/speu_model.sol"
        self.model.write(self.soln_file)
        print "alloc var for components", self.get_alloc_level_for_components_from_sol_file(self.soln_file)
        print "probabilities for scenarios", self.compute_scenario_probs_for_alloc_vars_soln(self.soln_file)
        probs_times_obj_vals = self.compute_scenario_probs_times_obj_vals_for_alloc_vars_soln(self.soln_file)
        print "probabilities times obj vals for scenarios", probs_times_obj_vals
        print "sum of probabilities times obj vals for scenarios", sum(probs_times_obj_vals.values())
        alloc_levels_and_state_probs = self.get_alloc_vals_and_state_probabilities(self.soln_file)
        with open('alloc_levels_and_state_probs.json', 'w') as outfile:
            json.dump(alloc_levels_and_state_probs, outfile, indent=2)
        return self.model.objVal

    def read_alloc_soln_from_sol_file(self, soln_file):
        var_vals = {}
        with open(soln_file) as f:
            f.readline()
            reader = csv.reader(f, delimiter=' ')
            for row in reader:
                var_vals[row[0]] = float(row[1])
        alloc_soln = {}
        for component in range(self.num_components):
            alloc_soln[component] = {}
            for alloc_level in range(self.num_alloc_levels):
                alloc_soln[component][alloc_level] = var_vals["allocVar_j_" + str(component) + "_k_" + str(alloc_level)]
        return alloc_soln

    def get_alloc_level_for_components_from_sol_file(self, soln_file):
        alloc_soln = self.read_alloc_soln_from_sol_file(soln_file)
        alloc_level_for_component = {}
        for component in range(self.num_components):
            for alloc_level in range(self.num_alloc_levels):
                if abs(alloc_soln[component][alloc_level] - 1.0) < 0.001:
                    alloc_level_for_component[component] = alloc_level
        return alloc_level_for_component

    def get_alloc_vals_and_state_probabilities(self, soln_file):
        alloc_soln = self.read_alloc_soln_from_sol_file(soln_file)
        alloc_levels_and_state_probs = {}
        for component in range(self.num_components):
            alloc_levels_and_state_probs[component] = {}
            for alloc_level in range(self.num_alloc_levels):
                if abs(alloc_soln[component][alloc_level] - 1.0) < 0.001:
                    alloc_levels_and_state_probs[component]['alloc_level'] = alloc_level
            alloc_level_for_component = alloc_levels_and_state_probs[component]['alloc_level']
            alloc_levels_and_state_probs[component]['state_probs'] = \
                self.probabilities_and_costs[str(alloc_level_for_component)]
        return alloc_levels_and_state_probs

    def compute_scenario_probs_for_alloc_vars_soln(self, soln_file):
        alloc_level_for_component = self.get_alloc_level_for_components_from_sol_file(soln_file)
        scen_probs = {}
        for scen in self.scenarios:
            scen_probs[scen] = 1
            for component in range(self.num_components):
                component_state = self.scenarios[str(scen)]['component_states'][component]
                component_exposure = self.scenarios[str(scen)]['exposures'][component]
                alloc_level = alloc_level_for_component[component]
                prob_of_state = self.probabilities_and_costs[str(alloc_level)][str(component_exposure)][
                    str(component_state)]
                #print "scenario info", scen, component, component_state, prob_of_state
                scen_probs[scen] *= prob_of_state
        return scen_probs

    def compute_scenario_probs_times_obj_vals_for_alloc_vars_soln(self, soln_file):
        probs_times_obj_vals = {}
        scen_probs = self.compute_scenario_probs_for_alloc_vars_soln(soln_file)
        for scen in self.scenarios:
            probs_times_obj_vals[scen] = scen_probs[scen] * self.scenarios[str(scen)]['objective_value']
        return probs_times_obj_vals

class SPEU_SAA_Algorithm(SPEU_Stochastic_Program):

    def __init__(self, maximize, params_file, scenarios_file, probabilities_file, debug):
        if maximize:
            self.obj_sense = gp.GRB.MAXIMIZE
        else:
            self.obj_sense = gp.GRB.MINIMIZE
        self.params_file = params_file
        self.params_dict = json.loads(open(params_file).read())
        self.num_first_stage_solns = self.params_dict['saa_first_stage_iterations']
        self.scenarios = json.loads(open(scenarios_file).read())
        self.sample_average_problems = []
        for iter in range(self.num_first_stage_solns):
            scenarios_for_iteration = {str(k): self.scenarios[str(k)] for k in range(iter*self.num_first_stage_solns,
                                                             (iter+1) * self.num_first_stage_solns)}
            self.sample_average_problems.append(SPEU_Stochastic_Program(maximize, params_file, scenarios_for_iteration,
                                                                   probabilities_file, debug))

    def solve(self):
        print "SOLVING SAA PROBLEM"
        objective_values_and_solutions = {}
        for sample_average_problem in self.sample_average_problems:
            objVal = sample_average_problem.solve()
            objective_values_and_solutions[objVal] = json.loads(open('alloc_levels_and_state_probs.json').read())
        obj_values = objective_values_and_solutions.keys()
        num_states = self.params_dict['num_states']
        num_facs = self.params_dict['num_facs']
        saa_first_stage_samples = self.params_dict['saa_first_stage_samples']
        cardinality_of_sample_space = num_states ** num_facs
        multiplier_to_compute_expectation = cardinality_of_sample_space / (saa_first_stage_samples + 0.0)
        print "multiplier_to_compute_expectation", multiplier_to_compute_expectation
        print "cardinality_of_sample_space", cardinality_of_sample_space
        adjusted_obj_values = [multiplier_to_compute_expectation*value for value in obj_values]
        print "adjusted_obj_values", adjusted_obj_values
        print "avg adjusted obj values", np.mean(adjusted_obj_values), "+/-", get_tdist_hw(adjusted_obj_values)
        if self.obj_sense == gp.GRB.MAXIMIZE:
            best_obj_value = max(obj_values)
        else:
            best_obj_value = min(obj_values)
        best_soln = objective_values_and_solutions[best_obj_value]
        print "best soln", {component : best_soln[str(component)]['alloc_level'] for component in range(num_facs)}
        with open('best_soln.json', 'w') as outfile:
            json.dump(best_soln, outfile, indent=2)
        cmd = self.params_dict['saa_sampler_command']
        world_states_file = 'dat/daskin_data/Hazards/hazardsDef_custom_facs' + str(num_facs) \
                            + "_levels2_allFullyExposedAlways.json"
        os.system(cmd + ' -a' + 'best_soln.json' + ' -e ' + self.params_file + ' -w ' + world_states_file)
        second_stage_scens = json.loads(open('params/scens_saa_secondStage.json').read())
        second_stage_obj_vals = [second_stage_scens[str(key)]['objective_value'] for key in second_stage_scens]
        first_phase_hw = get_tdist_hw(adjusted_obj_values)
        print "second_stage_obj_vals", second_stage_obj_vals
        print "avg second stage obj vals", np.mean(second_stage_obj_vals), "+/-", get_tdist_hw(second_stage_obj_vals)


def get_tdist_hw(x):
    n = len(x)
    return tDist.ppf(1 - alpha / 2.0, n - 1) * np.std(x) / np.sqrt(n)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read a filename.')
    parser.add_argument('-p', '--prob', help='the state probabilities file', default="probs.json")
    parser.add_argument('-d', '--debug', help='run in debug mode', action='store_false')
    parser.add_argument('-s', '--scenarios', help='scenarios definition file', default="scens.json")
    parser.add_argument('-m', '--maximize', help='use maximization objective', action='store_false')
    parser.add_argument('-a', '--params', help='params file', default="params.json")
    args = parser.parse_args()
    model = create_model_object(args.maximize, args.params, args.scenarios, args.prob, args.debug)
    model.solve()