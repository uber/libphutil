
from datetime import datetime
from tm1tests.reconciliation import Reconciliation

source_mdx = """SELECT NON EMPTY
    {{TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Period].[%s]}, ALL, RECURSIVE )}, 0)}}
    ON ROWS,
    NON EMPTY
    {[U4B Ops Metrics].[Gross Bookings],[U4B Ops Metrics].[Net Effective Take Rate (NETR)],[U4B Ops Metrics].[Variable Costs],[U4B Ops Metrics].[Variable Contribution],
    [U4B Ops Metrics].[Operating Expenses],[U4B Ops Metrics].[Adj EBITDA]}
    ON COLUMNS
FROM
    [U4B]
WHERE (
    [Version].[Actual],
    [Source].[Oracle],
    [Rate Type].[USD],
    [Line of Business].[Total Line of Business],   
    [Department].[Total Department],
    [U4B Org Segment].[Total U4B Org Segment],
    [U4B Product].[Total U4B Product],
    [U4B Sales Channel].[Total U4B Sales Channel],
    [U4B Trip Profile].[Total U4B Trip Profile],
    [Location].[Total Location by Country],
    [U4B Measure].[Amount]
)"""

target_mdx = """SELECT NON EMPTY
    {{TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Period].[%s]}, ALL, RECURSIVE )}, 0)}}
    ON ROWS,
    NON EMPTY
    {[U4B Ops Metrics].[Gross Bookings],[U4B Ops Metrics].[Net Effective Take Rate (NETR)],[U4B Ops Metrics].[Variable Costs],[U4B Ops Metrics].[Variable Contribution],
    [U4B Ops Metrics].[Operating Expenses],[U4B Ops Metrics].[Adj EBITDA]}
    ON COLUMNS
FROM
    [U4B]
WHERE (
    [Version].[Actual],
    [Source].[Product PL],
    [Rate Type].[USD],
    [Line of Business].[Total Line of Business],   
    [Department].[Total Department],
    [U4B Org Segment].[Total U4B Org Segment],
    [U4B Product].[Total U4B Product],
    [U4B Sales Channel].[Total U4B Sales Channel],
    [U4B Trip Profile].[Total U4B Trip Profile],
    [Location].[Total Location by Country],
    [U4B Measure].[Amount]
)"""

class Mytest(Reconciliation):

    name = 'U4B Oracle Vs Product PL Reconciliation'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', source_mdx]]
    target = [['ops', 'mdx', target_mdx]]
    schedule = '15 6,18 * * *'
    keyword = ['U4B']
    threshold = ('ge', 1)


    def prepare(self):
        super().prepare()
        now = datetime.now()
        curr_yr = now.year if now.month > 1 else now.year - 1
        self.source[0][2] = source_mdx % (curr_yr)
        self.target[0][2] = target_mdx % (curr_yr) 

