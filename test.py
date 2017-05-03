import subprocess
failing_command='ls non_existent_dir'

try:
    subprocess.check_output(failing_command, shell=True, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError as e:
    ret =   e.returncode 
    if ret in (1, 2):
        print("the command failed")
    elif ret in (3, 4, 5):
        print("the command failed very much")
