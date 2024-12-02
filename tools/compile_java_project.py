import os
import subprocess
import sys
from pathlib import Path

red, green, normal = "\033[0;31m", "\033[0;32m", "\033[0m"

def print_error(text, stderr):
    if stderr is not None:
        if type(stderr) == str:
            print(stderr)
        else:
            print(stderr.decode())
    print(f"{red}{text}")
    print(f"{red}Contact us at c4@cornellcollege.edu or through our discord to help you with this error!")
    print(f"{red}Failed to compile!{normal}")
    sys.exit(1)

script_directory = os.path.abspath(os.path.dirname(__file__))

os.chdir(Path(script_directory) / ".." / "c4_sign" / "java_c4sign")


try:
    result = subprocess.run(["mvn", "--version"])
    result = subprocess.run(["mvn", "dependency:resolve"])
    if result.returncode != 0:
        print_error("Unable to resolve dependencies!", result.stderr)

    result = subprocess.run(["mvn", "package"])
    if result.returncode != 0:
        print_error("Compilation failed!", result.stderr)

except FileNotFoundError as err:
    print_error("Compilation failed! Maybe you need to make sure Maven is installed?", str(err))
except subprocess.SubprocessError as err:
    print_error("Compilation failed as a result of a subprocess error!", str(err))

print(f"{green}Successfully compiled!{normal}")
