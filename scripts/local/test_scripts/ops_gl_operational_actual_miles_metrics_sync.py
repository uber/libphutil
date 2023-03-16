
from datetime import datetime
from tm1tests.reconciliation import Reconciliation

source_mdx = """SELECT NON EMPTY
    {UNION({TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Ops Metric].[Total Mileage (Mileage Type)]}, ALL, RECURSIVE )}, 0)},{[Ops Metric].[Completed Trips - Rides Insurance CM]})}
    ON ROWS,
    {%s}
    ON COLUMNS
FROM
    [Ops]
WHERE (
    [Version].[Actual],
    [Source].[Total Source],
    [Line of Business].[Total Line of Business],
    [Location].[Total Location Incl Discontinued],
    [Product Type].[Total Product Type],
    [Rate Type].[FX Rates],
    [Ops Measure].[Amount]
)
"""

target_mdx = """SELECT NON EMPTY
    {UNION({TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Account].[Total Mileage (Mileage Type)]}, ALL, RECURSIVE )}, 0)},{[Account].[Completed Trips - Rides Insurance CM]})}
    ON ROWS,
    {%s}
    ON COLUMNS
FROM
    [GL Operational]
WHERE (
    [Version].[Actual],
    [Source].[Total External Excl Sig Adj],
    [Rate Type].[FX Rates],
    [Line of Business].[Total Line of Business],
    [Location].[Total Location Incl Discontinued],
    [Department].[Total Department],
    [Product Type].[Total Product Type],
    [GL Operational].[Ops PL],
    [GL Operational Measure].[Amount]
)
"""

class Mytest(Reconciliation):

    name = 'Ops Vs GL Operational - Actual Miles Metrics Recon'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', source_mdx]]
    target = [['analytics', 'mdx', target_mdx]]
    schedule = '15 16 * * *'
    threshold = ('ge', 1)

    def prepare(self):
        super().prepare()
        now = datetime.now()
        curr_year = str(now.year)
        prev_year = str(int(curr_year) - 1)
        prev_month = str(int(now.month) - 1)
        if prev_month == '0':
           curr_year = prev_year
           prev_month = '12'
        if len(prev_month) == 1:
           prev_month = '0'+prev_month
        sCurrentMonth = curr_year+'-'+prev_month
        sMonth = "[Month].[{}-01]:[Month].[{}]".format(prev_year, sCurrentMonth)
        sPeriod = "[Period].[{}-01]:[Period].[{}]".format(prev_year, sCurrentMonth)
        self.source[0][2] =  source_mdx % (sPeriod)
        self.target[0][2] =  target_mdx % (sMonth)
