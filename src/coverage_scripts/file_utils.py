import os
import pathlib
import shutil
import subprocess

import yaml

# Get the most recent commit ID
commit_id = subprocess.check_output(
    ['git', 'rev-parse', 'HEAD']).decode().strip()

# Get the list of changed Python files
py_files_output = subprocess.check_output(
    ['git', 'diff', '--name-status', f'{commit_id}^..{commit_id}']).decode().strip()

# List to store modified and created Python files
changed_py_files = []

with open('coverage_metadata.yaml', 'r') as yaml_file:
    coverage_data = yaml.safe_load(yaml_file)

repo_name = list(coverage_data.keys())[0]
coverage_dict = coverage_data[repo_name]

for line in py_files_output.split('\n'):
    status, file_path = line.split(maxsplit=1)
    if file_path.endswith('.py') and 'scripts/' in file_path:
        if status.startswith('M') or status.startswith('A'):
            changed_py_files.append(file_path)
        elif status.startswith('D'):
            # remove from coverage_metadata if file is deleted.
            base_name = os.path.basename(file_path)
            coverage_dict.pop(base_name, None)
        elif status.startswith('R'):
            old_path, new_path = file_path.split(maxsplit=1)
            old_base_name = os.path.basename(old_path)
            new_base_name = os.path.basename(new_path)

            changed_py_files.append(new_path)
            coverage_dict[new_base_name] = coverage_dict.pop(old_base_name)

# Write the updated data back to the YAML file
with open('coverage_metadata.yaml', 'w') as yaml_file:
    yaml.dump(coverage_data, yaml_file, default_flow_style=False)

# Define paths
test_folder_path = 'scripts/tests'
temp_test_folder_path = 'scripts/test'

os.makedirs(temp_test_folder_path, exist_ok=True)
open(os.path.join(temp_test_folder_path, '__init__.py'), 'w').close()

# list of scripts in the diff to include for coverage.
files_to_include = []

# loop through the changed python files
for py_file in changed_py_files:
    # Check if it is a test file
    if os.path.basename(py_file).startswith('test_'):
        shutil.copy(py_file, temp_test_folder_path)

        # Extract the base name without 'test_' prefix and add file to the list
        base_name = os.path.basename(py_file)[5:]
        # corresponding_file_path = os.path.join('scripts/local', base_name)

        files_to_include.append(base_name)

    else:
        # add the file to the list
        base_name = os.path.basename(py_file)
        files_to_include.append(base_name)

        corresponding_test_file_path = os.path.join(
            test_folder_path, 'test_' + base_name)
        if os.path.exists(corresponding_test_file_path):
            shutil.copy(corresponding_test_file_path, temp_test_folder_path)

print(files_to_include)

files_to_omit = []

scripts = pathlib.Path("scripts")
scripts.rglob("*")
entries = list(scripts.rglob("*"))

for entry in entries:
    base_name = entry.name

    if entry.is_file() and not base_name.startswith('test'):
        if base_name not in files_to_include:
            files_to_omit.append(str(entry))

    elif entry.is_dir() and base_name.startswith('test'):
        files_to_omit.append(f"{entry}/*")

# print(files_to_omit)

# Write the omit string to the .coveragerc file
with open('.coveragerc', 'w') as coveragerc_file:
    coveragerc_file.write("[run]" + chr(10) + "omit = " + chr(10))
    for file in files_to_omit:
        coveragerc_file.write("    " + file + chr(10))
