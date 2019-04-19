import urllib.request
import re
import matplotlib.pyplot as plt

# a dictionary to save the number of the pagpers been publish each year of an author
datelist = {}
# let user to input author name
author_name = input("Input Author: ")

#to use the author search to get html, replace ' ' in author name with '+'
author = author_name.replace(' ', '+')
#set the url we want
url = "https://arxiv.org/search/?query=" + author + "&searchtype=author"
#get the html file content of arxiv
content = urllib.request.urlopen(url)
html_str = content.read().decode('utf-8')

#a re pattern to get the papers number of this author search (not use)
#page_pattern = 'of [0-9]* results for author:'
#paper_num = re.findall(page_pattern, html_str)

#a re pattern to get the originally announced date of each paper
date_pattern = 'originally announced</span>[\s\S]*?</p>'
#get string of announced date of each paper
date = re.findall(date_pattern, html_str)

for t in date:
    # cut the string of announced date(month & year)
    date = t.split('</span>')[1].split(".")[0].strip()
    #split date by ' ' to get the year of paper announced date
    date = date.split(' ')[1]
    #add this result to the date dictionary
    if date in datelist:
        datelist[date] += 1
    else:
        datelist[date] = 1

#sort the result by dictionary's key
datelist_key = list(datelist.keys())
datelist_key.reverse()
datelist_value = list(datelist.values())
datelist_value.reverse()

#construct the bar graph of datelist
plt.bar(range(len(datelist)), datelist_value, align='center')
plt.xticks(range(len(datelist)), datelist_key)
plt.yticks(range(max(datelist_value)+1))
#show the graph
plt.show()
