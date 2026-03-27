#!/usr/bin/env python
# coding: utf-8

# # Network Clustering

# In[1]:


# Load the libraries
import pandas as pd
import networkx
import matplotlib.pyplot as plt
import numpy as np


# In[2]:


# Load the data of the network of the first book of A Song of Ice and Fire
asoiaf_df = pd.read_csv('Data/asoiaf-book1-edges.csv')
asoiaf_df


# In[3]:


# Create a Network from a Pandas dataframe
G = networkx.from_pandas_edgelist(asoiaf_df, 'Source', 'Target', 'weight')
G['Jon-Snow']


# In[4]:


# Calculate the number of triangles each node is in
triangle_dict = networkx.triangles(G)
triangle_dict


# In[5]:


# The clustering of a node is the fraction of possible triangles through that node that exist
clustering_dict = networkx.clustering(G)
clustering_dict


# In[6]:


# Create a dataframe from the triangle dictionary
triangle_df = pd.DataFrame({'Name': triangle_dict.keys(), 'Triangles': triangle_dict.values()})
triangle_df = triangle_df.sort_values(by='Triangles', ascending=False)
triangle_df


# In[7]:


# Create a dataframe from the clustering dictionary
clustering_df = pd.DataFrame({'Name': clustering_dict.keys(), 'Clustering': clustering_dict.values()})
clustering_df


# In[8]:


# Merge the two dataframes
triangle_and_clustering_df = pd.merge(triangle_df, clustering_df, on='Name')
triangle_and_clustering_df


# # Task 1

# In[9]:


# Duplicate the process above to create a dataframe with triangles and clustering for each node in A Song of Ice and Fire Book 3.
# As is the case above, the results should be sorted by number of triangles, in descending order.

asoiaf_b3_df = pd.read_csv('Data/asoiaf-book3-edges.csv')
Gb3 = networkx.from_pandas_edgelist(asoiaf_b3_df, 'Source', 'Target', 'weight')
triangle_dict2 = networkx.triangles(Gb3)
clustering_dict2 = networkx.clustering(Gb3)

triangle_df2 = pd.DataFrame({'Name': triangle_dict2.keys(), 'Triangles': triangle_dict2.values()})
triangle_df2 = triangle_df2.sort_values(by='Triangles', ascending=False)

clustering_df2 = pd.DataFrame({'Name': clustering_dict2.keys(), 'Clustering': clustering_dict2.values()})

triangle_and_clustering_df2 = pd.merge(triangle_df2, clustering_df2, on='Name')

triangle_and_clustering_df2





# In[10]:


# Graph transitivity, the fraction of all possible triangles present in G.
# Possible triangles are identified by the number of "triads" (two edges with a shared node).
networkx.transitivity(G)


# # Task 2

# Calculate the graph transitivity for the network created based on the data from A Song of Ice and Fire Book 3. Is the graph transitivity higher or lower than the transitivity of the network constructed from A Song of Ice and Fire Book 1? Analyze the significance of this comparison, considering what it may reveal about the narrative development within <i>A Song of Ice and Fire</i>. If you're not familiar with the work, feel free to speculate on potential reasons. To provide context, please refer to the definitions of graph transitivity (included above) to clarify their implications. Include the calculation in the following cell (code) and the discussion in the next cell (markdown).

# In[11]:


asoiaf_b3_df = pd.read_csv('Data/asoiaf-book3-edges.csv')
Gb3 = networkx.from_pandas_edgelist(asoiaf_b3_df, 'Source', 'Target', 'weight')
networkx.transitivity(Gb3)


# The graph transitivity is lower in 'A Song of Ice and Fire Book 3' compared to Book 1. As someone who has only heard of game of thrones this may mean that as the books continue many supporting characters are introduced that don't form triangle connections or 'triads'. Or possibly the characters that were connected in triads and triangle connections in past books do not appear in future books for narrative reasons leaving the character roster with a smaller fraction of triangle connections. Since graph transitivity refers to the fraction of real triangle connections to possible triangle connections this means that the characters in Book 3 have less real triangular connections while having more 'possible' triangle connections compared to Book 1 characters. 

# # Basic Network Visualization with Bokeh

# In[12]:


# Changing bokeh version because the latest version will result in bugs in network visualization
get_ipython().system('pip install bokeh==2.4.3')


