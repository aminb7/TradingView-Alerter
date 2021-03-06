from tvDatafeed import TvDatafeed, Interval
import time
import os
from tabulate import tabulate
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Currency:
    def __init__(self, symbol=""):
        self.symbol = symbol
        self.changes = 0.0
        self.hist = None
        self.currentCandleChanges = None
        self.lastCandleChanges = None

def create_currencies(symbols):
    currencies = []
    for symbol in symbols:
        currencies.append(Currency(symbol))

    return currencies

class Alerter:
    def __init__(self, sender_pass, receiver_address):
        self.sender_address = 'tradingviewalerter1@gmail.com'
        self.sender_pass = sender_pass
        self.receiver_address = receiver_address
    
    def email(self, subject):
        message = MIMEMultipart()
        message['From'] = self.sender_address
        message['To'] = self.receiver_address
        message['Subject'] = 'Tradingview Alerter: ' + subject

        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(self.sender_address, self.sender_pass)
        text = message.as_string()
        session.sendmail(self.sender_address, self.receiver_address, text)
        session.quit()

    def beep(self, sound):
        beep_command = "if [ \"$1\" = --list ];     then         find \
            /usr/share/sounds -type f -exec basename {} \; | sort -n \
            | tr '\n' ' '; echo;     else         \paplay \
            $(find /usr/share/sounds -type f -iname \"" + sound + "*\" | head -1);     fi"
        os.system(beep_command)

class TradingViewManager:
    def __init__(self, currencies, exchange, candle_interval, alerter):
        self.currencies = currencies
        self.exchange = exchange
        self.candle_interval = candle_interval
        self.tv = TvDatafeed()
        self.alerter = alerter

    def update_currency_hists(self):
        currency_hists = []
        for currency in self.currencies:
            currency.hist = self.tv.get_hist(currency.symbol, self.exchange, self.candle_interval)
            currency.currentCandleChanges = (currency.hist.iloc[-1, :].at["close"]  - currency.hist.iloc[-1, :].at["open"]) / currency.hist.iloc[-1, :].at["open"]
            currency.lastCandleChanges = (currency.hist.iloc[-2, :].at["close"] - currency.hist.iloc[-2, :].at["open"]) / currency.hist.iloc[-2, :].at["open"]

    def must_alert(self, currency):
        return currency.currentCandleChanges * 100 > 0.7 or currency.lastCandleChanges * 100 > 0.7

    def show_currency_pannels(self):
        columns = ["Date", "Symbol", "Last Candle Changes",
                "Current Candle Changes", "Last Candle Open","Last Candle Close"]
        table = []

        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        for currency in self.currencies:
            curr_changes = round(currency.lastCandleChanges * 100, 3)
            last_changes = round(currency.currentCandleChanges * 100, 3)

            curr_changes_str = str(curr_changes) + " %"
            last_changes_str = str(last_changes) + " %"
            
            if self.must_alert(currency):
                message = currency.symbol + " " + last_changes_str + " " + curr_changes_str
                self.alerter.email(message)
                self.alerter.beep("Slick")

            row = [currency.hist.iloc[-1, :].name,
                    currency.symbol,
                    "\033[92m {}\033[00m".format(curr_changes_str) if (curr_changes > 0) else "\033[91m {}\033[00m".format(curr_changes_str),
                    "\033[92m {}\033[00m".format(last_changes_str) if (last_changes > 0) else "\033[91m {}\033[00m".format(last_changes_str),
                    currency.hist.iloc[-2, :].at["open"],
                    currency.hist.iloc[-2, :].at["close"]]
            table.append(row)

        print("\n", time.ctime())
        print(tabulate(table, columns, tablefmt="pretty", numalign="center", stralign="center"))

    def show_trading_view(self):
        while True:
            try:
                self.update_currency_hists()
                self.currencies = sorted(self.currencies, key=lambda x: x.lastCandleChanges, reverse=True)
                self.show_currency_pannels()
            except KeyboardInterrupt:
                print("KeyboardInterrupt exception is caught")
                exit()
            except:
                print("Connetion Failed", end='\r')

def main():
    symbols = ["GTOUSDT", "KEYUSDT", "MATICBTC", "MITHUSDT",
                "CHRUSDT", "NEARUSD", "DYDXUSDT", "CELRUSDT",
                # "XTZUSDT", "TLMUSDT", "SUSHIUSDT", "STORJUSDT",
                # "WINUSDT", "SANDBTC", "SHIBUSDT", "ONEUSDT",
                # "MANAUSDT", "BATUSDT", "GRTUSDT",
                "LRCUSDT", "SFPUSDT", "BTTUSDT", "TROYUSDT"]
    currencies = create_currencies(symbols)
    exchange = "BINANCE"
    candle_interval = Interval.in_1_minute

    print("Enter alerter password: ", end='')
    alerter_pass = input()
    print("Enter alert receiver: ", end='')
    alert_receiver = input()
    alerter = Alerter(alerter_pass, alert_receiver)

    trading_view_manager = TradingViewManager(currencies, exchange, candle_interval, alerter)

    trading_view_manager.show_trading_view()

if __name__ == "__main__":
    main()
