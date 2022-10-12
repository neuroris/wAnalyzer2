class Stock:
    def __init__(self):
        self.item_code = ''
        self.item_name = ''
        self.transaction_time = ''
        self.order_executed_time = ''
        self.order_state = ''
        self.order_position = ''
        self.trade_position = ''
        self.current_price = 0
        self.purchase_price = 0
        self.ask_price = 0
        self.bid_price = 0
        self.high_price = 0
        self.low_price = 0
        self.order_price = 0
        self.executed_price = 0
        self.open_price = 0
        self.reference_price = 0
        self.purchase_price_avg = 0
        self.purchase_sum = 0
        self.purchase_amount = 0
        self.purchase_amount_net_today = 0
        self.order_amount = 0
        self.executed_amount = 0
        self.open_amount = 0
        self.holding_amount = 0
        self.sellable_amount = 0
        self.volume = 0
        self.accumulated_volume = 0
        self.order_number = 0
        self.original_order_number = 0
        self.executed_order_number = 0
        self.deposit = 0
        self.profit = 0
        self.profit_rate = 0.0
        self.profit_realization = 0
        self.profit_realization_rate = 0.0
        self.evaluation_fee = 0
        self.transaction_fee = 0
        self.tax = 0