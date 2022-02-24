## Simple stripe integration script

- Fetch balances and payouts using the stripe api
- Ignore currencies other than GBP
- Extract pending balance
- Sum all payouts
- Sum balances and payouts

## Instructions:

1. Start and activate a venv. Inside the venv folder, run 'pip install stripe'

```
python -m venv stripe
cd stripe
. ./Scripts/activate
pip install --upgrade stripe
```

2. Create a file STRIPE_SECRET, save the stripe secret key in it
2. python stripe_bal_payouts.py
2. Output will go in ./stripe_bal_payout.txt
