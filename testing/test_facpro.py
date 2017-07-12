import unittest
from examples.facility_protection.src import facpro
import json
import os

class Test_FacPro(unittest.TestCase):

    def test_get_states_vector_sample(self):
        os.chdir('../examples/facility_protection/src')
        print "cwd", os.getcwd()
        sample_size = 100
        expr_file = "../expr_scripts_for_paper/baseExperimentParameters.json"
        params_dict = json.loads(open(expr_file).read())
        world_states_file = '../dat/daskin_data/Hazards/hazardsDef_custom_facs5'+ "_levels2_allFullyExposedAlways.json"
        world_states_dict = json.loads(open(world_states_file).read())
        allocation_file = "../alloc_levels_and_state_probs.json"
        allocation_dict = json.loads(open(allocation_file).read())
        sample = facpro.get_scen_sample_dict(sample_size, params_dict, world_states_dict, allocation_dict)
        print  sample

    def test_generate_scens_saa_second_stage(self):
        os.chdir('../examples/facility_protection/src')
        expr_file = "../expr_scripts_for_paper/baseExperimentParameters.json"
        params_dict = json.loads(open(expr_file).read())
        world_states_file = '../dat/daskin_data/Hazards/hazardsDef_custom_facs5' + "_levels2_allFullyExposedAlways.json"
        allocation_file = "../alloc_levels_and_state_probs.json"
        allocation_dict = json.loads(open(allocation_file).read())
        saa_params_dict = {"first_stage_iterations": 10, "first_stage_samples": 500, "second_stage_samples": 200}
        facpro.generate_scens_saa_second_stage(params_dict, allocation_dict, saa_params_dict, world_states_file)

    def test_facpro_script(self):
        os.chdir('../examples/facility_protection/src')
        expr_file = "../expr_scripts_for_paper/baseExperimentParameters.json"
        params_dict = json.loads(open(expr_file).read())
        world_states_file = '../dat/daskin_data/Hazards/hazardsDef_custom_facs5' + "_levels2_allFullyExposedAlways.json"
        allocation_file = "../alloc_levels_and_state_probs.json"
        os.system('python facpro.py -a ' + allocation_file + ' -e ' + expr_file + ' -w ' + world_states_file)