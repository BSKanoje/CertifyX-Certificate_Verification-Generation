def get_new_plan_price(new_plan):

    plan_prices = {
        'starter': 5.00,
        'professional': 10.00,
        'enterprise': 15.00,
    }
    return plan_prices.get(new_plan, 0.00)  
