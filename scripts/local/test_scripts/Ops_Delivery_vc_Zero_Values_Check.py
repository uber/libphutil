
from datetime import datetime
from datetime import timedelta
from tm1tests.validation import Validation
from tm1tests.tm1test import Statuses

MDX = """SELECT
    {[Period].[%s]}
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
    schedule = '0 2 * * *'
    keyword = ['vc_validation']

    def prepare(self):
        super().prepare()
        ops = self.apps_sessions['ops']
        now = datetime.now()
        global Num_Rate_Elements
        global Num_Period_Elements
        global NONZERO_RECORD_COUNT
        Rate_Elements = ops.dimensions.execute_mdx(dimension_name="Rate Type", mdx="{[Rate Type].[USD],[Rate Type].[No Rate Type]}")
        Num_Rate_Elements = len (Rate_Elements)
        NONZERO_RECORD_COUNT = Num_Rate_Elements * 1
        today_date = datetime.now()
        delta = timedelta(days = 2)
        two_days_ago = str(today_date - delta)
        two_days_ago = str(two_days_ago[0:10])
        self.source[0][2] = MDX % (two_days_ago)

    def execute(self):
        df, target_df = self.execute_query()

        if (len(df) < NONZERO_RECORD_COUNT):
            self.status = Statuses.CRITICAL.name
            self.message = 'Zero Data Found ' + str(NONZERO_RECORD_COUNT-len(df)) + ' records'
        else:
            self.status = Statuses.SUCCESS.name
            self.message = 'No values are zero'
