from datetime import datetime

from tm1tests.reconciliation import Reconciliation

target_mdx = (
"SELECT NON EMPTY"+
   "{[Ops Metric].[New Riders], [Ops Metric].[Continuing Riders],"+
   "[Ops Metric].[Active Riders], [Ops Metric].[New Drivers],"+
   "[Ops Metric].[Continuing Drivers], [Ops Metric].[Active Drivers],"+
   "[Ops Metric].[Completed Trips], [Ops Metric].[Shopping Sessions],"+
   "[Ops Metric].[P2P Rider Miles] , [Ops Metric].[Supply Hours],"+
   "[Ops Metric].[ Net Inflows], [Ops Metric].[Non-P2P Rider Miles]"+
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
   "[Location].[Total Location Incl Discontinued],"+
   "[Source].[Adjustment],"+
   "[Rate Type].[USD],"+
   "[Product Type].[Total Product Type],"+
   "[Ops Measure].[Amount]"+
   ")"
)

source_mdx = (
"SELECT NON EMPTY"+
   "{[Account].[New Riders], [Account].[Continuing Riders],"+
   "[Account].[Active Riders], [Account].[New Drivers],"+
   "[Account].[Continuing Drivers], [Account].[Active Drivers],"+
   "[Account].[Completed Trips], [Account].[Shopping_Sessions_],"+
   "[Account].[P2P Rider Miles] , [Account].[Supply_Hours_],"+
   "[Account].[ Net Inflows], Ops Metric].[Non-P2P Rider Miles]"+
   "} *"+
   "{[Line of Business].[Rides], [Line of Business].[Eats]}"+
"ON ROWS,"+
   "{[Month].[%s]} "+
"ON COLUMNS "+
"FROM "+
   "[PL Forecast]"+
"WHERE"+
   "("+
   "[Plan Version].[Plan 3],"+
   "[Location].[Total Location Incl Discontinued],"+
   "[Plan Model].[Adjustment],"+
   "[Currency Type].[USD],"+
   "[Department].[Total Department],"+
   "[Product Type].[Total Product Type],"+
   "[PL Forecast Measure].[Amount]"+
   ")"
)


class Mytest(Reconciliation):

    name = 'Ops Forecast monthly data sync'
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
        self.source[0][2] = source_mdx %(curr_year)
        self.target[0][2] = target_mdx %(curr_year)
