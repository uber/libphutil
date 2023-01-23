
from datetime import datetime
from tm1tests.reconciliation import Reconciliation

source_mdx = """SELECT NON EMPTY
    {{TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Period].[%s]}, ALL, RECURSIVE )}, 0)} + {TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Period].[%s]}, ALL, RECURSIVE )}, 0)}}
    ON ROWS,
NON EMPTY
    {[Delivery Ops Metrics].[P2 Non-P2P Miles],[Delivery Ops Metrics].[P2 P2P Miles],[Delivery Ops Metrics].[P3 Non-P2P Miles],[Delivery Ops Metrics].[P3 P2P Miles],[Delivery Ops Metrics].[Completed Trips - Rides Insurance CM]}
    ON COLUMNS
FROM
    [Delivery]
WHERE (
    [Version].[Actual],
    [Source].[FDS],
    [Rate Type].[FX Rates],
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

target_mdx = """SELECT NON EMPTY
    {{TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Period].[%s]}, ALL, RECURSIVE )}, 0)} + {TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Period].[%s]}, ALL, RECURSIVE )}, 0)}}
    ON ROWS,
    NON EMPTY
   {[Ops Metric].[P2 Non-P2P Miles],[Ops Metric].[P2 P2P Miles],[Ops Metric].[P3 Non-P2P Miles],[Ops Metric].[P3 P2P Miles],[Ops Metric].[Completed Trips - Rides Insurance CM]}
    ON COLUMNS
FROM
    [ops]
WHERE (
    [Version].[Actual],
    [Source].[FDS],
    [Rate Type].[FX Rates],
    [Line of Business].[Delivery],
    [Product Type].[Total Product Type],
    [Location].[Total Location Incl Discontinued],
    [Ops Measure].[Amount]
)"""

class Mytest(Reconciliation):

    name = 'Delivery - Ops Miles Metrics Recon'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', source_mdx]]
    target = [['ops', 'mdx', target_mdx]]
    schedule = '0 11,5,23 * * *'
    keyword = ['miles']
    threshold = ('ge', 1)

    def prepare(self):
        super().prepare()
        now = datetime.now()
        curr_yr = str(now.year)
        prev_yr = str(int(curr_yr) - 1)
        self.source[0][2] = source_mdx % (curr_yr,prev_yr)
        self.target[0][2] = target_mdx % (curr_yr,prev_yr)
