import key
import json
import Symbols
import Analiz
import time
import math
import telegram
import datetime
import Settings
#import matplotlib.pyplot as plt

from binance.client import Client
client = Client(key.api_key, key.api_secret)

from color import colorize
#from color import uncolorize

from telegram import (Animation, Audio, Contact, Document, Chat, Location,
                      PhotoSize, Sticker, TelegramObject, User, Video, Voice,
                      Venue, MessageEntity, Game, Invoice, SuccessfulPayment,
                      VideoNote, PassportData)

bot = telegram.Bot(token=key.token)

def Strategy_BB():
  symbol = Settings.symbolBB
  base_priceBB = Analiz.BB14(market=symbol+"BTC", tick_interval=Settings.tick_intervalBB)[0]
  base_priceBB = round(float(base_priceBB),8)

  up_price = Analiz.BB14(market=symbol+"BTC", tick_interval=Settings.tick_intervalBB)[1]
  up_price = round(float(up_price),8)
  down_price = Analiz.BB14(market=symbol+"BTC", tick_interval=Settings.tick_intervalBB)[2]
  down_price = round(float(down_price),8)

  balanceBTC = client.get_asset_balance(asset='BTC')
  balanceBTCJSON = json.dumps(balanceBTC)
  balanceBTCRESP = json.loads(balanceBTCJSON)
  balanceBTCFREE = balanceBTCRESP['free']
  budget_BTC = balanceBTCFREE

  start_operation = Settings.start_operationBB
  
  k = 0
  a=1

  while k <1:
    if symbol == Symbols.SymbolsMatrix[a][0]:
      le = len(str(Symbols.SymbolsMatrix[a][2]))
      k = 1
    else:
      a = int(a) + 1

  while True:
    try:
      base_priceBB = Analiz.BB14(market=symbol+"BTC", tick_interval=Settings.tick_intervalBB)[0]
      base_priceBB = round(float(base_priceBB),8)

      up_price = Analiz.BB14(market=symbol+"BTC", tick_interval=Settings.tick_intervalBB)[1]
      up_price = round(float(up_price),8)
      down_price = Analiz.BB14(market=symbol+"BTC", tick_interval=Settings.tick_intervalBB)[2]
      down_price = round(float(down_price),8)
      time.sleep(2)
      balanceALT = client.get_asset_balance(asset=str(symbol))
      balanceALTJSON = json.dumps(balanceALT)
      balanceALTRESP = json.loads(balanceALTJSON)
      balanceALTFREE = balanceALTRESP['free']
      balanceBTC = client.get_asset_balance(asset='BTC')
      balanceBTCJSON = json.dumps(balanceBTC)
      balanceBTCRESP = json.loads(balanceBTCJSON)
      balanceBTCFREE = balanceBTCRESP['free']
      budget_BTC = balanceBTCFREE

      price = client.get_symbol_ticker(symbol=str(symbol)+"BTC")
      priceJSON = json.dumps(price)
      priceRESP = json.loads(priceJSON)
      price = priceRESP['price']
      aprofit = float(price) / float(base_priceBB) - 1
      aprofit = float(aprofit) * 100
      aprofit = round(aprofit,2)

      aprofitup = float(up_price) / float(base_priceBB) - 1
      aprofitup = float(aprofitup) * 100
      aprofitup = round(aprofitup,2)

      aprofitdown = float(down_price) / float(base_priceBB) - 1
      aprofitdown = float(aprofitdown) * 100
      aprofitdown = round(aprofitdown,2)
      print("--------------------------------------------------------------------------------------------------------------------------------------------------------------")
      print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n\tSymbol:\t" + str(symbol + "BTC") 
      + "\n\tBase price:\t" + str(base_priceBB)
      + "\tProfit:\t\t" + str(aprofit) 
      + "%\n\tPrice UP:\t" + str(up_price)
      + "\tProfitUP:\t" + str(aprofitup)
      + "%\n\tPrice DOWN:\t" + str(down_price) 
      + "\tProfitDown:\t" + str(aprofitdown)+"%")

      print("\tPrice:\t\t" + str(price) 
      + "\n\tBalance:\t" + str(balanceALTFREE)
      + "\n\tBalance[BTC]:\t" + str(balanceBTCFREE))
      print("--------------------------------------------------------------------------------------------------------------------------------------------------------------")

      if start_operation == "SELL" and float(up_price) < float(price):
          qua = float(balanceALTFREE)
          if le==1:
            qua = math.floor(qua)
          else: 
            qua = str(qua)[0:le]
          OrderSell = client.create_order(symbol=str(symbol+"BTC"), side=client.SIDE_SELL, type=client.ORDER_TYPE_LIMIT, timeInForce=client.TIME_IN_FORCE_GTC, quantity=str(qua), price=str(price))
          print(str(OrderSell))
          start_operation = "BUY"
          com = "\t Sell Order. Balance: " + str(qua) + "\tPrice: " + str(price) + "\tNext operation: " + str(start_operation)
          print(colorize(47, 0, 32, com))
          bot.send_message(chat_id=key.chat_id, text=str(com))

      if start_operation == "BUY" and float(down_price) > float(price):
          qua = float(budget_BTC) / float(price)
          if le==1:
            qua = math.floor(qua)
          else: 
            qua = str(qua)[0:le]
          OrderBuy = client.create_order(symbol=str(symbol+"BTC"), side=client.SIDE_BUY, type=client.ORDER_TYPE_LIMIT, timeInForce=client.TIME_IN_FORCE_GTC, quantity=str(qua), price=str(price))
          print(str(OrderBuy))
          start_operation = "SELL"  
          com = "\t Buy Order. Balance: " + str(qua) + "\tPrice: " + str(price) + "\tNext operation: " + str(start_operation) + "\tBalance ALT: " + str(qua)
          print(colorize(47, 0, 32, com))
          bot.send_message(chat_id=key.chat_id, text=str(com))
    except:
      print("EOFError")