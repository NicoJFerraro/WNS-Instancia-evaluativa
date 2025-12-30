# src/services/price.py

import requests
from typing import Union
from datetime import datetime, timedelta, date

def get_exchange_rate_usd_to_ars(date_input: Union[str, datetime.date]) -> float:

    if isinstance(date_input, datetime):
        date_str = date_input.strftime('%Y-%m-%d')
    elif isinstance(date_input, date):
        date_str = date_input.strftime('%Y-%m-%d')
    else: 
        date_str = date_input

    url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{date_str}/v1/currencies/usd.json"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()


        data = response.json()
        exchange_rate = data['usd']['ars']
        return float(exchange_rate)
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching exchange rate from API: {e}")
    except KeyError as e:
        raise Exception(f"Exchange rate data not found in API response: {e}")
    
def validate_date_within_last_30_days(date: Union[str, datetime, date]) -> date:
    today = datetime.now().date()
    thirty_days_ago = today - timedelta(days=30)

    if isinstance(date, str):
        date_result = datetime.strptime(date, '%Y-%m-%d').date()
    elif isinstance(date, datetime):
        date_result = date.date()
    elif isinstance(date, date):
        date_result = date
    else:
        raise ValueError("Invalid date format. Must be str, datetime, or date.")

    if date_result < thirty_days_ago or date_result > today:
        raise ValueError(
            f"Date must be between {thirty_days_ago} and {today}. "
            f"Provided date: {date}"
        )

    return date_result