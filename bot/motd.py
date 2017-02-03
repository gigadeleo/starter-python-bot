
# -*- coding: utf-8 -*-
# this file loads functions to extract a Maltese word from a dictionary, load it in an image and identify a mathcing example phrase

import textwrap
import urllib2
import datetime
import json
import requests
import random
from random import randint
from PIL import Image, ImageDraw, ImageFont

# constants used to extract motd
GABRA_START_URL = "http://mlrs.research.um.edu.mt/resources/gabra/lexemes/random/"
GABRA_BASE_JSON_URL = "http://mlrs.research.um.edu.mt/resources/gabra-api/lexemes/"
GLOSBE_URL = "https://glosbe.com/gapi/tm?from=mlt&dest=eng&format=json&phrase="

# constants used to generate image
MAX_W, MAX_H = (500,500)

# extract maltese word and identify possible example phrases 
def extract_word(): 
    fields_full = 0
    while fields_full == 0:
        try:
            # Request start URL and get redirected URL value
            requested_url = urllib2.Request(GABRA_START_URL)
            resulting_url = urllib2.urlopen(requested_url)
            redirected_url = resulting_url.geturl()

            # Split redirected URL - extract unique id of lexemes and retrieve API URL equivalent
            word_id = redirected_url.rsplit('/', 1)
            api_url = GABRA_BASE_JSON_URL + word_id[1]
            # api_url = GABRA_BASE_JSON_URL + "5852ae33b0e7e6656e1032db"

            resulting_url = urllib2.urlopen(api_url)
            api_data = json.loads(resulting_url.read())

            # print to console for debugging
            # print api_data["_id"]

            maltese_word = api_data["lemma"]
            english_word = api_data["gloss"]
            english_word = english_word.replace("\n", "; ")
            word_type = api_data["pos"]

            # GLOSBE EXAMPLES
            examples_url = GLOSBE_URL + maltese_word
            examples_resulting_url = urllib2.urlopen(examples_url)
            examples_data = json.loads(examples_resulting_url.read())

            example_phrase1 = examples_data["examples"][0]["first"] + "\r\n" + examples_data["examples"][0]["second"]
            
            # if any empty strings, discard and try another word
            if not maltese_word or not english_word or not word_type:
                fields_full = 0
                # print "some fields empty"
            else:
                fields_full = 1
        except:
            fields_full = 0
            # print "Exception: Non-conforming format."
    return maltese_word, english_word, word_type, example_phrase1

# create motd image
def create_mwotd(maltese_word, english_word, word_type):
    # open a random background image, set draw, set fonts
    rnd_back = random.randint(1,6)
    img = Image.open("commands/motd/image" + str(rnd_back) + ".png")
    draw = ImageDraw.Draw(img)
    mword_font = ImageFont.truetype(font="Verdana.ttf", size=50)
    eword_font = ImageFont.truetype(font="Verdana.ttf", size=30)

    # textwrap long words (chances are it may overlap)
    maltese_wordwrap = textwrap.wrap(maltese_word, width=18)
    english_wordwrap = textwrap.wrap(english_word, width=30)

    # set initial height, padding for all words and start drawing on background image
    current_h, pad = 100, 0
    for line in maltese_wordwrap:
        w, h = draw.textsize(line, font=mword_font)
        draw.text(((MAX_W - w) / 2, current_h), line, font=mword_font)
        current_h += h + pad
    
    current_h, pad = 230, 0
    w, h = draw.textsize(word_type, font=eword_font)
    draw.text(((MAX_W - w) / 2, current_h), word_type, font=eword_font)
    
    current_h, pad = 270, 0
    for line in english_wordwrap:
        w, h = draw.textsize(line, font=eword_font)
        draw.text(((MAX_W - w) / 2, current_h), line, font=eword_font)
        current_h += h + pad
    current_h += h + pad

    # save image for today (where Monday is 0 and Sunday is 6)
    daynum = datetime.datetime.today().weekday()
    filename = 'commands/motd/' + str(daynum) + '_image.png'
    img.save(filename)

    return filename

# post image to slack as bot and return example phrases
def post_image(filename, token, channels):
    f = {'file': (filename, open(filename, 'rb'), 'image/png', {'Expires':'0'})}
    response = requests.post(url='https://slack.com/api/files.upload', data={'token': token, 'channels': channels, 'media': f}, headers={'Accept': 'application/json'}, files=f)
    return response.text