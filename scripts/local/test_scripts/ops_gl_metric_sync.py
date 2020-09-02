import datetime

from tm1tests.reconciliation import Reconciliation

source_mdx = (
"SELECT NON EMPTY "+
    "{[Ops Metric].[Completed Trips], [Ops Metric].[Vehicle Miles]," +
    "[Ops Metric].[P2P Rider Miles]," +
    "[Ops Metric].[Non-P2P Rider Miles]," + 
    "[Ops Metric].[Total Support Contacts]" +
    "} * "+
    "{[Line of Business].[Core Rides], [Line of Business].[Delivery ex M&A]," +
    "[Line of Business].[Freight], [Line of Business].[Total Careem]}"+
"ON ROWS,"+
    "{[Period].[%s]} "+
"ON COLUMNS "+
"FROM "+
    "[Ops] "+
"WHERE "+
    "("+
    "[Version].[Actual], "+
    "[Location].[Total Location Incl Discontinued],"+
    "[Source].[FDP],"+
    "[Rate Type].[USD],"+
    "[Product Type].[Total Product Type],"+
    "[Ops Measure].[Amount]"+
    ")"
)

target_mdx = (
"WITH MEMBER [Account].[Rider Miles] AS [Account].[Total Rider Miles] "+
"SELECT NON EMPTY "+
    "{[Account].[Completed Trips], [Account].[Vehicle Miles]," +
    "[Account].[P2P Rider Miles]," +
    "[Account].[Non-P2P Rider Miles]," + 
    "[Account].[Total Support Contacts]" +
    "} * "+
    "{[Line of Business].[Core Rides], [Line of Business].[Delivery ex M&A]," +
    "[Line of Business].[Freight], [Line of Business].[Total Careem]}"+
"ON ROWS,"+
    "{[Month].[%s]} "+
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
    email_to = ['pa-eng@uber.com']
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error', 'page': 'critical'}
    source = [['ops', 'mdx', source_mdx]]
    target = [['analytics', 'mdx', target_mdx]]
    schedule = '0 9 2-5 * *'
    threshold = ('ge', 1)
    keyword = ['ops']
    
    def prepare(self):
        super().prepare()
        today = datetime.date.today()
        first = today.replace(day=1)
        last_month = (first - datetime.timedelta(days=1)).strftime("%Y-%m")
        self.source[0][2] = source_mdx %(last_month)
        self.target[0][2] = target_mdx %(last_month)
