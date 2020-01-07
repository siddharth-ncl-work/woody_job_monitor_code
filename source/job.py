import pandas as pd
import numpy as np
import subprocess
import os
import sys
sys.path.extend([',','..'])

import config
from lib.io_chem import io
from source import stretch_bond
from source import wait


def fixAtoms(file_path,atoms_list):
  df=io.readFile(file_path,file_type='opt')
  print(df.head())
  io.writeFile(file_path,df,file_type='opt',info='fix_atoms',atoms_list=atoms_list)
  
def modifyControlFile(file_path,nxt_dir_name):
  data=None
  with open(file_path,'r') as file:
    data=file.readlines()
  for i,line in enumerate(data): 
    if '$title' in line:
      pos=i
      break
  data[pos+1]=nxt_dir_name+'\n'
  with open(file_path,'w') as file:
    file.write(''.join(data))

def modifyTryScript(file_path,nxt_dir_name):
  data=None
  with open(file_path,'r') as file:
    data=file.readlines()
  for i,line in enumerate(data):
    if 'dir=' in line:
      pos=i
      break
  data[pos]='dir=.\n'
  for i,line in enumerate(data):
    if 'job=' in line:
      pos=i
      break
  data[pos]='job='+nxt_dir_name+'\n'
  with open(file_path,'w') as file:
    file.write(''.join(data))

def modifyOptScript(file_path,nxt_dir_name):
  nxt_dir_abs_path=os.path.join(config.proj_dir_abs_path,nxt_dir_name)
  data=None
  with open(file_path,'r') as file:
    data=file.readlines()
  for i,line in enumerate(data):
    if '#PBS -N' in line:
      pos=i
      break
  data[pos]='#PBS -N '+nxt_dir_name+'\n'
  for i,line in enumerate(data):
    if 'job=' in line:
      pos=i
      break
  data[pos]='job='+nxt_dir_name+'\n'
  for i,line in enumerate(data):
    if 'mkdir ' in line:
      pos=i
      cmd=line
      break
  #data[pos]='#'+cmd
  data[pos]='mkdir '+nxt_dir_abs_path+'\n'
  for i,line in enumerate(data):
    if 'mv *' in line:
      pos=i
      cmd=line
      break
  #data[pos]='mv * .\n'
  data[pos]='mv * '+nxt_dir_abs_path+'\n'
  with open(file_path,'w') as file:
    file.write(''.join(data))

def checkProcess(process):
  command=' '.join(process.args)
  if process.returncode==0:
    print('command:{command} exected successfully')
  else:
    print('command:{command} encountered an error')

def runJob(prev_dir_name,nxt_dir_name,steps=list(range(1,10))):
  prev_dir_path=os.path.join(config.proj_dir_abs_path,prev_dir_name)
  nxt_dir_path=os.path.join(config.proj_dir_abs_path,nxt_dir_name)

  #step_1
  if 1 in steps:
    print('step 1 running...')
    prev_file_path=os.path.join(prev_dir_path,'coord')
    new_file_path=os.path.join(prev_dir_path,prev_dir_name+'.xyz')
    print(f't2x converting {prev_file_path} to {new_file_path}...') 
    p=subprocess.run(['t2x',prev_file_path],stdout=open(new_file_path,'w'),encoding='utf-8')
    checkProcess(p)
    print(f'creating directory {nxt_dir_path}...')
    p=subprocess.run(['mkdir',nxt_dir_path])  
    checkProcess(p)
    print('step 1 finished')

  #step_2
  if 2 in steps:
    print('step 2 running...')
    prev_file_path=os.path.join(prev_dir_path,prev_dir_name+'.xyz') 
    new_file_path=os.path.join(nxt_dir_path,nxt_dir_name+'.xyz')
    print('stetching bonds...')
    stretch_bond.stretchBond(prev_file_path,outfile_path=new_file_path,atom0=config.atom0,atom1=config.atom1,moiety=config.moiety,trans=config.step_size)
    print('step 2 finished')

  #step_3
  if 3 in steps:
    print('step 3 running...')
    prev_file_path=os.path.join(nxt_dir_path,nxt_dir_name+'.xyz')
    new_file_path=os.path.join(nxt_dir_path,'coord')
    print(f'x2t converting {prev_file_path} to {new_file_path}...')
    p=subprocess.run(['x2t',prev_file_path],stdout=open(new_file_path,'w'),encoding='utf-8')
    checkProcess(p) 
    print(f'fixing atoms {config.atom0},{config.atom1}...')
    fixAtoms(new_file_path,atoms_list=[config.atom0,config.atom1])
    print('step 3 finished')              

  #step_4(copy files)
  if 4 in steps:
    print('step 4 running...')
    print(f'copying files from {config.common_files_dir_abs_path}')
    p=subprocess.run(['cp','-a',config.common_files_dir_abs_path,nxt_dir_path]) 
    checkProcess(p)
    print('step 4 finished')

  #step_5
  if 5 in steps:
    print('step 5 running...')
    print('modifying control file...')
    file_path=os.path.join(nxt_dir_path,'control')
    modifyControlFile(file_path,nxt_dir_name)
    print('step 5 finished')

  #step_6
  if 6 in steps:
    print('step 6 running...')
    print('modifying try_script file...')
    file_path=os.path.join(nxt_dir_path,'try_script')
    modifyTryScript(file_path,nxt_dir_name)
    print('step 6 finished')

  #step_7(run_try_script)
  if 7 in steps:
    print('step 7 running...')
    print('running try_script...')
    p=subprocess.run(['./try_script'],cwd=nxt_dir_path)
    checkProcess(p)    
    print('step 7 finished')

  #step_8
  if 8 in steps:
    print('step 8 running...')
    print('modifying opt_woody_script file...')
    file_path=os.path.join(nxt_dir_path,'opt_woody_script')
    modifyOptScript(file_path,nxt_dir_name)
    print('step 8 finished')

  #step_9
  if 9 in steps:
    print('step 9 running...')
    print(f'submitting qsub job: {nxt_dir_name}')
    p=subprocess.run(['qsub','opt_woody_script'],cwd=nxt_dir_path)
    checkProcess(p)
    print(f'Waiting for job {nxt_dir_name} to finish...')
    wait.wait(nxt_dir_path,job_name=nxt_dir_name)
    print('step 9 finished')
  
if __name__=='__main__':
  prev_dir_name='2.7'
  nxt_dir_name='2.8'
  runJob(prev_dir_name,nxt_dir_name,steps=list(range(1,10)))  



