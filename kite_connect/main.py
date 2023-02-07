# # First Way to Login
# # You can use your Kite app in mobile
# # But You can't login anywhere in 'kite.zerodha.com' website else this session will disconnected

from kite_connect.kiteTrade import KiteApp


class KiteConnect:

    def __init__(self):

        enctoken = "sqMjpYKewH2C4Ce4HmNCasXEsITMFUx0pTezS38AIomXdHcQEL2aeJbzQf4SnSCDTb4KiGlc4SHcnsGAm75K5RBETH5xTa/kR/OF9ArY67TWSy6WAClFuA=="
        self.kite = KiteApp(enctoken=enctoken)