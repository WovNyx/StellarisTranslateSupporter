## Programmed by WovNyx

import os
import configparser
from datetime import datetime
import pprint


## 20180301 parseline, convline done, need convfile some work
## 20180303 convfile done, warp/unwrap reworked, l_english and l_english_tag header at PdxYml file not done.
##    processing indentation for writing also needed
## config.ini read/write problem fixed. parsing multiple kinds of delims in single line needed

def makedir(directory )  :
    try:
        if not os.path.isdir(directory):
            os.makedirs(directory)
        return True
    except OSError:
        print ('Error : Failed creating directory  ' + directory)
        return False
        
_config_default = """
## Orient : directory of JProc file (*.properties) you want to convert.
[PATH]
    Orient = ./jproc/
    Dest = ./result/

[DATAFORMAT]
    ## name of file format u convert from.
    ## these values are case sensitive.
    orn_formatname = ParadoxPsudoYml_l_english
    
    ## name of file format you'll get as result.
    ## these values are case sensitive.
    dest_formatname = JavaPropertiesOldType
    
    ##example of file format, section name [sectionname] must be same as orn/dest_name values of [data] section.
    ##others will be ignored.
    ##you can use multiple charactors as same delmitor but it may cause unintened behavior, use at your own risk.
    ##these values must be wraped with ' (single quato).
    [ParadoxPsudoYml]
    ## suffix of file, used for searching file in directory.
        suffix = '.yml'
        valdelim =  ' '
        chaindelim = ':'
        ref = '#'
        wletter = '"'
        headline = ''
        indent = 1
    [ParadoxPsudoYml_l_english]
    ## suffix of file, used for searching file in directory.
        suffix = '.yml'
        valdelim =  ' '
        chaindelim = ':'
        ref = '#'
        wletter = '"'
        headline = 'l_english:'
        indent = 1
    [ParadoxPsudoYml_l_english_tag]
    ## suffix of file, used for searching file in directory.
        suffix = '.yml'
        valdelim =  ' '
        chaindelim = ':'
        ref = '#'
        wletter = '"'
        headline = 'l_english_tag:'
        indent = 1
    [JavaProperties]
        suffix = '.properties'
        valdelim = '='
        chaindelim = '|'
        ref = '#'
        wletter = '"'
        headline = ''
        indent = 0
    [JavaPropertiesOldType]
        ## suffix of file, used for searching file in directory.
        suffix = '.properties'
        valdelim = '='
        chaindelim = '코'
        ref = '#'
        wletter = ''
        headline = ''
        indent = 0

## error handling and print setting for line parse.
#### "ignore" : just ignore that line does nothing
#### "warnwrite" : try parse and warn that line at result 
#### "warnpass"  : skip line and warn that line at result 
#### "nowrite" : don't write file and warn that line at result
[LINEPARSE]
    NoKey = warnpass
    NoValue = warnwrite
    BadKey = nowrite
    NoDelim = nowrite
    NoData = ignore

[DEBUG]
    DebugPrint = False
"""
    

