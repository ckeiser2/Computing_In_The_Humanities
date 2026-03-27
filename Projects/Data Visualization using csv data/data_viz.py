#!/usr/bin/env python
# coding: utf-8

# In[23]:


# Import Pandas library
import pandas as pd

# Import matplotlib
import matplotlib.pyplot as plt


# In[24]:


# Read the csv file and select a subset
data = pd.read_csv('Data/Trans_Atlantic_Slave_Trade.csv', delimiter=",", low_memory=False)
total_embarked_by_year = data.groupby('Year of arrival at port of disembarkation')['Total embarked'].sum()
percent_boys_by_year = data.groupby('Year of arrival at port of disembarkation')['Percent boys'].mean()
percent_girls_by_year = data.groupby('Year of arrival at port of disembarkation')['Percent girls'].mean()
percent_men_by_year = data.groupby('Year of arrival at port of disembarkation')['Percent men'].mean()
percent_women_by_year = data.groupby('Year of arrival at port of disembarkation')['Percent women'].mean()
year_data = pd.concat([total_embarked_by_year, percent_boys_by_year, percent_girls_by_year,
                       percent_men_by_year, percent_women_by_year], axis = 1)
year_data.reset_index(inplace=True)
year_data


# # Figure and Subplots

# In[25]:


# The figure acts as a container for the graph, each time you call the matplotlib.pyplot.figure function, 
# a new figure will be created.
fig = plt.figure()


# In[26]:


# Figure size can be specified
fig = plt.figure(figsize=(15,8))


# In[27]:


fig = plt.figure(figsize=(6,4))
ax = plt.subplot(1,1,1) # (rows, columns, and location)


# In[28]:


fig = plt.figure(figsize=(6,4))
ax1 = plt.subplot(2,1,1) # this would create a 2x1 grid of subplots and choose axes #1
ax2 = plt.subplot(2,1,2) # this would create a 2x1 grid of subplots and choose axes #2


# In[29]:


# We can also create subplots altogether
fig, ax = plt.subplots(2, 1, figsize=(6, 4))


# In[30]:


fig, axs = plt.subplots(2, 2, figsize=(10,6)) # This creates a figure of size 10x6 with a 2x1 grid of subplots.

axs[0][0].plot(year_data['Year of arrival at port of disembarkation'], year_data['Percent boys']) # The top-left axes
axs[0][1].plot(year_data['Year of arrival at port of disembarkation'], year_data['Percent girls']) # The top-right axes
axs[1][0].plot(year_data['Year of arrival at port of disembarkation'], year_data['Percent men']) # The bottom-left axes
axs[1][1].plot(year_data['Year of arrival at port of disembarkation'], year_data['Percent women']) # The bottom-right axes


# # Line plot

# In[31]:


# Plotting multiple lines in a same figure
fig, ax = plt.subplots(1, 1, figsize=(6, 4))
ax.plot(year_data['Year of arrival at port of disembarkation'], year_data['Percent boys'])
ax.plot(year_data['Year of arrival at port of disembarkation'], year_data['Percent girls'])


# In[32]:


# Styles of the lineplot
fig, ax = plt.subplots(1, 1, figsize=(6, 4))
ax.plot(year_data['Year of arrival at port of disembarkation'], year_data['Percent boys'], 
        color='yellow', lw=1, ls='-.', marker='o')
ax.plot(year_data['Year of arrival at port of disembarkation'], year_data['Percent girls'], 
        color='red', lw=2, ls='--',marker='s')


# In[33]:


# Adding legends
fig, ax = plt.subplots(1, 1, figsize=(6, 4))
ax.plot(year_data['Year of arrival at port of disembarkation'], year_data['Percent boys'], label='Percent boys')
ax.plot(year_data['Year of arrival at port of disembarkation'], year_data['Percent girls'], label = 'Percent girls')
ax.legend(loc='upper left', fontsize = 10)
# valid values include 'best', 'upper right', 'upper left', 'lower left', 'lower right', 'right',
# 'center left', 'center right', 'lower center', 'upper center', 'center'


# In[34]:


