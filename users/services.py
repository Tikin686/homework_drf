import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_product(name):
    """Создает продукт в stripe"""
    product = stripe.Product.create(name=name)
    return product


def create_price(price, name):
    """Создает цену в stripe"""
    product_id = create_product(name).id
    return stripe.Price.create(
        currency="rub",
        unit_amount=int(price * 100),
        product=product_id
    )


def create_session(price, name):
    """Создает сессию в Stripe и возвращает ID и URL сессии"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/courses/",
        line_items=[{"price": price.get("id"), "name": name.get("id"), "quantity": 2}],
        mode="payment",
    )
    return session.id, session.url