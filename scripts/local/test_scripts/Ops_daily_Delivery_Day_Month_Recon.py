
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
    {[Delivery Ops Metrics].[Gross Bookings],[Delivery Ops Metrics].[Net Effective Take Rate (NETR)],[Delivery Ops Metrics].[Variable Costs],[Delivery Ops Metrics].[Variable Contribution],
    [Delivery Ops Metrics].[Operating Expenses],[Delivery Ops Metrics].[Adj EBITDA],[Delivery Ops Metrics].[Completed Trips],[Delivery Ops Metrics].[P2 Non-P2P Miles],[Delivery Ops Metrics].[P2 P2P Miles],
    [Delivery Ops Metrics].[P3 Non-P2P Miles],[Delivery Ops Metrics].[P3 P2P Miles],[Delivery Ops Metrics].[Completed Trips - Rides Insurance CM]}
    ON COLUMNS
FROM
    [Delivery]
WHERE (
    [Version].[Actual],
    [Source].[FDS],
    [Rate Type].[USD],
    [Line of Business].[Delivery],
    [Department].[Total Department],
    [Delivery Fulfillment Type].[Total Fulfillment Type],
    [Delivery Merchant Type].[Total Merchant Type],
    [Delivery Order Category].[Total Order Category],
    [Delivery Merchant Segment].[Total Merchant Segment],
    [Delivery Features].[All Delivery Features],
    [Location].[Total Location Incl Discontinued],
    [Delivery Measure].[Amount]
)"""

target_mdx = """
WITH
    MEMBER [Period].[current_year] AS [Period].[%s]
    MEMBER [Period].[previous_year] AS [Period].[%s]
SELECT NON EMPTY
    {[Period].[current_year],[Period].[previous_year]}
    ON ROWS,
    NON EMPTY
    {[Delivery Ops Metrics].[Gross Bookings],[Delivery Ops Metrics].[Net Effective Take Rate (NETR)],[Delivery Ops Metrics].[Variable Costs],[Delivery Ops Metrics].[Variable Contribution],
    [Delivery Ops Metrics].[Operating Expenses],[Delivery Ops Metrics].[Adj EBITDA],[Delivery Ops Metrics].[Completed Trips],[Delivery Ops Metrics].[P2 Non-P2P Miles],[Delivery Ops Metrics].[P2 P2P Miles],
    [Delivery Ops Metrics].[P3 Non-P2P Miles],[Delivery Ops Metrics].[P3 P2P Miles],[Delivery Ops Metrics].[Completed Trips - Rides Insurance CM]}
    ON COLUMNS
FROM
    [Delivery]
WHERE (
    [Version].[Actual],
    [Source].[FDS],
    [Rate Type].[USD],
    [Line of Business].[Delivery],
    [Department].[Total Department],
    [Delivery Fulfillment Type].[Total Fulfillment Type],
    [Delivery Merchant Type].[Total Merchant Type],
    [Delivery Order Category].[Total Order Category],
    [Delivery Merchant Segment].[Total Merchant Segment],
    [Delivery Features].[All Delivery Features],
    [Location].[Total Location Incl Discontinued],
    [Delivery Measure].[Amount]
)"""

class Mytest(Reconciliation):

    name = 'Delivery FDS Day Vs Month Recon'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', source_mdx]]
    target = [['ops', 'mdx', target_mdx]]
    schedule = '0 19 * * *'
    keyword = ['Delivery']
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
