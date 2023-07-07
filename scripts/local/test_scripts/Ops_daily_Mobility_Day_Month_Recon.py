from datetime import datetime
from tm1tests.reconciliation import Reconciliation
    
source_mdx = """
WITH
    MEMBER [Period].[%s] AS [Period].[%s]
    MEMBER [Period].[%s] AS [Period].[%s]
SELECT NON EMPTY
    {[Period].[%s],[Period].[%s]}
    ON ROWS,
    NON EMPTY
    {[Mobility Ops Metrics].[Gross Bookings],[Mobility Ops Metrics].[Net Effective Take Rate (NETR)],[Mobility Ops Metrics].[Variable Costs],[Mobility Ops Metrics].[Variable Contribution],
    [Mobility Ops Metrics].[Operating Expenses],[Mobility Ops Metrics].[Adj EBITDA],[Mobility Ops Metrics].[Completed Trips],[Mobility Ops Metrics].[P2 Non-P2P Miles],[Mobility Ops Metrics].[P2 P2P Miles],
    [Mobility Ops Metrics].[P3 Non-P2P Miles],[Mobility Ops Metrics].[P3 P2P Miles],[Mobility Ops Metrics].[Completed Trips - Rides Insurance CM]}
    ON COLUMNS
FROM
    [Mobility]
WHERE (
    [Version].[Actual],
    [Source].[FDS],
    [Rate Type].[USD],
    [Line of Business].[Mobility],   
    [Department].[Total Department],
    [Product Type].[Total Product Type],
    [Mobility Features].[All Mobility Features],
    [Location].[Total Location Incl Discontinued],
    [Mobility Measure].[Amount]
)"""

target_mdx = """
WITH
    MEMBER [Period].[%s] AS [Period].[%s]
    MEMBER [Period].[%s] AS [Period].[%s]
SELECT NON EMPTY
    {[Period].[%s],[Period].[%s]}
    ON ROWS,
    NON EMPTY
    {[Mobility Ops Metrics].[Gross Bookings],[Mobility Ops Metrics].[Net Effective Take Rate (NETR)],[Mobility Ops Metrics].[Variable Costs],[Mobility Ops Metrics].[Variable Contribution],
    [Mobility Ops Metrics].[Operating Expenses],[Mobility Ops Metrics].[Adj EBITDA],[Mobility Ops Metrics].[Completed Trips],[Mobility Ops Metrics].[P2 Non-P2P Miles],[Mobility Ops Metrics].[P2 P2P Miles],
    [Mobility Ops Metrics].[P3 Non-P2P Miles],[Mobility Ops Metrics].[P3 P2P Miles],[Mobility Ops Metrics].[Completed Trips - Rides Insurance CM]}
    ON COLUMNS
FROM
    [Mobility]
WHERE (
    [Version].[Actual],
    [Source].[FDS],
    [Rate Type].[USD],
    [Line of Business].[Mobility],   
    [Department].[Total Department],
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
        current_year_comparison = curr_yr + '|' + day_curr_yr
        previous_year_comparison = prev_yr + '|' + day_prev_yr
        self.source[0][2] = source_mdx % (current_year_comparison,curr_yr,previous_year_comparison,prev_yr,current_year_comparison,previous_year_comparison)
        self.target[0][2] = target_mdx % (current_year_comparison,day_curr_yr,previous_year_comparison,day_prev_yr,current_year_comparison,previous_year_comparison)

