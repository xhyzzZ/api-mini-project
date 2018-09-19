# Multifunction Python-Based Twitter Library

Library that downloads images from a twitter feed, convert them to a video and describe the content of the images in the video.



## Basic Usage


You can download the pictures for a given user as follows:

```bash
# Download 20 images from the KDtrey5 Twitter Account
python run.py --username KDtrey5 --num 20


The library also allows to include retweets or replies, and to specify a different folder to save the pictures in ("pictures" is the default)

python run.py --username NASA --num 10 --replies --retweets
python run.py --username NASA --num 10 --replies --retweets --output ../NASA_Pictures
python run.py --username NASA --num 10 --replies --retweets --config config.cfg --output ../NASA_Pictures

```
You can convert downloaded images to a video as follows:
``` bash
# Convert downloaded imgaes to a video 
python ffmpeg.py
```
You can label image information as follows:
```bash
# Label image imformation use Google vision api

Step.1 This library requires you to have authentication setup. Refer to https://cloud.google.com/docs/authentication/getting-started the for instructions on setting up
credentials for applications.

Step.2 Clone the library and change directory to the library directory you want to use.

Step.3 Install pip and virtualenv if you do not already have them. You may want to refer to the https://cloud.google.com/python/setup for Google Cloud Platform for instructions.

Step.4 Install the dependencies needed to run the library.
$ pip install -r requirements.txt

Step.5 Create a virtualenv and activate.
$ virtualenv --python python3 env
$ source env/bin/activate

deactivate
$ deactivate

Step.6 Run the code
python label.py imgxxx.jpg

```

The library will only download pictures that are not in the output folder already to avoid duplications. 