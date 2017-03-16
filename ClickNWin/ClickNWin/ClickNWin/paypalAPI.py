import paypalrestsdk
import logging

paypalrestsdk.configure({
  "mode": "sandbox", 
  "client_id": "AVKGtdnAliBll5ns6SJXKpIeMsTLPyOJOYzj-1jSebRtB7wYqkfVRJhFDz35C9ug2Z5h4Ff64dQSkXMg",
  "client_secret": "EPZrxp9WFMEqEh2iQyAkNdnratHwgvbbeNQUyAA2qstBvHkJs6_QxBI57ntqqI2jcQrnauEkR0zpNe9l" })

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