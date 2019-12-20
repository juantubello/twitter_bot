import tweepy
import random
import os
import time
import codecs

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_KEY = os.getenv('ACCESS_KEY')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET) 
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET) 
api = tweepy.API(auth)

#Flag para identificar tweet's twitteados
flag_twitteado = False

indiceDeUltimaFrase = 100

#Id's twitteados
twitted_ids = []

#Minutos * Segundos * (Cuantas veces se repite = horas de intervalo)
INTERVALO = 60 * 10 #Responde cada 10 minutos.

while True:

 #Obtengo los tweets correspondientes a "CoscuBot"
 busqueda = api.search("CoscuBot")

 for tweet in busqueda:

     flag_twitteado = False
 
     #Id del tweet
     replyId = tweet.id
 
     #Id del tweet en string
     replyIdStr = tweet.id_str

     #Usuario que menciono al bot
     username = tweet.user.screen_name

     #Ignoro mis propios tweets
     if username == 'CoscuBot':
         print("Tweet ID: ",replyIdStr, " propio")
         continue

     #Valido no haber respondido previamente a ese tweet
     for tw_id in twitted_ids:
         if replyIdStr == tw_id:
             print("Tweet ID: ", replyId, " ya respondido" )
             flag_twitteado = True
             twitted_ids.append(replyIdStr)

     if not flag_twitteado:
         #Leeo las Quotes de Coscu
         with codecs.open('coscuQuotes.txt', encoding='ISO-8859-1', errors='ignore') as myfile:
             frases = myfile.readlines()
         myfile.close()      

         #Genero un numero random para usarlo como indice en la lista de Quotes
         r = random.randint(0, 18)
         while(r == indiceDeUltimaFrase):
             r = random.randint(0, 18)
         indiceDeUltimaFrase = r
         tweet = "@" + username +" "+ frases[r]
     
         #Twitteamos
         try:
             if api.update_status(status = tweet, in_reply_to_status_id = replyId) :
                  print("Twitteado con éxito")
         #Manejo de excepciones 
         except tweepy.error.TweepError as e:
             print(e)
         
 time.sleep(INTERVALO)


