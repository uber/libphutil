
from datetime import datetime
from tm1tests.reconciliation import Reconciliation

    
source_mdx = """SELECT NON EMPTY
    {[Month].[%s]}
    ON ROWS,
    NON EMPTY
    {[GL Operational].[Gross Bookings],[GL Operational].[Net Effective Take Rate (NETR)],[GL Operational].[Variable Costs],[GL Operational].[Variable Contribution],
    [GL Operational].[Operating Expenses],[GL Operational].[Adj EBITDA]}
    ON COLUMNS
FROM
    [GL Operational]
WHERE (
    [Account].[Ops P&L],
    [Version].[Actual],
    [Location].[Total Location Incl Discontinued],
    [Source].[Total External Excl Sig Adj],
    [Rate Type].[USD],
    [Line of Business].[Mobility],
    [Department].[Total Org],
    [Product Type].[Total Product Type],
    [GL Operational Measure].[Amount]
)"""

target_mdx = """SELECT NON EMPTY
    {[Period].[%s]}
    ON ROWS,
    NON EMPTY
    {[Mobility Ops Metrics].[Gross Bookings],[Mobility Ops Metrics].[Net Effective Take Rate (NETR)],[Mobility Ops Metrics].[Variable Costs],[Mobility Ops Metrics].[Variable Contribution],
    [Mobility Ops Metrics].[Operating Expenses],[Mobility Ops Metrics].[Adj EBITDA]}
    ON COLUMNS
FROM
    [Mobility]
WHERE (
    [Version].[Actual],
    [Source].[Oracle],
    [Rate Type].[USD],
    [Line of Business].[Mobility],   
    [Department].[Total Org],
    [Product Type].[Total Product Type],
    [Mobility Features].[All Mobility Features],
    [Location].[Total Location Incl Discontinued],
    [Mobility Measure].[Amount]
)"""

class Mytest(Reconciliation):

    name = 'GL Operational vs Ops Mobility Oracle Data Recon'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['analytics', 'mdx', source_mdx]]
    target = [['ops', 'mdx', target_mdx]]
    schedule = None
    keyword = ['Mobility']
    threshold = ('ge', 1)


    def prepare(self):
        super().prepare()
        session = self.apps_sessions['analytics']
        curr_month = session.cubes.cells.get_value('System Info', 'Current Month, String')
        self.source[0][2] = source_mdx % (curr_month)
        self.target[0][2] = target_mdx % (curr_month)  
