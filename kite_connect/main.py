# # First Way to Login
# # You can use your Kite app in mobile
# # But You can't login anywhere in 'kite.zerodha.com' website else this session will disconnected

from kite_connect.kiteTrade import KiteApp


class KiteConnect:

    def __init__(self):

        enctoken = ""
        self.kite = KiteApp(enctoken=enctoken)