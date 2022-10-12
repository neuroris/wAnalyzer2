from PyQt5.QtCore import QDate
import os
import pandas
from wookutil import WookMath

class DayAnalysis(WookMath):
    def __init__(self):
        self.date = None
        self.item_name = ''
        self.file_name = ''
        self.earning_count = 0
        self.loss_count = 0
        self.profit = 0
        self.profit_rate = 0.0
        self.net_profit = 0
        self.net_profit_rate = 0.0
        self.transaction_fee = 0
        self.tax = 0
        self.price_avg = 0

    def clear(self):
        self.date = None
        self.item_name = ''
        self.file_name = ''
        self.earning_count = 0
        self.loss_count = 0
        self.profit = 0
        self.profit_rate = 0.0
        self.net_profit = 0
        self.net_profit_rate = 0.0
        self.transaction_fee = 0
        self.tax = 0
        self.price_avg = 0

    def analyze(self, file_name, interval, loss_cut, fee_ratio):
        self.clear()
        self.file_name = file_name
        file = os.path.basename(file_name)
        self.item_name = file[:-17]
        self.date = QDate.fromString(file[-12:-4], 'yyyyMMdd')

        prices = self.get_simplified_prices(file_name, interval, loss_cut)
        previous_price = prices[0]
        for index, price in enumerate(prices[1:-1]):
            next_price = prices[index + 2]
            if price == (previous_price - interval):
                if price + interval == next_price:
                    self.earning_count += 1
                else:
                    self.loss_count += 1
            previous_price = price

        price_sum = 0
        for price in prices:
            price_sum += price
        self.price_avg = int(price_sum / len(prices))

        self.profit = (self.earning_count * interval) - (self.loss_count * loss_cut)
        self.profit_rate = round(self.profit / self.price_avg * 100, 2)
        transaction_number = self.earning_count + self.loss_count
        self.transaction_fee = round(transaction_number * self.price_avg * fee_ratio / 100, 2)
        self.net_profit = round(self.profit - self.transaction_fee, 2)
        self.net_profit_rate = round(self.net_profit / self.price_avg * 100, 2)

    def get_simplified_prices(self, file_name, interval, loss_cut):
        df = pandas.read_csv(file_name)
        initial_price = df.loc[0, 'Open']
        high_price = df['High']
        low_price = df['Low']
        open_price = df['Open']
        close_price = df['Close']

        # Main engine
        prices = list()
        prices.append(initial_price)
        get_floor = self.custom_get_floor(interval, loss_cut)
        get_ceiling = self.custom_get_ceiling(interval, loss_cut)
        for index in df.index:
            low_floor = get_floor(low_price[index])
            high_ceiling = get_ceiling(high_price[index])
            if open_price[index] < close_price[index]:
                while low_floor != get_floor(high_ceiling):
                    low_floor = get_ceiling(low_floor)
                    if prices[-1] != low_floor:
                        if not self.at_cut_price(low_floor, interval):
                            prices.append(low_floor)
            else:
                while low_floor != get_floor(high_ceiling):
                    high_ceiling = get_floor(high_ceiling - 1)
                    if prices[-1] != high_ceiling:
                        if prices[-1] != get_floor(high_ceiling):
                            prices.append(high_ceiling)

        # Filter out descending loss cut
        processed_prices = list()
        processed_prices.append(initial_price)
        for index, price in enumerate(prices[1:-1]):
            if self.at_cut_price(price, interval):
                ceiling = price + loss_cut
                floor = price - (interval - loss_cut)
                if not ((prices[index] == ceiling) and (prices[index + 2] == floor)):
                    processed_prices.append(price)
            else:
                processed_prices.append(price)
        processed_prices.append(prices[-1])
        return processed_prices

    def get_summary(self):
        summary = (self.item_name, self.date.toString('yyyy-MM-dd'), self.earning_count)
        summary += (self.loss_count, self.profit, self.profit_rate, self.transaction_fee)
        summary += (self.net_profit, self.net_profit_rate)
        return summary

class WookAnalysis:
    def __init__(self):
        self.analyses = dict()

    def add(self, analysis):
        self.analyses[analysis.date] = analysis

    def remove(self, analysis_time):
        del self.analyses[analysis_time]

    def clear(self):
        self.analyses.clear()

    def has(self, analysis_date):
        has_it = False
        if analysis_date in self.analyses:
            has_it = True
        return has_it

    def get_analysis(self, analysis_date):
        return self.analyses[analysis_date]

    def get_count(self):
        return len(self.analyses)

    def get_earning_count(self):
        earning_count = 0
        for analysis in self.analyses.values():
            earning_count += analysis.earning_count
        return earning_count

    def get_loss_count(self):
        loss_count = 0
        for analysis in self.analyses.values():
            loss_count += analysis.loss_count
        return loss_count

    def get_total_fee(self):
        fee = 0
        for analysis in self.analyses.values():
            fee += analysis.transaction_fee
        return int(fee)

    def get_winning_count(self):
        count = 0
        for analysis in self.analyses.values():
            if analysis.profit > 0:
                count += 1
        return count

    def get_winning_day_ratio(self):
        winning_count = self.get_winning_count()
        analysis_count = self.get_count()
        winning_ratio = winning_count / analysis_count
        return winning_ratio

    def get_total_profit(self):
        profit = 0
        for analysis in self.analyses.values():
            profit += analysis.profit
        return profit

    def get_average_price(self):
        price_sum = 0
        for analysis in self.analyses.values():
            price_sum += analysis.price_avg
        average_price = price_sum / self.get_count()
        return average_price

    def get_total_profit_rate(self):
        profit = self.get_total_profit()
        profit_rate = round(profit / self.get_average_price() * 100, 2)
        return profit_rate

    def get_total_net_profit(self):
        profit = self.get_total_profit()
        fee = self.get_total_fee()
        net_profit = round(profit - fee, 2)
        return net_profit

    def get_total_net_profit_rate(self):
        net_profit = self.get_total_net_profit()
        net_profit_rate = round(net_profit / self.get_average_price() * 100, 2)
        return net_profit_rate