# In[13]:


# Check the bokeh version. It should be 2.4.3.
get_ipython().system('pip show bokeh')


# In[14]:


# Set up Bokeh to work in Jupyter notebook
from bokeh.io import output_notebook
output_notebook()


# In[15]:


# Import necessary Bokeh modules
from bokeh.io import show, save
from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine
from bokeh.plotting import figure
from bokeh.plotting import from_networkx


# In[16]:


# Basic visualization

#Choose a title
title = 'A Song of Ice and Fire (Book 1) Network'

#Establish which categories will appear when hovering over each node
HOVER_TOOLTIPS = [("Character", "@index")] # Index is the name of the character

#Create a plot — set dimensions, toolbar, and title
plot = figure(tooltips = HOVER_TOOLTIPS,
              tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
            x_range=Range1d(-10.1, 10.1), y_range=Range1d(-10.1, 10.1), title=title)

#Create a network graph object with spring layout
#https://networkx.github.io/documentation/networkx-1.9/reference/generated/networkx.drawing.layout.spring_layout.html
network_graph = from_networkx(G, networkx.spring_layout, scale=10, center=(0, 0))

#Set node size and color
network_graph.node_renderer.glyph = Circle(size=15, fill_color='skyblue')

#Set edge opacity and width
network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)

#Add network graph to the plot
plot.renderers.append(network_graph)

show(plot)


# # Network with Nodes Sized and Colored By Attribute (Degree)

# In[17]:


# Include Bokeh color palettes
from bokeh.palettes import Blues8, Reds8, Purples8, Oranges8, Viridis8, Spectral8
from bokeh.transform import linear_cmap


# In[18]:


# Calculate degree for each node and add as node attribute
degrees = dict(networkx.degree(G))
networkx.set_node_attributes(G, name='degree', values=degrees)


# In[19]:


#Choose attributes from G network to size and color by degree (NEW)
size_by_this_attribute = 'degree'
color_by_this_attribute = 'degree'

#Pick a color palette — Blues8, Reds8, Purples8, Oranges8, Viridis8, Spectral8 (NEW)
color_palette = Blues8

#Choose a title
title = 'A Song of Ice and Fire (Book 1) Network'

#Establish which categories will appear when hovering over each node
HOVER_TOOLTIPS = [
       ("Character", "@index"),
        ("Degree", "@degree")
]

#Create a plot — set dimensions, toolbar, and title
plot = figure(tooltips = HOVER_TOOLTIPS,
              tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
            x_range=Range1d(-10.1, 10.1), y_range=Range1d(-10.1, 10.1), title=title)

#Create a network graph object
network_graph = from_networkx(G, networkx.spring_layout, scale=10, center=(0, 0))

#Set node sizes and colors according to node degree (color as spectrum of color palette) (NEW)
minimum_value_color = min(network_graph.node_renderer.data_source.data[color_by_this_attribute])
maximum_value_color = max(network_graph.node_renderer.data_source.data[color_by_this_attribute])
network_graph.node_renderer.glyph = Circle(size=size_by_this_attribute, fill_color=linear_cmap(color_by_this_attribute, color_palette, minimum_value_color, maximum_value_color))

#Set edge opacity and width
network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)

plot.renderers.append(network_graph)

show(plot)


# # Network with Nodes Colored By Attribute (Community)¶

# In[20]:


# Import community detection module and get the communities
from networkx.algorithms import community
communities = community.greedy_modularity_communities(G)


# In[21]:


# Make a dictionary by looping through the communities and, for each member of the community, adding their community number
# Make another dictionary to store colors for modularity
modularity_class = {}
modularity_color = {}
count = 0
#Loop through each community in the network
for commun in communities:
    #For each member of the community, add their community number
    for name in commun:
        modularity_class[name] = count
        modularity_color[name] = Blues8[count] # Set a distinct color
    count += 1
modularity_color


# In[22]:


# Add class and color as node attributes
networkx.set_node_attributes(G, modularity_class, 'modularity_class')
networkx.set_node_attributes(G, modularity_color, 'modularity_color')


# In[23]:


#Choose attributes from G network to size and color 
size_by_this_attribute = 'degree'
color_by_this_attribute = 'modularity_color' # (NEW)

