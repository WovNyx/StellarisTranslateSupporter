## Programmed by WovNyx

import os
import configparser
from datetime import datetime

_config_default = """
## Orient : directory of JProc file (*.properties) you want to convert
[PATH]
    Orient = ./jproc/
    Dest = ./result/


## error handling and print setting for line parse
#### "ignore" : just ignore that line does nothing
#### "warnwrite" : try parse and warn that line at result 
#### "warnpass"  : skip line and warn that line at result 
#### "nowrite" : don't write file and warn that line at result 
[LINEPARSE]
    NoKey = warnpass
    NoValue = warnwrite
    BadKey = nowrite
    NoDelim = nowrite

[DEBUG]
    DebugPrint = False
"""
    
class StellarisJProc2PdxYmlParser(object) :
    def __init__(self) :
        self.config = configparser.ConfigParser()
        self._config_file = None
        self.hasconfig = False
        ## reads default config first for easy exception handling
        self.config.read_string(_config_default )
        try :
            self._config_file = open('StellarisJProc2PdxYml.ini')
            self.config.read_string(self._config_file )
            self._config_file.close()
            self.hasconfig = True
            del self._config_file
        except :
            self.config.read_string(_config_default )
            print("config file not found. creating default")
        if self.hasconfig :
            with open("StellarisJProc2PdxYml.ini", "w") as configfile :
                self.config.write(configfile)
        
        self.config['PATH']['Orient'] = os.path.abspath(self.config['PATH']['Orient']) 
        self.config['PATH']['dest'] = os.path.abspath(self.config['PATH']['dest']) 
        
        for ii in self.config :
            print(ii)
            for jj in self.config[ii] :
                print("    ", jj,":", self.config[ii][jj])
        try :
            if str(self.config['DEBUG']['DEBUGPRINT'])  :
                self.debug = True
            else :
                self.debug = False
        except :
            self.debug = False
        
    def _debugprint(self, *args, debug = False) :
        if self.debug :
            rtn = ''
            for ii in args :
                if ii :
                    rtn += str(ii)
            print(rtn)
        else :
            pass
        
    def parseLine(self, line) :
        ## this function parses single JProc line to Paradox Yml-like line for Stellaris
        ## return (result, rdata) , result is status of parsing.
        #### "clear" when no problem happend. "ref" if start of line(except spaces) is #
        #### others are error codes
        temp = None
        if line.strip() != '' :
            if line.strip()[0] == "#" or line.strip()[0] == ';' :
                return("ref", line)
                
            temp = line.split("=", 1)
            print("start parse")
            if temp[0] == '' :
                self._debugprint("JProc2PdxYmlParser.parseLine : ", "key not found.\n", temp)
                return ('nokey', " " + line)
            if len(temp) != 2 :
                self._debugprint("JProc2PdxYmlParser.parseLine : ", "deliminonator not found.\n", temp)
                return ('nodelim', line)
                
            if "코" in temp[0] :
                temp[0] = temp[0].replace("코", ":")
            elif ":" in temp[0] :
                pass
                
                
            if ":" in temp[0] :
                if len(temp[0].split(":") ) != 2 :
                    self._debugprint("JProc2PdxYmlParser.parseLine : ", "bad key\n", temp)
                    self._debugprint("too few or too many seperator ", ":", " in key")
                    return ('badkey', line)
                elif "" in temp[0].split(":") :
                    self._debugprint("JProc2PdxYmlParser.parseLine : ", "bad key\n", temp)
                    self._debugprint("empty keyname or chaincount")
                    return ('badkey', line)
                elif temp[0].split(":")[1].isdecimal() == False :
                    self._debugprint("JProc2PdxYmlParser.parseLine : ", "bad key\n", temp)
                    self._debugprint("chain count not numberic")
                    return ('badkey', line)
            else  :
                self._debugprint("JProc2PdxYmlParser.parseLine : ", "bad key\n", temp)
                self._debugprint("no seperator ", ":", " in key")
                return ('badkey', line)

            
            if temp[1] == '' :
                self._debugprint("JProc2PdxYmlParser.parseLine : ", "no value\n", temp)
                temp[1] = '""'
                return ("novalue", temp[0] + " ")
            else :
                temp[1] = temp[1].replace("<?>","")
                if temp[1] == '"' :
                    temp[1] = '""'
                if temp[1][0] != '"' :
                    temp[1] = '"' + temp[1]
                if temp[1][-1] != '"' :
                    temp[1] = temp[1] + '"'
            return ("clean", " ".join(temp) )
        else :
            return ("clean", "")
        
    def parseFile(self, fname, orient, dest) :
        file = None
        proc = [] ## processed data, will be written on fname.yml
        rstatus = ''
        rdata = ''
        ## variables for error handling
        linecount = 0
        badline = {}
        badline['nodelim'] = [] ## deliminator '=' not found
        badline['badkey']  = []
        badline['novalue'] = []
        badline['nokey'] = []
        nowrite = False
        
        ## opening file and seperating by line
        try :
            #file = open(os.path.join(filedir, fname), "r", encoding = "UTF-8-SIG")
            file = open(os.path.join("./jproc", fname), "r", encoding = "UTF-8-SIG")
            self._debugprint("opening file {name} at {dir}".format( name = fname, dir = orient ) )
        except Exception as excp :
            print("error opening properties file")
            print(self.config['PATH']['orient'], fname)
            badline['failedwrite'] = True
        recv = file.read().split("\n") ## seperate by line
        file.close()
        ## file opened and seperated by line
        
        
        
        for line in recv :
            linecount += 1
            rstatus, rdata  = self.parseLine(line)
            if rstatus == "clean" :
                proc.append(rdata)
                self._debugprint("clean convertion\n", rdata, debug = self.debug)
            elif rstatus == "ref" :
                self._debugprint("reference found", debug = self.debug)
                continue
            else :
                for ii in self.config['LINEPARSE'] :
                    if ii == rstatus :
                        print(ii, rstatus )
                        if self.config['LINEPARSE'][ii] == 'ignore' :
                            self._debugprint("config says ignore ", ii, " error\n")
                            continue
                        elif self.config['LINEPARSE'][ii] == 'warnpass' :
                            self._debugprint("config says dont write when there is ", ii, " error\n")
                            badline[ii].append( (linecount, rdata) )
                            continue
                        elif self.config['LINEPARSE'][ii] == 'warnwrite' :
                            self._debugprint("config says dont write when there is ", ii, " error\n")
                            proc.append(rdata)
                            badline[ii].append( (linecount, rdata) )
                            continue
                        elif self.config['LINEPARSE'][ii] == 'nowrite' :
                            self._debugprint("config says dont write when there is ", ii, " error\n")
                            badline[ii].append( (linecount, rdata) )
                            nowrite = True
                            continue
                        else :
                            self._debugprint("wrong return value on .parseLine\n",rstatus, "\n", rdata)  
                    else :
                        pass
        self._debugprint("we {} write file".format( int(nowrite)*"won't" + (1-int(nowrite) )*"will" ) )
        
        if nowrite :
            self._debugprint("bad or faulty data on orient file. don't write file.")
            badline['iswritten'] = False
        else :   
            try :
                ##open file as UTF-8-SIG(with BOM) for not crashing if it has BOM or not
                file = open(os.path.join(self.config['PATH']['dest'], fname[:-10]) + "yml" , 'w', encoding = "UTF-8-SIG") 
                self._debugprint("writing file {name} at {dir}".format( name = fname[:-10]+"yml", dir = dest) )
                if "_l_english_tag" in fname :
                    file.write("l_english_tag" + "\n")
                else :
                    file.write("l_english" + "\n")
                for ii in proc :
                    file.write(" " + ii + "\n")
                file.close()
                badline['iswritten'] = True
            except Exception as excp :
                print("error making yaml-like paradox file", excp)
                badline['iswritten'] = False
        
        return badline
        
    def run(self) :
        cleanparse = []
        haswarning = []
        baddata = []
        unknownerror = []
    
    
        orient, dest = self.config['PATH']['orient'], self.config['PATH']['dest']
        filesindir = [f for f in os.listdir(orient) if os.path.isfile(os.path.join(orient, f) ) and '.properties' == f[-11:] ]
        self._debugprint("files in orient directory ", orient, "\n", filesindir)
        
        for file in filesindir :
            try :
                result = self.parseFile(file, orient, dest )
                if result['iswritten'] :
                    print("clean file convertion on ", file)
                    cleanparse.append((os.path.join(dest, file), result ) )
                else :
                    print("bad data on ", file)
                    baddata.append((os.path.join(dest, file), result ) )
            except :
                print("unknown error while convertin ", orient, dest, file)
                unknownerror.append((orient, dest, result) )
                    
        ## formatting needed
        print("convertion successed on")
        for ii in cleanparse :
            print(ii)
        print("bad data on")
        for ii in baddata :
            print(ii)
        print("unknown error on")
        for ii in unknownerror :
            print(ii)
if __name__ == "__main__" :
    test = StellarisJProc2PdxYmlParser()
    test.run()
    
    
    
    