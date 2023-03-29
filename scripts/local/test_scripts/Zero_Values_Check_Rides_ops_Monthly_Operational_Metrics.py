from datetime import datetime
from datetime import timedelta
from tm1tests.validation import Validation
from tm1tests.tm1test import Statuses

MDX = """SELECT NON EMPTY
    {[Ops Metric]. [Continuing Riders] ,
    [Ops Metric]. [Continuing Rider Trips],
    [Ops Metric]. [New Riders],
    [Ops Metric]. [New Rider Trips],
    [Ops Metric]. [Resurrected Riders],
    [Ops Metric]. [84 Day Inactive Riders],
    [Ops Metric]. [Continuing Drivers],
    [Ops Metric]. [Continuing Driver Trips],
    [Ops Metric]. [New Drivers],
    [Ops Metric]. [New Driver Trips]}

    ON ROWS,
    NON EMPTY
    {TM1FILTERBYLEVEL( {TM1SUBSETALL( [Rate Type] )}, 0)}
    ON COLUMNS
FROM
    [Ops]
WHERE (
     [Period].[%s],
    [Version].[Actual],
    [Source].[FDS],
    [Line of Business].[1001],
    [Product Type].[Total Product Type],
    [Location].[Total Location],
    [Ops Measure].[Amount]
    )"""

class Mytest(Validation):
    name = 'Rides Ops- Monthly Operational Data Check for Zero values'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', MDX]]
    schedule = '* 9 2-31 * *'
    keyword = ['Rides_ops_Monthly_operational']

    def prepare(self):
        super().prepare()
        ops = self.apps_sessions['ops']
        global Num_Rate_Elements
        global TOTAL_RECORD_COUNT

        # Define the length of ratetype elements
        Rate_Elements = ops.dimensions.execute_mdx(dimension_name="Rate Type", mdx="{TM1FILTERBYLEVEL( {TM1SUBSETALL( [Rate Type] )}, 0)}")
        Num_Rate_Elements = len (Rate_Elements)
        #calculate the previous Month
        today_date = datetime.now()
        one_day_ago = str(today_date - timedelta(days=1))[8:10]    ## eg., 08
        previous_day = str(today_date - timedelta(days=1))[0:10]   ## eg., 2022-06-08
        current_month = str(today_date - timedelta(days=1))[0:7]   ## eg., 2022-06
        previous_month = ops.cubes.cells.get_value('}ElementAttributes_Period', f'{current_month},Period-1')  ##eg., 2022-05


        self.source[0][2] = MDX % (previous_month)
        TOTAL_RECORD_COUNT = Num_Rate_Elements * 10 

    def execute(self):
        df, target_df = self.execute_query()

        if (len(df) < TOTAL_RECORD_COUNT):
            self.status = Statuses.CRITICAL.name
            self.message = 'Zero Data Found ' + str(TOTAL_RECORD_COUNT-len(df)) + ' records'
        else:
            self.status = Statuses.SUCCESS.name
            self.message = 'No values are zero'