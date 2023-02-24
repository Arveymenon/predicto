# # First Way to Login
# # You can use your Kite app in mobile
# # But You can't login anywhere in 'kite.zerodha.com' website else this session will disconnected

from kite_connect.kiteTrade import KiteApp


class KiteConnect:

    def __init__(self):

        enctoken = " M9XtJ3iExgtuh0dgvVYCeamDLAUX/YXUVHyuJIe8BuuWXyhzjLUNOz+J++zAN4B/JBV4WkmbBrRHksfEEPYNSaBkz8E+qct5WoXSd0nUaYr18Wsw7L2hbg=="
        self.kite = KiteApp(enctoken=enctoken)