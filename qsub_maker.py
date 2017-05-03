import os
import subprocess
import argparse
import glob
import re

def submit_job(exe_name, np, j_ID, q_ID):
    qsub_script = (\
                    "#!/bin/bash\n"
                    "#$ -notify\n"
                    "#$ -M negin-sobhani@uiowa.edu\n"
                    "#$ -m a\n"
                    "#$ -m abe\n"
                    "#$ -S /bin/bash\n"
                    "#$ -N "+exe_name+" # Job Name\n"
                    "#$ -j y # combine stderr & stdout into stdout\n"
                    "#$ -o $JOB_NAME.o$JOB_ID # Name of the output file (eg. myMPI.oJobID)\n"
                    "#$ -pe 56cpn "+str(np)+" # Requests XX cores total using the OpenMPI parallel environment\n"
                    "#$ -V # Inherit the submission environment\n"
                    "#$ -q "+ q_ID +"# Queue name\n"
                    "#$ -cwd # Start job in submission directory\n"
		    "source /opt/apps/parallel_studio/2017.1/bin/iccvars.sh intel64\n"
		    "source /opt/apps/parallel_studio/2017.1/bin/ifortvars.sh intel64\n"
		    "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/apps/openmpi/2.0.1_parallel_studio-2017.1/bin/mpirun:/opt/apps/hdf5/1.8.18_parallel_studio-2017.1/lib:/opt/apps/netcdf-fortran/4.4.4_parallel_studio-2017.1/lib\n"

                    "export JASPERINC=/opt/apps/jasper/1.900.1/include\n"
                    "export JASPERLIB=/opt/apps/jasper/1.900.1/lib\n"
                    "export NETCDF=/opt/apps/netcdf-fortran/4.4.4_parallel_studio-2017.1\n"
                    "ulimit -s unlimited\n"
                    "export KMP_STACKSIZE=512M\n"
                    "path_run='./'\n"
                    "cd $path_run\n"
                    "command='/opt/apps/openmpi/2.0.1_parallel_studio-2017.1/bin/mpirun -np "+str(np)+"' $path_run'"+ exe_name +"'\n"
		    #"command='/opt/apps/openmpi/2.0.1_parallel_studio-2017.1/bin/mpirun -np "+str(np)+ " ./"+exe_name+"'\n"
                    "echo $command\n"
                    "exec $command\n"
                    )
    qsub_name = 'run_'+exe_name+'.job'
    batch_script = open(qsub_name, "wb")
    batch_script.write(qsub_script)
    batch_script.close()
   
    if j_ID ==0:
    	cmd    = ('qsub '+ qsub_name)
    else:
	cmd    = ('qsub -hold_jid '+str(j_ID)+' '+ qsub_name)
    print '=========================================================='
    print (qsub_script)
    print cmd
    qsub   = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = qsub.communicate()
    ##print [qsub.returncode, errors, output]
    if qsub.returncode or errors:
        print 'something went wrong while submitting the job...'
        jobID = ysqID = None
    else:
        qsub_out = re.findall(r'\d+',output)
	jobID    = qsub_out[0]
    print '=========================================================='
    return (jobID)
