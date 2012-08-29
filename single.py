################# start of configureation ###################

single_fields = {
    'twitter_id':'0'
    }
single_show = False
single_output_result = True # must be true if you want to have file output

################# end of configureation ###################


#### do not edit bellow this line
import call
from main import *

if __name__ == '__main__':
    r = call.read_main(fields, looks)
    import json
    #print json.dumps(r, indent=4)
    r = call.single(r, txt_path, first_line_as_lable, tid_column, tid_limit, single_show, single_fields)
    call.single_output(fields, looks, r, single_fields, single_output_result)
    
    
