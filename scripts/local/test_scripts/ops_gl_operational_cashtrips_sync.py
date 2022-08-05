
from datetime import datetime
from tm1tests.reconciliation import Reconciliation

source_mdx = """SELECT NON EMPTY
    {[Ops Metric].[Cash Trips]}
    ON ROWS,
    {TM1FILTERBYLEVEL({TM1DRILLDOWNMEMBER({[Period].[%s]},ALL,RECURSIVE)},0)}
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
    {[Account].[Cash Trips]}
    ON ROWS,
    {TM1FILTERBYLEVEL({TM1DRILLDOWNMEMBER({[Month].[%s]},ALL,RECURSIVE)},0)}
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

    name = 'GL Operational Cash Trips Actuals Recon'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', source_mdx]]
    target = [['analytics', 'mdx', target_mdx]]
    threshold = ('ge', 1)

    def prepare(self):
        super().prepare()
        session = self.apps_sessions['analytics']
        current_actual_month = session.cubes.cells.get_value('System Info','Current Month, String')
        year = current_actual_month[:4]        
        self.source[0][2] =  source_mdx % (year)
        self.target[0][2] =  target_mdx % (year)
