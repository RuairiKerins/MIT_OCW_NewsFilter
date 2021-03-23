# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import re


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        '''
        Initializes a NewsStory object

        NewsStory  object has 5 objects
            self.guid - globally unique identifier (GUID) - a string
            self.title - title - a string
            self.description - description - a string
            self.link - link to more content - a string
            self.pubdate - pubdate - a ​ datetime

        '''
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        '''
        Used to safely access self.guid outside of the class
        
        Returns: self.guid
        '''
        return(self.guid)
    def get_title(self):
        '''
        Used to safely access self.title outside of the class
        
        Returns: self.title
        '''        
        return(self.title)
    def get_description(self):
        '''
        Used to safely access self.description outside of the class
        
        Returns: self.description
        '''
        return(self.description)
    def get_link(self):
        '''
        Used to safely access self.link outside of the class
        
        Returns: self.link
        '''
        return(self.link)
    def get_pubdate(self):
        '''
        Used to safely access self.pubdate outside of the class
        
        Returns: self.pubdate
        '''
        return(self.pubdate)
#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """

        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):

    def __init__(self, phrase):
        """
        Initializes a PhaseTrigger object
        Phrase (string): the phrase in all lowercase
        """
        self.phrase = str(phrase).lower()

    def is_phrase_in(self, text):
        """
        Returns ​ True​ if phrase​ is present in text, false​ otherwise  
        """
        self.text = text
        phrase_list = re.findall(r'\w+', self.phrase.lower())
        text_list = re.findall(r'\w+', self.text.lower())
        i = 0
        j = 0
        match = 0 

        while i < len(text_list) :
            
            if text_list[i] == phrase_list[j]:
                while j < len(phrase_list) and j+i < len(text_list):
                    if text_list[i+j] == phrase_list[j]:
                        match += 1 
                    j += 1
                if match is len(phrase_list):
                    return True
                j = 0
            i += 1
        else:
            return False

# Problem 3
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        """
        Initializes a PhaseTrigger object
        Phrase (string): the phrase in all lowercase
        """
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self,story):
        """
        Returns ​ True​ if phrase​ is present in text, false​ otherwise  
        """
        return self.is_phrase_in(story.get_title())


# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        """
        Initializes a PhaseTrigger object
        Phrase (string): the phrase in all lowercase
        """
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self,story):
        """
        Returns ​ True​ if phrase​ is present in text, false​ otherwise  
        """
        return self.is_phrase_in(story.get_description())


# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):

    def __init__(self, timestamp):
        """
        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
        Convert time from string to a datetime before saving it as an attribute.
        """
        date_object = datetime.strptime(timestamp, "%d %b %Y %H:%M:%S") 
        self.date_trigger = date_object

# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def __init__(self, date):
        TimeTrigger.__init__(self, date)
    def evaluate(self, story):
        pub_date = story.get_pubdate().replace(tzinfo=None)
        if self.date_trigger > pub_date:
            return True
        else:
            return False

class AfterTrigger(TimeTrigger):
    def __init__(self, date):
        TimeTrigger.__init__(self, date)
    def evaluate(self, story):
        pub_date = story.get_pubdate().replace(tzinfo=None)
        if self.date_trigger < pub_date:
            return True
        else:
            return False
# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__ (self, input_trigger):
        self.trigger = input_trigger
    def evaluate(self, story):
        return not self.trigger.evaluate(story)

# Problem 8
class AndTrigger(Trigger):
    def __init__ (self, input_trigger1, input_trigger2):
        self.trigger1 = input_trigger1
        self.trigger2 = input_trigger2
    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)
# Problem 9
class OrTrigger(Trigger):
    def __init__ (self, input_trigger1, input_trigger2):
        self.trigger1 = input_trigger1
        self.trigger2 = input_trigger2
    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    return stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    print(lines) # for now, print it so you see what it contains!



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

