import time
import subprocess
from subprocess import PIPE
import os

import config


def wait(dir_path,job_name='',interval=1):
  start_time=time.time()
  while True:
    time.sleep(interval)
    elapsed_time=round(time.time()-start_time,2)
    q_output=subprocess.run(['qstat'],stdout=PIPE,stderr=PIPE,encoding='utf-8')
    if job_name not in q_output.stdout.split():
      print('job is not running. Terminating the python programme')
      break
    else:
      print(f'Job:{job_name} is running... Time elapsed: {elapsed_time} seconds')
    if config.converge_file_name in os.listdir(dir_path) and 'coord' in os.listdir(dir_path):
      print(f'job:{job_name} CONVERGED!')
      break


if __name__=='__main__':
  dir_path='/home/vanka/sid/2.8'
  wait(dir_path)
