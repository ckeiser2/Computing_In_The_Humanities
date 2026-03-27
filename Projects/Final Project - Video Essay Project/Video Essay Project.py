#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import re
get_ipython().system(' pip install nltk')
import nltk
nltk.download('stopwords')
# Gensim, for topic modeling
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# Plotting tools
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


df = pd.read_csv("Data/YoutubeVideoEssayProject.csv")
df = df.drop(columns ="Unnamed: 9")
df


# In[ ]:


#cleaned text in df
def clean_text(list_): 
    regex_newline = re.compile(r'\n')
    regex_timestamp = re.compile(r'\d:\d\d')
    regex_whitespace = re.compile(r'\s{2,}')
    for index, item in enumerate(list_):
        item = str(item)
        item = re.sub(regex_newline, " ", item)
        item = re.sub(regex_timestamp, " ", item)
        item = re.sub(regex_whitespace, " ", item)
        item = re.sub(r'"', "", item)
        item = re.sub(r'\s1\s', ' ', item)
        item = re.sub(r'\s2\s', ' ', item)
        list_[index] = item
    return list_
df["Transcript"] = clean_text(df["Transcript"])
df["Description"] = clean_text(df["Description"])
df


# In[ ]:


# Initialize TfidfVectorizer, using English stopwords and converting words to lowercase
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)


# In[ ]:


tfidf_matrix = tfidf_vectorizer.fit_transform(df['Transcript']) # Generate a matrix
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out()) # Convert matrix to dataframe
tfidf_df.set_index(df['Title'], inplace=True) 
tfidf_df = tfidf_df.stack().reset_index()
tfidf_df = tfidf_df.rename(columns={0:'tfidf', 'Title': 'document','level_1': 'term'})
tfidf_df.sort_values(by=['document','tfidf'], ascending=[True,False]).groupby(['document']).head(1)


# In[ ]:


get_ipython().system('pip install altair')


# In[ ]:


# Some fancy visualizations to highlight the words with highest TF-IDF score in each inaugural address
import altair as alt

top_tfidf = tfidf_df.sort_values(by=['document','tfidf'], ascending=[True,False]).groupby(['document']).head(10)

# Terms in this list will get a red dot in the visualization
term_list = ['queer', 'peace']

# adding a little randomness to break ties in term ranking
top_tfidf_plusRand = top_tfidf.copy()
top_tfidf_plusRand['tfidf'] = top_tfidf_plusRand['tfidf'] + np.random.rand(top_tfidf.shape[0])*0.0001

# base for all visualizations, with rank calculation
base = alt.Chart(top_tfidf_plusRand).encode(
    x = 'rank:O',
    y = 'document:N'
).transform_window(
    rank = "rank()",
    sort = [alt.SortField("tfidf", order="descending")],
    groupby = ["document"],
)
# heatmap specification
heatmap = base.mark_rect().encode(
    color = 'tfidf:Q'
)

# red circle over terms in above list
circle = base.mark_circle(size=100).encode(
    color = alt.condition(
        alt.FieldOneOfPredicate(field='term', oneOf=term_list),
        alt.value('red'),
        alt.value('#FFFFFF00')        
    )
)

# text labels, white for darker heatmap colors
text = base.mark_text(baseline='middle').encode(
    text = 'term:N',
    color = alt.condition(alt.datum.tfidf >= 0.23, alt.value('white'), alt.value('black'))
)

# display the three superimposed visualizations
(heatmap + circle + text).properties(width = 600)


# In[ ]:





# In[ ]:





# In[ ]:




