From: <Saved by Blink>
Snapshot-Content-Location: data:text/html, <html contenteditable>
Subject: 
Date: Thu, 27 Aug 2026 20:29:42 -0600
MIME-Version: 1.0
Content-Type: multipart/related;
	type="text/html";
	boundary="----MultipartBoundary--QB3sDX9OvVE1hrCkIVl38umoQvckZl5mXGxS0ISR81----"


------MultipartBoundary--QB3sDX9OvVE1hrCkIVl38umoQvckZl5mXGxS0ISR81----
Content-Type: text/html
Content-ID: <frame-720B12DB0BB22739BDE01CB6CABCB317@mhtml.blink>
Content-Transfer-Encoding: quoted-printable
Content-Location: data:text/html, <html contenteditable>

<html contenteditable=3D""><head><meta http-equiv=3D"Content-Type" content=
=3D"text/html; charset=3Dwindows-1252"></head><body><div>import requests</d=
iv><div>import os</div><div>from datetime import datetime, timedelta</div><=
div><br></div><div># --- CONFIGURATION ENGINE (SECURE VAULT SHORTCUTS) ---<=
/div><div>FMP_API_KEY =3D os.environ.get("FMP_API_KEY")</div><div>TELEGRAM_=
BOT_TOKEN =3D os.environ.get("TELEGRAM_BOT_TOKEN")</div><div>TELEGRAM_CHAT_=
ID =3D os.environ.get("TELEGRAM_CHAT_ID")</div><div><br></div><div>MY_STOCK=
S =3D ["MPLX", "SPCX", "CIEN", "CRWV", "SMCI", "FSK", "RWAY", "QFIN", "HTGC=
", "BXSL", "MU", "NOW", "TSM", "NVDA", "TSLA", "PLTR", "AGNC", "ARCC", "ET"=
, "HRZN", "MELI", "MRVL", "PSEC", "TRIN", "WES"]</div><div><br></div><div>d=
ef send_telegram(text_message):</div><div>&nbsp; &nbsp; """Secure direct ro=
uting pipeline shortcut layout"""</div><div>&nbsp; &nbsp; if not TELEGRAM_B=
OT_TOKEN or not TELEGRAM_CHAT_ID:</div><div>&nbsp; &nbsp; &nbsp; &nbsp; pri=
nt("Telegram keys missing from vault settings.")</div><div>&nbsp; &nbsp; &n=
bsp; &nbsp; return</div><div>&nbsp; &nbsp; telegram_url =3D f"https://teleg=
ram.org{TELEGRAM_BOT_TOKEN}/sendMessage"</div><div>&nbsp; &nbsp; payload =
=3D {"chat_id": TELEGRAM_CHAT_ID, "text": text_message}</div><div>&nbsp; &n=
bsp; try:</div><div>&nbsp; &nbsp; &nbsp; &nbsp; requests.post(telegram_url,=
 json=3Dpayload)</div><div>&nbsp; &nbsp; except Exception as e:</div><div>&=
nbsp; &nbsp; &nbsp; &nbsp; print(f"Telegram transmission error: {e}")</div>=
<div><br></div><div>def check_dividends():</div><div>&nbsp; &nbsp; if not F=
MP_API_KEY: return</div><div>&nbsp; &nbsp; target_date =3D (datetime.now() =
+ timedelta(days=3D14)).strftime("%Y-%m-%d")</div><div>&nbsp; &nbsp; url =
=3D f"https://financialmodelingprep.com{target_date}&amp;to=3D{target_date}=
&amp;apikey=3D{FMP_API_KEY}"</div><div>&nbsp; &nbsp; try:</div><div>&nbsp; =
&nbsp; &nbsp; &nbsp; response =3D requests.get(url).json()</div><div>&nbsp;=
 &nbsp; &nbsp; &nbsp; if response is None or isinstance(response, dict): re=
