#!/bin/bash

code_dir_abs_path='/home/vanka/siddharth/woody_job_monitor_code'
proj_dir_abs_path='/home/vanka/siddharth/code_test_dir'
init_job_dir_name='init_2.7'
job_dir_name_suffix='test'
common_files_dir_abs_path='/home/vanka/siddharth/common_files'

atom0=0
atom1=56
moiety='list(range(56,89))'
init_bond_length=2.7
final_bond_length=5.0
step_size=0.1

converge_file_name='GEO_OPT_CONVERGED'


echo code_dir_abs_path="'$code_dir_abs_path'" > $code_dir_abs_path/config.py
echo proj_dir_abs_path="'$proj_dir_abs_path'" >> $code_dir_abs_path/config.py
echo init_job_dir_name="'$init_job_dir_name'" >> $code_dir_abs_path/config.py 
echo job_dir_name_suffix="'$job_dir_name_suffix'" >> $code_dir_abs_path/config.py
echo common_files_dir_abs_path="'$common_files_dir_abs_path'" >> $code_dir_abs_path/config.py

echo atom0="$atom0" >> $code_dir_abs_path/config.py
echo atom1="$atom1" >> $code_dir_abs_path/config.py
echo moiety=$moiety >> $code_dir_abs_path/config.py
echo init_bond_length=$init_bond_length >> $code_dir_abs_path/config.py
echo final_bond_length=$final_bond_length >> $code_dir_abs_path/config.py
echo step_size=$step_size >> $code_dir_abs_path/config.py

echo converge_file_name="'$converge_file_name'" >> $code_dir_abs_path/config.py

cd $code_dir_abs_path
nohup python -u main.py | tee $proj_dir_abs_path/output.log &

