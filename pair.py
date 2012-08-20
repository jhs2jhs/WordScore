################# start of configureation ###################

pair_file_path = 'txt/sequences.txt'
first_line_as_label_pair = True
pair_show = False

################# end of configureation ###################


#### do not edit bellow this line
import call
from main import *

if __name__ == '__main__':
    r = call.read_main(fields, looks)
    import json
    print json.dumps(r, indent=4)
    lines_out = call.pair(pair_file_path, fields, looks, r, first_line_as_label_pair)
    call.pair_output(lines_out, pair_file_path, pair_show)
    
    
