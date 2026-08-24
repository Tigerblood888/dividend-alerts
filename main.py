import requests
from datetime import datetime, timedelta

# --- CONFIGURATION ---
FMP_API_KEY = "OefKADASIS81FNIXFvv7KeaC8xjUekRo"
TELEGRAM_BOT_TOKEN = "8852179205:AAEPiOPnAk2Zg4A2v8B8T5y76t28TZm6JkE"
TELEGRAM_CHAT_ID = "8639836189"

MY_STOCKS = ["MPLX", "SPCX", "CIEN", "CRWV", "SMCI", "FSK", "RWAY", "QFIN", "HTGC", "BXSL", "MU", "NOW", "TSM", "NVDA", "TSLA", "PLTR", "AGNC", "ARCC", "ET", "HRZN", "MELI", "MRVL", "PSEC", "TRIN", "WES"]

def send_telegram(text_message):
    """Helper function to route alerts straight to your phone"""
    telegram_url = f"https://telegram.org{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text_message}
    requests.post(telegram_url, json=payload)

def check_dividends():
    target_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
    url = f"https://financialmodelingprep.com{target_date}&to={target_date}&apikey={FMP_API_KEY}"
    try:
        response = requests.get(url).json()
        if isinstance(response, dict): return
        alerts = [f"• {e.get('symbol')}: Ex-date {target_date} (Amt: ${e.get('dividend', 0)})" for e in response if e.get("symbol") in MY_STOCKS]
        if alerts: send_telegram("💰 14-Day Dividend Warning:\n" + "\n".join(alerts))
    except Exception as e: print(f"Div error: {e}")

def check_earnings():
    target_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    url = f"https://financialmodelingprep.com{target_date}&to={target_date}&apikey={FMP_API_KEY}"
    try:
        response = requests.get(url).json()
        if isinstance(response, dict): return
        alerts = [f"• {e.get('symbol')} reports on {target_date} ({e.get('time', 'unspecified')})" for e in response if e.get("symbol") in MY_STOCKS]
        if alerts: send_telegram("📊 7-Day Earnings Warning:\n" + "\n".join(alerts))
    except Exception as e: print(f"Earnings error: {e}")

def check_dividend_changes():
    start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")
    url = f"https://financialmodelingprep.com{start_date}&to={end_date}&apikey={FMP_API_KEY}"
    try:
        response = requests.get(url).json()
        if isinstance(response, dict): return
        for event in response:
            ticker = event.get("symbol")
            if ticker in MY_STOCKS:
                current_payout = event.get("dividend", 0)
                hist_res = requests.get(f"https://financialmodelingprep.com{ticker}?apikey={FMP_API_KEY}").json()
                historical_list = hist_res.get("historical", [])
                if len(historical_list) > 1 and isinstance(historical_list, list):
                    prior_payout = historical_list[1].get("dividend", current_payout)
                    if current_payout > prior_payout:
                        send_telegram(f"📈 Dividend Increase Declared!\n• {ticker} raised payout to ${current_payout} (was ${prior_payout})")
                    elif current_payout < prior_payout:
                        send_telegram(f"⚠️ Dividend Cut Declared!\n• {ticker} lowered payout to ${current_payout} (was ${prior_payout})")
    except Exception as e: print(f"Div change error: {e}")

def check_analyst_upgrades():
    url = f"https://financialmodelingprep.com{FMP_API_KEY}"
    try:
        response = requests.get(url).json()
        if isinstance(response, dict): return
        for e in response:
            ticker = e.get("symbol")
            if ticker in MY_STOCKS:
                new_g, prior_g, firm = e.get("newGrade", ""), e.get("previousGrade", ""), e.get("gradingCompany", "Wall Street")
                if any(x in str(new_g) for x in ["Buy", "Outperform", "Overweight"]) and new_g != prior_g:
                    send_telegram(f"🚀 Analyst Upgrade Alert:\n• {ticker} upgraded to {new_g} (from {prior_g}) by {firm}!")
    except Exception as e: print(f"Analyst error: {e}")

