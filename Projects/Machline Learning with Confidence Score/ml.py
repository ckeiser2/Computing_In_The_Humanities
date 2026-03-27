#!/usr/bin/env python
# coding: utf-8

# The term "machine learning" is surrounded by a mix of excitement and concerns. Some may call it "artificial intelligence" to highlight its complexity, while others might simplify it by dismissing it as nothing more than "glorified statistics." In reality, the boundary between traditional statistical modeling and the realm of "machine learning" is quite subtle.

# In[34]:


# Get the latest version of scikit-learn (library for machine learning)
get_ipython().system(' pip install --upgrade scikit-learn')


# In[35]:


# Check the scikit-learn version. It should be 1.3.2.
get_ipython().system('pip show scikit-learn')


# In[36]:


import numpy as np # performing calculations on arrays
import pandas as pd # dealing with dataframe

# Plotting tools
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

# For tokenizing text and build a machine learning model
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


# # Preprocessing

# In[37]:


# Load the data
trump = pd.read_csv("Data/trump.csv")
trump


# In[38]:


# Convert texts into a matrix of word counts
vectorizer = CountVectorizer(max_features = 500) # Select the top 500 words
sparse_matrix = vectorizer.fit_transform(trump['text']) # Fit and transform the original text into a matrix
termdoc = pd.DataFrame(sparse_matrix.toarray(), columns=vectorizer.get_feature_names_out())
# Convert the matrix to dataframe, using words as column names
termdoc


# In[39]:


# We want to begin with predicting what did Trump use to tweet. Let's see what "statusSource" looks like
trump.groupby('statusSource')['id'].count() 


# In[40]:


# Converting labels to numbers
def sourcestring_to_integer(sourcestring):
    if 'android' in sourcestring:
        return 0
    elif 'iphone' in sourcestring:
        return 1
    else:
        return 2


# In[41]:


trump['statusSource']= trump['statusSource'].map(sourcestring_to_integer) # map statusSource to 0, 1 or 2
trump = trump[(trump['statusSource']==0) | (trump['statusSource']==1)] # keep 0 and 1 only (Android or iPhone)
trump


# In[42]:


# First we have to shuffle the rows, as we're going to use the first 1000 rows as training set, and that might not be a random
trump = trump.sample(frac=1, random_state = 10) # This means we are keeping all data but have changed the order
trump


# In[43]:


# The list of keys (label to be predicted) for our prediction
source_keys = trump['statusSource']
source_keys


# In[44]:


# Select the word counts to match the index of the keys
termdoc = termdoc.loc[source_keys.index]
termdoc


# In[45]:


# We have to scale the matrix to reduce the power of frequent words (so that all data points will fall into the range of 0-1)
# In this way, the model will work better 
scaled_matrix = StandardScaler().fit_transform(termdoc)
scaled_matrix


# # Machine Learning: Train an Exact Model

# We can use the features in our matrix to predict whether a tweet came from android or iphone. It's possible to fit a model perfectly to the data. And if we're predicting the data we trained on, we'll be exactly right.
# The key element of the next line is C, which is "inverse of regularization strength; must be a positive float. Like in support vector machines, smaller values specify stronger regularization." Here, C = 10000000, which sets the regularization constant so high that it has no effect. There will be no blurriness in this model.
# First we train the model.

# In[46]:


# Using the first 1000 rows as the training set (note that we've already shuffled the data)
exact_model = LogisticRegression(C = 10000000).fit(scaled_matrix[:1000], source_keys[:1000])


# The logistic model is a statistical model that models the probability of an event taking place by having the log-odds for the event be a linear combination of one or more independent variables. It is commonly used in machine learning tasks. The goal is to model the probability of a random variable being 0 or 1 given experimental data.

# In[47]:


# Then we make predictions using the model we trained (on the same data)
predictions = exact_model.predict(scaled_matrix[:1000])


# In[48]:


