
from datetime import datetime
from tm1tests.reconciliation import Reconciliation

source_mdx = """SELECT NON EMPTY 
    {[Ops Metric].[Completed Trips]} 
ON ROWS,
    {[Period].[%s]}
ON COLUMNS 
FROM 
    [Ops] 
WHERE 
    (
    [Version].[Actual], 
    [Location].[Total Location Incl Discontinued],
    [Source].[Ops Incl Post Reported Adjs],
    [Rate Type].[USD],
    [Line of Business].[Total Line of Business],
    [Product Type].[Total Product Type],
    [Ops Measure].[Amount]
    )"""

target_mdx = """SELECT NON EMPTY 
    {[Account].[Completed Trips]}
ON ROWS,
     {[Month].[%s]}
ON COLUMNS 
FROM 
    [GL Operational] 
WHERE 
    (
    [Version].[Actual], 
    [Location].[Total Location Incl Discontinued],
    [Source].[Ops Incl Post Reported Adjs],
    [Line of Business].[Total Line of Business],
    [Rate Type].[USD],
    [Department].[Total Department],
    [Product Type].[Total Product Type],
    [GL Operational Measure].[Amount],
    [GL Operational].[Completed Trips]
    )"""

class Mytest(Reconciliation):

    name = 'Ops - Analytics Completed Trips Recon'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', source_mdx]]
    target = [['analytics', 'mdx', target_mdx]]
    schedule = None
    threshold = ('ge', 1)
    keyword = ['ops']
    
    def prepare(self):
        super().prepare()
        session = self.apps_sessions['ops']
        current_actual_month=session.cubes.cells.get_value('Admin Playbook','Oracle Sync, Current Actual Month')
        self.source[0][2] = source_mdx %(current_actual_month)
        self.target[0][2] = target_mdx %(current_actual_month)
