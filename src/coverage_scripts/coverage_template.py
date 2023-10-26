DIFF_COVERAGE_REPORT_TEMPLATE = """
**Diff Coverage Report**

<table>
    <tr>
        <th>Name</th>
        <th>Packages</th>
        <th>Files</th>
        <th>Lines</th>
    </tr>
    <tr>
        <td>Coverage Report</td>
        <td>{st_packages}</td>
        <td>{st_files}</td>
        <td>{st_lines}</td>
    </tr>
</table>

"""

FILE_COVERAGE_TABLE_TEMPLATE = """
<table>
    <tr>
        <th>File Name</th>
        <th>Coverage</th>
    </tr>
    {file_coverage_rows}
</table>
"""

REPO_COVERAGE_REPORT_TEMPLATE = """
**Repo Coverage Report**

<table>
    <tr>
        <th>Name</th>
        <th>Packages</th>
        <th>Files</th>
        <th>Lines</th>
    </tr>
    <tr>
        <td>Coverage Report</td>
        <td>{st_packages}</td>
        <td>{st_files}</td>
        <td>{st_lines}</td>
    </tr>
</table>
"""

WARNING_TEMPLATE = """
**Warning**: the following files have less than the threshold coverage!
{warning_files}
"""
