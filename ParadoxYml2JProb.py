import os

def PY2JP(filename, path = None) :
    
    if path :
        filedir = path
    else :
        filedir = os.getcwd()
        
        
    try :
        file = open(os.path.join(filedir, filename), "r", encoding = "UTF-8-SIG")
        print("opening file {name} at {dir}".format( name = filename, dir = filedir) )
    except :
        print("error opening paradox file")
        print(filedir, filename)
        return False
        
    
    recv = file.read().split("\n") ## seperate by line

    proc = []

    temp = None
    if recv[0] == "l_english:" :
        del recv[0]
    else :
        print("l_english not found on {}".format(filename) )
        return False
    
    for line in recv :
        temp = line[1:].split(" ", 1)
        print(temp)
        proc.append("=".join(temp))
        
    try :
        ##open file as UTF-8-SIG(with BOM) for not crashing if it has BOM or not
        file = open(os.path.join(filedir, filename[:-3]) + "properties" , 'w', encoding = "UTF-8-SIG") 
        print("writing file {name} at {dir}".format( name = filename[:-3]+"properties", dir = filedir) )
        for ii in proc :
            file.write(ii + "\n")
        file.close()
    except :
        print("error write properties file")
        return False
        
    return True
        
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
        if '.yml' == f[-4:] :
            try :
                result = PY2JP(f, path)
                print(result)
                if result :
                    #if result['NoDelim'] != []:
                    #    notproced.append((f, result) )
                    #elif result['BadKey'] != [] :
                    #    notproced.append( (f, result) )
                    #elif result['NoValue'] != [] :
                    #    completed.append( (f, result) )
                    #else :
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
