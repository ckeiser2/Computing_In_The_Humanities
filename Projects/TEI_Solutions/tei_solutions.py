#!/usr/bin/env python
# coding: utf-8

# # Convert html to xml

# In[1]:


# Open html document
document = open('Data/Clay.html', mode = 'r', encoding='utf-8')
document


# In[2]:


# Read html document
document.read()


# In[3]:


# Installing lxml, if it hasn't been installed
# lxml is used for parsing and manipulating XML and HTML documents
get_ipython().system('pip install lxml')


# In[4]:


# Parse html document
from lxml import html
document = open('Data/Clay.html', mode = 'r', encoding='utf-8')
htmldoc = html.fromstring(document.read())
htmldoc


# In[5]:


# Open a output.xml file and write the element/document to an encoded string representation of its XML tree
from lxml import etree
open("Data/Clay.xml", 'wb').write(etree.tostring(htmldoc)) # "wb" for binary mode for xml files


# In[6]:


# Load the xml file
xml_document = open('Data/Clay.xml', mode = 'r')
xml_document.read()


# In[7]:


# Use BeautifulSoup to parse the xml
from bs4 import BeautifulSoup
xml_document = open('Data/Clay.xml', mode = 'r')
soup = BeautifulSoup(xml_document, 'lxml')
soup


# In[8]:


# Prettify the parsed xml
print(soup.prettify())


# # Converting to TEI Following the TEI guidelines

# In[9]:


# Update root element to align with TEI guidelines (Chapter 2)
root = soup.find()
root.name = 'TEI'
del root['lang']
del root['xml:lang']
root['xmlns'] = 'http://www.tei-c.org/ns/1.0'
root


# In[10]:


# Update the div element to align with TEI guidelines (Chapter 3.1)
body = soup.find('body')
div = body.find('div')
del div['class']
div['xml:id'] = 'DUB10'
div['n'] = 10
div['type'] = 'chapter'
div


# In[11]:


# Update the header of the chapter to align with TEI guidelines (Chapter 3.2)
head = div.find('h2')
head.name = 'head'
a = head.find('a')
a.extract()
div


# In[12]:


# Update the poem paragraph to align with TEI guidelines (Chapter 3.3.1)
poem_paragraph = div.find('p', 'poem') # find the poem paragraph
del poem_paragraph['class']
poem_paragraph.name = 'lg'
poem_paragraph['rhyme'] = 'ABAB'
poem_text = poem_paragraph.find('i')
poem_text.unwrap() # Move the contents of <i> directly under <lg>
poem_paragraph


# In[13]:


# Split by lines and get the context
poem_text = poem_paragraph.stripped_strings
for line in poem_text:
    print(line)


# In[14]:


# Update each line of the poem paragraph and replace the original poem_paragraph with new_poem_paragraph
poem_text = poem_paragraph.stripped_strings
new_poem_paragraph = soup.new_tag('lg', rhyme=poem_paragraph['rhyme']) # create a new_poem_paragraph

count = 0 # this is used to calculate odds and even lines (for rhyme patterns)
for line in poem_text:
    new_tag = soup.new_tag('l') # create a new <l> tag
    new_tag.string = ' '.join(line.split()[:-1]) + ' ' # set the new tag to be the line without the rhyme word
    if count %2 == 0: # if 1,3,5,7 lines
        rhyme_tag = soup.new_tag('rhyme', label='A') # rhyme label is "A"
        if line.split()[-1][-1].isalpha(): # if last character of the last element after splitting is a character
            rhyme_tag.string = line.split()[-1] # the last element after splitting is the rhyme word
            new_tag.append(rhyme_tag)
        else: # if last character of the last element after splitting is a punctuation
            rhyme_tag.string = line.split()[-1][:-1] # the last element without the last character is the rhyme word
            new_tag.append(rhyme_tag)
            new_tag.append(line.split()[-1][-1]) # add the punctuation after the rhyme word ends
    else: # if 2,4,6,8 lines
        rhyme_tag = soup.new_tag('rhyme', label='B') # rhyme label is "B"
        if line.split()[-1][-1].isalpha(): # if last character of the last element after splitting is a character
            rhyme_tag.string = line.split()[-1] # the last element after splitting is the rhyme word
            new_tag.append(rhyme_tag)
        else: # if last character of the last element after splitting is a punctuation
            rhyme_tag.string = line.split()[-1][:-1] # the last element without the last character is the rhyme word
            new_tag.append(rhyme_tag)
            new_tag.append(line.split()[-1][-1]) # add the punctuation after the rhyme word ends
    new_poem_paragraph.append(new_tag)
    count += 1
new_poem_paragraph


# In[15]:


# Replace the poem paragraph with the newly created paragraph
poem_paragraph.replace_with(new_poem_paragraph)
div


