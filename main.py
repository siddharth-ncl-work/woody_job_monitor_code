#imports are relative to the dir where code is being executed
import pandas as pd
import numpy as np

from source import init
from source import job
import config


def getNxtDirName(i):
  return str(config.job_dir_name_suffix+str(round(i,1)))

init.init()
prev_dir_name=config.init_job_dir_name
for i in np.arange(config.init_bond_length+config.step_size,config.final_bond_length+config.step_size,config.step_size):
  nxt_dir_name=getNxtDirName(i)
  job.runJob(prev_dir_name,nxt_dir_name,steps=list(range(1,10)))
  prev_dir_name=nxt_dir_name 

