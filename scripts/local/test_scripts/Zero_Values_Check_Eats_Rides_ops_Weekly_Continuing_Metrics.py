from datetime import date
from datetime import datetime
from datetime import timedelta
from tm1tests.validation import Validation
from tm1tests.tm1test import Statuses

MDX = """SELECT
    {
    [Ops Metric]. [Continuing Rider Trips],
    [Ops Metric]. [Continuing Drivers]
    }*
     {[Line of Business].[1001],  [Line of Business].[2001]}
    ON ROWS,
    {TM1FILTERBYLEVEL( {TM1SUBSETALL( [Rate Type] )}, 0)} * {[Period].[%s] , [Period].[%s] ,[Period].[%s] ,[Period].[%s]
    }
    ON COLUMNS
FROM
    [Ops]
WHERE (
    [Version].[Actual],
    [Source].[FDS],
    [Product Type].[Total Product Type],
    [Location].[Total Location],
    [Ops Measure].[Amount]
    )"""

class Mytest(Validation):
    name = 'Eats_Rides_Ops - Weekly Continuing Data Check for Zero values'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', MDX]]
    schedule = '* 10 * * 1,3'
    keyword = ['Eats_Rides_ops_Weekly_Continuing']

    def prepare(self):
        super().prepare()
        ops = self.apps_sessions['ops']
        global Num_Rate_Elements
        global TOTAL_RECORD_COUNT

        # Define the length of ratetype elements
        Rate_Elements = ops.dimensions.execute_mdx(dimension_name="Rate Type", mdx="{TM1FILTERBYLEVEL( {TM1SUBSETALL( [Rate Type] )}, 0)}")
        Num_Rate_Elements = len (Rate_Elements)
        #Identify last 10 Monday
        today = date.today()
        first = today.replace(day=1)
        lastday = first - timedelta(days=1)
        offset = (lastday.weekday()) % 7
        last_monday = lastday - timedelta(days=(lastday.weekday()) % 7)
        p1 = 'WS '+str(last_monday)

        firstl1 = last_monday.replace(day=1)
        lastdayl1 = firstl1 - timedelta(days=1)
        offset = (lastdayl1.weekday()) % 7
        last_mondayl1 = lastdayl1 - timedelta(days=offset)
        p2 = 'WS '+str(last_mondayl1)

        firstl2 = last_mondayl1.replace(day=1)
        lastdayl2 = firstl2 - timedelta(days=1)
        offset = (lastdayl2.weekday()) % 7
        last_mondayl2 = lastdayl2 - timedelta(days=offset)
        p3 = 'WS '+str(last_mondayl2)

        firstl3 = last_mondayl2.replace(day=1)
        lastdayl3 = firstl3 - timedelta(days=1)
        offset = (lastdayl3.weekday()) % 7
        last_mondayl3 = lastdayl3 - timedelta(days=offset)
        p4 = 'WS '+str(last_mondayl3)

        self.source[0][2] = MDX % (p1,p2,p3,p4)
        TOTAL_RECORD_COUNT = Num_Rate_Elements * 2 * 2 * 4

    def execute(self):
        df, target_df = self.execute_query()

        if (len(df) < TOTAL_RECORD_COUNT):
            self.status = Statuses.CRITICAL.name
            self.message = 'Zero Data Found ' + str(TOTAL_RECORD_COUNT-len(df)) + ' records'
        else:
            self.status = Statuses.SUCCESS.name
            self.message = 'No values are zero'