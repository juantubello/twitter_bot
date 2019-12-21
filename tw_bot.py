import tweepy
import random
import os
import time
import codecs
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Completo las credenciales para interactuar con la API de tweepy
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_KEY = os.getenv('ACCESS_KEY')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET) 
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET) 
api = tweepy.API(auth)

#Completo las credenciales para interactuar con la API de google
json_creds = os.getenv('GOOGLE_SHEETS_CREDS_JSON')
creds_dict = json.loads(json_creds)
creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'] #Agrego un Endpoint para que funcione
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_dict, scope)
client = gspread.authorize(creds)

#Abro el archivo correspondiente al log
sheet = client.open("CoscuBot-IdLog").sheet1

#Flag para identificar tweets twitteados
flag_twitteado = False

#Minutos * Segundos * (Cuantas veces se repite = horas de intervalo)
INTERVALO = 60 * 10  #Responde cada 10 minutos.

while True:

 #Obtengo los tweets correspondientes a "CoscuBot"
 busqueda = api.search("CoscuBot")

 #Itero por cada tweet en especifico, obtenido de la busqueda anterior
 for tweet in busqueda:

     flag_twitteado = False
 
     #Id del tweet en string
     replyIdStr = tweet.id_str

     #Usuario que menciono al bot
     username = tweet.user.screen_name

     #Ignoro mis propios tweets
     if username == 'CoscuBot':
         print("Tweet ID: ",replyIdStr, " propio")
         continue

     #Valido no haber respondido previamente a ese tweet
     datos = sheet.col_values(1)
     log_Ids = datos[1:]

     for tweet_id in log_Ids:
         if replyIdStr == tweet_id:
             print("Tweet ID: ", replyIdStr, " ya respondido" )
             flag_twitteado = True

     if not flag_twitteado:
         #Leeo las Quotes de Coscu
         with codecs.open('coscuQuotes.txt', encoding='ISO-8859-1', errors='ignore') as myfile:
             frases = myfile.readlines()
         myfile.close()      

         #Genero un numero random para usarlo como indice en la lista de Quotes
         ultimoNumeroRandom = int(sheet.cell(2, 3).value)
         r = random.randint(0, 18)
         while(r == ultimoNumeroRandom):
             r = random.randint(0, 18)
         sheet.update_acell('C2', r)
         tweetTotweet = "@" + username +" "+ frases[r]
     
         #Twitteamos
         try:
             if api.update_status(status = tweetTotweet, in_reply_to_status_id = replyIdStr) :
                  print("Twitteado con éxito Id: ", replyIdStr)
                  indexToInsert = len(datos) + 1
                  row = [replyIdStr, tweetTotweet]
                  sheet.append_row(row)
         #Manejo de excepciones 
         except tweepy.error.TweepError as e:
             print(e)
         
 time.sleep(INTERVALO)



