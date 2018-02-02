# Stellaris Properties 2 psudo-Yaml converter

This program is for helping .properties file to .yml file used in Stellaris(Paradox Interactive) 

# How to use
  - Put all .properties file in specific directory(folder in Windows)
  - create path.txt and put that path of that directory
  - excecute program using python 3
  - see result

# Detail and Warning
  - Path can be relative or abstract
    - ex 1(abstract) : /dev/show/properties
    - ex 2(abstract) : C:\stella\ris\proer\ties\
    - ex 3(relative) : ./works
     - this directory is placed as same directory of program's .py file and directory name is 'works'(Without Quotes)
  - If path.txt not found or wrong path recieved, program used it's own directory as path
  - Program may be broken dealing with too much/large file. Always backup your file before using it

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