#Choose a title
title = 'A Song of Ice and Fire (Book 1) Network'

#Establish which categories will appear when hovering over each node
HOVER_TOOLTIPS = [
       ("Character", "@index"),
       ("Degree", "@degree"),
       ("Modularity Class", "@modularity_class")
]

#Create a plot — set dimensions, toolbar, and title
plot = figure(tooltips = HOVER_TOOLTIPS,
              tools="pan,wheel_zoom,save,reset, tap", active_scroll='wheel_zoom',
            x_range=Range1d(-10.1, 10.1), y_range=Range1d(-10.1, 10.1), title=title)

#Create a network graph object
network_graph = from_networkx(G, networkx.spring_layout, scale=10, center=(0, 0))

#Set node sizes according to node degree and colors according to modularity class (color as category from attribute) (NEW)
network_graph.node_renderer.glyph = Circle(size=size_by_this_attribute, fill_color=color_by_this_attribute)

#Set edge opacity and width
network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)

plot.renderers.append(network_graph)

show(plot)


# # Task 3

# In[24]:


# Create a visualization, where node size is based on eigenvector centrality, and color is based on community.
# Copy the code in the last cell, and update the "size_by_this_attribute" based on eigenvector centrality, and update colors.
# The eigenvector_centrality attribute should be mutiplied by 100 to make the nods visible. This can be realized by 
# writing a loop, and multiply the value of each node by 100, and add the result as a node attribute.
# The colors should be Spectral8 instead of Blues8. This can be realized by rerun the loop of setting colors for each community,
# and change the colors to Spectral8[count], and add the color as a node attribute again.

G = networkx.from_pandas_edgelist(asoiaf_df, 'Source', 'Target', 'weight')

eigenvector_centrality = networkx.eigenvector_centrality(G)
for node in eigenvector_centrality:
    eigenvector_centrality[node] *= 100

networkx.set_node_attributes(G, name='eigenvector', values=eigenvector_centrality)

communities = community.greedy_modularity_communities(G)

modularity_class = {}
modularity_color = {}
count = 0

for commun in communities:
    for name in commun:
        modularity_class[name] = count
        modularity_color[name] = Spectral8[count]
    count += 1

networkx.set_node_attributes(G, modularity_class, 'modularity_class')
networkx.set_node_attributes(G, modularity_color, 'modularity_color')

size_by_this_attribute = 'eigenvector'
color_by_this_attribute = 'modularity_color'

title = 'A Song of Ice and Fire (Book 1) Network'
HOVER_TOOLTIPS = [
    ("Character", "@index"),
    ("Eigenvector", "@eigenvector"),
    ("Modularity Class", "@modularity_class")
]

plot = figure(tooltips=HOVER_TOOLTIPS, tools="pan,wheel_zoom,save,reset, tap", active_scroll='wheel_zoom',
              x_range=Range1d(-10.1, 10.1), y_range=Range1d(-10.1, 10.1), title=title)

network_graph = from_networkx(G, networkx.spring_layout, scale=10, center=(0, 0))

network_graph.node_renderer.glyph = Circle(size=size_by_this_attribute, fill_color=color_by_this_attribute)

network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)

plot.renderers.append(network_graph)

show(plot)


# # Network with Responsive Highlighting

# In[25]:


# Include EdgesAndLinkedNodes, NodesAndLinkedEdges
from bokeh.models import EdgesAndLinkedNodes, NodesAndLinkedEdges


# In[26]:


#Choose colors for node and edge highlighting (NEW)
node_highlight_color = 'white'
edge_highlight_color = 'black'

#Choose attributes from G network to size and color
size_by_this_attribute = 'degree'
color_by_this_attribute = 'modularity_color'

#Choose a title
title = 'A Song of Ice and Fire (Book 1) Network'

#Establish which categories will appear when hovering over each node
HOVER_TOOLTIPS = [
       ("Character", "@index"),
       ("Degree", "@degree"),
       ("Modularity Class", "@modularity_class")
]

#Create a plot — set dimensions, toolbar, and title
plot = figure(tooltips = HOVER_TOOLTIPS,
              tools="pan,wheel_zoom,save,reset, tap", active_scroll='wheel_zoom',
            x_range=Range1d(-10.1, 10.1), y_range=Range1d(-10.1, 10.1), title=title)

