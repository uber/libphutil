from datetime import datetime
from tm1tests.reconciliation import Reconciliation

source_mdx = """SELECT NON EMPTY
    {[Ops Metric].[Cash Gross Bookings]}
    ON ROWS,
    {%s}
    ON COLUMNS
FROM
    [Ops]
WHERE (
    [Version].[Actual],
    [Source].[FDS Incl. Adj],
    [Line of Business].[Total Line of Business],
    [Location].[Total Location Incl Discontinued],
    [Product Type].[Total Product Type],
    [Rate Type].[USD],
    [Ops Measure].[Amount]
)
"""

target_mdx = """SELECT NON EMPTY
    {[Account].[Cash Gross Bookings]}
    ON ROWS,
    {%s}
    ON COLUMNS
FROM
    [GL Operational]
WHERE (
    [Version].[Actual],
    [Source].[OPS],
    [Rate Type].[USD],
    [Line of Business].[Total Line of Business],
    [Location].[Total Location Incl Discontinued],
    [Department].[Total Department],
    [Product Type].[Total Product Type],
    [GL Operational].[GL Operational Stat Accounts],
    [GL Operational Measure].[Amount]
)
"""

class Mytest(Reconciliation):

    name = 'GL Operational Cash Gross Bookings Actuals Recon'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', source_mdx]]
    target = [['analytics', 'mdx', target_mdx]]
    schedule = '0 10 * * *'
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
