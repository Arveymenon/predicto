import backtrader as bt

class CommissionsAnalyzer(bt.Analyzer):
    def __init__(self):
        self.total_commission = 0

    def start(self):
        self.total_commission = 0

    def notify_trade(self, trade):
        # Get the commission info for the broker
        commission_info = self.strategy.broker.getcommissioninfo(self.data)

        # Calculate the commission paid for the trade
        commission = commission_info.getcommission(
            trade.size, trade.price
        )

        # Add the commission to the total commission
        self.total_commission += commission

    def stop(self):
        print(f"Total commission paid: {self.total_commission:.2f}")