#Create a network graph object
network_graph = from_networkx(G, networkx.spring_layout, scale=10, center=(0, 0))

#Set node sizes according to node degree and colors according to modularity class (color as category from attribute)
network_graph.node_renderer.glyph = Circle(size=size_by_this_attribute, fill_color=color_by_this_attribute)

#Set edge opacity and width
network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)

#Set node highlight colors (NEW)
network_graph.node_renderer.hover_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color, line_width=2)
network_graph.node_renderer.selection_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color, line_width=2)

#Set edge highlight colors (NEW)
network_graph.edge_renderer.selection_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)
network_graph.edge_renderer.hover_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)

#Highlight nodes and edges (NEW)
network_graph.selection_policy = NodesAndLinkedEdges()
network_graph.inspection_policy = NodesAndLinkedEdges()

plot.renderers.append(network_graph)

show(plot)


# # Network with Labels

# In[27]:


# Include LabelSet
from bokeh.models import LabelSet


# In[28]:


#Choose colors for node and edge highlighting
node_highlight_color = 'white'
edge_highlight_color = 'black'

#Choose attributes from G network to size and color
size_by_this_attribute = 'degree'
color_by_this_attribute = 'modularity_color'

#Choose a title
title = 'A Song of Ice and Fire (Book 1) Network'

#Establish which categories will appear when hovering over each node
HOVER_TOOLTIPS = [
       ("Character", "@index"),
       ("Degree", "@degree"),
       ("Modularity Class", "@modularity_class")
]

#Create a plot — set dimensions, toolbar, and title
plot = figure(tooltips = HOVER_TOOLTIPS,
              tools="pan,wheel_zoom,save,reset, tap", active_scroll='wheel_zoom',
            x_range=Range1d(-10.1, 10.1), y_range=Range1d(-10.1, 10.1), title=title)

#Create a network graph object
network_graph = from_networkx(G, networkx.spring_layout, scale=10, center=(0, 0))

#Set node sizes according to node degree and colors according to modularity class (color as category from attribute)
network_graph.node_renderer.glyph = Circle(size=size_by_this_attribute, fill_color=color_by_this_attribute)

#Set edge opacity and width
network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)

#Set node highlight colors
network_graph.node_renderer.hover_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color, line_width=2)
network_graph.node_renderer.selection_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color, line_width=2)

#Set edge highlight colors
network_graph.edge_renderer.selection_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)
network_graph.edge_renderer.hover_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)

#Highlight nodes and edges
network_graph.selection_policy = NodesAndLinkedEdges()
network_graph.inspection_policy = NodesAndLinkedEdges()

plot.renderers.append(network_graph)

#Add Labels (NEW)
x, y = zip(*network_graph.layout_provider.graph_layout.values())
node_labels = list(G.nodes())
source = ColumnDataSource({'x': x, 'y': y, 'name': [node_labels[i] for i in range(len(x))]})
labels = LabelSet(x='x', y='y', text='name', source=source, background_fill_color='white', text_font_size='10px', background_fill_alpha=.7)
plot.renderers.append(labels)

show(plot)


# # Task 4

# In[29]:


# Duplicate the process above to create a visualization based on data of A Song of Ice and Fire Book 3.
# The node size should be based on degree centrality, and color should be based on community, and responsive highlighting and
# labels should also be included.
# You have to create a new network based on asoiaf_b3_df, recalculate degree of the new network and add it as node attribute.
# Then you should regenerate communities of the new network, rerun the loop to generate community number and colors, and add
# both modularity class and color as node attributes.
# Finally, copy the code in the last cell, and change the title, and update network names when creating graph and adding labels.

asoiaf_b3_df = pd.read_csv('Data/asoiaf-book3-edges.csv')
Gb3 = networkx.from_pandas_edgelist(asoiaf_b3_df, 'Source', 'Target', 'weight')

degree = dict(networkx.degree(Gb3))
node_highlight_color = 'white'
edge_highlight_color = 'black'
networkx.set_node_attributes(Gb3, modularity_class, 'modularity_class')
networkx.set_node_attributes(Gb3, modularity_color, 'modularity_color')

size_by_this_attribute = 'degree_centrality'
color_by_this_attribute = 'modularity_class'

title = 'A Song of Ice and Fire (Book 3) Network'

HOVER_TOOLTIPS = [
       ("Character", "@index"),
       ("Degree", "@degree_centrality"),
       ("Modularity Class", "@modularity_class")
]
communities = list(networkx.community.greedy_modularity_communities(Gb3))

modularity_class = {}
modularity_color = {}
count = 0
for commun in communities:
    for name in commun:
        modularity_class[name]= count
        modularity_color[name]= Spectral8[count]
    count += 1

plot = figure(tooltips = HOVER_TOOLTIPS,
              tools="pan,wheel_zoom,save,reset, tap", active_scroll='wheel_zoom',
            x_range=Range1d(-10.1, 10.1), y_range=Range1d(-10.1, 10.1), title=title)

network_graph = from_networkx(Gb3, networkx.spring_layout, scale=10, center=(0, 0))

network_graph.node_renderer.glyph = Circle(size=size_by_this_attribute, fill_color=color_by_this_attribute)

network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)

network_graph.node_renderer.hover_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color, line_width=2)
network_graph.node_renderer.selection_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color, line_width=2)

network_graph.edge_renderer.selection_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)
network_graph.edge_renderer.hover_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)

network_graph.selection_policy = NodesAndLinkedEdges()
network_graph.inspection_policy = NodesAndLinkedEdges()

plot.renderers.append(network_graph)

x, y = zip(*network_graph.layout_provider.graph_layout.values())
node_labels = list(Gb3.nodes())
source = ColumnDataSource({'x': x, 'y': y, 'name': [node_labels[i] for i in range(len(x))]})
labels = LabelSet(x='x', y='y', text='name', source=source, background_fill_color='white', text_font_size='10px', background_fill_alpha=.7)
plot.renderers.append(labels)

show(plot)



# # Network Simulation

# In[37]:


# Generate the list of people in the network

p1 = list(asoiaf_df['Source']) # convert "Source" in the dataframe to a list
p2 = list(asoiaf_df['Target']) # convert "Target" in the dataframe to a list
people = p1 + p2 # concatenate the two lists
print(len(people)) # let's see how many people we have

people = list(set(people)) # remove the duplicates
node_num = len(people) # number of nodes (people) in the network: the length of the people list
print(node_num) # let's see how many people we have now
print(people) # what the list looks like


# In[38]:


# Generate the matrix of people's relationships

relation_matrix = np.zeros((len(people), len(people)))  # create a 187*187 empty matrix

for i in range(len(asoiaf_df)): # loop through each line (relationship) in the data
    p1_index = people.index(asoiaf_df.loc[i, 'Source']) # get the index of "Source" in the list of people
    p2_index = people.index(asoiaf_df.loc[i, 'Target']) # get the index of "Target" in the list of people
    relation_matrix[p1_index, p2_index] = 1 # assign value, which means "Source has relationship with Target"
    relation_matrix[p2_index, p1_index] = 1 # correspondingly, assign value, which means "Target has relationship with Source"
    # Here, for the pairs of people with multiple relationships, we assign value 1 for multiple times, and the value is still 1
print(relation_matrix.shape) # let's see how large the matrix is
print(relation_matrix) # what the matrix looks like

edge_num = int(sum(sum(relation_matrix))/2) # sum all relationships and divide 2 (as each relationship is calculated twice)
print("The number of total edges in the network is {}".format(edge_num)) # let's see the number of total edges in the network


# In[39]:


# Generate the degree distribution

deg_num_dict = {} # an empty dictionary to record the number of nodes of each degree, key: degree; value: number of nodes with that degree

for i in range(len(relation_matrix)): # loop through the relation matrix
    deg_i  = sum(relation_matrix[i,]) # for each node (person), its degree is the summation of the line (number of its relationships)
    key = int(deg_i)
    if key in deg_num_dict.keys(): # add one to the number of nodes of that degree, if there are already some nodes
        deg_num_dict[key] += 1
    else:
        deg_num_dict[key] = 1 # assign value one as the number of nodes of that degree, if there is no node

deg_num_dict # what the dictionary looks like


# In[40]:


# Sort the degree distribution

sort_deg_num_list = sorted(deg_num_dict.items(), key=lambda d:-d[0]) # sort the dictionary and reorder it by degree number 
sort_deg_num_list # what the dictionary looks like after sorting


# In[41]:


# Generate the nodes and the number of nodes of each degree

deg_num_list = [[i for i, j in sort_deg_num_list], 
               [j for i, j in sort_deg_num_list]]  # unzip the tuples to two lists
degs = deg_num_list[0] # the first list is degree
nums = deg_num_list[1] # the second list is number of nodes of each degree
print(degs) # what the list of degrees looks like
print(nums) # what the number of nodes of each degree looks like


# In[42]:


# Visualization

plt.style.use('ggplot') # use the "ggplot" style
fig1 = plt.scatter(nums, degs, color = 'blue') # plot a scatterplot of degrees in the x axis and the number of nodes in the y axis
plt.xlabel('Number of Nodes') # set the label of the x axis
plt.ylabel('Degree') # set the label of the y axis


# In[43]:


# Preferential attachment model

import math, random # library "random", for generating the random number

def preferential_attachment(k): # the preferential attachment model
    dNetwork = {} # dictionary of lists
    iNodes = node_num # total number of nodes in the network
    iLinks = 0 # set the initial number of links (edges/relationships) as 0

    for i in range(iNodes): # loop through all the nodes
        dNetwork[i] = [] # initialize node i with a empty list, which will record its link with other nodes
        for node in dNetwork.values(): 
            fThresh = 1.0 / (iLinks + i + 1) * k *(len(node) + 1) 
            # create a "threshold" value, which is proportional to its current degree + 1,
            # and inversly proportional to the total number of links in the network
            if(random.random() <= fThresh): # if the random value (a random number between 0 and 1) is smaller than the threshold
                node.append(i) # add a link between this node and the node "i"
                iLinks += 1 # add one to the total number of links in the network
    lDegrees = [len(node) for node in dNetwork.values()] # calculate the degree distribution
    return lDegrees, iLinks


# In[44]:


# Run the preferential attachment model
def run_pa(k): 
    # k is a parameter which influences the fThresh (so that influence the probability of generating links)
    # I set k=3.7 below, but you can try to change the number and see what will happen!

    lDegrees,iLinks = preferential_attachment(k) # get the degrees and number of links generated in the preferential attachment model
    # below we duplicated what we have done earlier
    deg_num_sim_dict = {}
    for i in lDegrees :
        if i in deg_num_sim_dict.keys():
            deg_num_sim_dict[i] += 1
        else:
            deg_num_sim_dict[i] = 1

    sort_deg_num_sim_list = sorted(deg_num_sim_dict.items(), key=lambda d:-d[0])

    deg_num_sim_list = [[i for i, j in sort_deg_num_sim_list], 
                       [j for i, j in sort_deg_num_sim_list]]
    degs_sim = deg_num_sim_list[0]
    nums_sim = deg_num_sim_list[1]
    
    return degs_sim, nums_sim, iLinks


# In[45]:


iLinks = 0 # initialize iLinks = 0

# We will simulate the network so that it will have exactly the same number of nodes (already guaranteed) and edges as the observed network
while iLinks != edge_num: # so, we will loop until the requirement of the edge number is satisfied
    degs_sim, nums_sim, iLinks = run_pa(3.7) # run the preferential attachment model
    print(iLinks) # print the number of total links in the network


# In[46]:


# Visualization of both the simulated network and the observed network

plt.scatter(nums_sim, degs_sim, color = 'red', label = 'Simulated')  # plot a scatterplot of the simulated network
plt.scatter(nums, degs, color='blue', label='Observed') # plot a scatterplot of the observed network
plt.xlabel('Number of Nodes') # set the label of the x axis
plt.ylabel('Degree') # set the label of the y axis
plt.legend() # display the legend


# # Task 5

# The network observed in A Song of Ice and Fire Book 1 exhibits a significant degree distribution overlap with the simulated network using the Preferential Attachment model. In a Preferential Attachment model, the probability of any given node acquiring a new edge is proportional to the number of edges it already possesses. What does this correspondence suggest about character relationships in <i>A Song of Ice and Fire</i>? Once again, If you're not familiar with the work, feel free to speculate on potential reasons. Please include the discussion in the next cell (markdown).

# 
