import os
import xml.etree.ElementTree as Et

from coverage_template import REPO_COVERAGE_REPORT_TEMPLATE

XML_FILE = "full_report/coverage.xml"
PHABRICATOR_COMMENT = "phabricator-comment.txt"


# appending to the phabricator comments
def append_to_file(file_name, content):
    with open(file_name, "a") as file:
        file.write(content)


def generate_comment(results):
    """
    Generates a comment for the Buildkite UI containing overall coverage results.
    :param results: Dictionary containing coverage results.
    # :param repo_coverage: overall coverage percentage of the repo scripts.
    """

    append_to_file(PHABRICATOR_COMMENT, REPO_COVERAGE_REPORT_TEMPLATE.format(
        st_packages=results.get('st_packages'),
        st_files=results.get('st_classes'),
        st_lines=results.get('st_lines'),
        # repo_coverage=repo_coverage
    ))


def process_coverage(xml_file):
    """
    Processes coverage data from an XML file and generates a Buildkite UI comment.
    :param xml_file: Path to the XML file containing coverage data.
    """

    tree = Et.parse(xml_file)
    root = tree.getroot()

    t_lines = root.attrib["lines-valid"]
    c_lines = root.attrib["lines-covered"]
    r_lines = str(round(float(root.attrib["line-rate"]) * 100, 3))
    packages = root.findall("./packages/package")
    t_packages = c_packages = len(packages)
    t_classes = c_classes = 0
    # overall_coverage = 0

    for package in packages:
        if package.attrib["line-rate"] == "0":
            c_packages -= 1
        classes = package.findall("./classes/class")

        t_classes += len(classes)
        for cl in classes:
            file_coverage = round(float(cl.attrib["line-rate"]) * 100, 2)
            if file_coverage != 0:
                c_classes += 1
            # overall_coverage += file_coverage

    r_packages = round(c_packages * 100 / t_packages, 3)
    r_classes = round(c_classes * 100 / t_classes, 3)
    # overall_coverage_value = overall_coverage/t_classes
    # repo_coverage = "{:.2f}%".format(overall_coverage_value)

    results = {
        'st_packages': "{0}% [  {1}/{2}  ]".format(r_packages, c_packages, t_packages),
        'st_classes': "{0}% [  {1}/{2}  ]".format(r_classes, c_classes, t_classes),
        'st_lines': "{0}% [  {1}/{2}  ]".format(r_lines, c_lines, t_lines),
    }

    # writing the results as phabricator comment
    generate_comment(results)


# Main entry point of the coverage processing script.
def main():
    if os.path.exists(XML_FILE):
        process_coverage(XML_FILE)
    else:
        with open(PHABRICATOR_COMMENT, "w") as file:
            file.write(
                "\nCouldn't generate overall coverage report for the repo.\n")
            file.write(REPO_COVERAGE_REPORT_TEMPLATE.format(
                st_packages="",  # Leave empty to show no value
                st_files="",
                st_lines=""
            ))


if __name__ == "__main__":
    main()
