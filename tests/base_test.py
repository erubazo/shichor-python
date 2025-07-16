from pages.cookie_page import CookiePage
from pages.currency_page import CurrencyPage
from pages.main_page import MainPage
from pages.signin_page import SignInPage


class BaseTest:
    main_page: MainPage
    cookie_page: CookiePage
    currency_page: CurrencyPage
    signin_page: SignInPage