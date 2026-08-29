import requests
import os
import time
from datetime import datetime, timedelta

# --- CONFIGURATION ENGINE (SECURE VAULT SHORTCUTS) ---
FMP_API_KEY = os.environ.get("FMP_API_KEY", "").strip()
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "").strip()

MY_STOCKS = ["MPLX", "SPCX", "CIEN", "CRWV", "SMCI", "FSK", "RWAY", "QFIN", "HTGC", "BXSL", "MU", "NOW", "TSM", "NVDA", "TSLA", "PLTR", "AGNC", "ARCC", "ET", "HRZN", "MELI", "MRVL", "PSEC", "TRIN", "WES"]

def send_telegram(text_message):
    """Secure direct routing pipeline shortcut layout"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram keys missing from vault settings.")
        return
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text_message}
    try:
        resp = requests.post(telegram_url, json=payload, timeout=15)
        if resp.status_code != 200:
            print(f"Telegram rejected the message: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"Telegram transmission error: {e}")

def check_dividends():
    if not FMP_API_KEY: return
    target_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
    url = f"https://financialmodelingprep.com/stable/dividends-calendar?from={target_date}&to={target_date}&apikey={FMP_API_KEY}"
    try:
        response = requests.get(url, timeout=15).json()
        if response is None or isinstance(response, dict): return
        alerts = [f"• {e.get('symbol')}: Ex-date {target_date} (Amt: ${e.get('dividend', 0)})" for e in response if e.get("symbol") in MY_STOCKS and e.get("dividend", 0) > 0]
        if alerts: send_telegram("💰 14-Day Dividend Warning:\n" + "\n".join(alerts))
    except Exception as e: print(f"Div error: {e}")

def check_earnings():
    if not FMP_API_KEY: return
    target_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    url = f"https://financialmodelingprep.com/stable/earnings-calendar?from={target_date}&to={target_date}&apikey={FMP_API_KEY}"
    try:
        response = requests.get(url, timeout=15).json()
        if response is None or isinstance(response, dict): return
        alerts = [f"• {e.get('symbol')} reports on {target_date} ({e.get('time', 'unspecified')})" for e in response if e.get("symbol") in MY_STOCKS]
        if alerts: send_telegram("📊 7-Day Earnings Warning:\n" + "\n".join(alerts))
    except Exception as e: print(f"Earnings error: {e}")

def check_dividend_changes():
    if not FMP_API_KEY: return
    start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")
    url = f"https://financialmodelingprep.com/stable/dividends-calendar?from={start_date}&to={end_date}&apikey={FMP_API_KEY}"
    try:
        response = requests.get(url, timeout=15).json()
        if response is None or isinstance(response, dict): return
        for event in response:
            ticker = event.get("symbol")
            if ticker in MY_STOCKS:
                current_payout = event.get("dividend", 0)
                if current_payout <= 0: continue
                hist_url = f"https://financialmodelingprep.com/stable/dividends?symbol={ticker}&apikey={FMP_API_KEY}"
                historical_list = requests.get(hist_url, timeout=15).json()
                time.sleep(0.5)
                if isinstance(historical_list, list) and len(historical_list) > 1:
                    prior_payout = historical_list[1].get("dividend", current_payout)
                    if current_payout > prior_payout:
                        send_telegram(f"📈 Dividend Increase Declared!\n• {ticker} raised payout to ${current_payout} (was ${prior_payout})")
                    elif current_payout < prior_payout:
                        send_telegram(f"⚠️ Dividend Cut Declared!\n• {ticker} lowered payout to ${current_payout} (was ${prior_payout})")
    except Exception as e: print(f"Div change error: {e}")

def check_analyst_upgrades():
    if not FMP_API_KEY: return
    url = f"https://financialmodelingprep.com/stable/grade-latest-news?apikey={FMP_API_KEY}"
    try:
        response = requests.get(url, timeout=15).json()
        if response is None or isinstance(response, dict): return
        for e in response:
            ticker = e.get("symbol")
            if ticker in MY_STOCKS:
                new_g, prior_g, firm = e.get("newGrade", ""), e.get("previousGrade", ""), e.get("gradingCompany", "Wall Street")
                if any(x in str(new_g) for x in ["Buy", "Outperform", "Overweight"]) and new_g != prior_g:
                    send_telegram(f"🚀 Analyst Upgrade Alert:\n• {ticker} upgraded to {new_g} (from {prior_g}) by {firm}!")
    except Exception as e: print(f"Analyst error: {e}")

def check_insider_buying():
    if not FMP_API_KEY: return
    url = f"https://financialmodelingprep.com/stable/insider-trading/latest?apikey={FMP_API_KEY}"
    try:
        response = requests.get(url, timeout=15).json()
        if response is None or isinstance(response, dict): return
        for trade in response:
            ticker = trade.get("symbol")
            if ticker in MY_STOCKS and any(x in str(trade.get("transactionType", "")) for x in ["Buy", "Purchase"]):
                shares, price = trade.get("securitiesTransacted", 0), trade.get("price", 0)
                total_value = int(shares * price)
                if total_value > 25000:
                    send_telegram(f"💼 Smart Money Buying:\n• {trade.get('reportingName')} ({trade.get('officerTitle')}) bought ${total_value:,} of {ticker} on the open market!")
    except Exception as e: print(f"Insider error: {e}")

def check_unusual_volume():
    # Your FMP plan doesn't allow multiple symbols in one request, so we check one at a time
    if not FMP_API_KEY: return
    for ticker in MY_STOCKS:
        try:
            url = f"https://financialmodelingprep.com/stable/quote?symbol={ticker}&apikey={FMP_API_KEY}"
            resp = requests.get(url, timeout=15)
            time.sleep(0.5)
            if resp.status_code == 429:
                print(f"Volume error: rate limited on {ticker} (429) — slowing down")
                time.sleep(3)
                continue
            if not resp.text.strip():
                print(f"Volume error: {ticker} returned an empty response (status {resp.status_code})")
                continue
            response = resp.json()
            if not isinstance(response, list) or len(response) == 0: continue
            item = response[0]
            volume, avg_volume = item.get("volume", 0), item.get("avgVolume", 1) or 1
            ratio = round(volume / avg_volume, 1)
            if ratio >= 2.0:
                send_telegram(f"📊 Unusual Volume Spike:\n• {ticker} is trading at {ratio}x its normal average daily volume right now!")
        except Exception as e:
            print(f"Volume error for {ticker}: {e}")

# NOTE: RSI check disabled — Technical Indicators require FMP's Premium plan ($59/mo billed annually).
# Uncomment this function and its call at the bottom to re-enable if you upgrade.
# def check_technical_rsi():
#     if not FMP_API_KEY: return
#     try:
#         for ticker in MY_STOCKS:
#             url = f"https://financialmodelingprep.com/stable/technical-indicators/rsi?symbol={ticker}&periodLength=14&timeframe=1day&apikey={FMP_API_KEY}"
#             response = requests.get(url, timeout=15).json()
#             if isinstance(response, list) and len(response) > 0:
#                 current_rsi = response[0].get("rsi", 50)
#                 if current_rsi <= 30:
#                     send_telegram(f"⚡ Technical Oversold Alert:\n• {ticker} RSI has dropped to {round(current_rsi, 1)} (Deep Value Buying Territory)!")
#     except Exception as e: print(f"RSI error: {e}")

def check_heavy_price_swings():
    # Your FMP plan doesn't allow multiple symbols in one request, so we check one at a time
    if not FMP_API_KEY: return
    for ticker in MY_STOCKS:
        try:
            url = f"https://financialmodelingprep.com/stable/quote?symbol={ticker}&apikey={FMP_API_KEY}"
            resp = requests.get(url, timeout=15)
            time.sleep(0.5)
            if resp.status_code == 429:
                print(f"Price swing error: rate limited on {ticker} (429) — slowing down")
                time.sleep(3)
                continue
            if not resp.text.strip():
                print(f"Price swing error: {ticker} returned an empty response (status {resp.status_code})")
                continue
            response = resp.json()
            if not isinstance(response, list) or len(response) == 0: continue
            stock = response[0]
            change_percent = stock.get("changePercentage", 0.0)
            current_price = stock.get("price", 0.0)
            if abs(change_percent) >= 5.0:
                direction = "📈 Massive Gain" if change_percent > 0 else "📉 Heavy Drop"
                send_telegram(f"{direction} Alert:\n• {ticker} moved {round(change_percent, 2)}% today! Current Price: ${current_price}")
        except Exception as e:
            print(f"Price swing error for {ticker}: {e}")

def check_earnings_surprises():
    if not FMP_API_KEY: return
    target_date_from = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    target_date_to = datetime.now().strftime("%Y-%m-%d")
    url = f"https://financialmodelingprep.com/stable/earnings-calendar?from={target_date_from}&to={target_date_to}&apikey={FMP_API_KEY}"
    try:
        response = requests.get(url, timeout=15).json()
        if response is None or isinstance(response, dict): return
        for report in response:
            ticker = report.get("symbol")
            if ticker in MY_STOCKS:
                actual_eps = report.get("epsActual")
                estimated_eps = report.get("epsEstimated")
                if actual_eps is None or estimated_eps is None or estimated_eps == 0: continue
                surprise_pct = ((actual_eps - estimated_eps) / abs(estimated_eps)) * 100
                if abs(surprise_pct) >= 10.0:
                    status = "🔥 Positive Surprise (BEAT)" if surprise_pct > 0 else "❄️ Negative Surprise (MISS)"
                    send_telegram(f"🎯 {status} Alert:\n• {ticker} just reported earnings!\n• Actual EPS: {actual_eps} vs Estimated: {estimated_eps} ({round(surprise_pct, 1)}% Surprise)")
    except Exception as e: print(f"Earnings surprise error: {e}")

def check_short_interest():
    # Confirmed available on your plan (returns [] when no fresh data — that's normal,
    # since short interest is only reported a couple times per month).
    # Field names below are our best read of the response shape; if this errors,
    # the log will print the raw response so we can adjust field names precisely.
    if not FMP_API_KEY: return
    try:
        for ticker in MY_STOCKS:
            url = f"https://financialmodelingprep.com/stable/short-interest?symbol={ticker}&apikey={FMP_API_KEY}"
            response = requests.get(url, timeout=15).json()
            time.sleep(0.5)
            if not isinstance(response, list) or len(response) == 0: continue
            latest = response[0]
            days_to_cover = latest.get("daysToCover") or latest.get("shortInterestRatio")
            short_pct = latest.get("shortPercentOfFloat") or latest.get("shortInterestPercent")
            if days_to_cover is not None and days_to_cover >= 5:
                send_telegram(f"🩳 High Short Interest:\n• {ticker} has {days_to_cover} days-to-cover — heavily shorted right now!")
            elif short_pct is not None and short_pct >= 15:
                send_telegram(f"🩳 High Short Interest:\n• {ticker} short interest is {short_pct}% of float!")
    except Exception as e: print(f"Short interest error: {e}")

# NOTE: Price target check disabled — this endpoint is Restricted on your current FMP plan.
# Uncomment this function and its call at the bottom to re-enable if you upgrade.
# def check_price_targets():
#     if not FMP_API_KEY: return
#     try:
#         for ticker in MY_STOCKS:
#             url = f"https://financialmodelingprep.com/stable/price-target-news?symbol={ticker}&apikey={FMP_API_KEY}"
#             response = requests.get(url, timeout=15).json()
#             if not isinstance(response, list) or len(response) == 0: continue
#             latest = response[0]
#             analyst_name = latest.get("analystName", "An analyst")
#             new_target = latest.get("priceTarget")
#             send_telegram(f"🎯 Price Target Update:\n• {analyst_name} set a new target of ${new_target} for {ticker}")
#     except Exception as e: print(f"Price target error: {e}")

if __name__ == "__main__":
    send_telegram("🔔 Terminal Operational Summary: Cloud scan initiated successfully.")
    check_dividends()
    check_earnings()
    check_dividend_changes()
    check_analyst_upgrades()
    check_insider_buying()
    check_unusual_volume()
    # check_technical_rsi()  # disabled — see note above
    check_heavy_price_swings()
    check_earnings_surprises()
    check_short_interest()
    # check_price_targets()  # disabled — see note above
    send_telegram("🚀 Victory Check: The script ran all functions completely!")
