#!/usr/bin/env python
# coding: utf-8

# # Creating and Drawing a Network

# In[1]:


# Install the library networkx for network analysis
get_ipython().system('pip install networkx')


# In[2]:


# Load the libraries
import networkx
import pandas as pd
pd.set_option('display.max_rows', 200)
import matplotlib.pyplot as plt


# In[3]:


# Load the data of the network of A Song of Ice and Fire
# The dataset was created by Andrew Beveridge (https://github.com/mathbeveridge/asoiaf/tree/master)
asoiaf_df = pd.read_csv('Data/asoiaf-book1-edges.csv')
asoiaf_df


# These networks were created by connecting two characters whenever their names (or nicknames) appeared within 15 words of one another in one of the books in <i>A Song of Ice and Fire</i>. The edge weight corresponds to the number of interactions. For example, the following sentence counts as an “edge” or connection between Jon Snow and Sam Tarly:<br><i>“It was the bastard <b>Jon Snow</b> who had taken that from him, him and his fat friend <b>Sam Tarly</b>.”</i>

# In[4]:


# Create a Network from a Pandas dataframe
G = networkx.from_pandas_edgelist(asoiaf_df, 'Source', 'Target', 'weight')
G['Jon-Snow']


# In[5]:


# Draw a simple network
networkx.draw_networkx(G, with_labels=False)


# In[6]:


# Add labels and customize width, font, and figure size
plt.figure(figsize=(8,8))
networkx.draw_networkx(G, with_labels=True, node_color='skyblue', width=.3, font_size=8)


# # Calculate Degree and Weighted Degree

# Degree centrality is defined as the number of links incident upon a node (i.e., the number of ties that a node has).

# In[7]:


networkx.degree(G)


# In[8]:


# Make the degree values a dictionary, then add it as a network attribute
degrees = dict(networkx.degree(G))
networkx.set_node_attributes(G, name='degree', values=degrees)


# In[9]:


# Make a Pandas dataframe from the degree data, then sort from highest to lowest
degree_df = pd.DataFrame(G.nodes(data='degree'), columns=['node', 'degree'])
degree_df = degree_df.sort_values(by='degree', ascending=False)
degree_df


# In[10]:


# Plot the 10 nodes with the highest degree values
degree_df[:10].plot(kind='barh', x='node', title='Top 10 Characters with the Highest Degrees').invert_yaxis()


# Weighted degree centrality is defined as the summation of the weights of all links incident upon a node (i.e., the summation of weights of all ties that a node has).

# In[11]:


networkx.degree(G, weight='weight')


# # Task 1

# In[12]:


# First, make the weighted degree values a dictionary, and add it as a network attribute
# Then make a Pandas dataframe from the weighted degree data, and sort from highest to lowest
# Finally, plot the 15 (instead of 10) nodes with the highest weighted degree values, invert the y axis, 
# set color as red, and add reasonable title, xlabel, and ylabel

degrees = dict(networkx.degree(G, weight='weight'))
networkx.set_node_attributes(G, name='weighted_degree', values=degrees)
degree_df = pd.DataFrame(G.nodes(data='weighted_degree'), columns=['node', 'weighted_degree'])
degree_df = degree_df.sort_values(by='weighted_degree', ascending=False)
degree_df[:15].plot(kind='barh', x='node', title='Top 15 Characters with the Highest Weighted Degrees', color = 'red', xlabel = 'characters', ylabel='weighted_degrees').invert_yaxis()



# # Calculate Different Centrality Scores

# Eigenvector centrality is a measure of the influence of a node in a network. High eigenvector score means that a node is connected to many nodes who themselves have high scores.

# In[13]:


networkx.eigenvector_centrality(G)


# In[14]:


# Add eigenvector_centrality (which is already a dictionary) as a network attribute
eigenvector_centrality = networkx.eigenvector_centrality(G)
networkx.set_node_attributes(G, name='eigenvector', values=eigenvector_centrality)


# In[15]:


# Make a Pandas dataframe from the eigenvector centrality, then sort from highest to lowest
eigenvector_df = pd.DataFrame(G.nodes(data='eigenvector'), columns=['node', 'eigenvector'])
eigenvector_df = eigenvector_df.sort_values(by='eigenvector', ascending=False)
eigenvector_df


# Betweenness centrality is a measure of centrality in a graph based on shortest paths. The betweenness centrality for each node is the number of these shortest paths that pass through the node.

