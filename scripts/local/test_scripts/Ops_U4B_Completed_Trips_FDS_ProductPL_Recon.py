
from datetime import datetime
from tm1tests.reconciliation import Reconciliation

source_mdx = """SELECT NON EMPTY
    {TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Period].[Total Time - Month]}, ALL, RECURSIVE )}, 0)}
    ON ROWS,
    NON EMPTY
    {[U4B Ops Metrics].[Completed Trips]}
    ON COLUMNS
FROM
    [U4B]
WHERE (
    [Version].[Actual],
    [Source].[FDS Incl. Adj],
    [Rate Type].[FX Rates],
    [Line of Business].[Total Line of Business],   
    [Department].[Total Department],
    [U4B Org Segment].[Total U4B Org Segment],
    [U4B Product].[Total U4B Product],
    [U4B Sales Channel].[Total U4B Sales Channel],
    [U4B Trip Profile].[Total U4B Trip Profile],
    [Location].[Total Location Incl Discontinued],
    [U4B Measure].[Amount]
)"""

target_mdx = """SELECT NON EMPTY
    {TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Period].[Total Time - Month]}, ALL, RECURSIVE )}, 0)}
    ON ROWS,
    NON EMPTY
    {[U4B Ops Metrics].[Completed Trips]}
    ON COLUMNS
FROM
    [U4B]
WHERE (
    [Version].[Actual],
    [Source].[Product PL],
    [Rate Type].[FX Rates],
    [Line of Business].[Total Line of Business],   
    [Department].[Total Department],
    [U4B Org Segment].[Total U4B Org Segment],
    [U4B Product].[Total U4B Product],
    [U4B Sales Channel].[Total U4B Sales Channel],
    [U4B Trip Profile].[Total U4B Trip Profile],
    [Location].[Total Location Incl Discontinued],
    [U4B Measure].[Amount]
)"""

class Mytest(Reconciliation):

    name = 'U4B Completed Trips FDS Vs Product PL Reconciliation'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', source_mdx]]
    target = [['ops', 'mdx', target_mdx]]
    schedule = '0 6,10,17,22 * * *'
    keyword = ['U4B']
    threshold = ('ge', 1)


    def prepare(self):
        super().prepare()
        self.source[0][2] = source_mdx % ()
        self.target[0][2] = target_mdx % () 
