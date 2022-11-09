#!/usr/bin/env python3
from sql import *
from player import *
from speech import *
from multiprocessing import Process, Value, Array
#import multiprocessing as mp
import time

# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for, redirect, session

# Initialize the Flask application
app = Flask(__name__)

num = Value('i', 0)
arr = Array('i', range(10))

arr[0] = os.getpid()
arr[1] = 40 #volume 
arr[2] = 0  #current song
arr[3] = 0  #previous song
print(arr[0])



# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    create_table()
    data = select_data_stats(arr)
    return render_template('home.html',items=data)

def startTheadPlayer():
    create_table()
    data = select_data_stats(arr)
    \
    p = Process(target=threader, args=(num, arr))
    p.start()


@app.route('/', methods=['GET', 'POST'])
def controls():

##   session.init_app(app)
 
   if request.method == 'POST':
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=1)
        if request.form['submit'] == 'Play By Name':
            song = request.form['song']
            if len(song) > 0:
                songCount = update_play_queue(song)
                num.value = 1
                print("Play By Name")
                time.sleep(1)
            return redirect(url_for('controls'))                    
            pass # do something
        elif request.form['submit'] == 'Play Text':
            texttosend = request.form['texttospeech']
            songCount = TextToSpeechPlay(texttosend)
            num.value = 1
            print("Text to Speech")
            time.sleep(1)
            return redirect(url_for('controls'))                    
            pass # do something
        elif request.form['submit'] == 'Find and Store All Songs':
            password = request.form['password']
            if password == "mickey08":
                create_table()
                queue_kill()
                num.value = 0
                drop_table('tblMusic')
                create_table()
                find_store_files()
                print("Find All")
            return redirect(url_for('controls'))
            pass # do something else
        elif request.form['submit'] == 'Kill Queue':
            create_table()
            num.value = 0
            queue_kill()
            print("Kill")
            time.sleep(1)
            return redirect(url_for('controls'))
            pass # do something else
        elif request.form['submit'] == 'Next Song':
            create_table()
            num.value = 1
            queue_next()
            print("Next")
            time.sleep(1)
            return redirect(url_for('controls'))
            pass # do something else
        elif request.form['submit'] == 'Mute':
            arr[1] = 0
            print("Mute")
            return redirect(url_for('controls'))
            pass # do something else
        elif request.form['submit'] == '40':
            arr[1] = 40
            print("40%")
            return redirect(url_for('controls'))
            pass # do something else
        elif request.form['submit'] == '50':
            arr[1] = 50
            print("50%")
            return redirect(url_for('controls'))
            pass # do something else
        elif request.form['submit'] == '60':
            arr[1] = 60
            print("60%")
            return redirect(url_for('controls'))
            pass # do something else
        elif request.form['submit'] == '70':
            arr[1] = 70
            print("70%")
            return redirect(url_for('controls'))
            pass # do something else
        elif request.form['submit'] == '80':
            arr[1] = 80
            print("80%")
            return redirect(url_for('controls'))
            pass # do something else
        elif request.form['submit'] == '90':
            arr[1] = 90
            print("90%")
            return redirect(url_for('controls'))
            pass # do something else
        elif request.form['submit'] == '100':
            arr[1] = 100
            print("100%")
            return redirect(url_for('controls'))
            pass # do something else
        elif request.form['submit'] == 'Go to Controls':
            return render_template('control.html')
        elif request.form['submit'] == 'Text to Speech':
            return render_template('tts.html')
        elif request.form['submit'] == 'Utilities':
            return render_template('Utils.html')
        elif request.form['submit'] == 'Show All Songs':
            data = select_data_allsongs()
            return render_template('AllSongs.html',items=data)
        elif request.form['submit'] == 'Add to Queue':
            selected_songs = request.form.getlist("songs")
            #print(len(selected_songs))
            if (len(selected_songs)>0):
                update_play_queue_selected(selected_songs)
                num.value = 1
                time.sleep(1)
            return redirect(url_for('controls'))
        elif request.form['submit'] == 'Delete Selected':
            selected_songs = request.form.getlist("songs")
            password = request.form['password']
            if password == "mickey08":
                if (len(selected_songs)>0):
                    delete_songs(selected_songs)
                    num.value = 1
                    time.sleep(1)
                    print("Deleted File")
            return redirect(url_for('controls'))
            pass # unknown
   data = select_data_stats(arr)
   return render_template('home.html',items=data)
   



# Run the app :)
if __name__ == '__main__':
  print("pre Thread")
  startTheadPlayer()
  print("post Thread")
  app.secret_key = 'super secret key'
  app.config['SESSION_TYPE'] = 'filesystem'
  app.run(
        threaded=True,
        #debug=True,
        host="0.0.0.0",
        port=int("8081")
  )
