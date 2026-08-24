From: <Saved by Blink>
Snapshot-Content-Location: data:text/html, <html contenteditable>
Subject: 
Date: Mon, 24 Aug 2026 12:10:43 -0600
MIME-Version: 1.0
Content-Type: multipart/related;
	type="text/html";
	boundary="----MultipartBoundary--HHMZichpof0irAG7QStfFjMKb0FKfui5ZWnyiNWxoV----"


------MultipartBoundary--HHMZichpof0irAG7QStfFjMKb0FKfui5ZWnyiNWxoV----
Content-Type: text/html
Content-ID: <frame-B7C4EBAFEF07921C45164F233F656230@mhtml.blink>
Content-Transfer-Encoding: quoted-printable
Content-Location: data:text/html, <html contenteditable>

<html contenteditable=3D""><head><meta http-equiv=3D"Content-Type" content=
=3D"text/html; charset=3Dwindows-1252"></head><body><div><div>import reques=
ts</div><div>from datetime import datetime, timedelta</div><div><br></div><=
div># --- CONFIGURATION ---</div><div>FMP_API_KEY =3D "OefKADASIS81FNIXFvv7=
KeaC8xjUekRo"</div><div>TELEGRAM_BOT_TOKEN =3D "8852179205:AAEPiOPnAk2Zg4A2=
v8B8T5y76t28TZm6JkE"</div><div>TELEGRAM_CHAT_ID =3D "8639836189"</div><div>=
<br></div><div>MY_STOCKS =3D ["MPLX", "SPCX", "CIEN", "CRWV", "SMCI", "FSK"=
, "RWAY", "QFIN", "HTGC", "BXSL", "MU", "NOW", "TSM", "NVDA", "TSLA", "PLTR=
", "AGNC", "ARCC", "ET", "HRZN", "MELI", "MRVL", "PSEC", "TRIN", "WES"]</di=
v><div><br></div><div>def send_telegram(text_message):</div><div>&nbsp; &nb=
sp; """Helper function to route alerts straight to your phone"""</div><div>=
&nbsp; &nbsp; telegram_url =3D f"https://telegram.org{TELEGRAM_BOT_TOKEN}/s=
endMessage"</div><div>&nbsp; &nbsp; payload =3D {"chat_id": TELEGRAM_CHAT_I=
D, "text": text_message}</div><div>&nbsp; &nbsp; requests.post(telegram_url=
, json=3Dpayload)</div><div><br></div><div>def check_dividends():</div><div=
>&nbsp; &nbsp; target_date =3D (datetime.now() + timedelta(days=3D14)).strf=
time("%Y-%m-%d")</div><div>&nbsp; &nbsp; url =3D f"https://financialmodelin=
gprep.com{target_date}&amp;to=3D{target_date}&amp;apikey=3D{FMP_API_KEY}"</=
div><div>&nbsp; &nbsp; try:</div><div>&nbsp; &nbsp; &nbsp; &nbsp; response =
=3D requests.get(url).json()</div><div>&nbsp; &nbsp; &nbsp; &nbsp; if isins=
tance(response, dict): return</div><div>&nbsp; &nbsp; &nbsp; &nbsp; alerts =
=3D [f"=95 {e.get('symbol')}: Ex-date {target_date} (Amt: ${e.get('dividend=
', 0)})" for e in response if e.get("symbol") in MY_STOCKS]</div><div>&nbsp=
; &nbsp; &nbsp; &nbsp; if alerts: send_telegram("&#128176; 14-Day Dividend =
Warning:\n" + "\n".join(alerts))</div><div>&nbsp; &nbsp; except Exception a=
s e: print(f"Div error: {e}")</div><div><br></div><div>def check_earnings()=
:</div><div>&nbsp; &nbsp; target_date =3D (datetime.now() + timedelta(days=
=3D7)).strftime("%Y-%m-%d")</div><div>&nbsp; &nbsp; url =3D f"https://finan=
cialmodelingprep.com{target_date}&amp;to=3D{target_date}&amp;apikey=3D{FMP_=
API_KEY}"</div><div>&nbsp; &nbsp; try:</div><div>&nbsp; &nbsp; &nbsp; &nbsp=
; response =3D requests.get(url).json()</div><div>&nbsp; &nbsp; &nbsp; &nbs=
p; if isinstance(response, dict): return</div><div>&nbsp; &nbsp; &nbsp; &nb=
sp; alerts =3D [f"=95 {e.get('symbol')} reports on {target_date} ({e.get('t=
ime', 'unspecified')})" for e in response if e.get("symbol") in MY_STOCKS]<=
/div><div>&nbsp; &nbsp; &nbsp; &nbsp; if alerts: send_telegram("&#128202; 7=
-Day Earnings Warning:\n" + "\n".join(alerts))</div><div>&nbsp; &nbsp; exce=
pt Exception as e: print(f"Earnings error: {e}")</div><div><br></div><div>d=
ef check_dividend_changes():</div><div>&nbsp; &nbsp; start_date =3D (dateti=
me.now() - timedelta(days=3D1)).strftime("%Y-%m-%d")</div><div>&nbsp; &nbsp=
; end_date =3D datetime.now().strftime("%Y-%m-%d")</div><div>&nbsp; &nbsp; =
url =3D f"https://financialmodelingprep.com{start_date}&amp;to=3D{end_date}=
&amp;apikey=3D{FMP_API_KEY}"</div><div>&nbsp; &nbsp; try:</div><div>&nbsp; =
&nbsp; &nbsp; &nbsp; response =3D requests.get(url).json()</div><div>&nbsp;=
 &nbsp; &nbsp; &nbsp; if isinstance(response, dict): return</div><div>&nbsp=
; &nbsp; &nbsp; &nbsp; for event in response:</div><div>&nbsp; &nbsp; &nbsp=
; &nbsp; &nbsp; &nbsp; ticker =3D event.get("symbol")</div><div>&nbsp; &nbs=
p; &nbsp; &nbsp; &nbsp; &nbsp; if ticker in MY_STOCKS:</div><div>&nbsp; &nb=
sp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; current_payout =3D event.get(=
"dividend", 0)</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &=
nbsp; hist_res =3D requests.get(f"https://financialmodelingprep.com{ticker}=
?apikey=3D{FMP_API_KEY}").json()</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbs=
p; &nbsp; &nbsp; &nbsp; historical_list =3D hist_res.get("historical", [])<=
/div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if len(hi=
storical_list) &gt; 1 and isinstance(historical_list, list):</div><div>&nbs=
p; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; prior_pay=
out =3D historical_list.get("dividend", current_payout)</div><div>&nbsp; &n=
bsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if current_pay=
out &gt; prior_payout:</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; =
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; send_telegram(f"&#128200; Dividen=
d Increase Declared!\n=95 {ticker} raised payout to ${current_payout} (was =
${prior_payout})")</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbs=
p; &nbsp; &nbsp; &nbsp; elif current_payout &lt; prior_payout:</div><div>&n=
bsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; =
&nbsp; send_telegram(f"&#9888;&#65039; Dividend Cut Declared!\n=95 {ticker}=
 lowered payout to ${current_payout} (was ${prior_payout})")</div><div>&nbs=
p; &nbsp; except Exception as e: print(f"Div change error: {e}")</div><div>=
<br></div><div>def check_analyst_upgrades():</div><div>&nbsp; &nbsp; url =
=3D f"https://financialmodelingprep.com{FMP_API_KEY}"</div><div>&nbsp; &nbs=
p; try:</div><div>&nbsp; &nbsp; &nbsp; &nbsp; response =3D requests.get(url=
).json()</div><div>&nbsp; &nbsp; &nbsp; &nbsp; if isinstance(response, dict=
): return</div><div>&nbsp; &nbsp; &nbsp; &nbsp; for e in response:</div><di=
v>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ticker =3D e.get("symbol")</div=
><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if ticker in MY_STOCKS:</di=
v><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; new_g, prior=
_g, firm =3D e.get("newGrade", ""), e.get("previousGrade", ""), e.get("grad=
ingCompany", "Wall Street")</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &n=
bsp; &nbsp; &nbsp; if any(x in str(new_g) for x in ["Buy", "Outperform", "O=
verweight"]) and new_g !=3D prior_g:</div><div>&nbsp; &nbsp; &nbsp; &nbsp; =
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; send_telegram(f"&#128640; Analyst=
 Upgrade Alert:\n=95 {ticker} upgraded to {new_g} (from {prior_g}) by {firm=
}!")</div><div>&nbsp; &nbsp; except Exception as e: print(f"Analyst error: =
{e}")</div><div><br></div><div>def check_insider_buying():</div><div>&nbsp;=
 &nbsp; url =3D f"https://financialmodelingprep.com{FMP_API_KEY}"</div><div=
>&nbsp; &nbsp; try:</div><div>&nbsp; &nbsp; &nbsp; &nbsp; response =3D requ=
ests.get(url).json()</div><div>&nbsp; &nbsp; &nbsp; &nbsp; if isinstance(re=
sponse, dict): return</div><div>&nbsp; &nbsp; &nbsp; &nbsp; for trade in re=
sponse:</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ticker =3D trad=
e.get("symbol")</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if tick=
er in MY_STOCKS and any(x in str(trade.get("transactionType", "")) for x in=
 ["Buy", "Purchase"]):</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; =
&nbsp; &nbsp; shares, price =3D trade.get("securitiesTransacted", 0), trade=
.get("price", 0)</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;=
 &nbsp; total_value =3D int(shares * price)</div><div>&nbsp; &nbsp; &nbsp; =
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if total_value &gt; 25000:</div><div>&nb=
sp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; send_tel=
egram(f"&#128188; Smart Money Buying:\n=95 {trade.get('reportingName')} ({t=
rade.get('officerTitle')}) bought ${total_value:,} of {ticker} on the open =
market!")</div><div>&nbsp; &nbsp; except Exception as e: print(f"Insider er=
ror: {e}")</div><div><br></div><div>def check_unusual_volume():</div><div>&=
nbsp; &nbsp; url =3D f"https://financialmodelingprep.com{FMP_API_KEY}"</div=
><div>&nbsp; &nbsp; try:</div><div>&nbsp; &nbsp; &nbsp; &nbsp; response =3D=
 requests.get(url).json()</div><div>&nbsp; &nbsp; &nbsp; &nbsp; if isinstan=
ce(response, dict): return</div><div>&nbsp; &nbsp; &nbsp; &nbsp; for item i=
n response:</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ticker =3D =
item.get("symbol")</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if t=
icker in MY_STOCKS:</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nb=
sp; &nbsp; volume, avg_volume =3D item.get("volume", 0), item.get("avgVolum=
e", 1)</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ra=
tio =3D round(volume / avg_volume, 1)</div><div>&nbsp; &nbsp; &nbsp; &nbsp;=
 &nbsp; &nbsp; &nbsp; &nbsp; if ratio &gt;=3D 2.0:</div><div>&nbsp; &nbsp; =
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; send_telegram(f"&#1=
28202; Unusual Volume Spike:\n=95 {ticker} is trading at {ratio}x its norma=
l average daily volume right now!")</div><div>&nbsp; &nbsp; except Exceptio=
n as e: print(f"Volume error: {e}")</div><div><br></div><div>def check_tech=
nical_rsi():</div><div>&nbsp; &nbsp; try:</div><div>&nbsp; &nbsp; &nbsp; &n=
bsp; for ticker in MY_STOCKS:</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; =
&nbsp; url =3D f"https://financialmodelingprep.com{ticker}?type=3Drsi&amp;p=
eriod=3D14&amp;apikey=3D{FMP_API_KEY}"</div><div>&nbsp; &nbsp; &nbsp; &nbsp=
; &nbsp; &nbsp; response =3D requests.get(url).json()</div><div>&nbsp; &nbs=
p; &nbsp; &nbsp; &nbsp; &nbsp; if isinstance(response, list) and len(respon=
se) &gt; 0:</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbs=
p; current_rsi =3D response.get("rsi", 50)</div><div>&nbsp; &nbsp; &nbsp; &=
nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if current_rsi &lt;=3D 30:</div><div>&nbs=
p; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; send_tele=
gram(f"&#9889; Technical Oversold Alert:\n=95 {ticker} RSI has dropped to {=
round(current_rsi, 1)} (Deep Value Buying Territory)!")</div><div>&nbsp; &n=
bsp; except Exception as e: print(f"RSI error: {e}")</div><div><br></div><d=
iv>def check_heavy_price_swings():</div><div>&nbsp; &nbsp; tickers_string =
=3D ",".join(MY_STOCKS)</div><div>&nbsp; &nbsp; url =3D f"https://financial=
modelingprep.com{tickers_string}?apikey=3D{FMP_API_KEY}"</div><div>&nbsp; &=
nbsp; try:</div><div>&nbsp; &nbsp; &nbsp; &nbsp; response =3D requests.get(=
url).json()</div><div>&nbsp; &nbsp; &nbsp; &nbsp; if isinstance(response, d=
ict): return</div><div>&nbsp; &nbsp; &nbsp; &nbsp; for stock in response:</=
div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ticker =3D stock.get("sy=
mbol")</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; change_percent =
=3D stock.get("changesPercentage", 0.0)</div><div>&nbsp; &nbsp; &nbsp; &nbs=
p; &nbsp; &nbsp; current_price =3D stock.get("price", 0.0)</div><div>&nbsp;=
 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if abs(change_percent) &gt;=3D 5.0:</di=
v><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; direction =
=3D "&#128200; Massive Gain" if change_percent &gt; 0 else "&#128201; Heavy=
 Drop"</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; se=
nd_telegram(f"{direction} Alert:\n=95 {ticker} moved {round(change_percent,=
 2)}% today! Current Price: ${current_price}")</div><div>&nbsp; &nbsp; exce=
pt Exception as e: print(f"Price swing error: {e}")</div><div><br></div><di=
v>def check_earnings_surprises():</div><div>&nbsp; &nbsp; url =3D f"https:/=
/financialmodelingprep.com{FMP_API_KEY}"</div><div>&nbsp; &nbsp; try:</div>=
<div>&nbsp; &nbsp; &nbsp; &nbsp; response =3D requests.get(url).json()</div=
><div>&nbsp; &nbsp; &nbsp; &nbsp; if isinstance(response, dict): return</di=
v><div>&nbsp; &nbsp; &nbsp; &nbsp; for report in response:</div><div>&nbsp;=
 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ticker =3D report.get("symbol")</div><d=
iv>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if ticker in MY_STOCKS:</div><=
div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; actual_eps =3D =
report.get("actualEps", 0.0)</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &=
nbsp; &nbsp; &nbsp; estimated_eps =3D report.get("estimatedEps", 0.0)</div>=
<div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if estimated_e=
ps !=3D 0:</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp=
; &nbsp; &nbsp; surprise_pct =3D ((actual_eps - estimated_eps) / abs(estima=
ted_eps)) * 100</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; =
&nbsp; &nbsp; &nbsp; if abs(surprise_pct) &gt;=3D 10.0:</div><div>&nbsp; &n=
bsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; =
status =3D "&#128293; Positive Surprise (BEAT)" if surprise_pct &gt; 0 else=
 "&#10052;&#65039; Negative Surprise (MISS)"</div><div>&nbsp; &nbsp; &nbsp;=
 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; send_telegr=
am(f"&#127919; {status} Alert:\n=95 {ticker} just reported earnings!\n=95 A=
ctual EPS: {actual_eps} vs Estimated: {estimated_eps} ({round(surprise_pct,=
 1)}% Surprise)")</div><div>&nbsp; &nbsp; except Exception as e: print(f"Ea=
rnings surprise error: {e}")</div><div><br></div><div>if __name__ =3D=3D "_=
_main__":</div><div>&nbsp; &nbsp; send_telegram("&#128276; Terminal Operati=
onal Summary: Cloud scan initiated successfully.")</div><div>&nbsp; &nbsp; =
check_dividends()</div><div>&nbsp; &nbsp; check_earnings()</div><div>&nbsp;=
 &nbsp; check_dividend_changes()</div><div>&nbsp; &nbsp; check_analyst_upgr=
ades()</div><div>&nbsp; &nbsp; check_insider_buying()</div><div>&nbsp; &nbs=
p; check_unusual_volume()</div><div>&nbsp; &nbsp; check_technical_rsi()</di=
v><div>&nbsp; &nbsp; check_heavy_price_swings()</div><div>&nbsp; &nbsp; che=
ck_earnings_surprises()</div></div><div><br></div></body></html>
------MultipartBoundary--HHMZichpof0irAG7QStfFjMKb0FKfui5ZWnyiNWxoV------
