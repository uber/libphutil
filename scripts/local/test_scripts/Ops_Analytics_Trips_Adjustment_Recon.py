from datetime import datetime
from tm1tests.reconciliation import Reconciliation

source_mdx = """SELECT NON EMPTY 
    {[Ops Metric].[Completed Trips]}
ON ROWS,
NON EMPTY
    {[Period].[%s]} * %s
ON COLUMNS 
FROM 
    [Ops] 
WHERE 
    (
    [Version].[Actual], 
    [Location].[Total Location Incl Discontinued],
    [Source].[Ops Adjustment],
    [Line of Business].[Total Line of Business],
    [Product Type].[Total Product Type],
    [Ops Measure].[Amount]
)"""


target_mdx = """SELECT NON EMPTY 
    {[Account].[Completed Trips]}
ON ROWS,
NON EMPTY
     {[Month].[%s]} * %s
ON COLUMNS 
FROM 
    [GL Reporting] 
WHERE 
    (
    [Version].[Actual], 
    [Location].[Total Location Incl Discontinued],
    [Source].[Ops Adjustment],
    [Department].[Total Department],
    [Line of Business].[Total Line of Business],
    [Product Type].[Total Product Type],
    [GL Reporting Measure].[Amount]
    )"""

class Mytest(Reconciliation):

    name = 'Ops GL Reporting Completed Trips Adjustment Recon'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', source_mdx]]
    target = [['analytics', 'mdx', target_mdx]]
    schedule = '0 1,4,7,10,13,16,17,20,23 * * *'
    threshold = ('ge', 1)
    keyword = ['tripsadjustment']

    def prepare(self):
        super().prepare()
        now = datetime.now()
        curr_yr = now.year if now.month > 1 else now.year - 1
        FX = "{TM1SORT( {TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {TM1FILTERBYPATTERN( {TM1SUBSETALL( [Rate Type] )}, 'FX Rates')}, ALL, RECURSIVE )}, 0)}, ASC)}"
        self.source[0][2] = source_mdx %(curr_yr,FX)
        self.target[0][2] = target_mdx %(curr_yr,FX)