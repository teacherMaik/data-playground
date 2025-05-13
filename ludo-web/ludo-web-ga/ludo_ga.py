import os
import pandas as pd

CACHE_FILE = 'ga_cahche.csv'
REFRESH = False
# Define the GA4 request for date-based metrics
# request = RunReportRequest(
#     property=f"properties/{PROPERTY_ID}",
#     dimensions=[Dimension(name="date")],
#     metrics=[
#         Metric(name="sessions"),       # Total sessions per date
#         Metric(name="screenPageViews")       # Total pageviews per date
#     ],
#     date_ranges=[DateRange(start_date="30daysAgo", end_date="today")]
# )

if os.path.exists(CACHE_FILE) and not REFRESH:
    print("Loading GA data from cache...")
    df = pd.read_csv(CACHE_FILE, parse_dates=["date"])

else:

    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric
    from google.oauth2 import service_account

    def load_env(filepath="../../.env"):

        with open(filepath) as f:

            for line in f:

                if line.strip() and not line.startswith("#"):

                    key, _, value = line.strip().partition("=")
                    os.environ[key] = value

    load_env()

    # Authenticate and set up GA4 client
    KEY_PATH = os.getenv("GOOGLE_SERVICE_ACCOUNT_KEY_PATH")
    PROPERTY_ID = os.getenv("LUDO_GA_PROPERTY_ID")
    credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
    client = BetaAnalyticsDataClient(credentials=credentials)

    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        dimensions=[
            Dimension(name="date"),
            Dimension(name="pageTitle"),
            Dimension(name="country"),
            Dimension(name="deviceCategory"),
            Dimension(name="browser"),
            Dimension(name="city"),
            Dimension(name="pagePath"),
            Dimension(name="sessionSource")
        ],
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="newUsers"),
            Metric(name="screenPageViews"),
            Metric(name="engagedSessions"),
            Metric(name="averageSessionDuration"),
            Metric(name="bounceRate"),
            Metric(name="eventCount"),
            Metric(name="userEngagementDuration"),
            Metric(name="sessions"),
            Metric(name="conversions")
        ],
        date_ranges=[DateRange(start_date="30daysAgo", end_date="today")]
    )

    # Execute the request
    response = client.run_report(request)

    # Extract the data from GA response
    # ga_data = []
    # for row in response.rows:
    #     # Extract the date and convert it to SQL date format
    #     date_str = row.dimension_values[0].value  # Date in YYYYMMDD format
    #     date_obj = datetime.strptime(date_str, "%Y%m%d")
    #     sql_date = date_obj.strftime("%Y-%m-%d")  # Convert to SQL-compatible date format
        
    #     ga_data.append({
    #         'Date': sql_date,
    #         'Sessions': row.metric_values[0].value,
    #         'Pageviews': row.metric_values[1].value
    #     })

    rows = []
    for row in response.rows:
        row_data = {dim.name: dim_val.value for dim, dim_val in zip(response.dimension_headers, row.dimension_values)}
        row_data.update({metric.name: met_val.value for metric, met_val in zip(response.metric_headers, row.metric_values)})
        rows.append(row_data)

    df = pd.DataFrame(rows)
    
    # Convert the 'date' column from 'YYYYMMDD' to 'YYYY-MM-DD'
    df['date'] = pd.to_datetime(df['date'], format="%Y%m%d").dt.date
    df.to_csv(CACHE_FILE, index=False)


df = pd.read_csv(CACHE_FILE)

df_active_by_date = df.groupby('date')['activeUsers'].sum().sort_values(ascending=False)
print(df_active_by_date)
