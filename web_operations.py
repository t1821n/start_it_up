from email import header

from dotenv import load_dotenv
import os
import requests
from urllib.parse import quote_plus

load_dotenv()

dataset_id = "gd_lvz8ah06191smkebj4"


def _make_api_request(url, **kwargs):
    api_key = os.getenv("BRIGHTDATA_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(url, headers=headers, **kwargs)

        print(response.status_code)
        print(response.text)

        response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError as e:
        print(f"API request failed: {e}")
        return None

    except Exception as e:
        print(f"Unknown error: {e}")
        return None


def serp_search(query, engine="google"):
    if engine == "google":
        base_url = "https://www.google.com/search"
    elif engine == "bing":
        base_url = "https://www.bing.com/search"
    else:
        raise ValueError(f"Unknown search engine: {engine}")

    #send req to brightdata
    url = "https://api.brightdata.com/request"


    payload = {
        "zone": "ai_agent",
        "url": f"{base_url}?q={quote_plus(query)}&brd_json=1",
        "format": "raw"
    }


    full_res = _make_api_request(url, json=payload)
    if not full_res:
        return None

    extracted_data = {
        "knowledge": full_res.get("knowledge", {}),
        "organic": full_res.get("organic", []),
    }

    return extracted_data


def _trigger_and_download_snapshot(trigger_url, params):



def reddit_search(keyword, date="All Time", sort_by="Hot", no_of_posts=75):
    trigger_url = "https://api.brightdata.com/datasets/v3/trgger"

    params = {
        "dataset_id": dataset_id,
        "include_errors": "true",
        "type": "discover_new",
        "discover_by": "keyword",
    }

    data = [
        {
            "keyword": keyword,
            "date": date,
            "sort_by": sort_by,
            "no_of_posts": no_of_posts,
        }
    ]

    raw_data = None

    if not raw_data:
        return None

    return None