# Set title and labels
fig, ax = plt.subplots(1, 1, figsize=(6, 4))
ax.plot(year_data['Year of arrival at port of disembarkation'], year_data['Percent boys'], label='Percent Boys')
ax.set_title('Average proportion of boys each year')
ax.set_ylabel('Proportion')
ax.set_xlabel('Year', fontsize=15)


# In[35]:


# Set ticks
fig, ax = plt.subplots(1, 1, figsize=(6, 4))
ax.plot(year_data['Year of arrival at port of disembarkation'], year_data['Percent boys'], label='Percent Boys')
ax.set_title('Average proportion of boys each year')
ax.set_xticks(year_data['Year of arrival at port of disembarkation'][::30])
ax.set_xticklabels(year_data['Year of arrival at port of disembarkation'][::30], fontsize=6, color='red')
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
ax.set_yticklabels(['a', 'b', 'c', 'd', 'e', 'f'], fontsize=10, color='blue')


# # Task 1

# In[68]:


# Create two subplots in a 2x1 grid in a 6x8 figure.
# In the first subplot, create lineplots of percent boys and percent men, create legend in the upper center.
# Give it a resonable title, a reasonable xlabel, and a reasonable ylabel.
# In the second subplot, create linepplots of percent girls and percent women, in green and yellow lines respectively.
# Set xticks and xticklabels as year_data['Year of arrival at port of disembarkation'], with steps of 40.
# Set yticks and yticklabels as a list of values from 0 to 0.75, with steps of 0.15.




fig, ax = plt.subplots(2, 1,figsize=(6,8))

ax[0].plot(year_data['Year of arrival at port of disembarkation'], year_data['Percent boys'], label='Percent Boys') 
ax[0].plot(year_data['Year of arrival at port of disembarkation'], year_data['Percent men'], label='Percent Men') 
ax[0].legend(loc='upper left', fontsize = 10)
ax[0].set_xticks(year_data['Year of arrival at port of disembarkation'][::40])
ax[0].set_xticklabels(year_data['Year of arrival at port of disembarkation'][::40], fontsize=8, color='red')
ax[0].set_yticks([0, 0.15, 0.3, 0.45, 0.6, .75])
ax[0].set_yticklabels(['0', '.15', '.3', '.45', '.6', '.75'], fontsize=10, color='blue')
ax[0].set_title('Year of Arrival for Men & Boys')
ax[0].set_ylabel('Proportion')
ax[0].set_xlabel('Year', fontsize=8)

ax[1].plot(year_data['Year of arrival at port of disembarkation'], year_data['Percent women'], label='Percent Women', color = 'yellow') 
ax[1].plot(year_data['Year of arrival at port of disembarkation'], year_data['Percent girls'], label='Percent Girls', color = 'green') 
ax[1].legend(loc='upper left', fontsize = 10)
ax[1].set_xticks(year_data['Year of arrival at port of disembarkation'][::40])
ax[1].set_xticklabels(year_data['Year of arrival at port of disembarkation'][::40], fontsize=8, color='red')
ax[1].set_yticks([0, 0.15, 0.3, 0.45, 0.6, .75])
ax[1].set_yticklabels(['0', '.15', '.3', '.45', '.6', '.75'], fontsize=10, color='blue')
ax[1].set_title('Year of Arrival for Women & GIrls')
ax[1].set_ylabel('Proportion')
ax[1].set_xlabel('Year', fontsize=8)






# # Scatter plot

# In[37]:


fig, ax = plt.subplots(1, 1, figsize=(6, 4))
ax.scatter(year_data['Percent girls'], year_data['Percent boys'])


# In[60]:


# Size and transparency
fig, ax = plt.subplots(1, 1, figsize=(6, 4))
size = year_data['Total embarked']/1000
ax.scatter(year_data['Percent boys'], year_data['Percent girls'], s=size, alpha=.5)


# In[39]:


# Color map
map_dict = [
    (0, 20000, 'blue'),
    (20001, 50000, 'green'),
    (50001, 200000, 'red'),
]

