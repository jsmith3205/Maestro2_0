import os
from mkdir import mkdir
from python_terraform import *


def terra_init(terra_obj,target_dir):
    mkdir(target_dir)
    return_code, stdout, stderr = terra_obj.init(target_dir)

    print(return_code)
    print(stdout)
    print(stderr)

def terra_plan(terra_obj,target_dir):
    mkdir(target_dir)
    return_code, stdout, stderr = terra_obj.plan(target_dir)

    print(return_code)
    print(stdout)
    print(stderr) 

def terra_apply(terra_obj,target_dir):
    mkdir(target_dir)
    return_code, stdout, stderr = terra_obj.apply(target_dir)

    print(return_code)
    print(stdout)
    print(stderr)

def terra_destroy(terra_obj,target_dir):
    mkdir(target_dir)
    return_code, stdout, stderr = terra_obj.destroy(target_dir)

    print(return_code)
    print(stdout)
    print(stderr)


if __name__ == "__main__":
    print("Hello")
    terra_obj = Terraform()
    terra_init(terra_obj,'terraform_builds/test')
    terra_plan(terra_obj,'terraform_builds/test')
    terra_apply(terra_obj,'terraform_builds/test')
    terra_destroy(terra_obj,'terraform_builds/test')

    
   
