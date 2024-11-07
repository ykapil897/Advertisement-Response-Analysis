# run_all.py
import subprocess
import os

# Check if ext_and_load.py has been run before
if not os.path.exists('/app/tmp/ext_and_load_ran.txt'):
    # Run ext_and_load.py
    subprocess.run(["python3", "ext_and_load.py"], check=True)
    # Create a flag file
    with open('has_run.txt', 'w') as f:
        f.write("This file indicates that ext_and_load.py has been run.")

# Run ld_gform_responses.py and clean_and_transform.py
subprocess.run(["python3", "ld_gform_responses.py"], check=True)
subprocess.run(["python3", "clean_and_transform.py"], check=True)