# Let's see if the predicted results match the true labels
for i in range(20):
    if i in source_keys: # This is necessary because some rows are removed if they don't contain "Android" or "iPhone"
        print(source_keys[i], predictions[i])


# In[49]:


# Calculate the proportion of true predictions
sum(predictions == source_keys[:1000]) / len(predictions)


# In[50]:


# Then we try to make predictions outside the sample we originally trained on
test_predictions = exact_model.predict(scaled_matrix[1000 : , ])
sum(test_predictions == source_keys[1000 : ]) / len(test_predictions)


# One way to understand the problem is to look at predicted probabilities. This model tends to be very confident. Things are either iPhone (up at 1) or Android (down at 0). Colors indicate the real class values: red is android.

# In[51]:


def colorize(integer):
    if integer == 1:
        return 'Blue'
    else:
        return 'Red'


# In[52]:


# First we test the confidence of the model on the training data
probabilities_train_exact = [x[1] for x in exact_model.predict_proba(scaled_matrix[:1000, ])]
# Here, we calculate the probability for the model assigning the data to the second class, namely, "iPhone"
colors_train_exact = [colorize(x) for x in source_keys[: 1000]]

plt.figure(figsize = (8, 6))
plt.scatter(list(range(len(probabilities_train_exact))), probabilities_train_exact, c = colors_train_exact, alpha = 0.4)
plt.show()


# In[53]:


# Then we test the confidence of the model on the testing data
probabilities_test_exact = [x[1] for x in exact_model.predict_proba(scaled_matrix[1000:, ])]
colors_test_exact = [colorize(x) for x in source_keys[1000:]]

plt.figure(figsize = (8, 6))
plt.scatter(list(range(len(probabilities_test_exact))), probabilities_test_exact, c = colors_test_exact, alpha = 0.4)
plt.show()


# # Machine Learning: Train an Blurred Model

# To improve our accuracy out of sample, we need to be willing to let the model be imperfect.
# We can achieve this by using a regularization setting that limits the predictive power of features.

# In[54]:


# Let's change C value to 0.001 so that blurriness (randomness) is introduced to the model
blurry_model = LogisticRegression(C = 0.001).fit(scaled_matrix[0 : 1000, ], source_keys[0: 1000])


# In[55]:


# Make predictions within the sample we originally trained on
predictions = blurry_model.predict(scaled_matrix[0 : 1000, ])
sum(predictions == source_keys[0:1000]) / len(predictions)


# In[56]:


# Then we try to make predictions outside the sample we originally trained on
test_predictions = blurry_model.predict(scaled_matrix[1000 : , ])
sum(test_predictions == source_keys[1000 : ]) / len(test_predictions)


# And we can intuitively understand how that's working by looking at the predicted probabilities for individual tweets. This model is a lot less "confident" about any individual tweet.

# In[57]:


# First we test the confidence of the model on the training data using the blurry model
probabilities_train_blurry = [x[1] for x in blurry_model.predict_proba(scaled_matrix[:1000, ])]
colors_train_blurry = [colorize(x) for x in source_keys[: 1000]]

plt.figure(figsize = (8, 6))
plt.scatter(list(range(len(probabilities_train_blurry))), probabilities_train_blurry, c = colors_train_blurry, alpha = 0.4)
plt.show()


# In[58]:


# Then we test the confidence of the model on the testing data using the blurry model
probabilities_test_blurry = [x[1] for x in blurry_model.predict_proba(scaled_matrix[1000:, ])]
colors_test_blurry = [colorize(x) for x in source_keys[1000:]]

plt.figure(figsize = (8, 6))
plt.scatter(list(range(len(probabilities_test_blurry))), probabilities_test_blurry, c = colors_test_blurry, alpha = 0.4)
plt.show()


# # Task 1

