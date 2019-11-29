
import tweepy
import random
import os

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_KEY = os.getenv('ACCESS_KEY')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET) 
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET) 
api = tweepy.API(auth)
           
      #Minutos * Segundos * (Cuantas veces se repite = horas de intervalo)
#INTERVALO = 60 * 60 * 6 #Twittea cada 6 horas.
INTERVALO = 15

while True:

 #Obtenemos las frases del archivo de frases
 with open ("frases.txt", "rb") as myfile:
    frases = myfile.read()

 #Se genera un numero random el cual es utilizado como indice
 r = random.randint(0, 24)
 tweet = "@CamiMontielH " + frases[r]


 try:
     if api.update_status(tweet):
         print("Twitteado")
 #Manejo de excepciones 
 except tweepy.error.TweepError as e:
     print(e)

 time.sleep(INTERVALO)
