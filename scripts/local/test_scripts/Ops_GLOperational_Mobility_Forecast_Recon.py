from datetime import datetime
from tm1tests.reconciliation import Reconciliation

    
source_mdx = """WITH MEMBER [Account].[Ops PL - GAAP Contribution] AS [Account].[Ops P&L - GAAP Contribution]
    SELECT NON EMPTY
    {TM1SubsetToSet( [Month].[Month], 'Forecast Allocation Months', 'public' )}
    ON ROWS,
    NON EMPTY
    {[Account].[Ops PL - GAAP Contribution],[Account].[Completed Trips]}
    ON COLUMNS
FROM
    [GL Operational]
WHERE (
    [GL Operational].[Ops PL],
    [Version].[Forecast Excl Actuals],
    [Location].[Total Location Incl Discontinued],
    [Source].[Planning],
    [Rate Type].[USD],
    [Line of Business].[Mobility],
    [Department].[Total Department],
    [Product Type].[Total Mobility Product Type],
    [GL Operational Measure].[Amount]
)"""

target_mdx = """WITH MEMBER [Mobility Ops Metrics].[Ops PL - GAAP Contribution] AS [Mobility Ops Metrics].[GAAP Contribution]
    SELECT NON EMPTY
    {TM1SubsetToSet( [Period].[Period], 'Forecast Allocation Months', 'public' )}
    ON ROWS,
    NON EMPTY
    {[Mobility Ops Metrics].[Ops PL - GAAP Contribution],[Mobility Ops Metrics].[Completed Trips]}
    ON COLUMNS
FROM
    [Mobility]
WHERE (
    [Version].[Forecast Excl Actuals],
    [Source].[Planning],
    [Rate Type].[USD],
    [Line of Business].[Mobility],   
    [Department].[Total Department],
    [Product Type].[Total Mobility Product Type],
    [Mobility Features].[All Mobility Features],
    [Location].[Total Location Incl Discontinued],
    [Mobility Measure].[Amount]
)"""

class Mytest(Reconciliation):

    name = 'GL Operational vs Ops Mobility Forecast Data Recon'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['analytics', 'mdx', source_mdx]]
    target = [['ops', 'mdx', target_mdx]]
    schedule = None
    keyword = ['Mobility Forecast']
    threshold = ('ge', 1)


    def prepare(self):
        super().prepare()
        self.source[0][2] = source_mdx % ()
        self.target[0][2] = target_mdx % ()
