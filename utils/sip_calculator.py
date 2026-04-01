import numpy as np

def calculate_sip(monthly_sip, annual_return_pct, years):
    r = annual_return_pct / 100 / 12
    n = years * 12
    if r == 0:
        future_value = monthly_sip * n
    else:
        future_value = monthly_sip * (((1 + r) ** n - 1) / r) * (1 + r)
    total_invested = monthly_sip * n
    profit = future_value - total_invested
    return round(future_value, 2), round(total_invested, 2), round(profit, 2)

def get_yearly_breakdown(monthly_sip, annual_return_pct, years):
    breakdown = []
    r = annual_return_pct / 100 / 12
    for y in range(1, years + 1):
        n = y * 12
        if r == 0:
            fv = monthly_sip * n
        else:
            fv = monthly_sip * (((1 + r) ** n - 1) / r) * (1 + r)
        invested = monthly_sip * n
        breakdown.append({"year": y, "invested": round(invested, 2), "value": round(fv, 2), "profit": round(fv - invested, 2)})
    return breakdown
