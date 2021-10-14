from datetime import datetime


from tm1tests.reconciliation import Reconciliation

source_mdx = (
"WITH MEMBER [Ops Metric].[Total_Support_Contacts] AS [Ops Metric].[Total Support Contacts]"+
"SELECT NON EMPTY "+
    "{[Ops Metric].[Completed Trips], [Ops Metric].[Vehicle Miles]," +
    "[Ops Metric].[P2P Rider Miles]," +
    "[Ops Metric].[Non-P2P Rider Miles]," + 
    "[Ops Metric].[Total_Support_Contacts]" +
    "} * "+
    "{[Line of Business].[Core Rides], [Line of Business].[Delivery ex M&A]," +
    "[Line of Business].[Freight], [Line of Business].[Total Careem]}"+
"ON ROWS,"+
    "{TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Period].[%s]}, ALL, RECURSIVE )}, 0)} "+
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
"WITH MEMBER [Account].[Rider Miles] AS [Account].[Total Rider Miles]"+
     "MEMBER [Account].[Total_Support_Contacts] AS [Account].[Total Support Defects]"+
"SELECT NON EMPTY "+
    "{[Account].[Completed Trips], [Account].[Vehicle Miles]," +
    "[Account].[P2P Rider Miles]," +
    "[Account].[Non-P2P Rider Miles]," + 
    "[Account].[Total_Support_Contacts]" +
    "} * "+
    "{[Line of Business].[Core Rides], [Line of Business].[Delivery ex M&A]," +
    "[Line of Business].[Freight], [Line of Business].[Total Careem]}"+
"ON ROWS,"+
    "{TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Month].[%s]}, ALL, RECURSIVE )}, 0)} "+
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
    schedule = '0 9 * * *'
    threshold = ('ge', 1)
    keyword = ['ops']
    
    def prepare(self):
        super().prepare()
        now = datetime.now()
        curr_yr = str(now.year)
        self.source[0][2] = source_mdx %(curr_yr)
        self.target[0][2] = target_mdx %(curr_yr)
