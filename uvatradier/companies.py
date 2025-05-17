from .base import Tradier
from datetime import datetime, timedelta
import requests


class Companies(Tradier):
    def __init__(self, account_number, auth_token, live_trade=False):
        Tradier.__init__(self, account_number, auth_token, live_trade)
        self.FUNDAMENTALS_ENDPOINT = "/beta/markets/fundamentals/financials"  # GET


# Request wrappers
    def get_fundamentals(self, symbols, verbose=False):
        r = requests.get(
            url= f"{self.BASE_URL}/{self.FUNDAMENTALS_ENDPOINT}",
            params 	= {'symbols' :symbols},
            headers = self.REQUESTS_HEADERS
        )
        r.raise_for_status()

        data = r.json()

        if verbose:
            print(f"DATA:\n{data}\n")

        return data


#     def get_fundamentals_dividends(symbol):
#         response = requests.get(f"{TRADIER_BASE_URL}/dividends", params={"symbols": symbol}, headers=HEADERS)
#         return response.json()
#
#
#     def get_fundamentals_statistics(symbol):
#         response = requests.get(f"{TRADIER_BASE_URL}/statistics", params={"symbols": symbol}, headers=HEADERS)
#         return response.json()
#
#
# # Extractor using live data
# def extract_fundamentals_live(symbol):
#     try:
#         f = get_fundamentals_financials(symbol)
#         d = get_fundamentals_dividends(symbol)
#         s = get_fundamentals_statistics(symbol)
#
#         market_cap = float(s["statistics"]["valuation"]["market_cap"])
#         dividend_yield = float(s["statistics"]["dividend"]["dividend_yield"])
#         dividend_rate = float(s["statistics"]["dividend"]["dividend_rate"])
#         payout_ratio = float(s["statistics"]["dividend"]["payout_ratio"])
#         free_cash_flow_per_share = float(f["financials"]["statement"]["cash_flow"]["free_cash_flow"]["per_share"])
#         liquidity = int(s["statistics"]["liquidity"]["composite_rating"])
#         five_years_ago = datetime.today() - timedelta(days=5 * 365)
#         dividend_payments = sum(
#             1 for div in d["dividends"]["dividend"]
#             if datetime.strptime(div["ex_date"], "%Y-%m-%d") >= five_years_ago
#         )
#
#         return {
#             "symbol": symbol,
#             "market_cap": market_cap,
#             "dividend_yield": dividend_yield,
#             "free_cash_flow_per_share": free_cash_flow_per_share,
#             "dividend_rate": dividend_rate,
#             "dividend_payout_ratio": payout_ratio,
#             "liquidity": liquidity,
#             "dividend_payments_last_5y": dividend_payments
#         }
#
#     except Exception as e:
#         print(f"Error processing {symbol}: {e}")
#         return None


"""
import requests
import pandas as pd
from datetime import datetime, timedelta

# Configuration
TRADIER_API_TOKEN = "YOUR_TRADIER_API_TOKEN"  # Replace this with your actual token
TRADIER_BASE_URL = "https://api.tradier.com/v1/markets/fundamentals"
HEADERS = {
    "Authorization": f"Bearer {TRADIER_API_TOKEN}",
    "Accept": "application/json"
}

# Batch API calls
def get_fundamentals_financials_batch(symbols):
    joined = ",".join(symbols)
    response = requests.get(f"{TRADIER_BASE_URL}/financials", params={"symbols": joined}, headers=HEADERS)
    return response.json()

def get_fundamentals_dividends_batch(symbols):
    joined = ",".join(symbols)
    response = requests.get(f"{TRADIER_BASE_URL}/dividends", params={"symbols": joined}, headers=HEADERS)
    return response.json()

def get_fundamentals_statistics_batch(symbols):
    joined = ",".join(symbols)
    response = requests.get(f"{TRADIER_BASE_URL}/statistics", params={"symbols": joined}, headers=HEADERS)
    return response.json()

# Extract data per symbol from batch responses
def extract_fundamentals_batch(symbols):
    f = get_fundamentals_financials_batch(symbols)
    d = get_fundamentals_dividends_batch(symbols)
    s = get_fundamentals_statistics_batch(symbols)

    results = []

    for symbol in symbols:
        try:
            market_cap = float(s["statistics"][symbol]["valuation"]["market_cap"])
            dividend_yield = float(s["statistics"][symbol]["dividend"]["dividend_yield"])
            dividend_rate = float(s["statistics"][symbol]["dividend"]["dividend_rate"])
            payout_ratio = float(s["statistics"][symbol]["dividend"]["payout_ratio"])
            free_cash_flow_per_share = float(f["financials"][symbol]["statement"]["cash_flow"]["free_cash_flow"]["per_share"])
            liquidity = int(s["statistics"][symbol]["liquidity"]["composite_rating"])

            five_years_ago = datetime.today() - timedelta(days=5 * 365)
            dividend_payments = sum(
                1 for div in d["dividends"][symbol]["dividend"]
                if datetime.strptime(div["ex_date"], "%Y-%m-%d") >= five_years_ago
            )

            results.append({
                "symbol": symbol,
                "market_cap": market_cap,
                "dividend_yield": dividend_yield,
                "free_cash_flow_per_share": free_cash_flow_per_share,
                "dividend_rate": dividend_rate,
                "dividend_payout_ratio": payout_ratio,
                "liquidity": liquidity,
                "dividend_payments_last_5y": dividend_payments
            })

        except Exception as e:
            print(f"Error processing {symbol}: {e}")

    return pd.DataFrame(results)

# Screening logic
def apply_filters(df):
    return df[
        (df['market_cap'] >= 10e9) &
        (df['dividend_yield'] >= 0.02) &
        (df['free_cash_flow_per_share'] > df['dividend_rate']) &
        (df['dividend_payout_ratio'] <= 0.9) &
        (df['liquidity'] >= 2) &
        (df['dividend_payments_last_5y'] >= 10)
    ]

# Example usage
symbols = ['AAPL', 'MSFT', 'JNJ', 'XOM', 'KO']
df_all = extract_fundamentals_batch(symbols)
df_screened = apply_filters(df_all)
print(df_screened)

"""