# Create two new blurry models with different C values of 0.00001 and 0.01. For each model, duplicate the code for fitting the model with the first 1000 data points and predicting the data points after 1000. For each model, please answer: does the accuracy rate for the training set increase or decrease when compared to the original model with a C value of 0.001? Does the accuracy rate for the testing set increase or decrease when compared to the original model? What insights can be drawn from the impact of the C parameter on the model's performance?<br>
# Include your codes in the following cell (code) and the discussion in the next cell (markdown).

# In[59]:


blurry_model1 = LogisticRegression(C = 0.00001).fit(scaled_matrix[0 : 1000, ], source_keys[0: 1000])
predictions1 = blurry_model1.predict(scaled_matrix[0 : 1000, ])
print(sum(predictions1 == source_keys[0:1000]) / len(predictions1))
test_predictions1 = blurry_model1.predict(scaled_matrix[1000 : , ])
print(sum(test_predictions1 == source_keys[1000 : ]) / len(test_predictions1))
probabilities_train_blurry1 = [x[1] for x in blurry_model1.predict_proba(scaled_matrix[:1000, ])]
colors_train_blurry1 = [colorize(x) for x in source_keys[: 1000]]
plt.figure(figsize = (8, 6))
plt.scatter(list(range(len(probabilities_train_blurry1))), probabilities_train_blurry1, c = colors_train_blurry1, alpha = 0.4)
plt.show()




blurry_model2 = LogisticRegression(C = 0.01).fit(scaled_matrix[0 : 1000, ], source_keys[0: 1000])
predictions2 = blurry_model2.predict(scaled_matrix[0 : 1000, ])
print(sum(predictions2 == source_keys[0:1000]) / len(predictions2))
test_predictions2 = blurry_model2.predict(scaled_matrix[1000 : , ])
print(sum(test_predictions2 == source_keys[1000 : ]) / len(test_predictions2))
probabilities_train_blurry2 = [x[1] for x in blurry_model2.predict_proba(scaled_matrix[:1000, ])]
colors_train_blurry2 = [colorize(x) for x in source_keys[: 1000]]
plt.figure(figsize = (8, 6))
plt.scatter(list(range(len(probabilities_train_blurry2))), probabilities_train_blurry2, c = colors_train_blurry2, alpha = 0.4)
plt.show()


# With extremely high randomess like in model 1 than we see very inaccurate and worse outcomes for both the predictions. For model 2 introducing a bit of randomness actual helps the model with a very accurate prediction score. For model 1 with extremely high randomness we have worse accuracy than the original model, and with model 2 we have higher accuracy in the predictive accuracy and close accuracy in the tested predictive accuracy. What this tells us about the C value is that a little bit of randomness is healthy for the machine learning model.

# # Task 2

# Reload the dataset and create a new vectorizer with the "max_features" parameter set to 5000. Then, recreate the sparse matrix, term-document matrix, scaled matrix, and the blurry model by duplicating the codes provided above. Calculate the accuracy rate for the testing data with the new setup. Does the accuracy rate increase or decrease when compared to the original model with a "max_features" of 500? What insights can be drawn about the impact of the number of features on machine learning based on word frequency?<br>
# Include your codes in the following cell (code) and the discussion in the next cell (markdown).

# In[60]:


trump = pd.read_csv("Data/trump.csv")
vectorizer2 = CountVectorizer(max_features = 5000) 
sparse_matrix2 = vectorizer2.fit_transform(trump['text']) 
termdoc2 = pd.DataFrame(sparse_matrix2.toarray(), columns=vectorizer2.get_feature_names_out())
termdoc2 = termdoc2.loc[source_keys.index]
scaled_matrix2 = StandardScaler().fit_transform(termdoc2)
blurry_model3 = LogisticRegression(C = 0.001).fit(scaled_matrix2[0 : 1000, ], source_keys[0: 1000])
predictions3 = blurry_model3.predict(scaled_matrix2[0 : 1000, ])
print(sum(predictions3 == source_keys[0:1000]) / len(predictions3))
test_predictions3 = blurry_model3.predict(scaled_matrix2[1000 : , ])
print(sum(test_predictions3 == source_keys[1000 : ]) / len(test_predictions3))


