import os
from datetime import datetime, timedelta


REPORTS_API_BASE_ENDPOINT = "https://reports.api.clockify.me/v1"

WORKSPACE_ID = "633d6b623a6eb41ad795d25a"

API_URL = f"{REPORTS_API_BASE_ENDPOINT}/workspaces/{WORKSPACE_ID}/reports/detailed"

HEADERS = {
    'x-api-key': os.getenv("API_KEY", None),
    'Content-Type': 'application/json'
}

DATA = {
    # datetime 1 year ago today
    "dateRangeStart": (datetime.now() - timedelta(days=1 * 365)).isoformat(),
    # datetime today
    "dateRangeEnd": datetime.now().isoformat(),
    "detailedFilter": {
        "page": 1,
        "pageSize": 50
    }
}