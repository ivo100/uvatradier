#
# Example - Using uvatradier to fetch quote data for a given symbol
#

import os
import dotenv
from uvatradier import Quotes
from icecream import ic

# Create .env file within current working directory.
# Add the following to your .env file. Specify the correct account number and authorization token for your quote.
# 	tradier_acct = <ACCOUNT_NUMBER>
#	tradier_token = <AUTH_TOKEN>

dotenv.load_dotenv()

live = False
if os.getenv('live'):
    s = os.getenv('live')
    if s.upper().startswith("T"):
        live = True

ic(live)

prefix = "tradier"
if not live:
    prefix = f"t_{prefix}"

acct = os.getenv(f"{prefix}_acct")
token = os.getenv(f"{prefix}_token")
assert acct
assert token

# Initializing new Quotes object
Q = Quotes(acct, token, live_trade=live)
sym = 'AAPL'
q = Q.get_quote_day(sym)
ic(q)

ts = Q.get_timesales(
    sym,
    interval="5min",
    start_time="2025-01-07T09:30:00",
    end_time="2025-01-07T16:00:00")

ic(ts)