# In[16]:


# Update quotations to align with TEI guidelines (Chapter 3.5.2)
paragraphs = div.find_all('p')
for paragraph in paragraphs:
    quotations = paragraph.find_all('i') # quote and quotations are in italic
    for quotation in quotations:
        if quotation.text[0] == '“': # if it is a direct quote
            quotation.name = 'q' # we use quoted: "contains material which is distinguished from the surrounding text using
                                 # quotation marks or a similar method, for any one of a variety of reasons including, but not limited to: 
                                 # direct speech or thought, technical terms or jargon, authorial distance, quotations from elsewhere, 
                                 # and passages that are mentioned but not used
            print(quotation) 
        else: # if it is not a direct quote
            quotation.name = 'q' # we use quotation: "(quotation) contains a phrase or passage attributed
                                 # by the narrator or author to some agency external to the text."
            print(quotation)


# In[17]:


print(soup.prettify())


# # Tasks

# Please use the new HTML document "A_Little_Cloud_except.html" and complete the following tasks:<br>
# (1) Convert the provided HTML document to an XML document, and parse the xml document using Beautiful Soup (you may copy the codes above and simply modify the file directory accordingly). (0.5 points);<br>
# (2) Update the root element, the div element, and the header to align with the TEI guidelines (you may copy the codes above and change the "div['xml:id']" and "div['n']"). (0.5 points);<br>
# (3) Update the poem paragraphs and each line of the poem paragraphs, and replace the poem paragraphs with the new paragraphs elements (you may copy the codes above. Since there are multiple poem paragraphs in the document, consider implementing a for loop to update each of them, and create new paragraphs elements to replace each poem paragraphs). (0.5 points);<br>
# (4) There is no \<i> element in this document. Is there a way to identify the quotations and quotes in the document? Write a short paragraph on how you would solve this issue (you have to propose a solution, or at least outline some ideas to tackle this issue. Actual code implementation is not required). (0.5 points);<br>
# (5) Reflect on the process of converting HTML to TEI. Share your insights and takeaways, focusing on various aspects. Consider discussing: (a) What are the challenges encountered during the conversion process? (b) Whether aligning with TEI guidelines is useful? Why or why not? Feel free to provide any other perspectives you have gained from this task. (0.5 points)

# In[18]:


import re
new_document = open('Data/A_Little_Cloud_excerpt.html', mode = 'r', encoding='utf-8')

htmldoc = html.fromstring(new_document.read())
open("Data/A_Little_Cloud_excerpt.xml", 'wb').write(etree.tostring(htmldoc))
xml_document = open('Data/A_Little_Cloud_excerpt.xml', mode = 'r')
soup = BeautifulSoup(xml_document, 'lxml')

root = soup.find()
root.name = 'TEI'
del root['lang']
del root['xml:lang']
root['xmlns'] = 'http://www.tei-c.org/ns/1.0'

body = soup.find('body')
div = body.find('div')
del div['class']
div['xml:id'] = 'DUB08'
div['n'] = 8
div['type'] = 'chapter'

head = div.find('h2')
head.name = 'head'
a = head.find('a')
a.extract()

poem_paragraphs = div.find_all('p', 'poem')
for poem_paragraph in poem_paragraphs:
    del poem_paragraph['class']
    poem_paragraph.name = 'lg'
    poem_paragraph['rhyme'] = 'ABAB'
    poem_text = poem_paragraph.find('i')
    poem_text.unwrap()
    
for poem_paragraph in poem_paragraphs:
    poem_text = poem_paragraph.stripped_strings
    new_poem_paragraph = soup.new_tag('lg', rhyme=poem_paragraph['rhyme'])
    
    count = 0
    for line in poem_text:
        new_tag = soup.new_tag('l')
        new_tag.string = ' '.join(line.split()[:-1]) + ' '
        if count %2 == 0:
            rhyme_tag = soup.new_tag('rhyme', label='A')
            matches = re.findall(r'(\w+|[^\w]+)', line.split()[-1])
            if len(matches)==1:
                rhyme_tag.string = matches[0]
                new_tag.append(rhyme_tag)
            else:
                rhyme_tag.string = matches[0]
                new_tag.append(rhyme_tag)
                new_tag.append(matches[1])
        else:
            rhyme_tag = soup.new_tag('rhyme', label='B')
            matches = re.findall(r'(\w+|[^\w]+)', line.split()[-1])
            if len(matches)==1:
                rhyme_tag.string = matches[0]
                new_tag.append(rhyme_tag)
            else:
                rhyme_tag.string = matches[0]
                new_tag.append(rhyme_tag)
                new_tag.append(matches[1])
        new_poem_paragraph.append(new_tag)
        count += 1
    poem_paragraph.replace_with(new_poem_paragraph)

print(soup.prettify())

