from datetime import datetime
from datetime import timedelta
from tm1tests.validation import Validation
from tm1tests.tm1test import Statuses

MDX = """SELECT NON EMPTY 
    %s 
    ON ROWS,
NON EMPTY
    {[Rate Type].[USD],[Rate Type].[No Rate Type]}
    ON COLUMNS
FROM
    [Delivery]
WHERE (
    [Version].[Actual],
    [Source].[FDS],
    [Line of Business].[Delivery],
    [Department].[Total Org],
    [Delivery Fulfillment Type].[Total Fulfillment Type],
    [Delivery Merchant Type].[Total Merchant Type],
    [Delivery Order Category].[Total Order Category],
    [Delivery Merchant Segment].[Total Merchant Segment],
    [Delivery Features].[All Delivery Features],
    [Location].[Total Location by Country],
    [Delivery Ops Metrics].[Variable Contribution],
    [Delivery Measure].[Amount]
)"""

class Mytest(Validation):
    name = 'Delivery - vc Data Check for Zero values'
    email_to = []
    email_from = 'pa-eng@uber.com'
    alert_level = {'email': 'error'}
    source = [['ops', 'mdx', MDX]]
    schedule = '0 19 * * *'
    keyword = ['vc_validation']

    def prepare(self):
        super().prepare()
        ops = self.apps_sessions['ops']
        global TOTAL_RECORD_COUNT
        
        # calculate the dayno of previous day
        today_date = datetime.now()
        two_days_ago = str(today_date - timedelta(days=2))[8:10]    ## eg., 08
        previous_day = str(today_date - timedelta(days=2))[0:10]   ## eg., 2022-06-08
        current_month = str(today_date - timedelta(days=2))[0:7]   ## eg., 2022-06
        previous_month = ops.cubes.cells.get_value('}ElementAttributes_Period', f'{current_month},Period-1')  ##eg., 2022-05
        day_no = ops.cubes.cells.get_value('}ElementAttributes_Period', f'{previous_day},End of Period')
      
        # Form the MDX based on day 
        if (int(two_days_ago)>15):
          period_mdx = "{FILTER({TM1FILTERBYLEVEL({TM1DRILLDOWNMEMBER( {TM1FILTERBYPATTERN( {TM1SUBSETALL( [Period] )}, 'Day " +  current_month  + "')}, ALL, RECURSIVE )}, 0)} , [Period].[End of Period] <= " + str(int(day_no))  + ")}" 
          len_period_elements = len(ops.dimensions.execute_mdx(dimension_name="Period", mdx=period_mdx))
          TOTAL_RECORD_COUNT = len_period_elements * 2
        else:
          period_mdx = "{ UNION({FILTER({TM1FILTERBYLEVEL({TM1DRILLDOWNMEMBER( {TM1FILTERBYPATTERN( {TM1SUBSETALL( [Period] )},'Day " + current_month + "')}, ALL, RECURSIVE )}, 0)} , [Period].[End of Period] <= "+ str(int(day_no)) +")},{TM1FILTERBYLEVEL({TM1DRILLDOWNMEMBER( {TM1FILTERBYPATTERN( {TM1SUBSETALL( [Period] )},'Day " + previous_month + "')}, ALL, RECURSIVE )}, 0)} )}" 
          len_period_elements = len(ops.dimensions.execute_mdx(dimension_name="Period", mdx=period_mdx))
          TOTAL_RECORD_COUNT = len_period_elements * 2  
        
        self.source[0][2] = MDX % (period_mdx)
          

    def execute(self):
        df, target_df = self.execute_query()

        if (len(df) < TOTAL_RECORD_COUNT):
            self.status = Statuses.CRITICAL.name
            self.message = 'Zero Data Found ' + str(TOTAL_RECORD_COUNT-len(df)) + ' records'
        else:
            self.status = Statuses.SUCCESS.name
            self.message = 'No values are zero'