# In[16]:


networkx.betweenness_centrality(G)


# In[17]:


betweenness_centrality = networkx.betweenness_centrality(G)
networkx.set_node_attributes(G, name='betweenness', values=betweenness_centrality)
betweenness_df = pd.DataFrame(G.nodes(data='betweenness'), columns=['node', 'betweenness'])
betweenness_df = betweenness_df.sort_values(by='betweenness', ascending=False)
betweenness_df


# Closeness centrality is calculated as the reciprocal of the sum of the length of the shortest paths between the node and all other nodes in the graph. Thus, the more central a node is, the closer it is to all other nodes.

# In[18]:


networkx.closeness_centrality(G)


# In[29]:


closeness_centrality = networkx.closeness_centrality(G)
networkx.set_node_attributes(G, name='closeness', values=closeness_centrality)
closeness_df = pd.DataFrame(G.nodes(data='closeness'), columns=['node', 'closeness'])
closeness_df = closeness_df.sort_values(by='closeness', ascending=False)
closeness_df


# In[20]:


# Adding rank to the degree df
degree_df['degree_rank'] = range(1, len(degree_df) + 1)
degree_df


# # Task 2

# In[50]:


# Referring to what we have done to the degree_df, add "eigenvector_rank" column to eigenvector_df, "betweenness_rank" column 
# to betweenness_df, and "closeness_rank" to closeness_df
# Then create an "all_rank_df" by merging degree_df, eigenvector_df, betweenness_df, and closeness_df
# (this can be done by merging two dataframes at a time)
# Finally, slice the columns so that the final ouput should only have 5 columns: node and four different ranks
pd.set_option('display.width', 1000) #Reference since I was having issues having all the columns being displayed at once https://pandas.pydata.org/docs/user_guide/options.html

eigenvector_df['eigenvector_rank'] = range(1, len(eigenvector_df) + 1)
betweenness_df['betweenness_rank'] = range(1, len(betweenness_df) + 1)
closeness_df['closeness_rank'] = range(1, len(closeness_df) + 1)

merge_df = pd.merge(degree_df, eigenvector_df)

merge_df = pd.merge(merge_df, betweenness_df)

merge_df = pd.merge(merge_df, closeness_df)

all_rank_df = merge_df[['node', 'degree_rank', 'betweenness_rank', 'eigenvector_rank', 'closeness_rank']]

print(all_rank_df)



# # Task 3

# Discuss the results of task 2 in the next cell. You have to discuss at least two characters based on their ranks in different centralities. For instance, character A ranks high in all types of centralities; this may be attributed to reason XXX. On the other hand, character B ranks high in centrality C but low in centrality D, which could be a result of reason YYY. To provide context, please refer to the definitions of each centrality (included above) to clarify their implications. If you are familiar with A Song of Ice and Fire (or the television series Game of Thrones), you can attempt to interpret these results by exploring how a character's ranks in these centralities relate to the plot. If you haven't, you can just speculate on potential reasons, such as this character might have close association with key figures, leading to a high eigenvector centrality rank, etc.

# Answer:As someone who is vaguely knowledgable of Game of Thrones, I am familiar with Eddard Stark in the early seasons of the show/book. This can be attributed to him having the highest ranking in all relative stats. He is a central figure in his family and influential over the area he lives in, idk if its from being a king, or a warrior or just a nice guy but from what I remember he was well know and well liked. This shows in each one of the rankings as eigenvector shows he knew many other important figures, and betweeness shows that he was central in many interactions. Also his closeness ranking shows the closeness between different nodes in a system so when there is a connection it would make sense that it would be through Eddard Stark. A figure not as influential as Eddard Stark is the individual that ranks 101 Roose Bolton. What makes him not as central is that his key importance from my brief google search is only being the head of his house. Though this gives him more influence in the story over other minor characters it keeps him locked from say having a more central role in the story as many of his interactions and connections are locked into a niche of the story within his own family. He does know and interact with individuals outside of his family but only in limited forms unlike Eddard Stark. This makes sense as Bolton's highest rank is in Eigenvector as the head of his family he would also mingle and meet with other heads of other families. But his other rankings are lacking as Bolton isn't a figure you need to go through to know others which hurts his betweeness and closeness rankings.

# # Communities

# In[51]:


# Import the "community" module for network community detection
from networkx.algorithms import community


# In[52]:


