#!/bin/sh

echo $(pwd)
ls -lrt
# Extract the 'enforce' value from the YAML file
enforce_value=$(grep 'enforce:' METADATA | awk '{print $2}')

if [ "$enforce_value" = "true" ]; then

  # Specify the directory name for test
  directory_name="report"

  # This ensures that a fresh report is created each time we run tests and generate the coverage
  # Check if the directory exists.
  if [ -d "$directory_name" ]; then
    # If the directory exists, delete it
    rm -r "$directory_name"
    echo "Deleted the '$directory_name' directory."
  fi

  # Create the directory
  mkdir "$directory_name"
  echo "Created the '$directory_name' directory."

  # installing the coverage and pytest tools for running the test and coverage
  # /work/.local/bin/pip3.6 install pytest-cov coverage pytest pyyaml

  # /work/.local/bin/pip3.6 install boto3

  # getting the changed python files from the latest commit id
  /var/uber/python37/bin/python src/coverage_scripts/file_utils.py

  /var/uber/python37/bin/pytest --cov=scripts/ --cov-report=xml:./report/coverage.xml scripts/test/

  # generating a summary for the test cases run
  /var/uber/python37/bin/pytest ./scripts/test/ -v --junitxml=report/report.xml

  # Removing the temporary test folder
  rm -rf scripts/test
  echo "Tests, coverage, and temporary folder cleanup completed"

  # creating directories for build artifacts
  mkdir -p build/coverage/
  mkdir -p build/comment/
  mkdir -p build/junit/

  # parsing the coverage and test reports to extract info and display onto Buildkite UI.
  /var/uber/python37/bin/python src/coverage_scripts/unit_test_summary.py
  /var/uber/python37/bin/python src/coverage_scripts/coverage_report.py

  # getting the build artifacts ready. They are specified under the artifact_paths in the my-udj.yaml file
  cp report/coverage.xml build/coverage/
  cp phabricator-comment.txt build/comment/
  cp report/report.xml build/junit/

else
    echo "Code coverage is disabled. Skipping coverage script execution."
fi
