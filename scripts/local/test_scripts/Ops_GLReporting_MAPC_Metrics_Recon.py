
from datetime import datetime
from tm1tests.reconciliation import Reconciliation

source_mdx= """
SELECT NON EMPTY 
    {UNION({TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Period].[%s]}, ALL, RECURSIVE )}, 0)},{TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Period].[%s]}, ALL, RECURSIVE )}, 0)})}
    *{[Ops Metric].[New Riders],[Ops Metric].[Continuing Riders],[Ops Metric].[Active Drivers],[Ops Metric].[New Drivers],[Ops Metric].[Continuing Drivers],[Ops Metric].[Active Riders]}
ON ROWS,
NON EMPTY
    {[Line of Business].[2001],[Line of Business].[1001]}*{TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Location].[Total Location]}, ALL, RECURSIVE )}, 0)}
ON COLUMNS 
FROM 
    [Ops] 
WHERE 
    (
    [Version].[Actual],
    [Source].[FDS],
    [Rate Type].[USD],
    [Product Type].[Total Product Type],
    [Ops Measure].[Amount]
)"""

target_mdx = """
SELECT NON EMPTY 
    {UNION({TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Month].[%s]}, ALL, RECURSIVE )}, 0)},{TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Month].[%s]}, ALL, RECURSIVE )}, 0)})}
    *{[Account].[New Riders],[Account].[Continuing Riders],[Account].[Active Drivers],[Account].[New Drivers],[Account].[Continuing Drivers],[Account].[Active Riders]}    
ON ROWS,
NON EMPTY
    {[Line of Business].[2001],[Line of Business].[1001]}*{TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Location].[Total Location]}, ALL, RECURSIVE )}, 0)}
ON COLUMNS 
FROM 
    [GL Reporting] 
WHERE 
    (
    [Version].[Actual],
    [Source].[Total External Excl Sig Adj],
    [Department].[Total Department],
    [Rate Type].[USD],
    [Product Type].[Total Product Type],
    [GL Reporting Measure].[Amount]
)"""

class Mytest(Reconciliation):

    name = 'MAPC Metrics Ops VS GL Reporting Reconciliation'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', source_mdx]]
    target = [['analytics', 'mdx', target_mdx]]
    schedule = None
    keyword = ['']
    threshold = ('ge', 1)
    
    def prepare(self):
        super().prepare()
        now = datetime.now()
        curr_yr = now.year
        prev_yr = str(int(curr_yr) - 1)
        self.source[0][2] = source_mdx % (curr_yr,prev_yr)
        self.target[0][2] = target_mdx % (curr_yr,prev_yr)
