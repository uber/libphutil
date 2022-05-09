
from datetime import datetime
from tm1tests.reconciliation import Reconciliation

source_mdx = (
"WITH MEMBER [Ops Metric].[Total_Support_Contacts] AS [Ops Metric].[Total Support Contacts]"+
"SELECT NON EMPTY "+
    "{[Ops Metric].[Vehicle Miles]," +
    "[Ops Metric].[Non-P2P Rider Miles]," +
    "[Ops Metric].[Total_Support_Contacts]," +
    "[Ops Metric].[Cash Trips]"+
    "} * "+
    "{[Line of Business].[Total Line of Business]}" +
"ON ROWS,"+
    "{TM1FILTERBYLEVEL( {TM1DRILLDOWNMEMBER( {[Period].[%s]}, ALL, RECURSIVE )},0)} "+
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
"WITH MEMBER [Account].[Total_Support_Contacts] AS [Account].[Total Support Defects]"+
"SELECT NON EMPTY "+
    "{[Account].[Vehicle Miles]," +
    "[Account].[Non-P2P Rider Miles]," +
    "[Account].[Total_Support_Contacts]," +
    "[Account].[Cash Trips]" +
    "} * "+
    "{[Line of Business].[Total Line of Business]}"+
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
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', source_mdx]]
    target = [['analytics', 'mdx', target_mdx]]
    schedule = '0 9 * * *'
    threshold = ('ge', 1)
    keyword = ['ops']
    
    def prepare(self):
        super().prepare()
        now = datetime.now()
        curr_yr = now.year if now.month > 1 else now.year - 1
        self.source[0][2] = source_mdx %(curr_yr)
        self.target[0][2] = target_mdx %(curr_yr)
