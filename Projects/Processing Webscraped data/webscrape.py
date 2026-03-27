#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd


# # Extract Text from Webpage

# In[4]:


# Import data
urls = pd.read_csv("Data/raw_script_urls.csv", delimiter=',', encoding='utf=8')
urls


# In[5]:


# Use request to get response
import requests
response = requests.get(urls['script_url'][0])
response


# In[6]:


# Get text
html_string = response.text
print(html_string)


# # Task 1

# In[40]:


# Write a function that gets the text from a url
# Create a "sample_urls" dataframe that contains the 10th to 19th rows by slicing the "url" dataframe with iloc
# Finally, apply the function to the "sample_urls" dataframe
import requests

def text_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None
urls = ['https://en.wikipedia.org/wiki/Information_science',
        'https://en.wikipedia.org/wiki/University',
]
    
sample_urls =pd.DataFrame({'url': urls})


sample = sample_urls.iloc[10:20]

sample['text'] = sample['url'].apply(text_url)

print(sample)


# In[ ]:





# In[ ]:





# # Web Scrapping

# In[8]:


response = requests.get("http://static.decontextualize.com/kittens.html")
html_string = response.text
print(html_string)


# In[9]:


# BeautifulSoup: a library for parsing HTML and XML documents
from bs4 import BeautifulSoup


# In[10]:


# Parse the document
document = BeautifulSoup(html_string, "html.parser")
document


# In[11]:


# Find h1
document.find("h1")


# In[12]:


# Find the text of h1
document.find("h1").text


# In[13]:


# Find all h2
document.find_all("h2")


# In[15]:


# Find the text in all h2
document.find_all("h2").text


# In[ ]:


all_h2_headers = document.find_all("h2")
h2_headers = []
for header in all_h2_headers:
    header_contents = header.text
    h2_headers.append(header_contents)
h2_headers


# In[ ]:


# Find image
document.find("img")


# In[ ]:


# Find all images
document.find_all("img")


# In[ ]:


# Get attributes
src = document.find("img").get('src')
src


# In[ ]:


# Display image
from IPython.display import Image, display, IFrame
display(Image(url=src))


# In[ ]:


# Display video
IFrame("https://www.youtube.com/embed/y47naisRxTc", width='500', height='400')


# In[ ]:


# Find divisions
document.find_all("div", attrs={"class": "kitten"})


# # Task 2

# In[ ]:


# Create a dataframe of TV shows that kittens love, with two columns "Name" and "Link"
# Names and links are in the HTML document, and can be obtained using "find_all" functin = document.find_all("a")
text = document.find_all('a')
#kittens_df = 
text


# # Regular Expression

# In[ ]:


# re stands for regular expression
import re
sample_song = "\n              Back in the Day (Ft.\xa0JAY-Z)\n              Lyrics\n"
sample_song


# In[ ]:


# \W means not a word, + means match one or more instance
re.sub("\W+", " ", sample_song) # so we match every none word for one or more times and replace it with space


# In[ ]:


# This can also be done with compile
not_word_pattern = re.compile("\W+")
re.sub(not_word_pattern, " ", sample_song)


# In[ ]:


# Search for pattern
word_pattern = re.compile("\w+") # \w means a word
word_pattern.search(sample_song)


# In[ ]:


word_pattern.search(sample_song).group(0)


# In[ ]:


# Find all instances
word_pattern = re.compile("\w+")
word_pattern.findall(sample_song)


# In[ ]:


# Match before a certain string
before_ft_pattern = re.compile(".*(?=Ft)") # . means any character, * means match 0 or more times
# (?=desired_pattern) checks if the desired_pattern is present immediately after the current position
before_ft_pattern.search(sample_song).group(0)


# In[ ]:


# Backslash Escape Characters
before_ft_pattern = re.compile(".*(?=\(Ft)") # use backslash to convert ( to a literal "("
clean_sample_song_title = before_ft_pattern.search(sample_song).group(0)
clean_sample_song_title


# In[ ]:


# Strip leading and trailing whitespace
clean_sample_song_title.strip()


# # Task 3

# In[ ]:


# Write a function that cleans up the given text, and gets all IDs in it 
# You can first extract all emails by matching a certain pattern, and then extract the NetIDs by matching before "@"
# The output should be "['id1', 'id2', 'id3']""

def clean_up(text):
    #text_with_netIDs.recompile(\'W+')
    #text.search()
    
    

text_with_netIDs = "The important email addresses are id1@illinois.edu, id2@indiana.edu, id3@michigan.edu"
clean_up(text_with_netIDs)


# # Task 4

# In[ ]:


# Write a function that get the title of all songs from a certain album
# You can print "document" and see where the title of songs are in the parsed html file, and match them using "find_all"
# After getting all titles, you can print out the list and see how to clean them (hint: you can use "replace" and "strip")
# After cleaning each song, drop the last one in the list as it is not a title
# The result should be a list beginning with 'Welcome to New York' and ending with 'Clean'

def get_all_songs_from_album(artist, album_name):  
    response = requests.get("https://genius.com/albums/" + artist + '/' + album_name)
    html_string = response.text
    document = BeautifulSoup(html_string, "html.parser")
    document.find_all('h3')
    
    print(document)


get_all_songs_from_album("Taylor-Swift", "1989")


# In[ ]:





# # API

# In[ ]:


# Install the required library of HathiTrust API
get_ipython().system('pip install hathitrust-api')


# In[ ]:


# Import BibAPI and initialize
from hathitrust_api import BibAPI
bib_api = BibAPI()


# In[ ]:


# Load the bibliographic information of a book
bib_info = bib_api.get_single_record_json('recordnumber', '100481764', True) # Specify MARC record is included
bib_info


# In[ ]:


# Get XML data
marc = bib_info['records']['100481764']['marc-xml']
print(marc)


# In[ ]:


# Get all data field
soup = BeautifulSoup(marc, 'xml')
soup.find_all('datafield')


# In[ ]:


# Get a specific field
for field in soup.find_all('datafield'):
    if field.get('tag') == '035':
        print(field)


# In[ ]:


# Find subfield
for field in soup.find_all('datafield'):
    if field.get('tag') == '035':
        print(field.find_all('subfield'))





