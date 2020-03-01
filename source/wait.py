import time
import subprocess
from subprocess import PIPE
import os

import config


def qFlag(job_name):
  q_flag='not_defined'
  output=subprocess.run(['qstat'],stdout=PIPE,stderr=PIPE,encoding='utf-8')
  if job_name in output.stdout.split():
    q_flag='running'
  else:
    q_flag='not_running'
  return q_flag

def searchDirFlag(search_dir_path):
  search_dir_flag=None
  for file in os.listdir(search_dir_path):
    if 'GEO_OPT_'in file:
      search_dir_flag=file.split('_')[-1]
      break
  return search_dir_flag

def checkJobStatus(job_name,step=100):
  stop_flag=None
  q_flag=None
  job_dir_flag=None
  job_dir_path=os.path.join(config.proj_dir_abs_path,job_name)
  if not os.path.isdir(job_dir_path):
    print('Job directory does not exists')
    if step==0:
      return False
    else:
      print('Raising stop flag')
      return True 
  q_flag=qFlag(job_name)
  job_dir_flag=searchDirFlag(job_dir_path)
  print(f'Job:{job_name} is {q_flag}, GEO_OPT_{job_dir_flag}')
  if q_flag=='not_running':
    stop_flag=True
    if job_dir_flag==None:
      print('GEO_OPT is not yet created')
      if step==0:
        stop_flag=False
      else:
        stop_flag=True
    elif job_dir_flag.lower()=='running':
      print('Possible wall time exceeded error')
    elif job_dir_flag.lower()=='converged':
      if 'coord' in os.listdir(job_dir_path):
        print(f'Job: {job_name} is CONVERGED')
        stop_flag=True
      else:
        print(f'Job: {job_name} is CONVERGED but coord file is not yet created...')
        stop_flag=False
    elif job_dir_flag.lower()=='failed':
      print(f'Job: {job_name} is FAILED')
      if step==0:
        stop_flag=False
      else:
        stop_flag=True
    else:
      print(f'unknown GEO_OPT flag {job_dir_flag}')
  elif q_flag=='running':
    stop_flag=False
    if job_dir_flag==None:
      print('GEO_OPT is not yet created')
    elif job_dir_flag.lower()=='running':
      print(f'Job: {job_name} is RUNNING')
    elif job_dir_flag.lower()=='converged':
      if 'coord' in os.listdir(job_dir_path):
        print(f'Job: {job_name} is CONVERGED')
        stop_flag=True
      else:
        print(f'Job: {job_name} is CONVERGED but coord file is not yet created...')
        stop_flag=False
    elif job_dir_flag.lower()=='failed':
      print(f'Job: {job_name} is FAILED')
      stop_flag=True
    else:
      print(f'unknown GEO_OPT flag {job_dir_flag}')
  return stop_flag

def wait(job_name,interval=1):
  start_time=time.time()
  stop_flag=False
  while not stop_flag:
    time.sleep(interval)
    elapsed_time=round(time.time()-start_time,2)
    print(f'Time elapsed: {elapsed_time} seconds')
    stop_flag=checkJobStatus(job_name,step=9)

if __name__=='__main__':
  dir_path='/home/vanka/sid/2.8'
  wait(dir_path)