def map_color(total_embarked):
    for lower, upper, color in map_dict:
        if lower <= total_embarked and total_embarked <= upper:
            return color

fig, ax = plt.subplots(1, 1, figsize=(6, 4))
colors = year_data['Total embarked'].map(map_color)
ax.scatter(year_data['Percent boys'], year_data['Percent girls'], c=colors)


# # Task 2

# In[66]:


# Create a scatterplot in a 6x4 figure, and plot percent men in x axis and percent women in y axis.
# The color of each dot should be based on the Year of arrival at port of disembarkation, pre 17th century as blue,
# 18th century as green, and 19th century as red.
# The size of each dot should be based on total embarked divided by 500, and the transparency parameter should be 0.3.
# Give the plot a resonable title, a resonable xlabel, and a resonable ylabel.


map_dict = [
    (0, 1700, 'blue'),
    (1701, 1800, 'green'),
    (1801, 1900, 'red'),
]

def map_color(total_embarked):
    for lower, upper, color in map_dict:
        if lower <= total_embarked and total_embarked <= upper:
            return color


fig, ax = plt.subplots(1, 1, figsize=(6, 4))
colors = year_data['Year of arrival at port of disembarkation'].map(map_color)
ax.scatter(year_data['Percent men'], year_data['Percent women'], c=colors)
size = year_data['Total embarked']/500
ax.scatter(year_data['Percent men'], year_data['Percent women'], s=size, alpha=0.3)
ax.set_title('Year of Arrival for Men & Women')
ax.set_ylabel('Proportion')
ax.set_xlabel('Year', fontsize=15)




# # Bar plot

# In[41]:


# Select rows in the early 1840s
data_early_1840s = year_data[year_data['Year of arrival at port of disembarkation'].isin(range(1840, 1845))]
data_early_1840s


# In[42]:


# General barplot
fig, ax = plt.subplots(1, 1, figsize=(6, 4))
ax.bar(data_early_1840s['Year of arrival at port of disembarkation'], data_early_1840s['Total embarked'])


# In[43]:


# Set bar color and width
fig, ax = plt.subplots(1, 1, figsize=(6, 4))
ax.bar(data_early_1840s['Year of arrival at port of disembarkation'], data_early_1840s['Total embarked'],
      color = 'green', width = 0.5)


# In[44]:


# Stack barplot
fig, ax = plt.subplots(1, 1, figsize=(6, 4))
ax.bar(data_early_1840s['Year of arrival at port of disembarkation'], data_early_1840s['Percent boys'],
      color = 'blue', width = 0.5)
ax.bar(data_early_1840s['Year of arrival at port of disembarkation'], data_early_1840s['Percent girls'],
      color = 'red', width = 0.5)
ax.legend(['Percent boys','Percent girls'])


# In[45]:


# Side-by-side barplot
fig, ax = plt.subplots(1, 1, figsize=(6, 4))
ax.bar(data_early_1840s['Year of arrival at port of disembarkation'] - 0.2, data_early_1840s['Percent boys'],
      color = 'blue', width = 0.4)
ax.bar(data_early_1840s['Year of arrival at port of disembarkation'] + 0.2, data_early_1840s['Percent men'],
      color = 'red', width = 0.4)
ax.legend(['Percent boys','Percent men'], loc = 'upper left')


# In[46]:


# Grid and annotation
fig, ax = plt.subplots(1, 1, figsize=(6, 4))
ax.bar(data_early_1840s['Year of arrival at port of disembarkation'], data_early_1840s['Total embarked'], width = 0.5)
ax.grid(True)
for x, y in zip(data_early_1840s['Year of arrival at port of disembarkation'], data_early_1840s['Total embarked']):
    plt.text(x, y, y, ha='center', va='bottom') # ha: horizontal alignment, va: vertical alignment


# # Task 3

# In[73]:


# Create a side-by-side barplot in a 6x4 figure based on the data of years 1830, 1832, 1834, 1836, and 1838.
# Plot percent girls in green bars, percent women in yellow bars, adjust the width (0.4 in previous example)
# and the x-coordinates (+-0.2 in previous example) so that each bar is still twice as wide as the space between different years
# Create legend in top right corner, add grids, and give annotations for each bar.
# The annotations should be rounded to two decimal places (e.g., 0.14), and vertical alignment should be center.
# You need to adjust the x-coordinates in the annotation to ensure the annotations appear on the top of corresponding bars.


