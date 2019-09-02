import os
from flask import Flask, render_template, request
from flask import send_from_directory
import tweepy
from textblob import TextBlob
import numpy as np


app = Flask(__name__)

hashtags_file_path = 'uploads/hashtags_searched.txt'

#define variables for tweepy
consumer_key = '' #enter consumer key
consumer_secret = '' #enter consumer key secret
access_token = '' #enter access token
access_token_secret = '' #enter access token secret


#setup twitter authentication
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

# home page
@app.route('/')
def home():
   return render_template('index.html')


@app.route('/analyze', methods=['POST','GET'])
def analyzeTweet():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        hashtag = request.form['hashtag']
        f = open(hashtags_file_path,'a')
        if hashtag:
            tweets = []
            polaritylist = []
            subjectivitylist = []
            sentiments = []
            tweets = api.search(hashtag, rpp=100, since_id=1, count=5000)
            for tweet in tweets:
                if TextBlob(tweet.text).polarity != 0.0 and TextBlob(tweet.text).subjectivity != 0.0:
                    polaritylist.append(TextBlob(tweet.text).polarity)
                    subjectivitylist.append(TextBlob(tweet.text).subjectivity)
                    print(TextBlob(tweet.text).sentiment)


            if len(polaritylist) > 0 and len(subjectivitylist) > 0:
                polarity = round(np.mean(polaritylist),3)*100
                subjectivity = round(np.mean(subjectivitylist),3)*100
                sentiments = [polarity,subjectivity]
                f.write(hashtag + ' ' + '=> Polarity:' + str(polarity) + ' ' + 'Subjectivity:' + str(subjectivity) + '\n')
                f.close()
                return render_template('analyze.html', sentiments = sentiments, hashtag=hashtag)
            else:
                return render_template('analyze.html', error_message='No tweets found!')
        else:
            return render_template('analyze.html', error_message="Enter some hashtag!")



if __name__ == '__main__':
    app.run(debug=False,threaded=False)
