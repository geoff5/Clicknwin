import paypalrestsdk
import logging

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