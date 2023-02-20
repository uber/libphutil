
from datetime import datetime
from tm1tests.reconciliation import Reconciliation

source_mdx = """SELECT NON EMPTY
    {TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Period].[Total Time - Month]}, ALL, RECURSIVE )}, 0)}
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
    [Line of Business].[Total Line of Business],   
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
    {TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Period].[Total Time - Month]}, ALL, RECURSIVE )}, 0)}
    ON ROWS,
    NON EMPTY
    {[Delivery Ops Metrics].[Completed Trips]}
    ON COLUMNS
FROM
    [Delivery]
WHERE (
    [Version].[Actual],
    [Source].[Product PL],
    [Rate Type].[FX Rates],
    [Line of Business].[Total Line of Business],   
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

    name = 'Delivery Completed Trips FDS Vs Product PL Reconciliation'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', source_mdx]]
    target = [['ops', 'mdx', target_mdx]]
    schedule = '0 6,10,17,22 * * *'
    keyword = ['Delivery']
    threshold = ('ge', 1)


    def prepare(self):
        super().prepare()
        self.source[0][2] = source_mdx % ()
        self.target[0][2] = target_mdx % () 