data_early_1830s = year_data[year_data['Year of arrival at port of disembarkation'].isin(range(1830, 1838))]

fig, ax = plt.subplots(1, 1, figsize=(6, 4))

ax.bar(data_early_1830s['Year of arrival at port of disembarkation'] - 0.2, data_early_1830s['Percent women'],
      color = 'yellow', width = 0.4)
ax.bar(data_early_1830s['Year of arrival at port of disembarkation'] + 0.2, data_early_1830s['Percent girls'],
      color = 'green', width = 0.4)
ax.legend(['Percent women','Percent girls'], loc = 'upper right')

for x, y in zip(data_early_1830s['Year of arrival at port of disembarkation'], data_early_1830s['Percent girls']):
    plt.text(x+.2, y, round(y, 2), ha='center', va='center') 
    
for x, y in zip(data_early_1830s['Year of arrival at port of disembarkation'], data_early_1830s['Percent women']):
        plt.text(x-.2, y, round(y, 2), ha='center', va='center') 

ax.grid(True)








# # Pie chart

# In[48]:


# General plot
fig, ax = plt.subplots(1, 1, figsize=(6, 4))
ax.pie([data_early_1840s['Percent boys'][310], data_early_1840s['Percent girls'][310], data_early_1840s['Percent men'][310],
        data_early_1840s['Percent women'][310]], labels = ['Percent boys', 'Percent girls', 'Percent men', 'Percent women'],
        colors = ['yellow','green','red','blue'])


# In[49]:


# Shadow and explode
fig, ax = plt.subplots(1, 1, figsize=(6, 4))
explode = [0.3, 0.2, 0.1, 0]
ax.pie([data_early_1840s['Percent boys'][310], data_early_1840s['Percent girls'][310], data_early_1840s['Percent men'][310],
        data_early_1840s['Percent women'][310]], labels = ['Percent boys', 'Percent girls', 'Percent men', 'Percent women'],
        colors = ['yellow','green','red','blue'], shadow = True, explode = explode)


# In[50]:


# Percentage
fig, ax = plt.subplots(1, 1, figsize=(6, 4))
ax.pie([data_early_1840s['Percent boys'][310], data_early_1840s['Percent girls'][310], data_early_1840s['Percent men'][310],
        data_early_1840s['Percent women'][310]], labels = ['Percent boys', 'Percent girls', 'Percent men', 'Percent women'],
        colors = ['yellow','green','red','blue'], autopct='%0.1f%%', pctdistance=0.5)


# In[51]:


# Wedgeprops and textprops
fig, ax = plt.subplots(1, 1, figsize=(6, 4))
ax.pie([data_early_1840s['Percent boys'][310], data_early_1840s['Percent girls'][310], data_early_1840s['Percent men'][310],
        data_early_1840s['Percent women'][310]], labels = ['Percent boys', 'Percent girls', 'Percent men', 'Percent women'],
        colors = ['yellow','green','red','blue'], wedgeprops={"linewidth": 3, "width": 0.4, "edgecolor": "white"},
        textprops = {"color": "purple", "weight": "bold"})


# # Task 4

# In[76]:


# Create two subplots in a 1x2 grid in a 12x4 figure.
# In the first subplot, create a piechart of percent boys, percent girls, percent men, and percent women for year 1830.
# Include shadow, explodes, auto percentages, and set wedgeprops and textprops, and give it a resonable title.
# Repeat the entire process in the second plot for data of year 1831.


fig, ax = plt.subplots(1, 2, figsize=(12, 4))
ax[0].pie([data_early_1830s['Percent boys'][300], data_early_1830s['Percent girls'][300], data_early_1830s['Percent men'][300],
        data_early_1830s['Percent women'][300]], labels = ['Percent boys', 'Percent girls', 'Percent men', 'Percent women'],
        colors = ['yellow','green','red','blue'], wedgeprops={"linewidth": 3, "width": 0.4, "edgecolor": "white"},
        textprops = {"color": "purple", "weight": "bold"}, shadow = True, explode = explode, autopct='%0.1f%%')
