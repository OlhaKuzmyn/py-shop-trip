import json
from datetime import datetime

from app.shop import Shop
from app.customer import Customer


with open("app/config.json", "r") as config_file:
    config = json.load(config_file)

fuel_price, customers, shops = config.values()
customers_objects = [Customer(**customer) for customer in customers]
shops_objects = [Shop(**shop) for shop in shops]


def receipt(customer: Customer, shop_name: str) -> None:
    shop = [shop for shop in shops_objects if shop.name == shop_name][0]
    print(
        f"Date: {datetime(
            2021, 4, 1, 12, 33, 41
        ).strftime('%m/%d/%Y %H:%M:%S')}"
    )
    print(f"Thanks, {customer.name}, for your purchase!\nYou have bought:")
    for product, product_price in zip(customer.product_cart, shop.products):
        print(
            f"{product.number} "
            f"{product.name}s for {product * product_price} dollars"
        )

    print(
        f"Total cost is {customer.price_for_products(shop)} dollars\n"
        f"See you again!\n"
    )


def shop_trip() -> None:
    for customer in customers_objects:
        print(f"{customer.name} has {customer.money} dollars")
        trips_costs = {}
        for shop in shops_objects:
            cost_shop_trip = customer.price_for_shop_trip(shop, fuel_price)
            trips_costs[cost_shop_trip] = shop.name
            print(
                f"{customer.name}'s trip to the "
                f"{shop.name} costs {cost_shop_trip}"
            )

        if customer.money >= min(trips_costs):
            chosen_shop = trips_costs[min(trips_costs)]
            print(f"{customer.name} rides to {chosen_shop}\n")
            receipt(customer, chosen_shop)
            print(f"{customer.name} rides home")
            customer.money -= min(trips_costs)
            print(f"{customer.name} now has {customer.money} dollars\n")
        else:
            print(
                f"{customer.name} "
                f"doesn't have enough money to make a purchase in any shop"
            )