class StellarisTranslateSupporter(object) :
    def __init__(self) :
        self.config = configparser.ConfigParser()
        self.noconfig = True
        self.orn_formatdata = {}
        self.dest_formatdata = {}
        ## reads default config first for easy exception handling
        #self.config.read_string(_config_default )
        
        _configfile = None
        
        ## bug that don' read/write config
        try :
            _configfile = open("STSconfig.ini" , 'r' )
            self.config.read("STSconfig.ini" ) ## this one recieves name of file
            self.noconfig = False
            _configfile.close()
            print("config file loaded")
        except :
            self.config.read_string(_config_default )
            print(self.config)
            print("config file not found. creating default")
        if self.noconfig == True :
            with open("STSconfig.ini", "w") as configfile :
                #self.config.read_string(_config_default )
                #self.config.write(configfile)
                configfile.write(_config_default)
                configfile.close()
                print("STSconfig.ini file creadted")
        
        self.config['PATH']['Orient'] = os.path.abspath(self.config['PATH']['Orient']) 
        self.config['PATH']['dest'] = os.path.abspath(self.config['PATH']['dest']) 
        
        ## seperates orient/dest format data for ease of use
        self.orn_fmtdata = self.config[self.config['DATAFORMAT']['orn_formatname'] ]
        self.orn_fmtdata['name'] = self.config['DATAFORMAT']['orn_formatname']
        self.dest_fmtdata = self.config[self.config['DATAFORMAT']['dest_formatname'] ]
        self.dest_fmtdata['name'] = self.config['DATAFORMAT']['dest_formatname']
        
      
        for ii in self.orn_fmtdata :
            self.orn_fmtdata[ii] = self.unwrap(self.orn_fmtdata[ii], "'" )
            print(ii, self.orn_fmtdata[ii])
        for ii in self.dest_fmtdata :
            self.dest_fmtdata[ii] = self.unwrap(self.dest_fmtdata[ii], "'" )
            
        
        ## setting debug status
        try :
            if str(self.config['DEBUG']['DEBUGPRINT'])  :
                self.debug = True
            else :
                self.debug = False
        except :
            self.debug = False
        
        ## debug prints
        if self.debug :    
            for ii in self.config :
                print(ii)
                for jj in self.config[ii] :
                    print("    ", jj,":", self.config[ii][jj])
                
                
        
    def _debugprint(self, *args, debug = False) :
        if self.debug :
            rtn = ''
            for ii in args :
                if ii :
                    rtn += str(ii)
            print(rtn)
        else :
            pass
        
    def wrap(self, line, letter, force = False) :
        ## add first and last letter of line with letter
        ## don`t add if first/last letter is same as input
        ## if force = True, wraps line whenever it's first and/or last
        ## maybe it won't work letter has 2 or more charactors
        result = line
        if result == '' or result == letter :
            result = letter*2
        elif result[0] != result[-1] :
            if result[0] == letter :
                result = result + letter
            elif result[-1] == letter :
                result = letter + result
            else :
                result = letter + result + letter
        else :
            if result[0] == letter :
                pass
            else :
                result = letter + result + letter
        return result
    
    def unwrap(self, line, letter) :
        result = line
        if result == '' or result == letter :
            result = ''
        else :
            if result[0] == letter :
                result = result[1:]
            if result[-1] == letter :
                result = result[:-1]
            else :
                pass
        return result
        
    
    def parseLine(self, line, valdelim, chaindelim,  ref, wletter = '') :
        ## it parses string line into map
        ## status is result of data and key, chain, value is parsed outcome data
        ## don't parse chain if no chaindelim recieved
        ## if valdelim is ' '(space) or '\t'(tab), it might return nodelim status even if actual data has delim but has no key or value
        line = line.strip()
        print(line)
        if not line :
            return {'status' : 'nodata', 'key' : '', 'chain' : '', 'value' : ''}
        
        if line[0] in ref :
            return {'status' : 'ref', 'key' : '', 'chain' : '', 'value' : line[1:]}
        if line == self.orn_fmtdata['headline'] :
            return {'status' : 'headline', 'key' : '', 'chain' : '', 'value' : ''}
        if valdelim in line :
            key, value = line.split(valdelim, 1)
            value = self.unwrap(value, wletter)
            if '' == key :
                return {'status' :'nokey', 'key' : '', 'chain' : '' , 'value' : value}
            elif chaindelim != '' and chaindelim in key :
                kname, chain = key.split(chaindelim, 1)
                if (not chain.isdecimal() ) or (kname == '') :
                    return {'status' :'badkey', 'key' : key, 'chain' : '', 'value' : value}
                else :
                    
                    if value != '' :
                        return {'status' : 'clean', 'key' :kname, 'chain' : chain, 'value' : value}
                    else :
                        return {'status' : 'novalue', 'key' :kname, 'chain' : chain, 'value' : ''}
            elif chaindelim == '' :
                return {'status' : 'clean', 'key' :key, 'chain' : '', 'value' : value}
            else :
                return {'status' :'badkey', 'key' : key, 'chain' : '', 'value' : value}
        else :
            return {'status' :'nodelim', 'key' : '', 'chain' : '', 'value' : line }
            
    def parsedMapLineMake(self, map, valdelim, chaindelim, ref, wletter ) :
        # makes returned map from parseLine() has single completed line of data
        # outcome = key(chaindelim)chain(valdelim)<wrap>value<wrap>
        # ex)  KEY_NAME.EXAMPLE:126="This Is Value and Can use = " : etc "
        if map.get('status') :
            if map['status'] in 'ref' :
                return {'status' : map['status'], 'line' : ref + map['value'] }
            elif map['status'] in 'nodelim':
                return {'status' : map['status'], 'line' : map['value'] }
            else :                    
                if map.get('value') :
                    map['value'] = self.wrap(map['value'], wletter)
                    
            if map['status'] in ['clean', 'novalue', 'nokey'] :
                if map.get('chain') : ## if map['chain'] is '' or not exist
                    return {'status' : map['status'], 'line' : (map['key'] + chaindelim + map['chain'] + valdelim + map['value'] ) }
                else :
                    return {'status' : map['status'], 'line' : (map['key'] + valdelim + map['value']) }
            elif map['status'] == 'badkey' :
                return {'status' : map['status'], 'line' :  map['key'] + valdelim + map['value'] }
            elif map['status'] == 'novalue':
                if map.get('chain') : ## if map['chain'] is '' or not exist
                    return {'status' : map['status'], 'line' :  map['key'] + chaindelim + map['chain'] + valdelim }
                else :
                    return {'status' : map['status'], 'line' : map['key'] + valdelim }
            elif map['status'] in ['nodata', 'headline'] :
                return {'status' : map['status'], 'line' : '' }
        else :
            print("wrong input")
            raise ValueError
            
    def _convLine(self, line, orn_valdelim, orn_chaindelim, orn_ref, orn_wletter \
                           , dest_valdelim, dest_chaindelim, dest_ref, dest_wletter) : 
        return self.parsedMapLineMake(self.parseLine(line, orn_valdelim, orn_chaindelim, orn_ref, orn_wletter) \
                                                   , dest_valdelim, dest_chaindelim, dest_ref, dest_wletter)
                                                   
    def convLine(self, line) :
        return self._convLine(line,  self.orn_fmtdata['valdelim'],   self.orn_fmtdata['chaindelim'], \
                                    self.orn_fmtdata['ref'],   self.orn_fmtdata['wletter'], \
                                    self.dest_fmtdata['valdelim'], self.dest_fmtdata['chaindelim'], \
                                    self.dest_fmtdata['ref'],  self.dest_fmtdata['wletter'])
                                    
    def convFile(self, fname ) :
        file = None
        proc = [] ## processed data, will be written as file
        rstatus = ''
        rdata = ''
        extention = ''
        ## variables for error handling
        linecount = 0
        badline = {}
        badline['nodelim'] = [] ## deliminator '=' not found
        badline['badkey']  = []
        badline['novalue'] = []
        badline['nokey'] = []
        badline['haswarning'] = False
        nowrite = False
        ## re-name variables in config for ease of use
        orn_dir = self.config['PATH']['orient']
        dest_dir = self.config['PATH']['dest']
        
        
        ## opening file and seperating by line
        try :
            ## dont add orn_suffix for opening file since fname has it already from searching files
            file = open(os.path.join(orn_dir, fname), "r", encoding = "UTF-8-SIG")
            self._debugprint("opening file {name} at {dir}".format( name = fname, dir = orn_dir ) )
        except Exception as excp :
            print("error opening orient file ", os.path.join(orn_dir, fname))
            badline['failedwrite'] = True
        recv = file.read().splitlines() ## seperate by line
        file.close()
        ## file opened and seperated by line
        
        print(recv)
        
        ## parsing files and temperaly stores in memory
        if self.dest_fmtdata.get('headline' ) :
            proc.append(self.dest_fmtdata['headline'] )
            linecount += 1
        for line in recv :
            linecount += 1
            temp = self.convLine(line )
            rstatus = temp['status']
            rdata = temp['line']
            if rstatus == "clean" :
                proc.append(rdata)
                self._debugprint("clean convertion\n", rdata)
            elif rstatus == "ref" :
                self._debugprint("reference found\n", rdata)
                continue
            elif rstatus == "headline" :
                self._debugprint("header found\n", rdata)
            elif rstatus == "nodata" :
                proc.append('')
                self._debugprint("no data in this line")
            else :
                for ii in self.config['LINEPARSE'] :
                    if ii == rstatus :
                        print(ii, rstatus, rdata )
                        if self.config['LINEPARSE'][ii] == 'ignore' :
                            self._debugprint("config says ignore ", ii, " error\n")
                            continue
                        elif self.config['LINEPARSE'][ii] == 'warnpass' :
                            self._debugprint("config says dont write when there is ", ii, " error\n")
                            badline[ii].append( (linecount, rdata) )
                            badline['haswarning'] = True
                            continue
                        elif self.config['LINEPARSE'][ii] == 'warnwrite' :
                            self._debugprint("config says dont write when there is ", ii, " error\n")
                            proc.append(rdata)
                            badline[ii].append( (linecount, rdata) )
                            badline['haswarning'] = True
                            continue
                        elif self.config['LINEPARSE'][ii] == 'nowrite' :
                            self._debugprint("config says dont write when there is ", ii, " error\n")
                            badline[ii].append( (linecount, rdata) )
                            nowrite = True
                            continue
                        else :
                            self._debugprint("wrong return value on .convLine\n",rstatus, "\n", rdata)  
                    else :
                        pass
        self._debugprint("we {} write file".format( int(nowrite)*"won't" + (1-int(nowrite) )*"will" ) )
        
        
        if nowrite :
            self._debugprint("bad or faulty data on orient file. don't write file.")
            badline['iswritten'] = False
        else :   
            try :
                ##open file as UTF-8-SIG(with BOM) for not crashing if it has BOM or not
                file = open(os.path.join(dest_dir, fname[:-len(self.orn_fmtdata['suffix'])] + self.dest_fmtdata['suffix'] )
                            , 'w', encoding = "UTF-8-SIG")
                self._debugprint("writing file {name} at {dir}".format( name = fname[:-len(self.orn_fmtdata['suffix']) ] + self.dest_fmtdata['suffix'], dir = dest_dir) )
                for ii in proc :
                    file.write(" "*self.dest_fmtdata.getint('indent') + ii + "\n")
                file.close()
                badline['iswritten'] = True
            except Exception as excp :
                print("error writing dest file", excp)
                badline['iswritten'] = False
        
        return badline
        
    def convDirAll(self) :
        cleanconv = []
        haswarning = []
        baddata = []
        unknownerror = []

        final = {'cleanconv' : {}, 
                'baddata' : {},
                'haswarning' : {},
                'unknownerror' : {} }
        pp = pprint.PrettyPrinter(indent = 8)
        ##
        ## final = { resulttype1 :
        ##              { 'filedir1' : 
        ##                    { 'filename1' :
        ##                          { fileresult }    
        ##                      'filename2' :
        ##                         { fileresult }    
        ##                    ....
        ##                    }   
        ##                ...
        ##              }
        ##           ...
        ##          }
        ##
        ##
        ##
    
        orient, dest = self.config['PATH']['orient'], self.config['PATH']['dest']
        if makedir(orient) and makedir(dest) :
            pass
        else :
            print("errer creating directory for files")
            return
        filesindir = [f for f in os.listdir(orient) if os.path.isfile(os.path.join(orient, f) ) and self.orn_fmtdata['suffix'] in f ]
        self._debugprint("files in orient directory ", orient, "\n", filesindir)
        
        ## setting empty map for orient dir
        
        for file in filesindir :
            result = None
            try :
                result = self.convFile(file )
                if result['iswritten'] :
                    if result['haswarning'] :
                        print("file converted but has warnings on ", file)
                        final['cleanconv'][os.path.join(orient,file)] = result
                    else :
                        print("clean file convertion on ", file)
                        final['cleanconv'][os.path.join(orient,file)] = result
                else :
                    print("didin't write on ", file)
                    final['baddata'][os.path.join(orient,file)] = result
            except :
                raise error
                if result :
                    final['unknownerror'][os.path.join(orient,file)] = result
                else :
                    final['unknownerror'][os.path.join(orient,file)] = "{} failed to convert".format(os.path.join(orient,file) )
                    
                    ##
        print("!!!!!!\n")
        print(final)
                    
        print("@@@@@@\n")
        ## printing result
        for ii in final :
            print(ii)
            for jj in final[ii] :
                print("\t" + jj)
                if type(final[ii][jj]) == type({} ) :
                    for kk in final[ii][jj] :
                        print("\t\t",kk,  final[ii][jj][kk]  )
                else :
                    print("\t\t", final[ii][jj])
                    
        
        
if __name__ == "__main__" :
    test = StellarisTranslateSupporter()
    test.convDirAll()
    
   
    
        
        
    
