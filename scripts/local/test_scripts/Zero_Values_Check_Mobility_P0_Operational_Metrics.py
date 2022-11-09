
from datetime import datetime
from datetime import timedelta
from tm1tests.validation import Validation
from tm1tests.tm1test import Statuses

MDX = """SELECT NON EMPTY
    %s 
    ON ROWS,
    NON EMPTY
    {TM1FILTERBYLEVEL( {TM1SUBSETALL( [Rate Type] )}, 0)}*{[Mobility Ops Metrics].[Completed Trips],[Mobility Ops Metrics].[Rider Miles]}
    ON COLUMNS
FROM
    [Mobility]
WHERE (
    [Version].[Actual],
    [Source].[FDS Incl. Adj],
    [Line of Business].[Mobility],
    [Department].[Total Department],
    [Product Type].[Total Product Type],
    [Mobility Features].[All Mobility Features],
    [Location].[Total Location Incl Discontinued],
    [Mobility Measure].[Amount]
)"""

class Mytest(Validation):
    name = 'Mobility - Completed Trips Data Check for Zero values'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', MDX]]
    schedule = '45 15 * * *'
    keyword = ['completed_trips_validation']

    def prepare(self):
        super().prepare()
        ops = self.apps_sessions['ops']
        global Num_Rate_Elements
        global TOTAL_RECORD_COUNT
        
        # Define the length of ratetype elements
        Rate_Elements = ops.dimensions.execute_mdx(dimension_name="Rate Type", mdx="{TM1FILTERBYLEVEL( {TM1SUBSETALL( [Rate Type] )}, 0)}")
        Num_Rate_Elements = len (Rate_Elements)
        
        # calculate the dayno of previous day
        today_date = datetime.now()
        one_day_ago = str(today_date - timedelta(days=1))[8:10]    ## eg., 08
        previous_day = str(today_date - timedelta(days=1))[0:10]   ## eg., 2022-06-08
        current_month = str(today_date - timedelta(days=1))[0:7]   ## eg., 2022-06
        previous_month = ops.cubes.cells.get_value('}ElementAttributes_Period', f'{current_month},Period-1')  ##eg., 2022-05
        day_no = ops.cubes.cells.get_value('}ElementAttributes_Period', f'{previous_day},End of Period')
      
        # Form the MDX based on day 
        if (int(one_day_ago)>15):
          period_mdx = "{FILTER({TM1FILTERBYLEVEL({TM1DRILLDOWNMEMBER( {TM1FILTERBYPATTERN( {TM1SUBSETALL( [Period] )}, 'Day " +  current_month  + "')}, ALL, RECURSIVE )}, 0)} , [Period].[End of Period] <= " + str(int(day_no))  + ")}" 
          len_period_elements = len(ops.dimensions.execute_mdx(dimension_name="Period", mdx=period_mdx))
          TOTAL_RECORD_COUNT = Num_Rate_Elements * 2 * len_period_elements  
        else:
          period_mdx = "{ UNION({FILTER({TM1FILTERBYLEVEL({TM1DRILLDOWNMEMBER( {TM1FILTERBYPATTERN( {TM1SUBSETALL( [Period] )},'Day " + current_month + "')}, ALL, RECURSIVE )}, 0)} , [Period].[End of Period] <= "+ str(int(day_no)) +")},{TM1FILTERBYLEVEL({TM1DRILLDOWNMEMBER( {TM1FILTERBYPATTERN( {TM1SUBSETALL( [Period] )},'Day " + previous_month + "')}, ALL, RECURSIVE )}, 0)} )}" 
          len_period_elements = len(ops.dimensions.execute_mdx(dimension_name="Period", mdx=period_mdx))
          TOTAL_RECORD_COUNT = Num_Rate_Elements * 2 * len_period_elements  
        
        self.source[0][2] = MDX % (period_mdx)
          

    def execute(self):
        df, target_df = self.execute_query()

        if (len(df) < TOTAL_RECORD_COUNT):
            self.status = Statuses.CRITICAL.name
            self.message = 'Zero Data Found ' + str(TOTAL_RECORD_COUNT-len(df)) + ' records'
        else:
            self.status = Statuses.SUCCESS.name
            self.message = 'No values are zero'
