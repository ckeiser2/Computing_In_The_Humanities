#!/usr/bin/env python
# coding: utf-8

# # Named Entity Recognition (NER)

# Named Entity Recognition (NER) will help us computationally identify people, places, and things (of various kinds) in a text or collection of texts. It is useful for extracting key information from texts. You might use NER to identify the most frequently appearing characters in a novel or build a network of characters (related to network analysis), or you might use NER to identify the geographic locations mentioned in texts, a first step toward mapping the locations (related to spatial analysis).

# In[1]:


# Install spaCy for NER and other Natural Language Processing (NLP) tasks
get_ipython().system('pip install -U spacy')


# spaCy relies on machine learning models that were trained on a large amount of carefully-labeled texts. The English-language spaCy model that we’re going to use was trained on an annotated corpus called "OntoNotes": 2 million+ words drawn from "news, broadcast, talk shows, weblogs, usenet newsgroups, and conversational telephone speech," which were meticulously tagged by a group of researchers and professionals for people’s names and places, for nouns and verbs, for subjects and objects, and much more.

# In[2]:


import spacy
from spacy import displacy # visualization based on spaCy
from collections import Counter # counting the results
import pandas as pd # dealing with dataframe


# In[3]:


# Download the English-language model
get_ipython().system('python -m spacy download en_core_web_sm')


# In[4]:


# Load the English language model
import en_core_web_sm
nlp = en_core_web_sm.load()


# In[5]:


# Load the dataset
movie = pd.read_csv('Data/movie_dialogue.csv')
movie


# In[6]:


# Let's see the lines of the 1st character in the 1st movie
print(movie['lines'][0])


# In[7]:


# Visualize the name entity spaCy recognizes (note that the results are not perfect)
document = nlp(movie['lines'][0])
displacy.render(document, style="ent")


# # Exploring Different Types of Entities

# In[8]:


# Count and sort the number of characters with lines of each movie
movie.groupby('mname')['mid'].count().sort_values(ascending=False)


# In[9]:


# Count the number of entities in the lines of the characters in the movie magnolia
ent_types = dict() # initialize a dictionary
for line in movie[movie['mname']=='magnolia']['lines']: # loop through the lines in "magnolia"
    doc = nlp(line)
    for entity in doc.ents: # for each character, loop through all the entities
        label = entity.label_ # get their labels
        if label not in ent_types: # make sure there's a key for this label in the dictionary
            ent_types[label] = Counter() # each label key points to a Counter for examples
        text = entity.text
        ent_types[label][text] += 1 # count the number of times we see each example


# In[10]:


# Count of each type of entities
for etype, examples in ent_types.items():
    print(etype, len(examples))


# In[11]:


# Explain the entity type "PERSON"
spacy.explain('PERSON')


# In[12]:


# Get all people
people = []
for line in movie[movie['mname']=='magnolia']['lines']:
    doc = nlp(line)
    for named_entity in doc.ents:
        if named_entity.label_ == "PERSON": # we only want the labels with a type "PERSON"
            people.append(named_entity.text)
people_count = Counter(people)
# sort the people names by their occurences, and convert the results into a dataframe
people_magnolia = pd.DataFrame(people_count.most_common(), columns=['character', 'count'])
people_magnolia


# In[13]:


# Explain a certain type of entity "TIME" and "DATE"
print("TIME:", spacy.explain('TIME'))
print("DATE:", spacy.explain('DATE'))


# # Task 1

# In[14]:


# Get entities related to time and their numbers in the movie magnolia and convert the sorted results to a dataframe.
# Like what we did for "people", first create an empty list, and then loop through each line in the movie
# and use "nlp" to convert the line. Next, loop through each entity of the line, and select the entity based on labels
# "TIME" or "DATE", and append the result to the empity list. Finally, use Counter to count the results,
# create a dataframe and sort them using "most_common."

time = []
for line in movie[movie['mname']=='magnolia']['lines']:
    doc = nlp(line)
    for named_entity in doc.ents:
        if named_entity.label_ == "TIME" or named_entity.label_ == "DATE":
            time.append(named_entity.text)
time_count = Counter(time)
time_magnolia = pd.DataFrame(time_count.most_common(), columns=['character', 'count'])
print(time_magnolia)




# In[15]:


# Get the total word count of all lines of movies released in the year of 1960
movie_1960_df = movie[(movie['year']==1960)]
movie_1960_wordcount = movie_1960_df["wordcount"].sum()
movie_1960_wordcount