# Calculate communities with greedy_modularity_communities function, 
# which uses Clauset-Newman-Moore greedy modularity maximization to find the community partition with the largest modularity
communities = community.greedy_modularity_communities(G)
communities


# In[53]:


# Make a dictionary by looping through the communities and, for each member of the community, adding their community number
modularity_class = {} # Create empty dictionary
count = 0
#Loop through each community in the network
for community in communities:
    #For each member of the community, add their community number
    for name in community:
        modularity_class[name] = count
    count += 1
modularity_class


# In[54]:


# Add modularity class to the network as an attribute
networkx.set_node_attributes(G, modularity_class, 'modularity_class_b1')


# In[55]:


# Make a Pandas dataframe from modularity class data
communities_df = pd.DataFrame(G.nodes(data='modularity_class_b1'), columns=['node', 'modularity_class_b1'])
communities_df = communities_df.sort_values(by='modularity_class_b1')
communities_df


# In[56]:


# Visualization: plot all characters with their modularity class indicated by a star in a seaborn stripplot
get_ipython().system('pip install seaborn')
import seaborn as sns
plt.figure(figsize=(4,35))

ax =sns.stripplot(x='modularity_class_b1', y='node', data=communities_df,
              hue='modularity_class_b1', marker='*',size=15)

ax.legend(loc='upper right',bbox_to_anchor=(1.5, 1), title='Modularity Class')
ax.set_title("Characters By Modularity Class")
plt.show()


# # Task 4

# In[147]:


# Use the network data for the second book of A Song of Ice and Fire, and duplicate the process for creating the modularity
# of the first book and merge the results with the results of the first book
# First, you should create a network and use community.greedy_modularity_communities to generate the communities
# Then make a dictionary by looping through the communities and, for each member of the community, adding their community number
# Next, add modularity class to the network as an attribute and make a Pandas dataframe from modularity class data
# (remember to change column names to distinguish the modularity class of Book 2 and Book 1)
# Finally, merge the newly created dataframe for Book 2 and the communities_df for Book 1, and display the merged dataframe

from networkx.algorithms import community

asoiaf_b2_df = pd.read_csv('Data/asoiaf-book2-edges.csv')
G_b2 = nx.from_pandas_edgelist(asoiaf_b2_df, 'Source', 'Target', 'weight')

communities_b2 = community.greedy_modularity_communities(G_b2)

modularity_class_2 = {}
count = 0
for community in communities_b2:
    for name in community:
        modularity_class_2[name] = count
    count += 1

Book2 = pd.DataFrame(list(modularity_class_2.items()), columns=['Character', 'Modularity Class Book 2'])

Book1 = pd.read_csv('Data/asoiaf-book1-edges.csv')
Book1.rename(columns={'book': 'Modularity Class Book 1'}, inplace=True)
Book1.rename(columns={'Source': 'Character'}, inplace=True)

merged_df = pd.merge(Book1, Book2, on='Character', how='outer')


print(merged_df.head(150))


# # Task 5

# Discuss the results of task 4 in the next cell. Compare the modularity classes between Book 1 and Book 2. It's important to note that the actual number of modularity classes itself may not hold significant meaning. For instance, if characters A and B are the only members of modularity class 0 in Book 1 and they are also the only members of modularity class 1 in Book 2, there is no substantive difference despite the differing class numbers.<br>You should discuss at least two pairs of characters. The first pair should belong to the same modularity class in both books, while the second pair should belong to the same modularity class in one book but belong to different modularity classes in the other (e.g., character A and B both belong to modularity class 0 in Book 1 and modularity class 1 in Book 2; whereas character C and D both belong to modularity class 2 in Book 1, but in Book 2, C is in modularity class 2 while D is in modularity class 3). If you are familiar with A Song of Ice and Fire (or the television series Game of Thrones), you can attempt to interpret these results by exploring how the consistency or inconsistency in characters' modularity classes relates to the plot. If you haven't, you can just speculate on potential reasons for the consistency or inconsistency.

# In task 4 an example of a pair of individuals that had a change in modularity between books would be Aegon-I-Targaryen and Daenerys_Targaryan going from a 1 -> 6 between books. This may be explained by individuals from their families or individuals they both know being mentioned and introduced in the second book strengthening their modularity. An example of modularity staying the same between books would be Bran Stark and Stiv. This could be from the characters each one of these individuals know related to the plot hasn't changed much. To the point it hasn't effected their modularity class.
