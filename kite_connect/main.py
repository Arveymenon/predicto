# # First Way to Login
# # You can use your Kite app in mobile
# # But You can't login anywhere in 'kite.zerodha.com' website else this session will disconnected

from kite_connect.kiteTrade import KiteApp


class KiteConnect:

    def __init__(self):

        enctoken = "gG9n44Jzl9Rm/QkAFNI5OrhqpjEIWjnPE2ahcoz73kuPM6p1+roizlx2erQcnmuVhFs75geeiRwRTMkKFsFOTK3kKeEtVp62nq9LopFyc7G9B0HUGLwExA=="
        self.kite = KiteApp(enctoken=enctoken)