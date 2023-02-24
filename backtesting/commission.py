import backtrader as bt

class ZerodhaCommission(bt.CommInfoBase):
    params = (
        ('commission', 20),     # Fixed commission per trade
        ('commissionpct', 0.03),# Commission rate as a percentage of trade value
        ('stocklike', True),    # Treat instruments as stock-like
        ('commtype', bt.CommInfoBase.COMM_PERC),  # Commission model is percentage-based
    )

    def getsize(self, price, cash):
        return self.p.leverage * (cash / price)

    def _getcommission(self, size, price, pseudoexec, *args, **kwargs):
        commission = self.p.commission
        commissionpct = self.p.commissionpct
        value = abs(size) * price
        if value * commissionpct < commission:
            commission = value * commissionpct
        return commission