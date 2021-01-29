#!/usr/bin/python3

import os
import sys

def mkdir(path:str=''):
    print(f'The mkdir function has received direction to create {os.path.join(path)}')
    mkerror = False
    try:  
        os.mkdir(os.path.join(path),755)
    except OSError as error:  
        # print(error)
        mkerror = True
    
    if mkerror:
        print("Path Exists")
        return "Path Exists"
    else:
        print("success")
        return "success"

if __name__ == "__main__":
    print(sys.argv)
    if "-d" in sys.argv:
        print(f'Creating directory {sys.argv[sys.argv.index("-d")+1]}')
        mkdir(sys.argv[sys.argv.index("-d")+1])

