
from datetime import datetime
from tm1tests.reconciliation import Reconciliation
    
source_mdx = """SELECT NON EMPTY
    {[Month].[%s]}
    ON ROWS,
    NON EMPTY
    {[GL Operational].[Gross Bookings],[GL Operational].[Pricing, Incentives, and Other Revenue],[GL Operational].[Net Effective Take Rate (NETR)],[GL Operational].[Variable Costs],[GL Operational].[Variable Contribution],
    [GL Operational].[Operating Expenses],[GL Operational].[Adj EBITDA]}
    ON COLUMNS
FROM
    [GL Operational]
WHERE (
    [Account].[Ops P&L],
    [Version].[Actual],
    [Location].[Total Location Incl Discontinued],
    [Source].[Total External Excl Sig Adj],
    [Rate Type].[USD],
    [Line of Business].[Delivery],
    [Department].[Total Org],
    [Product Type].[Total Product Type],
    [GL Operational Measure].[Amount]
)"""

target_mdx = """SELECT NON EMPTY
    {[Period].[%s]}
    ON ROWS,
    NON EMPTY
    {[Delivery Ops Metrics].[Gross Bookings],[Delivery Ops Metrics].[Pricing, Incentives, and Other Revenue],[Delivery Ops Metrics].[Net Effective Take Rate (NETR)],[Delivery Ops Metrics].[Variable Costs],[Delivery Ops Metrics].[Variable Contribution],
    [Delivery Ops Metrics].[Operating Expenses],[Delivery Ops Metrics].[Adj EBITDA]}
    ON COLUMNS
FROM
    [Delivery]
WHERE (
    [Version].[Actual],
    [Source].[Oracle],
    [Rate Type].[USD],
    [Line of Business].[Delivery],   
    [Department].[Total Org],
    [Delivery Fulfillment Type].[Total Fulfillment Type],
    [Delivery Merchant Type].[Total Merchant Type],
    [Delivery Order Category].[Total Order Category],
    [Delivery Merchant Segment].[Total Merchant Segment],
    [Delivery Features].[All Delivery Features],
    [Location].[Total Location Incl Discontinued],
    [Delivery Measure].[Amount]
)"""

class Mytest(Reconciliation):

    name = 'GL Operational vs Ops Delivery Oracle Data Recon'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['analytics', 'mdx', source_mdx]]
    target = [['ops', 'mdx', target_mdx]]
    schedule = None
    keyword = ['Delivery']
    threshold = ('ge', 1)


    def prepare(self):
        super().prepare()
        session = self.apps_sessions['analytics']
        curr_month = session.cubes.cells.get_value('System Info', 'Current Month, String')
        self.source[0][2] = source_mdx % (curr_month)
        self.target[0][2] = target_mdx % (curr_month) 
