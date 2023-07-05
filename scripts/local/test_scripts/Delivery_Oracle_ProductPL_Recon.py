
from datetime import datetime
from tm1tests.reconciliation import Reconciliation

source_mdx = """SELECT NON EMPTY
    {{TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Period].[%s]}, ALL, RECURSIVE )}, 0)} + {TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Period].[%s]}, ALL, RECURSIVE )}, 0)}}
    ON ROWS,
    NON EMPTY
    {[Delivery Ops Metrics].[Gross Bookings],[Delivery Ops Metrics].[Pricing, Incentives, and Other Revenue],[Delivery Ops Metrics].[Net Effective Take Rate (NETR)],[Delivery Ops Metrics].[Variable Costs],[Delivery Ops Metrics].[Variable Contribution],
    [Delivery Ops Metrics].[Operating Expenses],[Delivery Ops Metrics].[Adj EBITDA]}*{TM1SubsetToSet( [Rate Type].[Rate Type], 'forecast_allocations' )}
    ON COLUMNS
FROM
    [Delivery]
WHERE (
    [Version].[Actual],
    [Source].[Oracle],
    [Line of Business].[Delivery],   
    [Department].[Total Org],
    [Delivery Fulfillment Type].[Total Fulfillment Type],
    [Delivery Merchant Type].[Total Merchant Type],
    [Delivery Order Category].[Total Order Category],
    [Delivery Merchant Segment].[Total Merchant Segment],
    [Delivery Features].[All Delivery Features],
    [Location].[Total Location by Country],
    [Delivery Measure].[Amount]
)"""

target_mdx = """SELECT NON EMPTY
    {{TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Period].[%s]}, ALL, RECURSIVE )}, 0)} + {TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Period].[%s]}, ALL, RECURSIVE )}, 0)}}
    ON ROWS,
    NON EMPTY
    {[Delivery Ops Metrics].[Gross Bookings],[Delivery Ops Metrics].[Pricing, Incentives, and Other Revenue],[Delivery Ops Metrics].[Net Effective Take Rate (NETR)],[Delivery Ops Metrics].[Variable Costs],[Delivery Ops Metrics].[Variable Contribution],
    [Delivery Ops Metrics].[Operating Expenses],[Delivery Ops Metrics].[Adj EBITDA]}*{TM1SubsetToSet( [Rate Type].[Rate Type], 'forecast_allocations' )}
    ON COLUMNS
FROM
    [Delivery]
WHERE (
    [Version].[Actual],
    [Source].[Product PL],
    [Line of Business].[Delivery],   
    [Department].[Total Org],
    [Delivery Fulfillment Type].[Total Fulfillment Type],
    [Delivery Merchant Type].[Total Merchant Type],
    [Delivery Order Category].[Total Order Category],
    [Delivery Merchant Segment].[Total Merchant Segment],
    [Delivery Features].[All Delivery Features],
    [Location].[Total Location by Country],
    [Delivery Measure].[Amount]
)"""

class Mytest(Reconciliation):

    name = 'Delivery Oracle Vs Product PL Reconciliation'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', source_mdx]]
    target = [['ops', 'mdx', target_mdx]]
    schedule = '15 18 * * *'
    keyword = ['Delivery']
    threshold = ('ge', 1)


    def prepare(self):
        super().prepare()
        now = datetime.now()
        curr_yr = str(now.year)
        prev_yr = str(now.year -1)
        self.source[0][2] = source_mdx % (curr_yr,prev_yr)
        self.target[0][2] = target_mdx % (curr_yr,prev_yr) 
