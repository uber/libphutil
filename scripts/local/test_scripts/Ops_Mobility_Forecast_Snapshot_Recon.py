from datetime import datetime
from tm1tests.reconciliation import Reconciliation

    
source_mdx = """SELECT NON EMPTY
    {{TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Period].[%s]}, ALL, RECURSIVE )}, 0)} + {TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Period].[%s]}, ALL, RECURSIVE )}, 0)}}
    ON ROWS,
    NON EMPTY
    {[Mobility Ops Metrics].[Gross Bookings],[Mobility Ops Metrics].[Pricing, Incentives, and Other Revenue],[Mobility Ops Metrics].[Net Effective Take Rate (NETR)],[Mobility Ops Metrics].[Variable Costs],[Mobility Ops Metrics].[Variable Contribution],
    [Mobility Ops Metrics].[Operating Expenses],[Mobility Ops Metrics].[Adj EBITDA]}
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

target_mdx = """SELECT NON EMPTY
    {{TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Period].[%s]}, ALL, RECURSIVE )}, 0)} + {TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Period].[%s]}, ALL, RECURSIVE )}, 0)}}
    ON ROWS,
    NON EMPTY
    {[Mobility Ops Metrics].[Gross Bookings],[Mobility Ops Metrics].[Pricing, Incentives, and Other Revenue],[Mobility Ops Metrics].[Net Effective Take Rate (NETR)],[Mobility Ops Metrics].[Variable Costs],[Mobility Ops Metrics].[Variable Contribution],
    [Mobility Ops Metrics].[Operating Expenses],[Mobility Ops Metrics].[Adj EBITDA]}
    ON COLUMNS
FROM
    [Mobility Snapshot]
WHERE (
    [Version].[Forecast Excl Actuals],
    [Source].[Product PL],
    [Rate Type].[USD],
    [Line of Business].[Mobility],   
    [Department].[Total Department],
    [Product Type].[Total Mobility Product Type],
    [Mobility Features].[All Mobility Features],
    [Location].[Total Location Incl Discontinued],
    [Mobility Measure].[Amount]
)"""

class Mytest(Reconciliation):

    name = 'Mobility Forecast Snapshot Data Recon'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', source_mdx]]
    target = [['ops', 'mdx', target_mdx]]
    schedule = None
    keyword = ['Mobility Forecast']
    threshold = ('ge', 1)


    def prepare(self):
        super().prepare()
        now = datetime.now()
        curr_yr = str(now.year)
        next_yr = str(int(curr_yr) + 1)
        self.source[0][2] = source_mdx % (curr_yr,next_yr)
        self.target[0][2] = target_mdx % (curr_yr,next_yr)