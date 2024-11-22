#!/bin/bash

set -o errexit

cd "$(dirname "$0")"

echo "Starting Java server!"
java -cp ~/.m2/repository/org/py4j/py4j/0.10.9.7/py4j-0.10.9.7.jar:../c4_sign/java_c4sign/target/java_c4sign-1.0-SNAPSHOT.jar com.cornellcollegecomputingclub.java_c4sign.App
