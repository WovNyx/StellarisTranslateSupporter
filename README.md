# Stellaris Properties 2 psudo-Yaml converter

This program is for converting .properties and .yml file used in Stellaris(Paradox Interactive) 

# How to use
  - Put all file in specific directory(folder in Windows) in your setting(default <directory_of_program>/jproc/ )
  - excecute program using python 3
  - see result
  - file wil be in directory you set (default <directory_of_program>/result> )

# setting detail
  - section names ([SECTIONNAME] ) are case sensitive
  - ### PATH
    - Path can be relative or abstract
        - ex 1(abstract) : ```/dev/show/properties```
        - ex 2(abstract) : ```C:\stella\ris\proer\ties\```
        - ex 3(relative) : ```./works```
            - this directory is placed as same directory of program's .py file and directory name is ```works```
  - ### DATATYPE 
    - orn_formatname, dest_formatname : name of orient and dest(result) format name
    - program will find section name of these, and use those values
    - 
  - ### LINEPARSE
    - behavior of parsing errored line in file
    - error types
        - nokey : as it is, No key found
        - novalue : as it is, No Value found
        - nodelim : Value Deliminator not found
        - badkey : this line has bad/broken key
        - nodata : no data in line, 
    - error handling case
        - ignore : as it is
        - warnpass : skip line and warn that line at result 
        - warnwrited : try parse and warn that line at result 
        - nowrite : don't write file and warn that line at result


# Warnings
  - Program may be broken dealing with too much/large file. Always backup your file before using it
  - may cause problem while parsing multiple kinds of deliminator
  - This is not profer Yaml parser!

#  To-dos
 - add recieving arguments in command line
 - add targeting Specific file
 - add processing multiple directory at once
 - add profer config file
 - add seperated result directory
 - may change default directory to something under program's directory(like ./properties)
License
----

MPL 2.0
