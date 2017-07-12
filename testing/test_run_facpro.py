import argparse
import os
from examples.facility_protection.params import generate_probs_and_scens_files
from modeling import speu
import json
import unittest

class Test_FacPro(unittest.TestCase):

    def test_run_deterministic_equivalent(self):
        os.chdir('../examples/facility_protection')
        print "cwd", os.getcwd()
        debug = True
        expr_file = "expr_scripts_for_paper/baseExperimentParameters.json"
        params_dict = json.loads(open(expr_file).read())
        num_facs = params_dict["num_facs"]
        num_cap_levels = params_dict["num_states"]
        num_allocation_levels = params_dict["num_allocation_levels"]
        scens_file = 'params/fac_pro_scens_' + generate_probs_and_scens_files.get_params_string_scens(num_facs,
                                                                                                num_cap_levels) + '.json'
        probs_file = 'params/fac_pro_probs_and_costs_' + generate_probs_and_scens_files.get_params_string_probs(
            num_allocation_levels,
            num_cap_levels) + '.json'
        model = speu.create_model_object(True, expr_file, scens_file, probs_file, debug)
        model.solve()

    def test_run_saa(self):
        os.chdir('../examples/facility_protection')
        print "cwd", os.getcwd()
        debug = True
        expr_file = "expr_scripts_for_paper/baseExperimentParameters.json"
        params_dict = json.loads(open(expr_file).read())
        num_facs = params_dict["num_facs"]
        num_cap_levels = params_dict["num_states"]
        num_allocation_levels = params_dict["num_allocation_levels"]
        scens_file = 'params/fac_pro_scens_saa_' + generate_probs_and_scens_files.get_params_string_scens(num_facs,
                                                                                                num_cap_levels) + '.json'
        probs_file = 'params/fac_pro_probs_and_costs_' + generate_probs_and_scens_files.get_params_string_probs(
            num_allocation_levels,
            num_cap_levels) + '.json'
        model = speu.create_model_object(True, expr_file, scens_file, probs_file, debug)
        model.solve()