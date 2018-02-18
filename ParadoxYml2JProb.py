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
        
        
        
if __name__ == "__main__" :
    PY2JP("test.yml")