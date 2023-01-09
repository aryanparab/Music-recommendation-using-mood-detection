from flask import Flask, render_template, url_for, request, redirect
import pickle
import numpy as np
import requests
# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer
from tensorflow.keras.models import load_model
import json
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import random
import requests
import pandas as pd
import librosa
import librosa.display
from scipy.io import wavfile as wav
import soundfile
import os
API_KEY = 'caa9d0da933f513c47b9ac0434d8e087'
shared_key = 'fb80ea9571da0ab0378ba06690717368'
#aryanparabmpr Aryan,2001
USER_AGENT = 'aryanparabmpr'
nltk.download('vader_lexicon')
lemmatizer = WordNetLemmatizer()

TEMPLATE_NAME  = 'home.html'
app = Flask(__name__)
#create chatbot
# englishBot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
# trainer = ChatterBotCorpusTrainer(englishBot)
# trainer.train("chatte=2bot.corpus.english") #train the chatter bot for english
sia = SIA()
model = load_model('chatbot_1.h5')
sentiment_model = pickle.load(open("siaModel.pkl","rb"))
intents = json.loads(open('intents.json').read())
classes = pickle.load(open('classes.pkl','rb'))
words = pickle.load(open('words.pkl','rb'))
tone_model = pickle.load(open("MLPmodel.h5","rb"))
#define app routes

def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'
    payload['limit'] = 20

    response = requests.get(url, headers=headers, params=payload)
    return response

def get_tone(sentiment):
  happy = ['rock', "pop", "dance", "classic rock", "Disco"]
  sad = ["indie rock", "mellow", "chill", "blues", "country", "soft rock", "slow" ]
  print(sentiment)
  if sentiment =='happy':
    return happy[random.randint(0,len(happy)-1)]
  else:
    return sad[random.randint(0,len(sad)-1)]


def getSongs(tone):
    
    r = lastfm_get({'method': 'tag.getTopTracks','tag':tone})
    
    r0_json = r.json()
    l=[]
    artist1 = r0_json['tracks']['track'][0]['artist']['name']
    for i in range(0,20):
        similar_song = r0_json['tracks']['track'][i]['name']
        url = r0_json['tracks']['track'][i]['url']
        artist_name = r0_json['tracks']['track'][i]['artist']['name']
        l.append([similar_song,artist_name,url])

    #random.shuffle(l)
    return l,artist1


def getAlbum(tone):
    
    r = lastfm_get({'method': 'tag.getTopAlbums','tag':tone})
    
    r0_json = r.json()
    l=[]
    artist1 = r0_json['albums']['album'][0]['artist']['name']
    for i in range(0,20):
        similar_song = r0_json['albums']['album'][i]['name']
        url = r0_json['albums']['album'][i]['url']
        artist_name = r0_json['albums']['album'][i]['artist']['name']
        l.append([similar_song,artist_name,url])

    #l = random.shuffle(l)
    return l,artist1

def clean_up_sentence(sentence):
  sentence_words = nltk.word_tokenize(sentence)
  sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
  return sentence_words 

def bag_of_words(sentence):
  sentence_words = clean_up_sentence(sentence)
  bag = [0] * len(words)
  for w in sentence_words:
    for i, word in enumerate(words):
      if word == w :
        bag[i] = 1
  return np.array(bag)

def predict_class(sentence):
  bow = bag_of_words(sentence)
  res = model.predict(np.array([bow]))[0]
  ERROR_THRESHOLD = 0.20
  results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD ]

  results.sort(key=lambda x : x[1],reverse = True)
  return_list = []
  for r in results : 
    return_list.append({'intent':classes[r[0]] , 'probablity' : str(r[1])})
  return return_list

def tonetext(text):
  
  scores = sia.polarity_scores(str(text))
  
  if scores['pos'] > scores['neg']:
  
    return 'happy'
  else:
    return 'sad'

def get_tone_response(tone,no):
  songs = getSongs(tone)
  extra = ""
  extraa = []
  for n, song in enumerate(random.sample(songs[0],10)) or [[]]:
    extra = extra + "<br> " +str(n)+ ") Name: <a href ="+ str(song[2]) + ">"+str(song[0])+"</a><br> Artist: " + str(song[1])
    extraa.append(song)
    if n == 4:
      break
  if no == 1:
    return extra
  else:
    return [extraa,extra]

def get_response(intents_list,intents_json,text):
  tag = intents_list[0]['intent']
  list_of_intents = intents_json['intents']
  result = ""
  extra = ""
  for i in list_of_intents : 
    if i['tag'] == tag:
      if tag == 'bored' or tag == 'music':
        tone = get_tone(tonetext(text))
        print(tone) 
        extra = get_tone_response(tone,1)
        # songs = getSongs(tone)
        
        # for n, song in enumerate(random.sample(songs[0],10)) or [[]]:
        #   extra = extra + "<br> " +str(n)+ ") Name: <a href ="+ str(song[2]) + ">"+str(song[0])+"</a><br> Artist: " + str(song[1])
        #   if n == 4:
        #     break
      result = random.choice(i['responses']) + extra 
      break
    
  return result




@app.route("/",methods=['GET','POST'])
def index():
  res = ""
  if request.method == 'POST':
    file = request.files["file"]
    print(file)
    if file:
      print(file)
      librosa_data, libroasa_sample_rate = librosa.load(file)
      mel = np.mean(librosa.feature.melspectrogram(librosa_data,sr = libroasa_sample_rate).T, axis =0 )
      result = np.array([])
      result = np.hstack((result,mel))
      inp = pd.DataFrame(result).T
      tone_pred = tone_model.predict(np.array(inp))[0]
      print(tone_pred)
      if tone_pred == 2:
        prediction = "sad"
      else:
        prediction = "happy"
      res = get_tone_response(prediction,2)
      print(tone_pred,res)
      return render_template(TEMPLATE_NAME,context = res[0])
    else:
  
      return render_template(TEMPLATE_NAME,context = res)
  else:
    return render_template(TEMPLATE_NAME,context = res)
  return render_template(TEMPLATE_NAME,context = res)
  
@app.route("/get",methods=['GET','POST'])
#function for the bot response
def get_bot_response(res=""):
  #if request.method == "POST":
  if res =="":
    userText = request.args.get('msg')
    
    userText = str(userText)

    
    ints = predict_class(userText)
    res = get_response(ints, intents,userText)

  
    
  return str(res)

#    return str(englishBot.get_response(userText))

if __name__ == "__main__":
	#print(type(classes))
	app.run(debug=False)




