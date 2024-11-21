#!/bin/bash

set -o errexit

# Set current working directory to that of the script. (c4-sign/bin)
cd "$(dirname "$0")"

# Set current working directory to the java project.
cd ../c4_sign/java_c4sign/

# Compile java project
mvn dependency:resolve
mvn package

echo -e "\033[1;32m Succesfully compiled!\033[0m"
