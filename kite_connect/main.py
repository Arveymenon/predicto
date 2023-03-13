# # First Way to Login
# # You can use your Kite app in mobile
# # But You can't login anywhere in 'kite.zerodha.com' website else this session will disconnected

from kite_connect.kiteTrade import KiteApp


class KiteConnect:

    def __init__(self):

        enctoken = "QuS9J9Sw57+/HEg5+kUUY2vkIxFX+JGVhNH260e9yX8u8wRU/+WqJ+bMv75tf7JuXTudbxIDoPEo3Iztkwsi5gr5fGc7PoZHehWcNmPAuoLdj7nQYSC9KA=="
        self.kite = KiteApp(enctoken=enctoken)