# woody_job_monitor_code
(Saumya's Project)
This repository contains code to monitor and submit qsub jobs in the following system:
Linux woody.ncl.res.in 2.6.32-220.13.1.el6.x86_64 #1 SMP Tue Apr 17 23:56:34 BST 2012 x86_64 x86_64 x86_64 GNU/Linux

* This code optimizes different geometries/configurations of the molecule
* New geometry/configuration is generated from previously optimized geometry
* Here, we vary bond length between two atoms and shift the moities by the increment in bond length
* This new molecule is submited for optimization by fixing positions of those two atoms
* The Process is repeatd for the optimized geometry
