import os
import xml.etree.ElementTree as ET

# Path to the XML file
xml_file_path = "report/report.xml"

try:
    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Extract relevant attributes from the testsuite element
    testsuite = root.find(".//testsuite")
    tests = int(testsuite.attrib.get("tests", 0))
    failures = int(testsuite.attrib.get("failures", 0))
    skipped = int(testsuite.attrib.get("skipped", 0))
    errors = int(testsuite.attrib.get("errors", 0))
    time_seconds = round(float(testsuite.attrib.get("time", 0)), 3)

    # Generate and print the test summary string
    test_summary = "Test Summary: {} Passed, {} Failed, {} skipped, {} errors in {} seconds".format(
        tests - failures - skipped - errors, failures, skipped, errors, time_seconds
    )
    print(test_summary)

    job_link = 'https://buildkite.com/uber/generic-udj/builds/' + \
        os.getenv('BUILDKITE_BUILD_NUMBER')

    # Write the test summary to a file
    with open('phabricator-comment.txt', 'w') as comment_file:
        comment_file.write(
            f"More information can be found [here]({job_link}).\n")
        comment_file.write(test_summary)
        if failures > 0:
            comment_file.write("\n\nWarning: There are test failures!")

except Exception as e:
    print("Error:", str(e))
