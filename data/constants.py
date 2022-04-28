# CONSTANTS
IS_VALID = "is-valid"
IS_INVALID = "is-invalid"
AVATAR_UPLOAD_FOLDER = r"static/img/avatars"
AVATARS_UPLOAD_URL_FOR_FOLDER = r"img/avatars"
AVATAR_FILENAME_DEFAULT = "default.jpg"
AVATAR_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
TIMEZONE_DEFAULT = "UTC +3"  # стандартный часовой пояс
TRANSACTION_CATEGORIES_LIST = ["Расход", "Доход"]
MONTHS = ["Января", "Феварля", "Марта", "Апреля", "Мая", "Июня", "Июля",
          "Августа", "Сентября", "Октября", "Ноября", "Декабря"]
WEEK_DAYS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]


# START_PAGE
START_PAGE_HTML = "start_page.html"
START_PAGE_TITLE = "Mylbudget"


# REGISTRATION_PAGE
REGISTRATION_PAGE_HTML = "registration_page.html"
REGISTRATION_PAGE_TITLE = "Регистрация"
REGISTRATION_PAGE_INPUT_ERRORS = {
    "email": {
        "errclass": "",
        "invalid-feedback": ""},
    "username": {
        "errclass": "",
        "invalid-feedback": ""},
    "password": {
        "errclass": "",
        "invalid-feedback": ""},
    "password_again": {
        "errclass": "",
        "invalid-feedback": ""},
    "main_currency": {
        "errclass": "",
        "invalid-feedback": ""},
    "timezone": {
        "errclass": "",
        "invalid-feedback": ""},
    "avatar": {
        "errclass": "",
        "invalid-feedback": ""}
}
REGISTRATION_PAGE_CURRENCIES_LIST = ["₽ (RUB)", "$ (USD)", "€ (EUR)"]  # список валют при регистрации
REGISTRATION_PAGE_TIMEZONES_LIST = [f"UTC +{zone}" if zone >= 0 else f"UTC {zone}" for zone in range(-11, 13)]  # список часовых поясов


# LOGIN_PAGE
LOGIN_PAGE_HTML = "login_page.html"
LOGIN_PAGE_TITLE = "Авторизация"
LOGIN_PAGE_INPUT_ERRORS = {
        "email": {
            "errclass": "",
            "invalid-feedback": ""},
        "password": {
            "errclass": "",
            "invalid-feedback": ""},
    }


# CABINET_PAGE
CABINET_PAGE_SIDEBAR_ELEMENTS = {
    "Главная": {
        "href": "/cabinet",
        "a_class": "list-group-item list-group-item-action py-2 ripple",
        "i_class": "fas fa-tachometer-alt fa-fw me-3",
        "text": "Главная"},
    "Счета": {
        "href": "/cabinet/wallets",
        "a_class": "list-group-item list-group-item-action py-2 ripple",
        "i_class": "fas fa-tachometer-alt fa-fw me-3",
        "text": "Счета"},
    "Операции": {
        "href": "/cabinet/transactions",
        "a_class": "list-group-item list-group-item-action py-2 ripple",
        "i_class": "fas fa-tachometer-alt fa-fw me-3",
        "text": "Операции"
    }
}

# CABINET_WALLETS_PAGE
# ADD_WALLET_MODAL
CABINET_WALLETS_PAGE_ADD_WALLET_MODAL_INPUT_ERRORS = {
    "name": {
        "errclass": "",
        "invalid-feedback": ""},
    "balance": {
        "errclass": "",
        "invalid-feedback": ""},
    "color": {
        "errclass": "",
        "invalid-feedback": ""},
    "main_currency": {
        "errclass": "",
        "invalid-feedback": ""}
}

CABINET_WALLETS_PAGE_WALLETS_LIST = [
    {
        "name": "visa"
    },
    {
        "name": "123"
    },
    {
        "name": "2"
    },
    {
        "name": "1243"
    }
]

# CABINET_TRANSACTIONS_PAGE
# ADD_TRANSACTION_MODAL
CABINET_TRANSACTIONS_PAGE_ADD_TRANSACTION_MODAL_INPUT_ERRORS = {
    "transaction_sum": {
        "errclass": "",
        "invalid-feedback": ""},
    "currency": {
        "errclass": "",
        "invalid-feedback": ""},
    "transaction_type": {
        "errclass": "",
        "invalid-feedback": ""},
    "wallet": {
        "errclass": "",
        "invalid-feedback": ""},
    "name": {
        "errclass": "",
        "invalid-feedback": ""},
    "transaction_income_category": {
        "errclass": "",
        "invalid-feedback": ""},
    "comment": {
        "errclass": "",
        "invalid-feedback": ""},
    "transaction_expenses_category": {
        "errclass": "",
        "invalid-feedback": ""}
}

CABINET_TRANSACTIONS_PAGE_EXPENSES_CATEGORIES_LIST = \
    ["Продукты", "Транспорт", "ЖКХ", "Связь", "Образование",
      "Кафе", "Подарки", "Гаджеты", "Путешествия", "Досуг", "Другое"]  # РАСХОДЫ СПИСОК
CABINET_TRANSACTIONS_PAGE_INCOME_CATEGORIES_LIST = \
    ["Зарплата", "Дивиденты", "Подарок", "Другое"]  # доходы список
# CABINET_TRANSACTIONS_PAGE_WALLETS_LIST = ["dfsatgrsyhgcdfhdytrdyhfxhnbcfvhnvn", "visa", "dfsatgrsyhgcdfhdytrdyhfxhnbcfvhnvn"]
CABINET_TRANSACTIONS_PAGE_CATEGORIES_ICONS_LIST = {
    "Продукты": "fa fa-shopping-basket",
    "Транспорт": "fa fa-bus",
    "ЖКХ": "fa fa-home",
    "Связь": "fa fa-phone-square",
    "Образование": "fa fa-graduation-cap",
    "Кафе": "fa fa-coffee",
    "Подарки": "fa fa-gift",
    "Гаджеты": "fa fa-mobile",
    "Путешествия": "fa fa-plane",
    "Досуг": "fa fa-gamepad",
    "Другое": "fa fa-navicon",
    "Зарплата": "fa fa-credit-card",
    "Подарок": "fa fa-gift",
    "Дивиденты": "fa fa-bar-chart",
}
