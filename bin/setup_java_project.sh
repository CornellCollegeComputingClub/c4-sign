#!/bin/bash

set -o errexit

mvn --version

# Set current directory to the directory containing this script.
cd "$(dirname "$0")"

py4j_location=$(python -m pip show -f py4j | grep Location: | cut -d' ' -f2)
echo "Py4j found at" $py4j_location

py4j_jar_location=$(python -m pip show -f py4j | grep jar | awk '{$1=$1};1')
echo "Relative to that directory, found py4j jar at" $py4j_jar_location

cd $py4j_location
cd $(dirname $py4j_jar_location)

jar_name=$(basename $py4j_jar_location)

jar_version=$(echo $jar_name | grep -oP "(?<=py4j).+(?=\.jar)")

echo "Jar name:" $jar_name
echo "Jar version:" $jar_version

if [ "$jar_version" = "0.10.9.7" ]; then
    echo "Jar version is valid!"
else
    echo -e "\033[0;31mJar version is invalid!"
    echo "Required version is 0.10.9.7"
    echo "Contact C4 by emailing us at c4@cornellcollege.edu, or through our Discord in the LED sign channel!"
    echo "Let us know that we should update our packages :)"
    exit 1
fi

mvn install:install-file -Dfile="$jar_name" -DgroupId=org.py4j -DartifactId=py4j -Dversion=0.10.9.7 -Dpackaging=jar -DgeneratePom=true

echo -e "\033[0;32mSuccessfully set up the java project!"