# With the new model accuracy is higher than the old '500 features' model. This gives us insight into the relationship between features and accuracy in machine learning as it seems to be a positive relationship. After some quick research features in machine learning allow for more pieces of mesaureable data. As we learned this can help the dataset and make it more accurate but we also want a focused model so "more features always more accurate" may not be the best analysis. But with considering that there is a positive relationship to a certain degree.

# # Task 3

# Reload the dataset and recreate a vectorizer by incorporating stop words (you can achieve this by specifying a new parameter when creating the CountVectorizer: "stop_words = stop_words_used"). Then, recreate the sparse matrix, term-document matrix, scaled matrix, and the blurry model by duplicating the codes provided above. Calculate the accuracy rate for the testing data with the new setup. Does the accuracy rate increase or decrease when compared to the original model without a stop word list? What insights can be drawn about the impact of stop words on machine learning based on word frequency?<br>
# Include your codes in the following cell (code) and the discussion in the next cell (markdown).

# In[61]:


import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words_used = stopwords.words('english')

trump = pd.read_csv("Data/trump.csv")
vectorizer_stopword = CountVectorizer(max_features = 500, stop_words = stop_words_used) 
sparse_matrix_stopword = vectorizer_stopword.fit_transform(trump['text'])
termdoc_stopword = pd.DataFrame(sparse_matrix_stopword.toarray(), columns=vectorizer_stopword.get_feature_names_out())
termdoc_stopword = termdoc_stopword.loc[source_keys.index]
scaled_matrix_stopword = StandardScaler().fit_transform(termdoc_stopword)
blurry_model_stopword = LogisticRegression(C = 0.001).fit(scaled_matrix_stopword[0 : 1000, ], source_keys[0: 1000])
probabilities_train_blurry_stopword = [x[1] for x in blurry_model_stopword.predict_proba(scaled_matrix[:1000, ])]
predictions_stopword = blurry_model_stopword.predict(scaled_matrix_stopword[0 : 1000, ])
print(sum(predictions_stopword == source_keys[0:1000]) / len(predictions_stopword))
test_predictions_stopword = blurry_model_stopword.predict(scaled_matrix_stopword[1000 : , ])
print(sum(test_predictions_stopword == source_keys[1000 : ]) / len(test_predictions_stopword))


# The model with stopwords has a significantly worse accuracy then the previous model. This makes sense as we are analyzing Trumps often 'colloquial' language in his tweets. Adding stop words may remove certain words that would be associated with his Android or Iphone tweets. Hypothetically if it were to remove a hashtag or url trump shared alot on one of his posts this would mess with the data and accuracy of the model.

# # Finding the Features That Lead to Differentiation

# In[62]:


# Reload the original model. This is unnecessary if you always give the new variables new names
trump = pd.read_csv("Data/trump.csv")
vectorizer = CountVectorizer(max_features = 500)
sparse_matrix = vectorizer.fit_transform(trump['text'])
termdoc = pd.DataFrame(sparse_matrix.toarray(), columns=vectorizer.get_feature_names_out())
termdoc = termdoc.loc[source_keys.index]
scaled_matrix = StandardScaler().fit_transform(termdoc)
blurry_model = LogisticRegression(C = 0.001).fit(scaled_matrix[0 : 1000, ], source_keys[0: 1000])


# In[63]:


coefs = blurry_model.coef_
coefs = zip(coefs[0], vectorizer.get_feature_names_out()) # load the words and their weights into dictionary
coefs = sorted(coefs) # sort to find the top words that lead to differentiation


# In[64]:


# words that suggest posted via iPhone
coefs[0:10]


# In[65]:


# words that suggest posted via Android
coefs[-10:]


