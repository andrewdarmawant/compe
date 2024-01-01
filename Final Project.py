#!/usr/bin/env python
# coding: utf-8

# In[17]:


import keras
import aylien_news_api
from aylien_news_api.rest import ApiException
import re
from gensim.summarization.summarizer import summarize
import matplotlib.pyplot as plt


#load data from the dataset
imdb = keras.datasets.imdb
(train_data, train_labels),(test_data, test_labels) = imdb.load_data(num_words=10000)

word_index = imdb.get_word_index()

#account for reserved words such as "<PAD>" and "<START>"
word_index = {k:(v+3) for k,v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2
word_index["<UNUSED>"] = 3
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

def encode_data(decoded):
    return_this = []
    for words in decoded:
        return_this.append(word_index[words])
    return return_this

new_model = keras.models.load_model("/home/idstudent/Desktop/Theodore_Dhruv_model.h5")
new_model.load_weights("/home/idstudent/Desktop/checkpoints")
print("model loaded")


# In[18]:



new_model.summary()

def handle_inputs(string):
    ret = string.replace(" ", "AND")
    return ret

def set_inputs(inputs):
    # Configure API key authorization: app_id
    aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = ' 59139373'
    # Configure API key authorization: app_key
    aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = 'ce52a537a8fac6a82ce7ed55473a0444'

    # create an instance of the API class
    api_instance = aylien_news_api.DefaultApi()
    

    inputs = handle_inputs(inputs)
    opts = {
      'title': inputs,
      'sort_by': 'social_shares_count.facebook',
      'language': ['en'],
      'published_at_start': 'NOW-31DAYS',
      'published_at_end': 'NOW',
    }

def create_keep_list(news, dictionary):
    keep = []
    for i in news:
        if i in dictionary and i != '':
            keep.append(i)
    return keep

def load_news(index):
    api_response = api_instance.list_stories(**opts)
    news = api_response.stories[index]
    return news

def format_news(news, word_index):
    word_index_list = list(word_index.values())
    news = re.sub('"', '', news)
    #formatting the news
    news_list = re.split('[. ! ? , — % $ @ ( ) ]', news)
    
    keep_list = create_keep_list(news_list, word_index)
    return keep_list

def avg(ls):
    total = 0
    for i in range(len(preds)):
        total += preds[i]
    return (((total/len(preds))))

def setup_the_news():
    #try:
    # List stories 
    news = load_news(0).body.lower()
    keywords = load_news(0).keywords
    keep_list = format_news(news, word_index)
    preds = new_model.predict(encode_data(keep_list))
    summarized_news = summarize(news)
    print(news, summarized_news)
    return [news, summarized_news]
    #except:
     #   print("error")
      #  return(['Error'], ['Error'])
print("done")
        
'''
    #graph#
    sentiments = []
    counter = []
    number = input()
    number_of_articles = int(number)
    for j in range(number_of_articles):
        news = load_news(j).body.lower()
        keep_list = format_news(news, word_index)
        preds = new_model.predict(encode_data(keep_list))
        sentiments.append(avg(preds))
    
    for i in range(number_of_articles):
        counter.append(i)
    
    plt.plot(counter, sentiments, 'k-')
    #graph#
    
except ImportError:
    print("an error occured")
'''


# In[19]:


import numpy as np
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg


root = tk.Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
widget_value  = ""

def keyup(e):
    widget_value = user_input.get()
    if e.keycode == 36:
        if widget_value != '':
            print("going to page 2")
            PageTwo()
def PageOne():
    global user_input
    user_input = tk.Entry(canvas)
    user_input.place(x=10, y=10, width=100)
    root.bind("<KeyRelease>", keyup)
    user_input.pack()
    
def PageTwo():
    #clear page
    for widget in root.winfo_children():
        widget.destroy()
        
    set_inputs(widget_value)
    returned = setup_the_news()
    news = returned[0]
    summarized_news = returned[1]
    
    scrollbar = tk.Scrollbar()
    news_display = tk.Text(root, height=100, width=75)
    news_display.pack(side=tk.RIGHT)
    news_display.insert(tk.END, news)
    news_display.configure(state='disabled')

    summary_display = tk.Text(root, height=25, width=75)
    summary_display.pack(side=tk.LEFT)
    summary_display.insert(tk.END, summarized_news)
    summary_display.configure(state='disabled')



    sentiment_display = tk.Text(root, height=25, width=50)
    sentiment_display.pack(side=tk.LEFT)
    sentiment_display.insert(tk.END, current_sentiment)
    sentiment_display.configure(state='disabled')
    
    graph = matplotlib.figure.Figure(figsize=(2,1))
    a = fig.add_axes([0,0,1,1])
    a.plot(counter, sentiments)

canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

PageOne()
tk.mainloop()


# In[79]:
# In[ ]:




