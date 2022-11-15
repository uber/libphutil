from datetime import datetime
from datetime import timedelta
from tm1tests.validation import Validation
from tm1tests.tm1test import Statuses

MDX = """SELECT NON EMPTY
    {
    [Ops Metric]. [Continuing Rider Trips],
    [Ops Metric]. [New Riders],
    [Ops Metric]. [New Rider Trips],
    [Ops Metric]. [Resurrected Riders],
    [Ops Metric]. [84 Day Inactive Riders],
    [Ops Metric]. [Continuing Driver Trips],
    [Ops Metric]. [New Drivers],
    [Ops Metric]. [New Driver Trips]}

    ON ROWS,
    NON EMPTY
    {TM1FILTERBYLEVEL( {TM1SUBSETALL( [Rate Type] )}, 0)} * {[Period].[%s],[Period].[%s], [Period].[%s], [Period].[%s], [Period].[%s], [Period].[%s], [Period].[%s], [Period].[%s], [Period].[%s], [Period].[%s]}
    ON COLUMNS
FROM
    [Ops]
WHERE (
    [Version].[Actual],
    [Source].[FDS],
    [Line of Business].[1001],
    [Product Type].[Total Product Type],
    [Location].[Total Location],
    [Ops Measure].[Amount]
    )"""

class Mytest(Validation):
    name = 'Rides Ops - Weekly Operational Data Check for Zero values'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', MDX]]
    schedule = '30 9 * * *'
    keyword = ['Rides_ops_Weekly_operational']

    def prepare(self):
        super().prepare()
        ops = self.apps_sessions['ops']
        global Num_Rate_Elements
        global TOTAL_RECORD_COUNT

        # Define the length of ratetype elements
        Rate_Elements = ops.dimensions.execute_mdx(dimension_name="Rate Type", mdx="{TM1FILTERBYLEVEL( {TM1SUBSETALL( [Rate Type] )}, 0)}")
        Num_Rate_Elements = len (Rate_Elements)
        #Identify last 10 Monday
        today_date = datetime.now()
        monday = today_date - timedelta(days = today_date.weekday())
        prev_mon1 = 'WS ' + str(monday - timedelta(days=7))[0:10]
        prev_mon2 = 'WS ' + str(monday - timedelta(days=14))[0:10]
        prev_mon3 = 'WS ' + str(monday - timedelta(days=21))[0:10]
        prev_mon4 = 'WS ' + str(monday - timedelta(days=28))[0:10]
        prev_mon5 = 'WS ' + str(monday - timedelta(days=35))[0:10]
        prev_mon6 = 'WS ' + str(monday - timedelta(days=42))[0:10]
        prev_mon7 = 'WS ' + str(monday - timedelta(days=49))[0:10]
        prev_mon8 = 'WS ' + str(monday - timedelta(days=56))[0:10]
        prev_mon9 = 'WS ' + str(monday - timedelta(days=63))[0:10]
        prev_mon10 = 'WS ' + str(monday - timedelta(days=63))[0:10]


        self.source[0][2] = MDX % (prev_mon1,prev_mon2, prev_mon3, prev_mon4, prev_mon5, prev_mon6, prev_mon7, prev_mon8, prev_mon9 , prev_mon10)
        TOTAL_RECORD_COUNT = Num_Rate_Elements * 10 * 8

    def execute(self):
        df, target_df = self.execute_query()

        if (len(df) < TOTAL_RECORD_COUNT):
            self.status = Statuses.CRITICAL.name
            self.message = 'Zero Data Found ' + str(TOTAL_RECORD_COUNT-len(df)) + ' records'
        else:
            self.status = Statuses.SUCCESS.name
            self.message = 'No values are zero'