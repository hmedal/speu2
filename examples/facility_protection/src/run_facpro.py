import argparse
import os
from examples.facility_protection.params import generate_probs_and_scens_files
from modeling import speu
import json

if __name__ == "__main__":
    print "cwd", os.getcwd()
    parser = argparse.ArgumentParser(description='Read a filename.')
    parser.add_argument('-e', '--expr', help='experiment file', default='exprFile.json')
    args = parser.parse_args()
    params_dict = json.loads(open(args.expr).read())
    num_facs = params_dict["changing"]["num_facs"]
    num_cap_levels = params_dict["changing"]["num_cap_levels"]
    num_allocation_levels = params_dict["changing"]["num_allocation_levels"]
    scens_file = 'params/fac_pro_scens_' + generate_probs_and_scens_files.get_params_string_scens(num_facs,
                                                                                            num_cap_levels) + '.json'
    probs_file = 'params/fac_pro_probs_and_costs_' + generate_probs_and_scens_files.get_params_string_probs(
        num_allocation_levels,
        num_cap_levels) + '.json'
    model = speu.create_model_object(True, args.expr, scens_file, probs_file, args.debug)
    model.solve()

