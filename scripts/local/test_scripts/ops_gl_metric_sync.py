from datetime import datetime

from tm1tests.reconciliation import Reconciliation

source_mdx = (
"SELECT NON EMPTY "+
    "{[Ops Metric].[New Riders], [Ops Metric].[Continuing Riders]," +
    "[Ops Metric].[Active Riders], [Ops Metric].[New Drivers]," +
    "[Ops Metric].[Continuing Drivers], [Ops Metric].[Active Drivers],"+
    "[Ops Metric].[Completed Trips], [Ops Metric].[Vehicle Miles]," +
    "[Ops Metric].[Rider Miles] " +
    "} * "+
    "{[Line of Business].[Rides], [Line of Business].[Eats]," +
    "[Line of Business].[8001]}"+
"ON ROWS,"+
    "{[Period].[%s], [Period].[%s]} "+
"ON COLUMNS "+
"FROM "+
    "[Ops] "+
"WHERE "+
    "("+
    "[Version].[Actual], "+
    "[Location].[Total Location Incl Discontinued],"+
    "[Source].[Total Source],"+
    "[Rate Type].[USD],"+
    "[Product Type].[Total Product Type],"+
    "[Ops Measure].[Amount]"+
    ")"
)

target_mdx = (
"WITH MEMBER [Account].[Rider Miles] AS [Account].[Total Rider Miles] "+
"SELECT NON EMPTY "+
    "{[Account].[New Riders], [Account].[Continuing Riders],"+
    "[Account].[Active Riders], [Account].[New Drivers],"+
    "[Account].[Continuing Drivers], [Account].[Active Drivers], "+
    "[Account].[Completed Trips], [Account].[Vehicle Miles], "+
    "[Account].[Rider Miles] "+
    "} * "+
    "{[Line of Business].[Rides], [Line of Business].[Eats]," +
    "[Line of Business].[8001]}"+
"ON ROWS,"+
    "{[Month].[%s], [Month].[%s]} "+
"ON COLUMNS "+
"FROM "+
    "[GL Reporting] "+
"WHERE "+
    "("+
    "[Version].[Actual], "+
    "[Location].[Total Location Incl Discontinued],"+
    "[Source].[OPS],"+
    "[Rate Type].[USD],"+
    "[Department].[Total Department],"+
    "[Product Type].[Total Product Type],"+
    "[GL Reporting Measure].[Amount]"+
    ")"
)

class Mytest(Reconciliation):

    name = 'Ops GL Metric Sync'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error', 'page': 'critical'}
    source = [['ops', 'mdx', source_mdx]]
    target = [['analytics', 'mdx', target_mdx]]
    #schedule = '0 9 1 * *' # First day of month 9AM
    threshold = ('ge', 1)
    keyword = ['ops']
    
    def prepare(self):
        super().prepare()
        now = datetime.now()
        curr_year = str(now.year)
        last_year = str(now.year -1)
        self.source[0][2] = source_mdx %(curr_year, last_year)
        self.target[0][2] = target_mdx %(curr_year, last_year)
