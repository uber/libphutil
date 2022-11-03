
from datetime import datetime
from tm1tests.reconciliation import Reconciliation

source_mdx = """SELECT NON EMPTY
    {FILTER( {UNION({TM1DRILLDOWNMEMBER( {TM1FILTERBYPATTERN( {TM1SUBSETALL( [Period] )}, "%s")}, ALL, RECURSIVE )},{TM1DRILLDOWNMEMBER( {TM1FILTERBYPATTERN( {TM1SUBSETALL( [Period] )}, "%s")}, ALL, RECURSIVE )})}, [Period].[End of Period] > 44651.000000)}
    ON ROWS,
NON EMPTY
    {[Delivery Ops Metrics].[Completed Trips]}
    ON COLUMNS
FROM
    [Delivery]
WHERE (
    [Version].[Actual],
    [Source].[FDS Incl. Adj],
    [Rate Type].[FX Rates],
    [Line of Business].[Delivery],   
    [Department].[Total Department],
    [Delivery Fulfillment Type].[Total Fulfillment Type],
    [Delivery Merchant Type].[Total Merchant Type],
    [Delivery Order Category].[Total Order Category],
    [Delivery Merchant Segment].[Total Merchant Segment],
    [Delivery Features].[All Delivery Features],
    [Location].[Total Location by Country],
    [Delivery Measure].[Amount]
)"""

target_mdx = """SELECT NON EMPTY
    {FILTER( {UNION({TM1DRILLDOWNMEMBER( {TM1FILTERBYPATTERN( {TM1SUBSETALL( [Period] )}, "%s")}, ALL, RECURSIVE )},{TM1DRILLDOWNMEMBER( {TM1FILTERBYPATTERN( {TM1SUBSETALL( [Period] )}, "%s")}, ALL, RECURSIVE )})}, [Period].[End of Period] > 44651.000000)}
    ON ROWS,
    NON EMPTY
   {[Ops Metric].[Completed Trips]}
    ON COLUMNS
FROM
    [ops]
WHERE (
    [Version].[Actual],
    [Source].[FDS Incl. Adj],
    [Rate Type].[FX Rates],
    [Line of Business].[Delivery],
    [Product Type].[Total Product Type],
    [Location].[Total Location Incl Discontinued],
    [Ops Measure].[Amount]
)"""

class Mytest(Reconciliation):

    name = 'Delivery - Ops Completed Trips Recon'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', source_mdx]]
    target = [['ops', 'mdx', target_mdx]]
    schedule = '0 11,4,23 * * *'
    keyword = ['Delivery']
    threshold = ('ge', 1)

    def prepare(self):
        super().prepare()
        now = datetime.now()
        curr_yr = str(now.year)
        prev_yr = str(int(curr_yr) - 1)
        self.source[0][2] = source_mdx % (curr_yr,prev_yr)
        self.target[0][2] = target_mdx % (curr_yr,prev_yr)
