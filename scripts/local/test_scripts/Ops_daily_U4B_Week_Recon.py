
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
    {[U4B Ops Metrics].[Gross Bookings],[U4B Ops Metrics].[Net Effective Take Rate (NETR)],[U4B Ops Metrics].[Variable Costs],[U4B Ops Metrics].[Variable Contribution],
    [U4B Ops Metrics].[Operating Expenses],[U4B Ops Metrics].[Adj EBITDA]}
    ON COLUMNS
FROM
    [U4B]
WHERE (
    [Version].[Actual],
    [Source].[FDS],
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

target_mdx = """
WITH
    MEMBER [Period].[%s] AS [Period].[%s]
    MEMBER [Period].[%s] AS [Period].[%s]
SELECT NON EMPTY
   {[Period].[%s],[Period].[%s]}
    ON ROWS,
    NON EMPTY
    {[U4B Ops Metrics].[Gross Bookings],[U4B Ops Metrics].[Net Effective Take Rate (NETR)],[U4B Ops Metrics].[Variable Costs],[U4B Ops Metrics].[Variable Contribution],
    [U4B Ops Metrics].[Operating Expenses],[U4B Ops Metrics].[Adj EBITDA]}
    ON COLUMNS
FROM
    [U4B]
WHERE (
    [Version].[Actual],
    [Source].[FDS],
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

    name = 'U4B FDS Week Reconciliation'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', source_mdx]]
    target = [['ops', 'mdx', target_mdx]]
    schedule = '0 6,18 * * *'
    keyword = ['U4B']
    threshold = ('ge', 1)

    def prepare(self):
        super().prepare()
        now = datetime.now()
        curr_yr = str(now.year)
        prev_yr = str(int(curr_yr) - 1)
        wd_curr_yr='WD ' + curr_yr
        wd_prev_yr='WD ' + prev_yr
        wk_curr_yr='Week ' + curr_yr
        wk_prev_yr='Week ' + prev_yr
        currentyear_week_comparison = wd_curr_yr + '|' + wk_curr_yr
        prevyear_week_comparison = wd_prev_yr + '|' + wk_prev_yr  
        self.source[0][2] = source_mdx % (currentyear_week_comparison,wd_curr_yr,prevyear_week_comparison,wd_prev_yr,currentyear_week_comparison,prevyear_week_comparison)
        self.target[0][2] = target_mdx % (currentyear_week_comparison,wk_curr_yr,prevyear_week_comparison,wk_prev_yr,currentyear_week_comparison,prevyear_week_comparison)
