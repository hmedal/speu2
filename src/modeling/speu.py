import argparse
import json

def create_model_object(maximize, scenarios, probabilities, debug):
    return SPEU_Model(maximize, scenarios, probabilities, debug)

class SPEU_Model():

    def __init__(self, maximize, scenarios_file, probabilities_file, debug):
        '''
        Constructor
        '''
        self.maximize = maximize
        self.scenarios = json.loads(open(scenarios_file).read())
        self.probabilities = json.loads(open(probabilities_file).read())
        self.debug = debug
        self.create_model()

    def create_model(self):
        self.create_variables()
        self.create_objective()
        self.create_constraints()

    def create_variables(self):
        pass

    def create_constraints(self):
        pass

    def create_objective(self):
        pass

    def solve(self):
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read a filename.')
    parser.add_argument('-p', '--prob', help='the state probabilities file', default="probs.json")
    parser.add_argument('-d', '--debug', help='run in debug mode', action='store_false')
    parser.add_argument('-s', '--scenarios', help='scenarios definition file', default="scens.json")
    parser.add_argument('-m', '--maximize', help='use maximization objective', action='store_false')
    args = parser.parse_args()
    model = create_model_object(args.maximize, args.scenarios, args.prob, args.debug)
    model.solve()