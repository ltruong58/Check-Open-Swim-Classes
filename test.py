import requests
import json
api_url = "https://anc.apm.activecommunities.com/buenapark/rest/activities/list?locale=en-US"  # Replace with your API endpoint

payload = {
  "activity_search_pattern": {
    "skills": [],
    "time_after_str": "",
    "days_of_week": 'null',
    "activity_select_param": 2,
    "center_ids": [],
    "time_before_str": "",
    "open_spots": 'null',
    "activity_id": 'null',
    "activity_category_ids": [],
    "date_before": "",
    "min_age": 'null',
    "date_after": "",
    "activity_type_ids": [],
    "site_ids": [],
    "for_map": 'false',
    "geographic_area_ids": [],
    "season_ids": [],
    "activity_department_ids": [],
    "activity_other_category_ids": [],
    "child_season_ids": [],
    "activity_keyword": "starfish",
    "instructor_ids": [],
    "max_age": 'null',
    "custom_price_from": "",
    "custom_price_to": ""
  },
  "activity_transfer_pattern": {}
}



try:
    response = requests.post(api_url, json=payload)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

    result_data = response.json()
    activities = result_data['body']['activity_items']

    print("API call successful. Stored data:")

    open_classes = []

    for item in activities:
        # if(item.get('urgent_message').get('status_description'))
        print(item.get('id'), item.get('urgent_message').get('status_description'))

except requests.exceptions.RequestException as e:
    print(f"An error occurred during the API call: {e}")