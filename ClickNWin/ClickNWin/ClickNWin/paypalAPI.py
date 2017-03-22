"""Functions for interacting with paypal to receive and make payments"""

import paypalrestsdk
from paypalrestsdk import Payout, ResourceNotFound
import logging
import random
import string

paypalrestsdk.configure({
  "mode": "sandbox", 
  "client_id": "AVAIfIc67oJ5raw8pFxkp8OGyyOliG_4CQRXJPwU2HMY53gBHRcPwUi-XqRMpmtvKeSfFDigy6PC2IVB",
  "client_secret": "EPm1x9KMEVsVK6aymuHFrZgCTG7EGSWQmTTR9ab7RZNXjq5gCFEvfUxOa2Mk_YSAO2NdYzAJtjBGndTz" })

def topUp(card, amount, cvv):
    payment = paypalrestsdk.Payment({
      "intent": "sale",
      "payer": {
        "payment_method": "credit_card",
        "funding_instruments": [{
          "credit_card": {
            "type": card[5],
            "number": card[1],
            "expire_month": card[2],
            "expire_year": card[3],
            "cvv2": cvv,
            "first_name": card[4],
            "last_name": card[7] }}]},
      "transactions": [{
        "item_list": {
          "items": [{
            "name": "Funds Top Up",
            "sku": "Funds Top Up",
            "price": amount,
            "currency": "EUR",
            "quantity": 1 }]},
        "amount": {
          "total": amount,
          "currency": "EUR" },
        "description": "Fund Top Up for ClickNWin" }]})

    if payment.create():
      return True
    else:
      return False  


def balanceRedeem(email, amount):
    sender_batch_id = ''.join(
    random.choice(string.ascii_uppercase) for i in range(12))

    payout = Payout({
        "sender_batch_header": {
            "sender_batch_id": sender_batch_id,
            "email_subject": "ClickNWin Balance Redeeemed"
        },
        "items": [
            {
                "recipient_type": "EMAIL",
                "amount": {
                    "value": amount,
                    "currency": "EUR"
                },
                "receiver": email,
                "note": "Thank you.",
                "sender_item_id": "item_1"
            }
        ]
    })

    if payout.create(sync_mode=True):
        return True
    else:
        return False

   