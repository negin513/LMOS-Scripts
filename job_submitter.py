def submit_job(script):
    cmd    = ('qsub'+ script)
    qsub   = subprocess.Popen(job_run, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = qsub.communicate()
    print [bsub.returncode, errors, output]
    if qsub.returncode or errors:
        print 'something went wrong while submitting the job...'
        jobID = ysqID = None
    else:
        bsub_out = re.findall(r'\<([^<]*)\>',output)
        jobID    = qsub_out[0]
        ysqID    = qsub_out[1]
    return (jobID, ysqID)
