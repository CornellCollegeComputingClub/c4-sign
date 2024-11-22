import os
import subprocess
import sys
from pathlib import Path

red, green, normal = "\033[0;31m", "\033[0;32m", "\033[0m" #]]]

def print_error(text, stderr):
    if stderr is not None:
        if type(stderr) == str:
            print(stderr)
        else:
            print(stderr.decode())
    print(f"{red}{text}")
    print(f"{red}Contact us at c4@cornellcollege.edu or through our discord to help you with this error!")
    print(f"{red}Failed to start java server!{normal}")
    sys.exit(1)

script_directory = os.path.abspath(os.path.dirname(__file__))

os.chdir(Path(script_directory))

py4j_jar_location = Path.home() / ".m2" / "repository" / "org" / "py4j" / "py4j" / "0.10.9.7" / "py4j-0.10.9.7.jar"
java_c4sign_jar_location = Path.cwd() / ".." / "c4_sign" / "java_c4sign" / "target" / "java_c4sign-1.0-SNAPSHOT.jar"

try:
    result = subprocess.run([
        "java",
        "-cp",
        str(py4j_jar_location) + ":" + str(java_c4sign_jar_location),
        "com.cornellcollegecomputingclub.java_c4sign.App"
    ])

    if result.returncode != 0:
        print_error("Java server failed to start! Maybe you forgot to compile with tools/compile_java_project.py first?", result.stderr)
except FileNotFoundError as err:
    print_error("Java server failed to start! Maybe you need to make sure the Java JRE or JDK is installed?", str(err))
except subprocess.SubprocessError as err:
    print_error("Java server failed to start as a result of a subprocess error!", str(err))
