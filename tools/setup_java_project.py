import os
import subprocess
import sys
import re
from pathlib import Path

red, green, normal = "\033[0;31m", "\033[0;32m", "\033[0m" #]]]

supported_py4j_version = "0.10.9.7"

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

try:
    result = subprocess.run(["mvn", "--version"])

    result = subprocess.run(["python", "-m", "pip", "show", "-f", "py4j"], capture_output=True, text=True)

    if result.returncode != 0 or result.stdout is None:
        print_error("Failed to setup Java project! Maybe you need to make sure py4j is installed?", result.stderr)

    lines = result.stdout.split("\n")

    py4j_location = None
    py4j_jar_location = None

    for line in lines:
        if line.startswith("Location:"):
            py4j_location = line.split(" ")[-1]
        if line.endswith(".jar"):
            py4j_jar_location = line.split(" ")[-1]

        if py4j_location is not None and py4j_jar_location is not None:
            break

    py4j_jar_name = Path(py4j_jar_location).name
    py4j_jar_version = re.search(r"(?<=py4j).+(?=\.jar)", Path(py4j_jar_location).name).group()
    
    os.chdir(Path(py4j_location))
    os.chdir(Path(py4j_jar_location).resolve().parent)

    print("Py4J jar found: ", Path(os.getcwd()) / py4j_jar_name)

    if py4j_jar_version != supported_py4j_version:
        print_error(f"Py4J version {py4j_jar_version} does not match {supported_py4j_version}! Please let us know we should update our code!", None)

    result = subprocess.run([
            "mvn",
            "install:install-file",
            f"-Dfile={py4j_jar_name}",
            "-DgroupId=org.py4j",
            "-DartifactId=py4j",
            f"-Dversion={supported_py4j_version}",
            "-Dpackaging=jar",
            "-DgeneratePom=true"
        ])

    if result.returncode != 0:
        print_error("Failed to install py4j in the maven repository...", result.stderr)

    print(f"{green}Successfully setup Maven project!{normal}")

except FileNotFoundError as err:
    print_error("Failed to setup Java project! Maybe you need to make sure Maven is installed?", str(err))
except subprocess.SubprocessError as err:
    print_error("Failed to setup Java project as a result of a subprocess error!", str(err))
