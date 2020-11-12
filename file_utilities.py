'''
Created on Nov 12, 2020

@author: dan trepanier
'''

import os
import pandas as pd

def read_csv(filepath_or_buffer, sep=',', output='dict', delimiter=None, *args, **kwargs):
    assert output in ('dict','pd','list')
    result = pd.read_csv(filepath_or_buffer, sep, *args, **kwargs)
    if output=='dict':          
        tmp = list(result.T.to_dict().values())
        answer = []
        for row in tmp:
            tmp = {}
            for (k,v) in list(row.items()):
                if 'date' in k:
                    if type(v) == str and '-' in v:
                        v = v.replace('-',"")
                    tmp[k] = str(int(v))
                else:
                    tmp[k] = v
            answer += [tmp]
        return answer
    elif output == 'list':      return [list(result.columns)] + result.values.tolist()
    elif output == 'pd':        return result

def write_csv( contents, prefix, revise=True, separator=',',extension='.csv'):
    if '/' in prefix:
        lst = prefix.split('/')
        working_dir = '/'.join(lst[:-1]) + '/'
        prefix = lst[-1]
    else:
        working_dir = os.getcwd() + '/'
    #print 'plumbing.Write -- working dir',working_dir
    #print 'file',prefix
    files = os.listdir(working_dir)
    header = contents[0]
    output = separator.join(header) + '\n'
    for line in contents[1:]:
        assert len(line) == len(header),'header (%d): %s\nline (%d): %s' % (len(header), str(header), len(line), str(line))
        output += separator.join([str(x) for x in line]) + '\n'
    if revise:
        rev = 0
        #ext = '.csv'
        file = prefix + str(rev) + extension 
        while file in files:
            rev += 1
            file = prefix + str(rev) + extension
    else:
        file = prefix + extension
    
    filename = working_dir + file 
    with open(filename, "w") as out:
        out.write(output)  
    return filename