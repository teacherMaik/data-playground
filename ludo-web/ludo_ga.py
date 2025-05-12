import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric
from google.oauth2 import service_account

def load_env(filepath="../.env"):

    with open(filepath) as f:

        for line in f:

            if line.strip() and not line.startswith("#"):

                key, _, value = line.strip().partition("=")
                os.environ[key] = value

load_env()

# Path to your service account key file
KEY_PATH = os.getenv("GOOGLE_SERVICE_ACCOUNT_KEY_PATH")

# Your GA4 property ID
PROPERTY_ID = os.getenv("LUDO_GA_PROPERTY_ID")

# Authenticate and initialize the client
credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
client = BetaAnalyticsDataClient(credentials=credentials)

print(client)
# Define a report request
# request = RunReportRequest(
#     property=f"properties/{PROPERTY_ID}",
#     dimensions=[Dimension(name="city")],
#     metrics=[Metric(name="activeUsers")],
#     date_ranges=[DateRange(start_date="2023-01-01", end_date="2023-12-31")]
# )


# request = RunReportRequest(
#     property=f"properties/{PROPERTY_ID}",
#     dimensions=[Dimension(name="date")],
#     metrics=[Metric(name="activeUsers")],
#     date_ranges=[DateRange(start_date="7daysAgo", end_date="today")]
# )

request = RunReportRequest(
    property=f"properties/{PROPERTY_ID}",
    dimensions=[{"name": "pageTitle"}],
    metrics=[{"name": "screenPageViews"}],
    date_ranges=[{"start_date": "7daysAgo", "end_date": "today"}],
)

# Execute the request
response = client.run_report(request)
print(response)

# Print the results
for row in response.rows:
    print(f"{row.dimension_values[0].value}: {row.metric_values[0].value}")
