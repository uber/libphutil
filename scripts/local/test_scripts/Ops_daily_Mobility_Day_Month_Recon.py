from datetime import datetime
from tm1tests.reconciliation import Reconciliation
    
source_mdx = """
WITH
    MEMBER [Period].[current_year] AS [Period].[%s]
    MEMBER [Period].[previous_year] AS [Period].[%s]
SELECT NON EMPTY
    {[Period].[current_year],[Period].[previous_year]}
    ON ROWS,
    NON EMPTY
    {[Mobility Ops Metrics].[Gross Bookings],[Mobility Ops Metrics].[Pricing, Incentives, and Other Revenue],[Mobility Ops Metrics].[Net Effective Take Rate (NETR)],[Mobility Ops Metrics].[Variable Costs],[Mobility Ops Metrics].[Variable Contribution],
    [Mobility Ops Metrics].[Operating Expenses],[Mobility Ops Metrics].[Adj EBITDA],[Mobility Ops Metrics].[Completed Trips],[Mobility Ops Metrics].[Rider Miles]}
    ON COLUMNS
FROM
    [Mobility]
WHERE (
    [Version].[Actual],
    [Source].[FDS],
    [Rate Type].[USD],
    [Line of Business].[Mobility],   
    [Department].[Total Org],
    [Product Type].[Total Product Type],
    [Mobility Features].[All Mobility Features],
    [Location].[Total Location Incl Discontinued],
    [Mobility Measure].[Amount]
)"""

target_mdx = """
WITH
    MEMBER [Period].[current_year] AS [Period].[%s]
    MEMBER [Period].[previous_year] AS [Period].[%s]
SELECT NON EMPTY
    {[Period].[current_year],[Period].[previous_year]}
    ON ROWS,
    NON EMPTY
    {[Mobility Ops Metrics].[Gross Bookings],[Mobility Ops Metrics].[Pricing, Incentives, and Other Revenue],[Mobility Ops Metrics].[Net Effective Take Rate (NETR)],[Mobility Ops Metrics].[Variable Costs],[Mobility Ops Metrics].[Variable Contribution],
    [Mobility Ops Metrics].[Operating Expenses],[Mobility Ops Metrics].[Adj EBITDA],[Mobility Ops Metrics].[Completed Trips],[Mobility Ops Metrics].[Rider Miles]}
    ON COLUMNS
FROM
    [Mobility]
WHERE (
    [Version].[Actual],
    [Source].[FDS],
    [Rate Type].[USD],
    [Line of Business].[Mobility],   
    [Department].[Total Org],
    [Product Type].[Total Product Type],
    [Mobility Features].[All Mobility Features],
    [Location].[Total Location Incl Discontinued],
    [Mobility Measure].[Amount]
)"""

class Mytest(Reconciliation):

    name = 'Mobility FDS Day Vs Month Recon'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', source_mdx]]
    target = [['ops', 'mdx', target_mdx]]
    schedule = '0 18 * * *'
    keyword = ['Mobility']
    threshold = ('ge', 1)

    def prepare(self):
        super().prepare()
        now = datetime.now()
        curr_yr = str(now.year)
        prev_yr = str(int(curr_yr) - 1)
        day_curr_yr='Day ' + curr_yr    
        day_prev_yr='Day ' + prev_yr
        self.source[0][2] = source_mdx % (curr_yr,prev_yr)
        self.target[0][2] = target_mdx % (day_curr_yr,day_prev_yr)     