# # Task 4

# Examine the top 10 words that suggest tweets posted via iPhone and the top 10 words that suggest tweets posted via Android.  Write a short paragraph to explore the commonalities within each group of words, and draw assumptions about Trump's tweeting preferences. What types of tweets he tended to post via Android, and what types of tweets he tended to post via iPhone?

# I would say both android and iphone most used words from his posts both heavily have to do with his campaigning. Whats interesting though is that android seems to be hashtags or phrases from his campaign or the 'https' being from urls he shares through his android. While with Iphone we see alot of individual names like journalist Megyn kelly, himself 'Trump', and 'TheRealDonaldTrump' which probably is his twitter tag or the username of some of his socials. But with Iphone we see alot of commonly used english words like is, are, that as he may be elaborating into more detail on some of these political/media members. The similarities have to do with the topics being discussed mostly with Trumps election or trends to bash others on his platforms. Saying that an individual is 'this or that'. While the way he talks about his campaign on android has alot to do with hashtags, and posting urls.

# # Classifying Based on Retweet Numbers

# In[66]:


# Convert retweet number to two categories
def map_retweet(number):
    if number <= 5000: 
        return 0
    else:
        return 1
trump['retweetCount']= trump['retweetCount'].map(map_retweet)
trump = trump.sample(frac=1, random_state = 10) 
trump


# In[67]:


# Regenerate the word matrix based on the new dataset
source_keys_retweet = trump['retweetCount']
vectorizer = CountVectorizer(max_features = 500)
sparse_matrix = vectorizer.fit_transform(trump['text'])
termdoc = pd.DataFrame(sparse_matrix.toarray(), columns=vectorizer.get_feature_names_out())
termdoc_retweet = termdoc.loc[source_keys_retweet.index]
scaled_matrix_retweet= StandardScaler().fit_transform(termdoc_retweet)
scaled_matrix_retweet


# # Task 5

# Create a new model for predicting the number of retweets (source_keys_retweet) using the scaled_matrix_retweet created above. Calculate the new accuracy rate in predicting whether a tweet has more than 5000 retweets or not. Is this accuracy rate high? Note that random classification would yield an accuracy of 0.5. What insights can be derived from this result?<br>
# Include your codes in the following cell (code) and the discussion in the next cell (markdown).

# In[72]:


source_keys_retweet5 = trump['retweetCount']
vectorizer5 = CountVectorizer(max_features = 5000)
sparse_matrix5 = vectorizer5.fit_transform(trump['text'])
termdoc5 = pd.DataFrame(sparse_matrix5.toarray(), columns=vectorizer5.get_feature_names_out())
termdoc_retweet5 = termdoc5.loc[source_keys_retweet5.index]
scaled_matrix_retweet5= StandardScaler().fit_transform(termdoc_retweet5)

retweet_blurry_model = LogisticRegression(C = 0.001).fit(scaled_matrix_retweet5[0 : 1000, ], source_keys[0: 1000])
predictions_retweet = retweet_blurry_model.predict(scaled_matrix_retweet5[1000: , ])
print(sum(predictions_retweet == source_keys_retweet5[1000 : ]) / len(predictions_retweet))


# The new accuracy rate for a model with 5000 retweets or below has a very poor accurracy. This can be explained by what I was referring to above with the relatinoship between features and accuracy being that too high of features may lead to the mudding of the data, meaning it is less clear the results with so many samples. Having a .45 means that these results are less than random classification which may imply that are results were truly confused by the large amount of Trump tweets under 5000 retweets. Another thing to pull away is that there is a random component to what tweets do get reciprocated with high amounts of retweets especially with Trumps following. Maybe global events or news cycles could impact the average Americans news consumption and social media engagement with policiticans. So this unclear behavior with individuals and their social media behavior are important cofounders that could explain why its so hard for our model to predict what whether a tweet gets over 5000 retweets. 
