################# configureation ###################

## the path of your words dictionary file
liwc_path = 'dic/LIWC2007_ENGLISH080730.dic'

## the path of the file you want to process
txt_path = 'txt/texts_all.txt'

## whether you want to ignore the first line which is lable for each column
first_line_as_lable = True

## which column stores the id info for each row
tid_column = 1

## limit into a specific array of ids, otherwise if want to look at all, simply leave it as txt_limit=[]
tid_limit = ['/thing:8917', '/thing:17473']
#tid_limit = [] # uncomment this line if you want to look at all raws

## which columns you want to look in your .txt file
fields = {
    'desc':'4',
    'insc':'5'
    }

## which categories you want to look at
looks = {
    'posemo':['126'],
    'negemo':['19', '127', '128', '129', '130'],
    }

## do you want to show the process during executing code
show = True

## do you want to save results into txt file in /ouput folder?
output_result = True



#### do not edit bellow this line
import call
r = call.get_scores(liwc_path, txt_path, first_line_as_lable, tid_column, tid_limit, fields, looks, show)
call.output(fields, looks, r, output_result)
