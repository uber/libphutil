from datetime import datetime
from datetime import timedelta
from calendar import calendar
from tm1tests.validation import Validation
from tm1tests.tm1test import Statuses

MDX = """SELECT
    NON EMPTY
    %s
    ON columns,
    NON EMPTY{[U4B Ops Metrics].[Rider Miles],
    [U4B Ops Metrics].[P2P Miles],
    [U4B Ops Metrics].[Completed Trips]} * {TM1FILTERBYLEVEL( {TM1SUBSETALL( [Rate Type] )}, 0)}
    ON ROWS
    FROM [U4B]
    WHERE ([Version].[Actual],
    [Source].[FDS],
    [U4B Measure].[Amount],
    [Department].[Total Org],
    [Location].[Total Location by Country],
    [U4B Org Segment].[Total U4B Org Segment],
    [U4B Product].[Total U4B Product],
    [U4B Sales Channel].[Total U4B Sales Channel],
    [U4B Trip Profile].[Total U4B Trip Profile],
    [Line of Business].[Total Line of Business]
        )"""

class Mytest(Validation):
    name = 'U4B P0 Metrics-Data Check for Zero values for all Months'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', MDX]]
    schedule = '0 16 * * *'
    keyword = ['completed_trips_validation']

    def prepare(self):
        super().prepare()
        ops = self.apps_sessions['ops']
        now = datetime.now()
        global Num_Rate_Elements
        global Num_Period_Elements
        global NONZERO_RECORD_COUNT
        global day

# day Previous_month days
        today_date = datetime.now()
        one_day_ago = str(today_date - timedelta(days=1))[8:10]    ## eg., 08
        previous_day = str(today_date - timedelta(days=1))[0:10]   ## eg., 2022-06-08
        current_month = str(today_date - timedelta(days=1))[0:7]   ## eg., 2022-06
        previous_month = ops.cubes.cells.get_value('}ElementAttributes_Period', f'{current_month},Period-1')  ##eg., 2022-05
        day_no = ops.cubes.cells.get_value('}ElementAttributes_Period', f'{previous_day},End of Period')
##################################
        Rate_Elements = ops.dimensions.execute_mdx(dimension_name="Rate Type", mdx="{TM1FILTERBYLEVEL( {TM1SUBSETALL( [Rate Type] )}, 0)}")
        Num_Rate_Elements = len (Rate_Elements)

##################################
        if (int(one_day_ago)>15):
            period_mdx = period_mdx = "{FILTER({TM1FILTERBYLEVEL({TM1DRILLDOWNMEMBER( {TM1FILTERBYPATTERN( {TM1SUBSETALL( [Period] )}, 'Day " +  current_month  + "')}, ALL, RECURSIVE )}, 0)} , [Period].[End of Period] <= " + str(int(day_no))  + ")}"
            len_period_elements = len(ops.dimensions.execute_mdx(dimension_name="Period", mdx=period_mdx))
            NONZERO_RECORD_COUNT = 3 * Num_Rate_Elements * len_period_elements
        else:
            period_mdx = "{ UNION({FILTER({TM1FILTERBYLEVEL({TM1DRILLDOWNMEMBER( {TM1FILTERBYPATTERN( {TM1SUBSETALL( [Period] )},'Day " + current_month + "')}, ALL, RECURSIVE )}, 0)} , [Period].[End of Period] <= "+ str(int(day_no)) +")},{TM1FILTERBYLEVEL({TM1DRILLDOWNMEMBER( {TM1FILTERBYPATTERN( {TM1SUBSETALL( [Period] )},'Day " + previous_month + "')}, ALL, RECURSIVE )}, 0)} )}"
            len_period_elements = len(ops.dimensions.execute_mdx(dimension_name="Period", mdx=period_mdx))
            NONZERO_RECORD_COUNT = 3 * Num_Rate_Elements * len_period_elements

        self.source[0][2] = MDX % (period_mdx)

    def execute(self):
        df, target_df = self.execute_query()

        if (len(df) < NONZERO_RECORD_COUNT):
            self.status = Statuses.CRITICAL.name
            self.message = 'Zero Data Found ' + str(NONZERO_RECORD_COUNT-len(df)) + ' records'
        else:
            self.status = Statuses.SUCCESS.name
            self.message = 'No values are zero'

