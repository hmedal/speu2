import os
import argparse
from modeling import speu
import generate_params_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read a filename.')
    parser.add_argument('-j', '--num_facs', help='number of facilities', default=3)
    parser.add_argument('-k', '--num_alloc_levels', help='number of allocation levels', default=3)
    parser.add_argument('-d', '--debug', help='run in debug mode', action='store_false')
    parser.add_argument('-l', '--num_states', help='number of facility states', default=3)
    parser.add_argument('-w', '--world_states_file',
                        help='file describing the world states and how affect the components', default = 'none')
    args = parser.parse_args()
    scens_file = 'fac_pro_scens_' + generate_params_files.get_params_string_scens(args.num_facs,
                                                                                  args.num_states) + '.json'
    probs_file = 'fac_pro_probs_' + generate_params_files.get_params_string_probs(args.num_alloc_levels,
                                                                                  args.num_states) + '.json'
    model = speu.create_model_object(True, scens_file, probs_file, args.debug)
    model.solve()

