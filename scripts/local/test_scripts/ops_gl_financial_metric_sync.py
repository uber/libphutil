
from datetime import datetime

from tm1tests.reconciliation import Reconciliation

source_mdx = (
"SELECT NON EMPTY "+
    "{"+
    "[Ops Metric].[Cash Gross Bookings]" +
    "} * "+
    "{[Line of Business].[Total Line of Business]}" +
"ON ROWS,"+
    "{[Period].[%s]}"+
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
"SELECT NON EMPTY "+
    "{"+
    "[Account].[Cash Gross Bookings]" +
    "} * "+
    "{[Line of Business].[Total Line of Business]}"+
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

    name = 'Ops GL Financial Metric Sync'
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
        session = self.apps_sessions['analytics']
        current_actual_month=session.cubes.cells.get_value('System Info','Current Month, String')
        self.source[0][2] = source_mdx %(current_actual_month)
        self.target[0][2] = target_mdx %(current_actual_month)
