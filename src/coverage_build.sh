#!/bin/sh

echo $(pwd)
ls -lrt

## Get the current working directory.
#current_path=$(pwd)
#
## Update the PYTHONPATH environment variable.
#export PYTHONPATH=$PYTHONPATH:$current_path/scripts/local
#
## Print the updated PYTHONPATH environment variable.
#echo $PYTHONPATH

# Extract the 'enforce' value from the YAML file
enforce_value=$(grep 'enforce:' METADATA | awk '{print $2}')

if [ "$enforce_value" = "true" ]; then

  # Specify the directory name for test
  directory_name="report"
  cov_directory_name="full_report"

  # This ensures that a fresh report is created each time we run tests and generate the coverage
  # Check if the directory exists.
  if [ -d "$directory_name" ]; then
    # If the directory exists, delete it
    rm -r "$directory_name"
    echo "Deleted the '$directory_name' directory."
  fi

  if [ -d "$cov_directory_name" ]; then
    # If the directory exists, delete it
    rm -r "$cov_directory_name"
    echo "Deleted the '$cov_directory_name' directory."
  fi

  # Create the directory
  mkdir "$directory_name"
  echo "Created the '$directory_name' directory."

  mkdir "$cov_directory_name"
  echo "Created the '$cov_directory_name' directory."

#####################################################
# testing coverage for full repo
#####################################################
  TEST_DIR="scripts/tests"

  # Loop through each test file in the specified directory
  # shellcheck disable=SC2231
  for test_file in $TEST_DIR/test_*.py; do
    echo "Running tests in $test_file with pytest-cov"
    /var/uber/python37/bin/pytest --cov=scripts/ --cov-append --cov-report=term-missing "$test_file"
  done

  # After running all tests, generate the combined XML coverage report
  echo "Generating combined coverage report..."
  /var/uber/python37/bin/pytest --cov=scripts/ --cov-report=xml:./full_report/coverage.xml --cov-append

#####################################################
# testing coverage for full repo completed
#####################################################

  # getting the changed python files from the latest commit id
  /var/uber/python37/bin/python src/coverage_scripts/file_utils.py

  # running the unit tests using pytest and generating the xml coverage report for the scripts using pytest-cov
  /var/uber/python37/bin/pytest --cov=scripts/ --cov-report=xml:./report/coverage.xml scripts/test/

  # generating a summary for the test cases run
  /var/uber/python37/bin/pytest ./scripts/test/ -v --junitxml=report/report.xml

  # Removing the temporary test folder
  rm -rf scripts/test
  echo "Tests, coverage, and temporary folder cleanup completed"

  # creating directories for build artifacts
  mkdir -p build/coverage/
  mkdir -p build/full_coverage/
  mkdir -p build/comment/
  mkdir -p build/junit/

  # parsing the coverage and test reports to extract info and display onto Buildkite UI.
  /var/uber/python37/bin/python src/coverage_scripts/unit_test_summary.py
  /var/uber/python37/bin/python src/coverage_scripts/full_coverage_report.py
  /var/uber/python37/bin/python src/coverage_scripts/coverage_report.py


  # getting the build artifacts ready. They are specified under the artifact_paths in the my-udj.yaml file
  cp report/coverage.xml build/coverage/
  cp full_report/coverage.xml build/full_coverage/
  cp phabricator-comment.txt build/comment/
  cp report/report.xml build/junit/

else
    echo "Code coverage is disabled. Skipping coverage script execution."
fi
