## Programmed by WovNyx

import os

## actually this thing is not real yml file..
## Do your Work Paradox!
def Properties2ParadoxYaml(filename, path = None) :
    ## use current directory of program as default path
    if path :
        filedir = path
    else :
        filedir = os.getcwd()
    ##
    try :
        file = open(os.path.join(filedir, filename), "r", encoding = "UTF-8-SIG")
        print("opening file {name} at {dir}".format( name = filename, dir = filedir) )
    except :
        print("error opening properties file")
        print(filedir, filename)
    recv = file.read().split("\n") ## seperate by line

    proc = []

    temp = None

    ## this 2 line is all we actually do for conversion.
    ## WTF Paradox...... this isn't Yaml......
    ## data : ...코x='...' x is number
    for ii in recv :
        if ii.strip() != '' :
            if ii[0] == "#" :
                continue
            temp = ii.split("=")
            print(temp)
            temp[0] = temp[0].replace("코", ":")
            temp[1] = temp[1].replace("<?>","")
            if temp[1][0] != '"' :
                temp[1] = '"' + temp[1]
            if temp[1][-1] != '"' :
                temp[1] = temp[1] + '"'
            proc.append(" ".join(temp) )
        else :
            proc.append("")
    file.close()

    try :
        ##open file as UTF-8-SIG(with BOM) for not crashing if it has BOM or not
        file = open(os.path.join(filedir, filename[:-10]) + "yml" , 'w', encoding = "UTF-8-SIG") 
        print("writing file {name} at {dir}".format( name = filename[:-10]+"yml", dir = filedir) )
    except :
        print("error making yaml-like paradox file")
        
        
    file.write("l_english" + "\n")
    for ii in proc :
        file.write(" " + ii + "\n")

    file.close()

    return

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
    print("files in this directory", files)
    for f in files:
        if '.properties' == f[-11:] :
            Properties2ParadoxYaml(f, path)
