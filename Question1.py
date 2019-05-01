import urllib.request
import re
import matplotlib.pyplot as plt
import math

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

#a re pattern to get the papers number of this author search
page_pattern = 'of [0-9]* results for author:'
paper_num = re.findall(page_pattern, html_str)
page_num = paper_num[0].split('of ')[1].split(" results")[0].strip()
page_num = int(page_num)
#the result page number we want
page_num = math.ceil(page_num/50)

#search by pages
for i in range(0, page_num):
    # set the url we want (each page)
    url = "https://arxiv.org/search/?query=" + author + "&searchtype=author&start=" + str(i*50)
    # get the html file content of arxiv
    page_content = urllib.request.urlopen(url)
    page_html_str = page_content.read().decode('utf-8')

    #a re pattern to get the originally announced date of each paper
    date_pattern = 'originally announced</span>[\s\S]*?</p>'
    #get string of announced date of each paper
    date = re.findall(date_pattern, page_html_str)

    # a re pattern to get the author of each paper
    author_line_pattern = 'Authors:</span>[\s\S]*?</p>'
    # get string of co-author of each paper
    co_author_line = re.findall(author_line_pattern, page_html_str)

    author_line_num = 0
    for t in date:

        # check if this paper is the author's, if not -> skip for next paper
        author_line = co_author_line[author_line_num]
        author_line_num = author_line_num + 1
        if author_name not in author_line:
            continue

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
datelist_key = []
datelist_value = []
for i in sorted(datelist):
    datelist_key.append(i)
    datelist_value.append(datelist[i])

#construct the bar graph of datelist
plt.bar(range(len(datelist)), datelist_value, align='center')
plt.xticks(range(len(datelist)), datelist_key)
plt.yticks(range(max(datelist_value)+1))

k = 0
for i in datelist_value:
    k += i
print(k)

#show the graph
plt.show()