turn</div><div>&nbsp; &nbsp; &nbsp; &nbsp; alerts =3D [f"=95 {e.get('symbol=
')}: Ex-date {target_date} (Amt: ${e.get('dividend', 0)})" for e in respons=
e if e.get("symbol") in MY_STOCKS and e.get("dividend", 0) &gt; 0]</div><di=
v>&nbsp; &nbsp; &nbsp; &nbsp; if alerts: send_telegram("&#128176; 14-Day Di=
vidend Warning:\n" + "\n".join(alerts))</div><div>&nbsp; &nbsp; except Exce=
ption as e: print(f"Div error: {e}")</div><div><br></div><div>def check_ear=
nings():</div><div>&nbsp; &nbsp; if not FMP_API_KEY: return</div><div>&nbsp=
; &nbsp; target_date =3D (datetime.now() + timedelta(days=3D7)).strftime("%=
Y-%m-%d")</div><div>&nbsp; &nbsp; url =3D f"https://financialmodelingprep.c=
om{target_date}&amp;to=3D{target_date}&amp;apikey=3D{FMP_API_KEY}"</div><di=
v>&nbsp; &nbsp; try:</div><div>&nbsp; &nbsp; &nbsp; &nbsp; response =3D req=
uests.get(url).json()</div><div>&nbsp; &nbsp; &nbsp; &nbsp; if response is =
None or isinstance(response, dict): return</div><div>&nbsp; &nbsp; &nbsp; &=
nbsp; alerts =3D [f"=95 {e.get('symbol')} reports on {target_date} ({e.get(=
'time', 'unspecified')})" for e in response if e.get("symbol") in MY_STOCKS=
]</div><div>&nbsp; &nbsp; &nbsp; &nbsp; if alerts: send_telegram("&#128202;=
 7-Day Earnings Warning:\n" + "\n".join(alerts))</div><div>&nbsp; &nbsp; ex=
cept Exception as e: print(f"Earnings error: {e}")</div><div><br></div><div=
>def check_dividend_changes():</div><div>&nbsp; &nbsp; if not FMP_API_KEY: =
return</div><div>&nbsp; &nbsp; start_date =3D (datetime.now() - timedelta(d=
ays=3D1)).strftime("%Y-%m-%d")</div><div>&nbsp; &nbsp; end_date =3D datetim=
e.now().strftime("%Y-%m-%d")</div><div>&nbsp; &nbsp; url =3D f"https://fina=
ncialmodelingprep.com{start_date}&amp;to=3D{end_date}&amp;apikey=3D{FMP_API=
_KEY}"</div><div>&nbsp; &nbsp; try:</div><div>&nbsp; &nbsp; &nbsp; &nbsp; r=
esponse =3D requests.get(url).json()</div><div>&nbsp; &nbsp; &nbsp; &nbsp; =
if response is None or isinstance(response, dict): return</div><div>&nbsp; =
&nbsp; &nbsp; &nbsp; for event in response:</div><div>&nbsp; &nbsp; &nbsp; =
&nbsp; &nbsp; &nbsp; ticker =3D event.get("symbol")</div><div>&nbsp; &nbsp;=
 &nbsp; &nbsp; &nbsp; &nbsp; if ticker in MY_STOCKS:</div><div>&nbsp; &nbsp=
; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; current_payout =3D event.get("d=
ividend", 0)</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nb=
sp; if current_payout &lt;=3D 0: continue</div><div>&nbsp; &nbsp; &nbsp; &n=
bsp; &nbsp; &nbsp; &nbsp; &nbsp; hist_res =3D requests.get(f"https://financ=
ialmodelingprep.com{ticker}?apikey=3D{FMP_API_KEY}").json()</div><div>&nbsp=
; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if hist_res is None or i=
sinstance(hist_res, dict): continue</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &=
nbsp; &nbsp; &nbsp; &nbsp; historical_list =3D hist_res.get("historical", [=
])</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if len=
(historical_list) &gt; 1 and isinstance(historical_list, list):</div><div>&=
nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; prior_=
payout =3D historical_list.get("dividend", current_payout)</div><div>&nbsp;=
 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if current_=
payout &gt; prior_payout:</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbs=
p; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; send_telegram(f"&#128200; Divi=
dend Increase Declared!\n=95 {ticker} raised payout to ${current_payout} (w=
as ${prior_payout})")</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &=
nbsp; &nbsp; &nbsp; &nbsp; elif current_payout &lt; prior_payout:</div><div=
>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbs=
p; &nbsp; send_telegram(f"&#9888;&#65039; Dividend Cut Declared!\n=95 {tick=
er} lowered payout to ${current_payout} (was ${prior_payout})")</div><div>&=
nbsp; &nbsp; except Exception as e: print(f"Div change error: {e}")</div><d=
iv><br></div><div>def check_analyst_upgrades():</div><div>&nbsp; &nbsp; if =
not FMP_API_KEY: return</div><div>&nbsp; &nbsp; url =3D f"https://financial=
modelingprep.com{FMP_API_KEY}"</div><div>&nbsp; &nbsp; try:</div><div>&nbsp=
; &nbsp; &nbsp; &nbsp; response =3D requests.get(url).json()</div><div>&nbs=
p; &nbsp; &nbsp; &nbsp; if response is None or isinstance(response, dict): =
return</div><div>&nbsp; &nbsp; &nbsp; &nbsp; for e in response:</div><div>&=
nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ticker =3D e.get("symbol")</div><d=
iv>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if ticker in MY_STOCKS:</div><=
div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; new_g, prior_g,=
 firm =3D e.get("newGrade", ""), e.get("previousGrade", ""), e.get("grading=
Company", "Wall Street")</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp=
; &nbsp; &nbsp; if any(x in str(new_g) for x in ["Buy", "Outperform", "Over=
weight"]) and new_g !=3D prior_g:</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nb=
sp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; send_telegram(f"&#128640; Analyst Up=
grade Alert:\n=95 {ticker} upgraded to {new_g} (from {prior_g}) by {firm}!"=
)</div><div>&nbsp; &nbsp; except Exception as e: print(f"Analyst error: {e}=
")</div><div><br></div><div>def check_insider_buying():</div><div>&nbsp; &n=
bsp; if not FMP_API_KEY: return</div><div>&nbsp; &nbsp; url =3D f"https://f=
inancialmodelingprep.com{FMP_API_KEY}"</div><div>&nbsp; &nbsp; try:</div><d=
iv>&nbsp; &nbsp; &nbsp; &nbsp; response =3D requests.get(url).json()</div><=
div>&nbsp; &nbsp; &nbsp; &nbsp; if response is None or isinstance(response,=
 dict): return</div><div>&nbsp; &nbsp; &nbsp; &nbsp; for trade in response:=
</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ticker =3D trade.get("=
symbol")</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if ticker in M=
Y_STOCKS and any(x in str(trade.get("transactionType", "")) for x in ["Buy"=
, "Purchase"]):</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; =
&nbsp; shares, price =3D trade.get("securitiesTransacted", 0), trade.get("p=
rice", 0)</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;=
 total_value =3D int(shares * price)</div><div>&nbsp; &nbsp; &nbsp; &nbsp; =
&nbsp; &nbsp; &nbsp; &nbsp; if total_value &gt; 25000:</div><div>&nbsp; &nb=
sp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; send_telegram(f=
"&#128188; Smart Money Buying:\n=95 {trade.get('reportingName')} ({trade.ge=
t('officerTitle')}) bought ${total_value:,} of {ticker} on the open market!=
")</div><div>&nbsp; &nbsp; except Exception as e: print(f"Insider error: {e=
}")</div><div><br></div><div>def check_unusual_volume():</div><div>&nbsp; &=
nbsp; if not FMP_API_KEY: return</div><div>&nbsp; &nbsp; url =3D f"https://=
financialmodelingprep.com{FMP_API_KEY}"</div><div>&nbsp; &nbsp; try:</div><=
div>&nbsp; &nbsp; &nbsp; &nbsp; response =3D requests.get(url).json()</div>=
<div>&nbsp; &nbsp; &nbsp; &nbsp; if response is None or isinstance(response=
, dict): return</div><div>&nbsp; &nbsp; &nbsp; &nbsp; for item in response:=
</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ticker =3D item.get("s=
ymbol")</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if ticker in MY=
_STOCKS:</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; =
volume, avg_volume =3D item.get("volume", 0), item.get("avgVolume", 1)</div=
><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ratio =3D rou=
nd(volume / avg_volume, 1)</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nb=
sp; &nbsp; &nbsp; if ratio &gt;=3D 2.0:</div><div>&nbsp; &nbsp; &nbsp; &nbs=
p; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; send_telegram(f"&#128202; Unus=
ual Volume Spike:\n=95 {ticker} is trading at {ratio}x its normal average d=
aily volume right now!")</div><div>&nbsp; &nbsp; except Exception as e: pri=
nt(f"Volume error: {e}")</div><div><br></div><div>def check_technical_rsi()=
:</div><div>&nbsp; &nbsp; if not FMP_API_KEY: return</div><div>&nbsp; &nbsp=
; try:</div><div>&nbsp; &nbsp; &nbsp; &nbsp; for ticker in MY_STOCKS:</div>=
<div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; url =3D f"https://financialm=
odelingprep.com{ticker}?type=3Drsi&amp;period=3D14&amp;apikey=3D{FMP_API_KE=
Y}"</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; response =3D reques=
ts.get(url).json()</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if r=
esponse is None or isinstance(response, dict): continue</div><div>&nbsp; &n=
bsp; &nbsp; &nbsp; &nbsp; &nbsp; if isinstance(response, list) and len(resp=
onse) &gt; 0:</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &n=
bsp; current_rsi =3D response.get("rsi", 50)</div><div>&nbsp; &nbsp; &nbsp;=
 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if current_rsi &lt;=3D 30:</div><div>&n=
bsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; send_te=
legram(f"&#9889; Technical Oversold Alert:\n=95 {ticker} RSI has dropped to=
 {round(current_rsi, 1)} (Deep Value Buying Territory)!")</div><div>&nbsp; =
&nbsp; except Exception as e: print(f"RSI error: {e}")</div><div><br></div>=
<div>def check_heavy_price_swings():</div><div>&nbsp; &nbsp; if not FMP_API=
_KEY: return</div><div>&nbsp; &nbsp; tickers_string =3D ",".join(MY_STOCKS)=
</div><div>&nbsp; &nbsp; url =3D f"https://financialmodelingprep.com{ticker=
s_string}?apikey=3D{FMP_API_KEY}"</div><div>&nbsp; &nbsp; try:</div><div>&n=
bsp; &nbsp; &nbsp; &nbsp; response =3D requests.get(url).json()</div><div>&=
nbsp; &nbsp; &nbsp; &nbsp; if response is None or isinstance(response, dict=
): return</div><div>&nbsp; &nbsp; &nbsp; &nbsp; for stock in response:</div=
><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ticker =3D stock.get("symbo=
l")</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; change_percent =3D =
stock.get("changesPercentage", 0.0)</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &=
nbsp; &nbsp; current_price =3D stock.get("price", 0.0)</div><div>&nbsp; &nb=
sp; &nbsp; &nbsp; &nbsp; &nbsp; if abs(change_percent) &gt;=3D 5.0:</div><d=
iv>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; direction =3D "&=
#128200; Massive Gain" if change_percent &gt; 0 else "&#128201; Heavy Drop"=
</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; send_tel=
egram(f"{direction} Alert:\n=95 {ticker} moved {round(change_percent, 2)}% =
today! Current Price: ${current_price}")</div><div>&nbsp; &nbsp; except Exc=
eption as e: print(f"Price swing error: {e}")</div><div><br></div><div>def =
check_earnings_surprises():</div><div>&nbsp; &nbsp; if not FMP_API_KEY: ret=
urn</div><div>&nbsp; &nbsp; url =3D f"https://financialmodelingprep.com{FMP=
_API_KEY}"</div><div>&nbsp; &nbsp; try:</div><div>&nbsp; &nbsp; &nbsp; &nbs=
p; response =3D requests.get(url).json()</div><div>&nbsp; &nbsp; &nbsp; &nb=
sp; if response is None or isinstance(response, dict): return</div><div>&nb=
sp; &nbsp; &nbsp; &nbsp; for report in response:</div><div>&nbsp; &nbsp; &n=
bsp; &nbsp; &nbsp; &nbsp; ticker =3D report.get("symbol")</div><div>&nbsp; =
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if ticker in MY_STOCKS:</div><div>&nbsp;=
 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; actual_eps =3D report.get=
("actualEps")</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &n=
bsp; estimated_eps =3D report.get("estimatedEps")</div><div>&nbsp; &nbsp; &=
nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if actual_eps is None or estimated=
_eps is None or estimated_eps =3D=3D 0: continue</div><div>&nbsp; &nbsp; &n=
bsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; surprise_pct =3D ((actual_eps - est=
imated_eps) / abs(estimated_eps)) * 100</div><div>&nbsp; &nbsp; &nbsp; &nbs=
p; &nbsp; &nbsp; &nbsp; &nbsp; if abs(surprise_pct) &gt;=3D 10.0:</div><div=
>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; stat=
us =3D "&#128293; Positive Surprise (BEAT)" if surprise_pct &gt; 0 else "&#=
10052;&#65039; Negative Surprise (MISS)"</div><div>&nbsp; &nbsp; &nbsp; &nb=
sp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; send_telegram(f"&#127919; {st=
atus} Alert:\n=95 {ticker} just reported earnings!\n=95 Actual EPS: {actual=
_eps} vs Estimated: {estimated_eps} ({round(surprise_pct, 1)}% Surprise)")<=
/div><div>&nbsp; &nbsp; except Exception as e: print(f"Earnings surprise er=
ror: {e}")</div><div><br></div><div>if __name__ =3D=3D "__main__":</div><di=
v>&nbsp; &nbsp; send_telegram("&#128276; Terminal Operational Summary: Clou=
d scan initiated successfully.")</div><div>&nbsp; &nbsp; check_dividends()<=
/div><div>&nbsp; &nbsp; check_earnings()</div><div>&nbsp; &nbsp; check_divi=
dend_changes()</div><div>&nbsp; &nbsp; check_analyst_upgrades()</div><div>&=
nbsp; &nbsp; check_insider_buying()</div><div>&nbsp; &nbsp; check_unusual_v=
olume()</div><div>&nbsp; &nbsp; check_technical_rsi()</div><div>&nbsp; &nbs=
p; check_heavy_price_swings()</div><div>&nbsp; &nbsp; check_earnings_surpri=
ses()</div><div>&nbsp; &nbsp; send_telegram("&#128640; Victory Check: The s=
cript ran all functions completely!")</div><div><br></div></body></html>
------MultipartBoundary--QB3sDX9OvVE1hrCkIVl38umoQvckZl5mXGxS0ISR81------
