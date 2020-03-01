import pandas as pd
import numpy as np
import sys
sys.path.extend(['.','..'])

from lib.io_chem import io


def stretchBond(infile_path,outfile_path='',atom0=0,atom1=1,moiety=list(range(56,90)),trans=0.1):
  df=io.readFile(infile_path)
  atom0_vec=df.iloc[atom0,:]
  atom1_vec=df.iloc[atom1,:]
  vec=np.zeros((3,))
  vec[0]=atom1_vec['x']-atom0_vec['x']
  vec[1]=atom1_vec['y']-atom0_vec['y']
  vec[2]=atom1_vec['z']-atom0_vec['z']
 
  mag=np.linalg.norm(vec)
  uvec=vec/mag
  trans_vec=trans*uvec
  cords=df.loc[:,['x','y','z']].values
  cords[moiety]=cords[moiety]+trans_vec
  new_df=df.copy()
  new_df.loc[:,['x','y','z']]=cords
  io.writeFile(outfile_path,new_df)
  validate(infile_path,outfile_path,atom0=atom0,atom1=atom1,moiety=moiety)
 

def validate(infile_path,outfile_path,atom0=0,atom1=1,moiety=list(range(56,90))):
  prev_df=io.readFile(infile_path)
  print(prev_df)
  atom0_row=prev_df.iloc[atom0,:][['x','y','z']]
  atom1_row=prev_df.iloc[atom1,:][['x','y','z']]
  prev_dist=np.sqrt((atom0_row['x']-atom1_row['x'])**2 + \
                    (atom0_row['y']-atom1_row['y'])**2 + \
                    (atom0_row['z']-atom1_row['z'])**2)
  nxt_df=io.readFile(outfile_path)
  atom0_row=nxt_df.iloc[atom0,:][['x','y','z']]
  atom1_row=nxt_df.iloc[atom1,:][['x','y','z']]
  nxt_dist=np.sqrt((atom0_row['x']-atom1_row['x'])**2 + \
                    (atom0_row['y']-atom1_row['y'])**2 + \
                    (atom0_row['z']-atom1_row['z'])**2)
  print('strech along {} , {}'.format(atom0,atom1))
  print('moiety:'+str(moiety))
  print('prev_dist: {}   nxt_dist:{}  difference:{}'.format(prev_dist,nxt_dist,nxt_dist-prev_dist))

 
if __name__=='__main__':
  file_path='/home/vanka/siddharth/CisHH/C2.4/C2.4.xyz'
  output_file_path='test_stretch_bond.xyz'
  stretchBond(file_path,outfile_path=output_file_path,atom0=0,atom1=55,moiety=list(range(55,89)),trans=1)
