from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta
import time
import os

class Currency:
    def __init__(self, symbol=""):
        self.symbol = symbol

def create_currencies(symbols):
    currencies = []
    for symbol in symbols:
        currencies.append(Currency(symbol))

    return currencies

class TradingViewManager:
    def __init__(self, currencies, screener, exchange, candle_interval):
        self.currencies = currencies
        self.screener = screener
        self.exchange = exchange
        self.candle_interval = candle_interval

    def create_currency_handlers(self):
        currency_handlers = []
        for currency in self.currencies:
            currency_handlers.append(TA_Handler(
                symbol= currency.symbol,
                screener=self.screener,
                exchange=self.exchange,
                interval=Interval.INTERVAL_1_MINUTE,
                timeout=10
            ))
        return currency_handlers

    def create_currencies_analysis(self, currency_handlers):
        currencies_analysis = []
        for currency_handler in currency_handlers:
            currencies_analysis.append(currency_handler.get_analysis())
        return currencies_analysis

    def show_currency_analysis(self, analysis):
        open_price = analysis.indicators["open"]
        close_price = analysis.indicators["close"]
        chagnes = ((close_price - open_price) / close_price) * 100

        print("\t\t\t\t\tOpen Price:\t\t", open_price)
        print("\t\t\t\t\tClose Price:\t\t", close_price)
        print("\t\t\t\t\tPrice Changes:\t\t", chagnes, "%")

    def show_currency_pannels(self, counter):
        currency_handlers = self.create_currency_handlers()
        currencies_analysis = self.create_currencies_analysis(currency_handlers)

        os.system('cls' if os.name == 'nt' else "printf '\033c'")

        print("\t\t\t\t\t", time.ctime(), "\n")
        for i in range(len(self.currencies)):
            print("\t\t\t\t\t--------- ", self.currencies[i].symbol," ", counter," ---------")
            self.show_currency_analysis(currencies_analysis[i])

    def show_trading_view(self):
        counter = 0
        while True:
            counter += 1
            self.show_currency_pannels(counter)

            if counter == 4:
                break

def main():
    symbols = ["TROYUSDT", "GTOUSDT", "KEYUSDT", "MATICBTC",
                "CHRUSDT", "SANDUSDT", "MANAUSDT", "ONEUSDT",
                "SHIBUSDT", "WINUSDT", "BTTUSDT", "LRCUSDT",
                "SUSHIUSDT", "STORJUSDT", "AVAXUSDT", "XTZUSDT",
                "SLPUSDT"]
    currencies = create_currencies(symbols)
    
    screener = "crypto"
    exchange = "BINANCE"
    candle_interval = Interval.INTERVAL_1_MINUTE
    trading_view_manager = TradingViewManager(currencies, screener, exchange, candle_interval)

    trading_view_manager.show_trading_view()

if __name__ == "__main__":
    main()
