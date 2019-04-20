import urllib.request
import re
import math

# a dictionary to save the number of the co-author appear in all papers
co_author_list = {}
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

    #a re pattern to get the co-author of each paper
    co_author_line_pattern = 'Authors:</span>[\s\S]*?</p>'
    #get string of co-author of each paper
    co_author_line = re.findall(co_author_line_pattern, html_str)

    #a re pattern to get each co-author of a paper
    co_author_pattern = '\">[\s\S]*?</a>'
    for t in co_author_line:
        # get each co-author of a paper
        co_author = re.findall(co_author_pattern, t)
        for t in co_author:
            # cut the string of co-author
            co = t.split('\">')[1].split("</a>")[0].strip()
            # add this result to the co-author dictionary
            if co in co_author_list:
                co_author_list[co] += 1
            else:
                co_author_list[co] = 1

#print the co-author's name and times (co-author's name sorted by alphabet)
#the result won't print the author name you search
for author in sorted(co_author_list):
    if author != author_name:
        print(author, ': ', co_author_list[author], 'times')
