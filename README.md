# twitter_bot
I always wanted to know how bots work... and the best way to understand is to try! So this is how the **@CoscuBot** came to life! I researched some popular and not too complicated bots (since I had never programmed a bot before) and finally, I ended up with the idea of creating a bot that responds with random phrases every time you mention it.

## Functionality 
The functionality of this bot is to reply to the user who **@mentions** it with a random quote :trollface: from the Argentinian streamer 'Coscu' within 0 to 5 minutes.

## Features

- **Not repeat**: The bot does not reply to a previously replied tweet

- **No duplicate tweets**: The bot has an index indicating which was the last quote tweeted to avoid duplicates

- **Log** : The use of this bot implements a log where we keep all the tweets answered with ID and the answer given for that ID

- **Doesn't need much**: It's quite simple to implement this bot locally, you only need `python` and the libraries of: `tweepy`, `gspread`, `oauth2client` and of course access to twitter API and access to google drive API.
                         
# Setup

- First you will need [Python](https://www.python.org/downloads/)
  - Then you will need your consumer key for Twitter, so:
    - Go to [Twitter Devs](https://dev.twitter.com/apps/new) and log in, if necessary
    - Supply the necessary required fields, accept the Terms Of Service, and solve the CAPTCHA.
    - Submit the form
    - Go to the API Keys tab, there you will find your Consumer key and Consumer secret keys.
    - Copy the consumer key (API key) and consumer secret from the screen into our application.
    
  - Finally you will need your Google creds to use google drive API so:
    -  Go to the [Google APIs Console](https://console.developers.google.com/).
    -  Create a new project.
    -  Click Enable API. Search for and enable the Google Drive API.
    -  Create credentials for a Web Server to access Application Data.
    -  Name the service account and grant it a Project Role of Editor.
    -  Download the JSON file.
    -  Copy the JSON file to your code directory and rename it to client_secret.json
    -  Find the  client_email inside client_secret.json. Back in your spreadsheet, click the Share button in the top right, and paste the client email into the People field to give it edit rights. Hit Send.

- Once you have the stuff from above, we need to crate a virtualenv, run this commands on your CMD (This steps are for Windows):
```
 - mkdir tw_bot
 - cd tw_bot
 - python -m venv environment   | Make sure the name you choose for your virtualenv is in lower case with no special characters and spaces
 - cd tw_bot                    | Enter the tw_bot - if already in skip this
 - environment\Scripts\activate | You will know that you have virtualenv started when you see that the prompt in your console is prefixed with (environment)
```      
- Now we need to import the dependencies to our virtualenv, there are 2 ways:

     - if the script is going to be deploy to a server like Heroku, create a **```requirements.txt```** file 
       that contain a list of items to be installed
       - tweepy
       - gspread
       - oauth2client
                                                   
       and then run on cmd -> **```pip install -r requirements.txt```** 
     
     - The other way is to manually install all dependencies running **```pip install nameOfDependency```** 
    
     - Boring part done! :heavy_check_mark:

 - If you got here, copy the `tw_bot.py` that has the source code for the bot, also in order to work locally on your machine
   you will need to create a `.txt file` for example `quotes.txt` in the project folder and fill it with quotes or just text that you want to tweet...
   
   - You need to adjust this with:
     ```
     CONSUMER_KEY    = 'Your twitter consumer_key'
     CONSUMER_SECRET = 'Your twitter consumer_secret'
     ACCESS_KEY      = 'Your twitter access_key'
     ACCESS_SECRET   = 'Your twitter access_secret'
     ```
     
   -  To work locally lines 21 - 27 should be replaced with:
       ```
       #Completo las credenciales para interactuar con la API de google
       scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'] #Agrego un Endpoint para que funcione
       creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
       client = gspread.authorize(creds)
       ```
   -  Make sure that you write the correct name of your `.txt` and your `spreadsheet`
       ```
       30 | sheet = client.open("YOUR_SPREADSHEET").sheet1
      
       70 | with codecs.open('YOUR_TXT.txt', encoding='ISO-8859-1', errors='ignore') as myfile:
       ```
  - **FINALLY** to end [here](https://tweepy.readthedocs.io/en/latest/) you can find documentation for **tweepy** and [here](https://gspread.readthedocs.io/en/latest/) for
    **gspread** to play and modify the bot as your wish! 