def check_insider_buying():
    url = f"https://financialmodelingprep.com{FMP_API_KEY}"
    try:
        response = requests.get(url).json()
        if isinstance(response, dict): return
        for trade in response:
            ticker = trade.get("symbol")
            if ticker in MY_STOCKS and any(x in str(trade.get("transactionType", "")) for x in ["Buy", "Purchase"]):
                shares, price = trade.get("securitiesTransacted", 0), trade.get("price", 0)
                total_value = int(shares * price)
                if total_value > 25000:
                    send_telegram(f"💼 Smart Money Buying:\n• {trade.get('reportingName')} ({trade.get('officerTitle')}) bought ${total_value:,} of {ticker} on the open market!")
    except Exception as e: print(f"Insider error: {e}")

def check_unusual_volume():
    url = f"https://financialmodelingprep.com{FMP_API_KEY}"
    try:
        response = requests.get(url).json()
        if isinstance(response, dict): return
        for item in response:
            ticker = item.get("symbol")
            if ticker in MY_STOCKS:
                volume, avg_volume = item.get("volume", 0), item.get("avgVolume", 1)
                ratio = round(volume / avg_volume, 1)
                if ratio >= 2.0:
                    send_telegram(f"📊 Unusual Volume Spike:\n• {ticker} is trading at {ratio}x its normal average daily volume right now!")
    except Exception as e: print(f"Volume error: {e}")

def check_technical_rsi():
    try:
        for ticker in MY_STOCKS:
            url = f"https://financialmodelingprep.com{ticker}?type=rsi&period=14&apikey={FMP_API_KEY}"
            response = requests.get(url).json()
            if isinstance(response, list) and len(response) > 0:
                current_rsi = response[0].get("rsi", 50)
                if current_rsi <= 30:
                    send_telegram(f"⚡ Technical Oversold Alert:\n• {ticker} RSI has dropped to {round(current_rsi, 1)} (Deep Value Buying Territory)!")
    except Exception as e: print(f"RSI error: {e}")

def check_heavy_price_swings():
    tickers_string = ",".join(MY_STOCKS)
    url = f"https://financialmodelingprep.com{tickers_string}?apikey={FMP_API_KEY}"
    try:
        response = requests.get(url).json()
        if isinstance(response, dict): return
        for stock in response:
            ticker = stock.get("symbol")
            change_percent = stock.get("changesPercentage", 0.0)
            current_price = stock.get("price", 0.0)
            # Temporarily set to 0.1% to guarantee your phone text pipes fire instantly!
            if abs(change_percent) >= 0.1:
                direction = "📈 Massive Gain" if change_percent > 0 else "📉 Heavy Drop"
                send_telegram(f"{direction} Alert:\n• {ticker} moved {round(change_percent, 2)}% today! Current Price: ${current_price}")
    except Exception as e: print(f"Price swing error: {e}")

def check_earnings_surprises():
    url = f"https://financialmodelingprep.com{FMP_API_KEY}"
    try:
        response = requests.get(url).json()
        if isinstance(response, dict): return
        for report in response:
            ticker = report.get("symbol")
            if ticker in MY_STOCKS:
                actual_eps = report.get("actualEps", 0.0)
                estimated_eps = report.get("estimatedEps", 0.0)
                if estimated_eps != 0:
                    surprise_pct = ((actual_eps - estimated_eps) / abs(estimated_eps)) * 100
                    if abs(surprise_pct) >= 10.0:
                        status = "🔥 Positive Surprise (BEAT)" if surprise_pct > 0 else "❄️ Negative Surprise (MISS)"
                        send_telegram(f"🎯 {status} Alert:\n• {ticker} just reported earnings!\n• Actual EPS: {actual_eps} vs Estimated: {estimated_eps} ({round(surprise_pct, 1)}% Surprise)")
    except Exception as e: print(f"Earnings surprise error: {e}")

if __name__ == "__main__":
        send_telegram("🔔 Terminal Operational Summary: Cloud scan initiated successfully.")
    
    check_dividends()
    check_earnings()
    check_dividend_changes()
    check_analyst_upgrades()
    check_insider_buying()
    check_unusual_volume()
    check_technical_rsi()
    check_heavy_price_swings()
    check_earnings_surprises()
