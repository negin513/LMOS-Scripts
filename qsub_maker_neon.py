def make_qsub(exe_name, np):
    qsub_script = (\
                    "#!/bin/bash\n"
                    "#$ -notify\n"
                    "#$ -M maryam-abdioskouei@uiowa.edu\n"
                    "#$ -m a\n"
                    "#$ -m abe\n"
                    "#$ -S /bin/bash\n"
                    "#$ -N wrf_lmos # Job Name\n"
                    "#$ -j y # combine stderr & stdout into stdout\n"
                    "#$ -o $JOB_NAME.o$JOB_ID # Name of the output file (eg. myMPI.oJobID)\n"
                    "#$ -pe 16cpn "+str(np)+" # Requests XX cores total using the OpenMPI parallel environment\n"
                    "#$ -V # Inherit the submission environment\n"
                    "##$ -q UI-HM # Queue name\n"
                    "#$ -q CGRER # Queue name\n"
                    "#$ -q all.q # Queue name\n"
                    "#$ -q UI,COE,all.q@@FISH\n"
                    "#$ -cwd # Start job in submission directory\n"
                    "source /opt/intel/bin/iccvars.sh intel64\n"
                    "source /opt/intel/bin/ifortvars.sh intel64\n"
                    "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/openmpi-intel/1.6.5/lib:/opt/intel/lib/intel64:/opt/hdf5/1.8.11/lib:/opt/netcdf4/4.2.1.1/lib\n"
                    "export JASPERINC=/usr/include\n"
                    "export JASPERLIB=/usr/lib\n"
                    "export NETCDF=/opt/netcdf4/4.2.1.1\n"
                    "ulimit -s unlimited\n"
                    "export KMP_STACKSIZE=512M\n"
                    "path_run='./'\n"
                    "cd $path_run\n"
                    "command='/opt/openmpi-intel/1.6.5/bin/mpirun -np "+str(np)+" '$path_run'wrf.exe'\n"
                    "echo $command\n"
                    "exec $command\n"
                    )
    batch_script = open(exe_name+'runner.sh', "wb")
    batch_script.write(qsub_script)
    batch_script.close()




