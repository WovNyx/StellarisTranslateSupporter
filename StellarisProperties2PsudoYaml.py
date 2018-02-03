## Programmed by WovNyx

import os

## actually this thing is not real yml file..
## Do your Work Paradox!
def Properties2ParadoxYaml(filename, path = None) :
    ## use current directory of program as default path
    if path :
        filedir = path
    else :
        filedir = "./"
    ##
    try :
        file = open(filedir + filename, "r", encoding = "UTF-8")
        print("opening file {name} at {dir}".format( name = filename, dir = filedir) )
    except :
        print("error opening properties file")
        print(filedir, filename)
    recv = file.read().split("\n") ## seperate by line

    proc = []

    temp = None

    ## this 2 line is all we actually do for conversion.
    ## WTF Paradox...... this isn't Yaml......
    for ii in recv :
        proc.append(":0 ".join(ii.split("코0=") ).replace("<?>", "") )
        
    file.close()

    try :
        file = open(filedir + filename[:-10] + "yml" , 'w', encoding = "UTF-8-SIG") 
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
        if path[-1] == "/" or path[-1] == "\\" :
            pass
        else :
            if "/" in path :
                path += "/"
            elif "\\" in path :
                path += "\\"
            else :
                print("bad path")
        print("found path", path)
    except :
        path = './'
        print("properties path not found. using current directory")
    ## os.listdir(path) shows all thing in path directory
    ## os.path.isfile returns True if target(path+f in this case) is file
    ## files is list of f which is fils in path directory
    files = [f for f in os.listdir(path) if os.path.isfile(path+f ) ]
    print("files in this directory", files)
    for f in files:
        if '.properties' == f[-11:] :
            Properties2ParadoxYaml(f, path)