# In[16]:


# Get the total word count of all lines of movies released in the year of 2009
movie_2009_df = movie[(movie['year']==2009)]
movie_2009_wordcount = movie_2009_df["wordcount"].sum()
movie_2009_wordcount


# # Task 2

# In[17]:


# Calculate the number of entities related to time in movies released in 1960 and 2009, and divide by respective word counts.
# First, initialize a variable "time_1960_count" and set it as 0. Then like what we did before, loop through each line in 
# movie_1960_df['lines'], and use "nlp" to convert the line. Next, loop through each entity of the line, 
# and if the entity has a label of "TIME" or "DATE", add 1 to time_1960_count. Finally, print time_1960_count,
# divided by movie_1960_wordcount. And then repeat the process for 2009 movies.

time_1960_count = 0
for line in movie[movie['year']==1960]['lines']:
    doc = nlp(line)
    for named_entity in doc.ents:
        if named_entity.label_ == "TIME" or named_entity.label_ == "DATE":
            time_1960_count += 1 
print('1960:',time_1960_count/movie_1960_wordcount)

time_2009_count = 0
for line in movie[movie['year']==2009]['lines']:
    doc = nlp(line)
    for named_entity in doc.ents:
        if named_entity.label_ == "TIME" or named_entity.label_ == "DATE":
            time_2009_count += 1 
print('2009:', time_2009_count/movie_2009_wordcount)




# # Part-of-Speech (POS) Tagging

# Parts of speech are the grammatical units of language, such as (in English) nouns, verbs, adjectives, adverbs, pronouns, and prepositions. Each of these parts of speech plays a different role in a sentence. By computationally identifying parts of speech, we can start computationally exploring syntax, the relationship between words, rather than only focusing on words in isolation, as we did with tf-idf.

# In[18]:


# Get the POS tagging of a sample text
sample = """Or set upon a golden bough to sing to lords and ladies of Byzantium of what is past, or passing, or to come."""
# This is an excerpt from "Sailing to Byzantium" by the Irish poet W. B. Yeats
document = nlp(sample)
options = {"compact": True, "distance": 90, "color": "yellow", "bg": "black", "font": "Gill Sans"}
displacy.render(document, style="dep", options=options) # visualize it


# In[19]:


# Get part-of-speech tags
for token in document:
    print(token.text, token.pos_, token.dep_) # pos_ means part-of-speech tags, and dep_ means dependency


# In[20]:


# Get verbs from the movie "magnolia" in the movie dialogue dataset

verbs = []
for line in movie[movie['mname']=='magnolia']['lines']:
    doc = nlp(line)
    for token in doc: # loop through the token, instead of entities
        if token.pos_ == 'VERB': # we only want the tokens with a POS tagging of "VERB"
            verbs.append(token.text)
verbs_count = Counter(verbs)
# sort the verb by their occurences, and convert the results into a dataframe
verbs_magnolia = pd.DataFrame(verbs_count.most_common(), columns=['verb', 'count'])
verbs_magnolia


# # Task 3

# In[21]:


# Get the top 10 adjectives by count in movies released in 1960 and 2009.
# Like what we did for the movie "magnolia", first create an empty list of adjectives, and then loop through each line in 
# movie_1960_df['lines'], and use "nlp" to convert the line. Next, loop through each token of the line, and select the entity 
# based on POS tagging "ADJ", and append the result to the empity list. Finally, use Counter to count the results,
# create a dataframe and sort them using "most_common," and print the top 10 adjectives.
# And then repeat the process for 2009 movies.

adjectives = []
for line in movie[movie['year']==1960]['lines']:
    doc = nlp(line)
    for token in doc:
        if token.pos_ == 'ADJ':
            adjectives.append(token.text)
adj_count = Counter(adjectives)
adj_1960 = pd.DataFrame(adj_count.most_common(), columns=['adjectives', 'count'])
print('1960', adj_1960[:10])

adjectives2 = []
for line in movie[movie['year']==2009]['lines']:
    doc = nlp(line)
    for token in doc:
        if token.pos_ == 'ADJ':
            adjectives2.append(token.text)
adj2_count = Counter(adjectives2)
adj_2009 = pd.DataFrame(adj2_count.most_common(), columns=['adjectives', 'count'])
print('2009', adj_2009[:10])



# # Keyword Extraction

# In[22]:


import re # regular expression
from IPython.display import Markdown, display # for visualization


# In[23]:


# Visualize the data from the movie Casablanca
movie_casablanca = movie[movie['mname']=='casablanca'].reset_index(drop=True)
for line in movie_casablanca['lines']:
    displacy.render(nlp(line), style="ent")


# In[24]:


# Define a function to find keywords in its context
def find_sentences_with_keyword(keyword, document): 
    # loop through all the sentences in the document and pull out the text of each sentence
    for sentence in document.sents:
        sentence = sentence.text        
        # check to see if the keyword is in the sentence (and ignore capitalization by making both lowercase)
        if keyword.lower() in sentence.lower():            
            # use regular expression to replace linebreaks and to make the keyword bolded, again ignoring capitalization
            sentence = re.sub('\n', ' ', sentence)
            sentence = re.sub(f"{keyword}", f"**{keyword}**", sentence, flags=re.IGNORECASE)            
            display(Markdown(sentence))


# In[25]:


# Highlight the name of the protagonist Rick in its context of the lines of the second character of the movie
find_sentences_with_keyword(keyword="Rick", document=nlp(movie_casablanca['lines'][1]))


# In[26]:


# Create a list of tokens and POS labels from document if the token is a word 
tokens_and_labels = [(token.text, token.pos_) for token in nlp(movie_casablanca['lines'][1]) if token.is_alpha]
tokens_and_labels


# In[27]:


# Define a function to get all two-word combinations
def get_bigrams(word_list, number_consecutive_words=2):  
    ngrams = []
    adj_length_of_word_list = len(word_list) - (number_consecutive_words - 1)   
    # loop through numbers from 0 to the (slightly adjusted) length of your word list
    for word_index in range(adj_length_of_word_list):       
        # index the list at each number, grabbing the word at that number index as well as N number of words after it
        ngram = word_list[word_index : word_index + number_consecutive_words]        
        # append this word combo to the master list "ngrams"
        ngrams.append(ngram)        
    return ngrams


# In[28]:


# Getting all bigram of the lines, including both the word and its POS label
bigrams = get_bigrams(tokens_and_labels)
bigrams


# In[29]:


# Define a function to get the neighboring words based on bigrams
def get_neighbor_words(keyword, bigrams, pos_label = None):    
    neighbor_words = []
    keyword = keyword.lower()    
    for bigram in bigrams:       
        # extract just the lowercased words (not the labels) for each bigram
        words = [word.lower() for word, label in bigram]                
        # check to see if keyword is in the bigram
        if keyword in words:         
            for word, label in bigram:
                if word.lower() != keyword: # focusing on the neighbor word, not the keyword
                    neighbor_words.append(word.lower())    
    # return the word list after sorting it
    return Counter(neighbor_words).most_common()


# In[30]:


# Get the neighboring words of the character Rick
get_neighbor_words("Rick", bigrams)


# # Task 4

# In[31]:


# Print the neighboring words of the character Rick in each character's lines of the movie Casablanca and the characters' names.
# Write a loop through the movie_casablanca dataframe, copy the codes above of creating a list of tokens and POS labels 
# from each line if the token is a word, and then get all bigram of the lines. Finally, print movie_casablanca['cname'] of 
# that line, along with the neighboring words of Rick in that line.

for i in range(len(movie_casablanca['lines'])):
    tokens_and_labels = [(token.text, token.pos_) for token in nlp(movie_casablanca['lines'][i]) if token.is_alpha]
    bigrams = get_bigrams(tokens_and_labels)
    print(movie_casablanca['cname'][i], get_neighbor_words('Rick',bigrams))


# # Task 5

# What insights can be derived from the movie dialogue dataset using the Named Entity Recognition extraction method? Similarly, what insights can be gained through the Position-of-Speech tagging method? Please provide an example for each method, either based on the experiments covered above or by thinking of something else.

# Some of the key takeaways we can pull from the movie dialogues using the Named entity recognition is being able to identify different types of entities in the movie dialogue. Although not 100% accurate this does serve to get an idea of how many People, Time, Cardinal, etc are in a given text. For instance if we are doing an analysis of the movie magnolia like in Task 1 but analyzing the motif of time we can analyze the occurrences of different words like today, tonight, years, etc. By doing this we can extract different themes from the text/movie. With position-of-speech tagging we can understand what common words are surrounding characters from a piece of work like a movie/text/etc. What we did in Task 4 is show different characters names with neighboring words. This can give a lot of context for the characters and their importance/role in the play such as Annina being referred to as 'Monsieur' multiple times showing that she is a woman of high importance maybe even high social status or class. 
