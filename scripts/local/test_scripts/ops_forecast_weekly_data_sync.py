from datetime import datetime

from tm1tests.reconciliation import Reconciliation

target_mdx = (
"WITH MEMBER [Period].[%s] as [Period].[%s]"+
"SELECT NON EMPTY"+
   "{[Ops Metric].[Completed Trips],[Ops Metric].[ Net Inflows]"+
   "} *"+
   "{[Line of Business].[Rides], [Line of Business].[Eats]}"+
"ON ROWS,"+
   "{[Period].[%s]} "+
"ON COLUMNS "+
"FROM "+
   "[Ops]"+
"WHERE"+
   "("+
   "[Version].[Forecast Excl Actuals],"+
   "[Location].[Total Location],"+
   "[Source].[Adjustment],"+
   "[Rate Type].[USD],"+
   "[Product Type].[Total Product Type],"+
   "[Ops Measure].[Amount]"+
   ")"
)

source_mdx = (
"WITH MEMBER [Period].[%s] as [Period].[%s]"+
"SELECT NON EMPTY"+
   "{[Account].[Completed Trips], [Account].[Net Inflows]"+
   "} *"+
   "{[Line of Business].[Rides], [Line of Business].[Eats]}"+
"ON ROWS,"+
   "{[Period].[%s]}"+
"ON COLUMNS "+
"FROM "+
   "[PL Forecast MWM]"+
"WHERE"+
   "("+
   "[Plan Version].[Plan 3],"+
   "[Location].[Total Location],"+
   "[Plan Model].[Adjustment],"+
   "[Currency Type].[USD],"+
   "[Product Type].[Total Product Type],"+
   "[PL Forecast MWM Measure].[Amount]"+
   ")"
)


class Mytest(Reconciliation):

    name = 'Ops Forecast weekly data sync'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error', 'page': 'critical'}
    source = [['planning', 'mdx', source_mdx]]
    target = [['ops', 'mdx', target_mdx]]
    # schedule = '0 9 1 * *' # First day of month 9AM
    keyword = ['ops']
    threshold = ('ge', 1)


    def prepare(self):
        super().prepare()
        now = datetime.now()
        curr_year = str(now.year)
        week_curr_year = 'Week ' + curr_year
        total_year = 'Year ' + curr_year
        self.source[0][2] = source_mdx %(total_year, week_curr_year, total_year)
        self.target[0][2] = target_mdx %(total_year, curr_year, total_year)
