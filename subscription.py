from datetime import date


SUBSCRIPTION_EXPIRES = date(2026, 12, 31)


def expiration_text():
    return SUBSCRIPTION_EXPIRES.strftime("%d/%m/%Y")


def is_active():
    return date.today() <= SUBSCRIPTION_EXPIRES