ax[0].set_title('Percent of Demographics of People in 1830')



ax[1].pie([data_early_1830s['Percent boys'][301], data_early_1830s['Percent girls'][301], data_early_1830s['Percent men'][301],
        data_early_1830s['Percent women'][301]], labels = ['Percent boys', 'Percent girls', 'Percent men', 'Percent women'],
        colors = ['yellow','green','red','blue'], wedgeprops={"linewidth": 3, "width": 0.4, "edgecolor": "white"},
        textprops = {"color": "purple", "weight": "bold"}, shadow = True, explode = explode, autopct='%0.1f%%')
ax[1].set_title('Percent of Demographics of People in 1831')




# In[74]:


data_early_1830s


# # Interactive visualization

# In[53]:


# Install required library bokeh
get_ipython().system('pip install bokeh')


# In[54]:


# Import necessary Bokeh modules and set up Bokeh to work in Jupyter notebook
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.io import output_notebook, show
from bokeh.transform import linear_cmap, jitter
output_notebook()


# In[55]:


data_new = data[['Voyage ID', 'Year of arrival at port of disembarkation', 'Total embarked']]
data_new = data_new.dropna()
data_new = data_new.sample(1000)
data_new


# In[56]:


# Set up the source data by converting dataframe 
source = ColumnDataSource(data_new)
source


# In[98]:


# Set the hover tool tip to the film title, release year, and proportion of dialogue
TOOLTIPS = [("Voyage ID", "@{Voyage ID}"),
            ("Year", "@{Year of arrival at port of disembarkation}"),
            ("Total embarked", "@{Total embarked}")]

#Set up Bokeh plot
bokeh_plot = figure(title="Total embarked of each voyage", x_axis_label = 'Year of arrival at port of disembarkation',
                    y_axis_label = 'Total embarked', x_range = [1500, 1900], y_range = [0, 2050],
                    tooltips=TOOLTIPS, width=800, height=550, active_scroll='wheel_zoom')

# Supply inidivudal points values
bokeh_plot.circle(y='Total embarked', x=jitter('Year of arrival at port of disembarkation', width=.2),
                  size = 10,
                  line_color ='black',
                  line_alpha =.4,
                  source = source,
                  alpha =.5)

bokeh_plot.title.text_font_size='20pt'

show(bokeh_plot)


# # Task 5

# In[108]:


# Create an interactive visualization with Bokeh to visualize percent boys in 19th century.
# The source should be a subset of the original dataframe, with ID, years, and percent boys, after dropping nan values.
# Adjust the codes accordingly (in addition to source and column names, also think of x and y ranges, and title/labels).
data_boys = data[['Voyage ID', 'Year of arrival at port of disembarkation', 'Percent boys']]
data_boys = data_boys.dropna()
data_boys = data_boys[data_boys['Year of arrival at port of disembarkation']>=1800]


source = ColumnDataSource(data_boys)

TOOLTIPS2 = [("Voyage ID", "@{Voyage ID}"),
            ("Year", "@{Year of arrival at port of disembarkation}"),
            ("Percent boys", "@{Percent boys}")]

bokeh_plot1= figure(title="Boys arrival 19th Century", x_axis_label = 'Year of arrival at port of disembarkation',
                    y_axis_label = 'Percent boys', x_range = [1800,1900], y_range = [0, 1],
                    tooltips=TOOLTIPS2, width=800, height=550, active_scroll='wheel_zoom')

bokeh_plot1.circle(y=jitter('Percent boys', width=.2), x=jitter('Year of arrival at port of disembarkation', width=.2),
                  size = 10,
                  line_color ='black',
                  line_alpha =.4,
                  source = source,
                  alpha =.5)

bokeh_plot1.title.text_font_size='20pt'

show(bokeh_plot1)










# In[87]:


data_boys


# In[ ]:




