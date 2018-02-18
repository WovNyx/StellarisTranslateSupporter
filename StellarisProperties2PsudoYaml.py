## Programmed by WovNyx

import os

testing = False

def _debugprint(*args, debug = False) :
    if debug :
        rtn = ''
        for ii in args :
            if ii :
                rtn += str(ii)
        print(rtn)
    else :
        pass
    

## actually this thing is not real yml file..
## Do your Work Paradox!
## returns list of broken line, return None if nothing wrong
## returns False for file IO problem
def Properties2ParadoxYaml(filename, path = None) :
    ## use current directory of program as default path
    if path :
        filedir = path
    else :
        filedir = os.getcwd()
    file = None
    ##
    try :
        file = open(os.path.join(filedir, filename), "r", encoding = "UTF-8-SIG")
        print("opening file {name} at {dir}".format( name = filename, dir = filedir) )
    except :
        print("error opening properties file")
        print(filedir, filename)
        return False
    recv = file.read().split("\n") ## seperate by line

    proc = []

    temp = None
    
    ## variables for error handling
    linecount = 0
    badline = {}
    badline['NoDelim'] = [] ## deliminator '=' not found
    badline['BadKey']  = []
    badline['NoValue'] = []
    
    for line in recv :
        linecount += 1
        if line.strip() != '' :
            if line.strip()[0] == "#" :
                continue
                
            temp = line.split("=", 1)
            _debugprint(temp, debug = testing)
            
            if len(temp) != 2 :
                badline['NoDelim'].append(linecount)
                print("wrong data, delminonator not found. skipping this line", linecount)
                continue
                
            if "코" in temp[0] :
                temp[0] = temp[0].replace("코", ":")
            elif ":" in temp[0] :
                pass
            else :
                badline['BadKey'].append(linecount)
                print("wrong key in line {fileline}, key {lkey}".format(fileline = linecount, lkey = temp[0] ) )
                continue

            
            if temp[1] == '' :
                print("no value in line {fileline}, key {lkey}".format(fileline = linecount, lkey = temp[0] ) )
                temp[1] = '""'
                badline['NoValue'].append(linecount)
            else :
                temp[1] = temp[1].replace("<?>","")
                if temp[1][0] != '"' :
                    temp[1] = '"' + temp[1]
                if temp[1][-1] != '"' :
                    temp[1] = temp[1] + '"'
            proc.append(" ".join(temp) )
        else :
            proc.append("")
            
    file.close()
    
    if badline['NoDelim'] != []:
        return badline
    elif badline['BadKey'] != [] :
        return badline
    
    try :
        ##open file as UTF-8-SIG(with BOM) for not crashing if it has BOM or not
        file = open(os.path.join(filedir, filename[:-10]) + "yml" , 'w', encoding = "UTF-8-SIG") 
        print("writing file {name} at {dir}".format( name = filename[:-10]+"yml", dir = filedir) )
        file.write("l_english" + "\n")
        for ii in proc :
            file.write(" " + ii + "\n")
        file.close()
    except :
        print("error making yaml-like paradox file")
        return False
        
    return badline

    
    
if __name__ == "__main__" :
    ## path.txt is text file with 1 line of string which is path of target directory
    path = ''
    try :
        target = open("./path.txt", 'r')
        path = target.read()
        str(path)
        ## temperal patch for os.path.join() bug
        if path[-1] == "/" or path[-1] == "\\" :
            pass
        else :
            if "/" in path :
                path += "/"
            elif "\\" in path :
                path += "\\"
            else :
                print("bad path")
        ## temperal patch over
        print("found path", path)
    except :
        path = os.getcwd()
        print("properties path not found. using current directory")
    ## os.listdir(path) shows all thing in path directory
    ## os.path.isfile returns True if target(path+f in this case) is file
    ## files is list of f which is fils in path directory
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f) ) ]
    completed = []
    notproced = []
    print("files in this directory", files)
    for f in files:
        if '.properties' == f[-11:] :
            try :
                result = Properties2ParadoxYaml(f, path)
                print(result)
                if result :
                    if result['NoDelim'] != []:
                        notproced.append((f, result) )
                    elif result['BadKey'] != [] :
                        notproced.append( (f, result) )
                    elif result['NoValue'] != [] :
                        completed.append( (f, result) )
                    else :
                        completed.append((f, "clean") )
                else :
                    notproced.append(f, "FileI/Oerror")
            except :
                print("file {} has wrong data".format(f) )
                notproced.append(f)
                
    print("conversion completed on")
    for ii in completed :
        print(ii)
    print("conversion failed on")
    for ii in notproced :
        print(ii)
