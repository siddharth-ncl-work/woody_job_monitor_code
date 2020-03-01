import pandas as pd
import os
import subprocess

from lib.io_chem import io
import config 
from source import job


def init():
  init_struct_file_path=os.path.join(config.proj_dir_abs_path,config.init_job_dir_name,config.init_job_dir_name+'.xyz')
  print(f'optimizing intial structure file: {init_struct_file_path}')
  df=io.readFile(init_struct_file_path)
  job.runJob(config.init_job_dir_name,config.init_job_dir_name,steps=list(range(3,10)))
