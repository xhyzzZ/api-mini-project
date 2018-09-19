import tweepy
import os
import glob
from tweepy import OAuthHandler
import json
import wget
import argparse
import configparser

def parse_arguments():
  parser = argparse.ArgumentParser(description='Download pictures from Twitter.')
  group = parser.add_mutually_exclusive_group(required=True)
  parser.add_argument('--config', type=str, default='./config.cfg', help='Path to the configuration file')
  group.add_argument('--username', type=str, help='Fetch pictures from user account')
  parser.add_argument('--num', type=int, default=50, help='The maximum number allow to download')
  parser.add_argument('--retweets', default=False, action='store_true', help='Include retweets')
  parser.add_argument('--replies', default=False, action='store_true', help='Include replies')
  parser.add_argument('--output', default='pictures/', type=str, help='folder where the pictures will be stored')

  args = parser.parse_args()
  return args

def parse_config(config_file):
  config = configparser.ConfigParser()
  config.read(config_file)
  return config 
  
@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

def init_tweepy():
  # Status() is the data model for a tweet
  tweepy.models.Status.first_parse = tweepy.models.Status.parse
  tweepy.models.Status.parse = parse
  # User() is the data model for a user profil
  tweepy.models.User.first_parse = tweepy.models.User.parse
  tweepy.models.User.parse = parse

def authorise_api(config):
  auth = OAuthHandler(config['DEFAULT']['consumer_key'], config['DEFAULT']['consumer_secret'])
  auth.set_access_token(config['DEFAULT']['access_token'], config['DEFAULT']['access_secret'])
  return auth

# It returns [] if the tweet doesn't have any media
def media_urls(tweet_status):
  media = tweet_status._json.get('extended_entities', {}).get('media', [])
  if (len(media) == 0):
    return []
  else:
    return [item['media_url'] for item in media]

def createFolder(output_folder):
  if not os.path.exists(output_folder):
      os.makedirs(output_folder)

def downloadImages(status, num_tweets, output_folder):
  createFolder(output_folder)
  downloaded = 0

  for tweet_status in status:

    if(downloaded >= num_tweets):
      break

    for media_url in media_urls(tweet_status):
      # Only download if there is not a picture with the same name in the folder already
      file_name = os.path.split(media_url)[1]
      if not os.path.exists(os.path.join(output_folder, file_name)):
        wget.download(media_url +":orig", out=output_folder+'/'+file_name)
        downloaded += 1

def download_images_by_user(api, username, retweets, replies, num_tweets, output_folder):
  status = tweepy.Cursor(api.user_timeline, screen_name=username, include_rts=retweets, exclude_replies=replies, tweet_mode='extended').items()
  downloadImages(status, num_tweets, output_folder)
  os.chdir(r'./pictures')
  for index, oldfile in enumerate(glob.glob("*.jpg"), start=1):
      newfile = 'img{:03}.jpg'.format(index)
      os.rename (oldfile,newfile)

def main():
  arguments = parse_arguments() 
  username = arguments.username
  retweets = arguments.retweets
  replies = arguments.replies
  num_tweets = arguments.num
  output_folder = arguments.output
  config_path = arguments.config

  config = parse_config(config_path)
  auth = authorise_api(config)
  api = tweepy.API(auth, wait_on_rate_limit=True)

  download_images_by_user(api, username, retweets, replies, num_tweets, output_folder)

if __name__=='__main__':
    main()
