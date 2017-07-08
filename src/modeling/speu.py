import argparse
import json
import gurobipy as gp

FUZZ = 0.0001

def create_model_object(maximize, params_file, scenarios, probabilities, debug):
    return SPEU_Model(maximize, params_file, scenarios, probabilities, debug)

class SPEU_Model():

    def __init__(self, maximize, params_file, scenarios_file, probabilities_file, debug):
        '''
        Constructor
        '''
        if maximize:
            self.obj_sense = gp.GRB.MAXIMIZE
        else:
            self.obj_sense = gp.GRB.MINIMIZE
        self.params_dict = json.loads(open(params_file).read())
        self.read_scens_file(scenarios_file)
        self.read_probabilities_file(probabilities_file)
        budgetMultiplier = self.params_dict['budget_multiplier']
        self.params_dict['budget'] = round(budgetMultiplier * self.num_components * (self.num_alloc_levels - 1))
        self.debug = debug
        self.create_model()

    def read_scens_file(self, scenarios_file):
        self.scenarios = json.loads(open(scenarios_file).read())
        self.num_components = len(self.scenarios['0']['component_states'])
        self.num_scenarios = len(self.scenarios)

    def read_probabilities_file(self, probabilities_and_costs_file):
        self.probabilities_and_costs = json.loads(open(probabilities_and_costs_file).read())
        self.num_alloc_levels = len(self.probabilities_and_costs)

    def create_model(self):
        self.model = gp.Model()
        self.create_variables()
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
                for scen in range(self.num_scenarios):
                    self.cum_prob_var[component][alloc_level][scen] = self.model.addVar(0,gp.GRB.INFINITY,
                        name="cum_prob_j_" + str(component) + "_k_" + str(alloc_level) + "_s_" + str(scen))

    def create_constraints(self):
        #constraints for first component
        for scen in range(self.num_scenarios):
            for alloc_level in range(self.num_alloc_levels):
                component_state = self.scenarios[str(scen)]['component_states'][0] #first component state
                component_exposure = self.scenarios[str(scen)]['exposures'][0] #first component exposure
                prob_of_state = self.probabilities_and_costs[str(alloc_level)][str(component_exposure)][str(component_state)]
                if prob_of_state > FUZZ:
                    second_stage_obj_val = self.scenarios[str(scen)]['objective_value']
                    self.model.addConstr(self.cum_prob_var[0][alloc_level][scen] ==
                                    second_stage_obj_val * prob_of_state * self.alloc_var[0][alloc_level],
                                         "first_component_s_" +str(scen) + "_k_" + str(alloc_level))
        #constraints for other components
        for scen in range(self.num_scenarios):
            print "scen", scen
            for component in range(1, self.num_components):
                print "component", component
                left_sum = 0
                for alloc_level1 in range(self.num_alloc_levels):
                    component_state = self.scenarios[str(scen)]['component_states'][component-1]
                    component_exposure = self.scenarios[str(scen)]['exposures'][component-1]
                    prob_of_state = self.probabilities_and_costs[str(alloc_level1)][str(component_exposure)][str(component_state)]
                    print "prob_of_state left sum", alloc_level1, prob_of_state
                    if prob_of_state > FUZZ:
                        left_sum += self.cum_prob_var[component-1][alloc_level1][scen]
                right_sum = 0
                for alloc_level2 in range(self.num_alloc_levels):
                    component_state = self.scenarios[str(scen)]['component_states'][component]
                    component_exposure = self.scenarios[str(scen)]['exposures'][component]
                    prob_of_state = self.probabilities_and_costs[str(alloc_level2)][str(component_exposure)][str(component_state)]
                    print "prob_of_state right sum", alloc_level2, prob_of_state
                    if prob_of_state > FUZZ:
                        right_sum += (1/prob_of_state) * self.cum_prob_var[component][alloc_level2][scen]
                if not (left_sum == 0 and right_sum == 0):
                    self.model.addConstr(left_sum == right_sum, "prob_chain_j_" +str(component) + "_s_" + str(scen))
        # variable upper bound (VUB) constraints
        for scen in range(self.num_scenarios):
            second_stage_obj_val = self.scenarios[str(scen)]['objective_value']
            for component in range(self.num_components):
                for alloc_level in range(self.num_alloc_levels):
                    self.model.addConstr(self.cum_prob_var[component][alloc_level][scen] <=
                                         second_stage_obj_val  * self.alloc_var[component][alloc_level],
                                         "VUB_j_" +str(component) + "_k_" + str(alloc_level) + "_s_" + str(scen))
        # multiple choice constraints
        for component in range(self.num_components):
            vars_sum = 0
            for alloc_level in range(self.num_alloc_levels):
                vars_sum += self.alloc_var[component][alloc_level]
            self.model.addConstr(vars_sum == 1, "multiple_choic_j_" + str(component))
        cost_sum = 0
        for component in range(self.num_components):
            for alloc_level in range(self.num_alloc_levels):
                cost_sum += self.probabilities_and_costs[str(alloc_level)]['cost'] * \
                            self.alloc_var[component][alloc_level]
        self.model.addConstr(cost_sum <= self.params_dict['budget'], "budget")

    def set_objective(self):
        objective_sum = 0
        for scen in range(self.num_scenarios):
            objective_sum += self.scenarios[str(scen)]['prob_of_world_state']*\
                             sum([self.cum_prob_var[self.num_components - 1][alloc_level][scen]
                                  for alloc_level in range(self.num_alloc_levels)])
        self.model.setObjective(objective_sum, gp.GRB.MAXIMIZE)

    def solve(self):
        self.model.optimize()
        self.model.write("./output/speu_model.sol")

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