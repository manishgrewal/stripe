import logging
import traceback
from logging.config import fileConfig

import stripe

# Initialize the variables
PATH_TO_SECRET_KEY = './STRIPE_SECRET'
PATH_TO_LOGGING_CONF = './logging.ini'
PATH_TO_OUTPUT_FILE = './stripe_bal_payout.txt'
DEBUG = 0; # set to 1 to print api responses

# Setup the logger
logger = logging.getLogger()
fileConfig(PATH_TO_LOGGING_CONF)

try:
    logger.info('Read the stripe key file from disc')
    with open(PATH_TO_SECRET_KEY) as keyfile:
        secret_key = keyfile.read().strip()

    logger.info('Set the credentials')
    stripe.api_key = secret_key

    logger.info('Fetch balance')
    balance = stripe.Balance.retrieve()

    logger.info('Fetch payouts')
    payouts = stripe.Payout.list()

    if DEBUG == 1:
        print("BALANCE:", balance)
        print("PAYOUTS:", payouts)

    logger.info('Select the pending balance')
    pending_balance = 0
    for balance in balance.pending:
        if balance.currency == 'gbp':
            pending_balance += balance.amount
            logger.info('Found balance: %.2f %s', pending_balance, balance.currency)
            break

    logger.info('Add the payouts')
    total_payout = 0
    for payout in payouts.data:
        if payout.currency == 'gbp':
            total_payout += payout.amount
            logger.info('Found payout: %.2f %s', payout.currency, payout.amount)

    amount = pending_balance + total_payout
    logger.info("Saving the amount to a file: %.2f", amount)

    with open(PATH_TO_OUTPUT_FILE, 'w') as fp:
        fp.write(str(amount))

except Exception as e:
    logger.error('Exception while running script, traceback is: \n{}'.format(
    traceback.format_exc()))
    with open(PATH_TO_OUTPUT_FILE, 'w') as fp:
        fp.write('0')
else:
    logger.info('Script execution completed successfully')
