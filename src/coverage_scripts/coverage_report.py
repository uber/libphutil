import os
import xml.etree.ElementTree as Et

import yaml
from coverage_template import DIFF_COVERAGE_REPORT_TEMPLATE
from coverage_template import FILE_COVERAGE_TABLE_TEMPLATE
from coverage_template import WARNING_TEMPLATE

METADATA = 'coverage_metadata.yaml'
CONFIG = 'METADATA'
XML_FILE = "report/coverage.xml"
PHABRICATOR_COMMENT = "phabricator-comment.txt"


# appending to the phabricator comments
def append_to_file(file_name, content):
    with open(file_name, "a") as file:
        file.write(content)


def generate_comment(
        results,
        # overall_coverage_report,
        warning_files=None,
        file_coverage_report=None
):
    """
    Generates a comment for the Buildkite UI containing coverage results and warnings.

    :param results: Dictionary containing coverage results.
    :param overall_coverage_report: Overall coverage percentage.
    :param warning_files: List of files with coverage warnings.
    :param file_coverage_report: Dictionary containing per-file coverage data.
    """

    if warning_files:   # if there exist certain files that do not meet the coverage requirement.
        append_to_file(PHABRICATOR_COMMENT, "\n" +
                       WARNING_TEMPLATE.format(warning_files="\n".join(warning_files)))

    append_to_file(PHABRICATOR_COMMENT, DIFF_COVERAGE_REPORT_TEMPLATE.format(
        st_packages=results.get('st_packages'),
        st_files=results.get('st_classes'),
        st_lines=results.get('st_lines')
    ))

    file_coverage_rows = ""
    for filename, coverage in file_coverage_report.items():
        file_coverage_rows += f"<tr><td>{filename}</td><td>{coverage}</td></tr>\n"

    append_to_file(PHABRICATOR_COMMENT,
                   FILE_COVERAGE_TABLE_TEMPLATE.format(file_coverage_rows=file_coverage_rows))

    # append_to_file(PHABRICATOR_COMMENT, REPO_COVERAGE_REPORT_TEMPLATE.format(
    #     repo_name=overall_coverage_report[0],
    #     repo_coverage=overall_coverage_report[1]
    # ))


# loads data from a YAML file.
def load_yaml_file(file_name):
    with open(file_name, 'r') as yaml_file:
        return yaml.safe_load(yaml_file)


# writes data to a YAML file.
def write_yaml_file(file_name, data):
    with open(file_name, 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)


def load_coverage_configuration(file_name):
    with open(file_name, 'r') as yaml_file:
        documents = list(yaml.safe_load_all(yaml_file))
        return documents[2]


def update_coverage_metadata(coverage_dict, filename, file_coverage, file_coverage_report):
    """
    Updates the coverage metadata with file coverage information.

    :param coverage_dict: Dictionary containing coverage metadata.
    :param filename: Name of the file to update coverage for.
    :param file_coverage: Coverage percentage for the file.
    :param file_coverage_report: Dictionary containing file names with their coverage percentage.
    """

    format_file_coverage = "{:.2f}%".format(file_coverage)
    coverage_dict[filename] = format_file_coverage
    file_coverage_report[filename] = format_file_coverage
    return


def calculate_overall_coverage(coverage_data, repo_name):
    """
    Calculates the overall coverage percentage.
    :param coverage_data: Dictionary containing coverage data.
    :param repo_name: Name of the application (taken from the coverage_metadata file).
    :return (string): Overall coverage percentage.
    """

    coverage_values = list(coverage_data[repo_name].values())
    percentage_values = [float(value.strip('%')) for value in coverage_values]
    overall_coverage = sum(percentage_values) / len(percentage_values)
    overall_coverage_percentage = "{:.2f}%".format(overall_coverage)

    return repo_name, overall_coverage_percentage


def warning_check(filename, coverage_dict, threshold_data, file_coverage):
    """
    Checks if a coverage warning should be generated for a file.

    Args:
        filename: Name of the file to check.
        coverage_dict: Dictionary containing coverage data.
        threshold_data: Dictionary containing coverage threshold data.
        file_coverage: Coverage percentage for the file.

    Returns: True if a warning should be generated, False otherwise.
    """

    coverage_threshold = threshold_data['code-quality']['coverage']
    if filename in coverage_dict:
        if float(coverage_dict[filename].strip('%')) > file_coverage:
            return True
    elif file_coverage < coverage_threshold['min']:
        return True
    return False


def parse_coverage(xml_file):
    """
    Parses coverage data from an XML file.
    :param xml_file: Path to the XML file containing coverage data.
    :return: Dictionary containing parsed coverage results.
    """

    tree = Et.parse(xml_file)
    root = tree.getroot()

    t_lines = root.attrib["lines-valid"]
    c_lines = root.attrib["lines-covered"]
    r_lines = str(round(float(root.attrib["line-rate"]) * 100, 3))
    packages = root.findall("./packages/package")
    t_packages = c_packages = len(packages)
    t_classes = c_classes = r_packages = r_classes = 0
    classes = root.findall(".//classes/class")

    for package in packages:
        if package.attrib["line-rate"] == "0":
            c_packages -= 1
        classes = package.findall("./classes/class")
        t_classes += len(classes)
        for cl in classes:
            rate = float(cl.attrib['line-rate'])
            if rate != 0:
                c_classes += 1

    r_packages = round(c_packages * 100 / t_packages, 3)
    r_classes = round(c_classes * 100 / t_classes, 3)

    return {
        'st_packages': "{0}% [  {1}/{2}  ]".format(r_packages, c_packages, t_packages),
        'st_classes': "{0}% [  {1}/{2}  ]".format(r_classes, c_classes, t_classes),
        'st_lines': "{0}% [  {1}/{2}  ]".format(r_lines, c_lines, t_lines),
        'classes': classes
    }


def process_coverage(xml_file):
    """
    Processes coverage data from an XML file and generates a Buildkite UI comment.
    :param xml_file: Path to the XML file containing coverage data.
    """

    results = parse_coverage(xml_file)
    coverage_data = load_yaml_file(METADATA)

    repo_name = list(coverage_data.keys())[0]
    coverage_dict = coverage_data[repo_name]
    threshold_data = load_coverage_configuration(CONFIG)

    warning_files = []
    file_coverage_report = {}

    # fetching each file name and its coverage percentage
    for class_element in results['classes']:
        filename = class_element.attrib["name"]
        file_coverage = round(
            float(class_element.attrib["line-rate"]) * 100, 2)

        if warning_check(filename, coverage_dict, threshold_data, file_coverage):
            warning_files.append(filename)

        # updating the metadata
        update_coverage_metadata(
            coverage_dict, filename, file_coverage, file_coverage_report)

    write_yaml_file(METADATA, coverage_data)

    overall_coverage_report = calculate_overall_coverage(
        coverage_data, repo_name)
    # to view in the logs
    print(overall_coverage_report)

    # writing the results as phabricator comment
    generate_comment(
        results,
        # overall_coverage_report,
        warning_files,
        file_coverage_report
    )


# Main entry point of the coverage processing script.
def main():
    if os.path.exists(XML_FILE):
        process_coverage(XML_FILE)
    else:
        with open(PHABRICATOR_COMMENT, "w") as file:
            file.write("\nNo test targets exist for the changed files.\n")
            file.write(DIFF_COVERAGE_REPORT_TEMPLATE.format(
                st_packages="",  # Leave empty to show no value
                st_files="",
                st_lines=""
            ))


if __name__ == "__main__":
    main()
