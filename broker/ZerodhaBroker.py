import backtrader as bt
from kite_connect.main import KiteConnect

bt.brokers.BackBroker
bt.BrokerBase
class ZerodhaBroker(bt.brokers.BackBroker):
    
    params = (
        ("access_token", None),
        ("api_key", None),
        ("api_secret", None),
        ("symbol_lookup_url", None),
        ("debug", False),
    )
    
    def __init__(self, **kwargs):
        self.data_started = False
        self.orders = []
        self.kite = KiteConnect().kite
        # self.kite.set_access_token(self.params.access_token)
        # self.ticker = KiteTicker(self.params.api_key, self.params.access_token)
        super().__init__(**kwargs)
    
    def start(self):
        print("Zerodha's backtrader")
        # self.kite._login()
        # self.ticker.start()
    
    # def stop(self):
        # self.ticker.stop()
        # pass
    
    def getcash(self):
        margins = self.kite.margins()
        return margins["equity"]["available"]
    
    def setcash(self, cash):
        self.cash = cash
    
    def _submit(self, o):
        # TODO Uncomment below to actually place buy and sell orders
        # self.kite.place_order(
        #     variety="regular",
        #     exchange=o.data._name.split(":")[0].upper(),
        #     tradingsymbol=o.data._name.split(":")[1],
        #     transaction_type="BUY" if o.isbuy() else "SELL",
        #     quantity=o.size,
        #     order_type="MARKET" if o.exectype == bt.Order.Market else "LIMIT",
        #     price=o.price,
        # )
        self.orders.append(o)
    
    def _get_order_status(self, o):
        for order in self.kite.orders():
            if order["order_id"] == o.ref:
                status = order["status"]
                if status == "COMPLETE":
                    return bt.Order.Completed
                elif status == "REJECTED":
                    return bt.Order.Rejected
                elif status == "CANCELLED":
                    return bt.Order.Canceled
                elif status == "OPEN":
                    return bt.Order.Accepted
        return bt.Order.Accepted