#
# Example - Using uvatradier to fetch quote data for a given symbol
#

import os
import dotenv

from uvatradier import Quotes, Account, OptionsData, Companies
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

#ic(live)
prefix = "tradier"
if not live:
    prefix = f"t_{prefix}"

acct = os.getenv(f"{prefix}_acct")
token = os.getenv(f"{prefix}_token")
assert acct
assert token
assert len(acct) == 8
assert len(token) > 10

def example1():
    Q = Quotes(acct, token, live_trade=live)
    sym = 'SPX'
    q = Q.get_quote_day(sym)
    ic(q)

    ts = Q.get_timesales(
        sym,
        interval="5min",
        start_time="2025-03-13T09:30:00",
        end_time="2025-03-13T16:00:00")
    ic(ts)


def example2(sym: str = 'SPY', dte: int=1):
    Q = Quotes(acct, token, live_trade=live)
    q = Q.get_quote_day(sym)
    r = q.iloc[0]
    price = r['last']
    print(f"{sym} : prev.close: {r.prevclose} last: {r['last']}")
    """
    ic(q.columns)
    ic| q.columns: Index(['symbol', 'description', 'exch', 'type', 'last', 'change', 'volume',
                      'open', 'high', 'low', 'close', 'bid', 'ask', 'change_percentage',
                      'average_volume', 'last_volume', 'trade_date', 'prevclose',
                      'week_52_high', 'week_52_low', 'bidsize', 'bidexch', 'bid_date',
                      'asksize', 'askexch', 'ask_date', 'root_symbols'],
                     dtype='object')
    """

    opt = OptionsData(acct, token, live_trade=live)
    exp = opt.get_closest_expiry(sym, 5)
    ic(exp)
    # chains = opt.get_chain_day(sym, exp)
    # ic(chains.columns)
    """
    https://www.barchart.com/stocks/quotes/$SPX/put-call-ratios
    smv_vol = "ORATS final implied volatility"
    higher implied volatility in call options suggests that traders expect upward price movements or higher uncertainty in the stock price
    higher implied volatility in put options suggests that traders expect downward price movements or higher uncertainty in the stock price
    """
    strike_low = price * 0.9
    strike_high = price * 1.1
    # filter by strike
    chains = opt.get_chain_day(sym, exp, strike_low = strike_low, strike_high = strike_high, greeks=True)
    df = chains.round(2).copy()

    df = df.drop(columns=["type", "exch", "bidexch", "askexch", 'ask_date', 'bid_date', 'underlying', 'contract_size', 'root_symbol', 'week_52_high', 'week_52_low', 'expiration_date', 'expiration_type','greeks.rho', 'greeks.phi', 'greeks.updated_at', 'greeks.bid_iv', 'greeks.ask_iv',"greeks.mid_iv", ])
    df = df.rename(columns={"greeks.delta": "delta", "greeks.gamma": "gamma", "greeks.theta": "theta", "greeks.vega": "vega", "greeks.smv_vol": "trad_vol"})

    # separate puts and calls
    puts = df.query('option_type == "put"')
    calls = df.query('option_type == "call"')

    print(f"filtered by strike price between {strike_low:.0f} and {strike_high:.0f}")
    print_stats(calls, puts)
    # filter by delta
    puts = puts.query('delta <= -0.2 and delta >= -0.7')
    calls = calls.query('delta >= 0.2 and delta <= 0.7')

    print("filtered by delta between 0.2 and 0.7")
    print_stats(calls, puts)



def print_stats(calls, puts):
    num_puts = len(puts)
    oi_puts = puts['open_interest'].sum()
    vol_puts = puts['volume'].sum()
    num_calls = len(calls)
    vol_calls = calls['volume'].sum()
    oi_calls = calls['open_interest'].sum()
    pcr = oi_puts / oi_calls
    pcvr = vol_puts / vol_calls
    print("")
    print(f"num strikes puts: {num_puts:6d}, calls: {num_calls:6d}")
    print(f"OI          puts: {oi_puts:6d}, calls: {oi_calls:6d},   PCR: {pcr:-6.02f}")
    print(f"volume      puts: {vol_puts:6d}, calls: {vol_calls:6d}, ratio: {pcvr:-6.02f} ")
    print("")
    calls = calls.sort_values(by=['volume','open_interest'], ascending=False)
    puts = puts.sort_values(by=[ 'volume','open_interest'], ascending=False)

    print("CALLS")
    for i, r in calls.head(2).iterrows():
        #print(f"{r.symbol} {r.strike:.2f}  ask: {r.ask:5.2f} bid: {r.bid:5.2f}  last: {r['last']:5.2f}  HLOC: {r.high:5.2f} {r.low:5.2f} {r.open:5.2f} {r.close:5.2f}   vol: {r.volume:6.0f} OI: {r.open_interest:6.0f} | delta: {r.delta:5.2f} gamma: {r.gamma:.2f} IV: {r.trad_vol:.2f}")
        print(f"{r.symbol} {r.strike:.2f}  ask: {r.ask:5.2f} bid: {r.bid:5.2f}  last: {r['last']:5.2f}     vol: {r.volume:6.0f} OI: {r.open_interest:6.0f} | delta: {r.delta:5.2f}  IV: {r.trad_vol:.2f}")

    print("PUTS")
    for i, r in puts.head(2).iterrows():
        print(f"{r.symbol} {r.strike:.2f}  ask: {r.ask:5.2f} bid: {r.bid:5.2f}  last: {r['last']:5.2f}     vol: {r.volume:6.0f} OI: {r.open_interest:6.0f} | delta: {r.delta:5.2f}  IV: {r.trad_vol:.2f}")
    print("===")


def example3():
    account = Account(acct, token, live_trade=live)
    # Fetch account balance info
    balance = account.get_account_balance(return_as_series=True)
    ic(balance)
    ic(balance.pdt)

def example4(sym: str = 'AAPL'):
    C = Companies(acct, token, live_trade=live)
    f = C.get_fundamentals(sym)
    print(f)
    market_cap = float(f["statistics"]["valuation"]["market_cap"])
    print(market_cap)


if __name__ == "__main__":
    #example1()
    #example2("SPY")
    #example3()
    example4()



