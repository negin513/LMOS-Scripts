def make_qsub(exe_name, np):
    qsub_script = (\
                    "#!/bin/bash\n"
                    "#$ -notify\n"
                    "#$ -M maryam-abdioskouei@uiowa.edu\n"
                    "#$ -m a\n"
                    "#$ -m abe\n"
                    "#$ -S /bin/bash\n"
                    "#$ -N lmos_ # Job Name\n"
                    "#$ -j y # combine stderr & stdout into stdout\n"
                    "#$ -o $JOB_NAME.o$JOB_ID # Name of the output file (eg. myMPI.oJobID)\n"
                    "#$ -pe 56cpn "+str(np)+" # Requests XX cores total using the OpenMPI parallel environment\n"
                    "#$ -V # Inherit the submission environment\n"
                    "#$ -q CGRER # Queue name\n"
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
		    "command='/opt/apps/openmpi/2.0.1_parallel_studio-2017.1/bin/mpirun -np "+str(np)+" '$path_run'real.exe'\n"
                    "echo $command\n"
                    "exec $command\n"
                    )
    batch_script = open('run_'+exe_name+'.sh', "wb")
    batch_script.write(qsub_script)
    batch_script.close()




