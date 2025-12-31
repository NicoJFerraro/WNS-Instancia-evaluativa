# src/services/exchange_rate.py

import requests
from typing import Union
from datetime import datetime, timedelta, date

def get_exchange_rate_usd_to_ars(date_input: Union[str, datetime, date]) -> float:

    if isinstance(date_input, (datetime, date)):
        date_str = date_input.strftime('%Y-%m-%d')
    elif isinstance(date_input, str):
        try:
            datetime.strptime(date_input, '%Y-%m-%d')
            date_str = date_input
        except ValueError:
            raise ValueError(f"Invalid date format: {date_input}. Expected format: YYYY-MM-DD")
    else:
        raise ValueError(f"Invalid date type: {type(date_input)}. Expected str, datetime, or date")

    url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{date_str}/v1/currencies/usd.json"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()


        data = response.json()
        
        if not isinstance(data, dict):
            raise Exception("Invalid API response: expected JSON object")
        
        if 'usd' not in data:
            raise Exception("Exchange rate data not found in API response: missing 'usd' key")
        
        if not isinstance(data['usd'], dict):
            raise Exception("Invalid API response: 'usd' must be an object")
        
        if 'ars' not in data['usd']:
            raise Exception("Exchange rate data not found in API response: missing 'ars' key")
        
        try:
            exchange_rate = float(data['usd']['ars'])
            if exchange_rate <= 0:
                raise Exception(f"Invalid exchange rate value: {exchange_rate}")
            return exchange_rate
        except (ValueError, TypeError) as e:
            raise Exception(f"Invalid exchange rate format in API response: {e}")
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching exchange rate from API: {e}")
    
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