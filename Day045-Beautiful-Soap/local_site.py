from bs4 import BeautifulSoup
# lxml package required for using lxml parser

filename = 'website.html'

with open(filename, 'r', encoding='utf-8') as f:
    contents = f.read()

# Pass on the extracted html content as well as python html parser
# Sometimes, lxml parser can be used.
# See: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#:~:text=each%20parser%20library%3A-,Parser,-Typical%20usage
soup = BeautifulSoup(contents, 'html.parser')

print(soup.title)
print(soup.title.name)
print(soup.title.string)

# Print the website code but indented
# print(soup.prettify())

print(soup.a)  # get the first 'a' tag

print('\n\n'+'-'*50+'\n')

# --- Searching through the soup ------------- #
# Find all occurrences of a tag with a given query
all_anchor_tags = soup.find_all(name='a')
[print(tag.getText(), tag.get('href')) for tag in all_anchor_tags]

print('\n'+'-'*20+'\n')

# Find the first occurrence of a tag with a give query
heading = soup.find(name='h1', id='name')
print(heading.text)

# Non-existing attribute
heading = soup.find(name='h1', id='wrong-id')
print(heading)

# Attribute with special Python keyword
heading = soup.find(name='h3', class_='heading')
print(heading.text, heading.get('class'))

# Using selectors to reach a specific nested tag
# NOTE: select -> all items, select_on -> first item
company_url = soup.select_one(selector="p a")  # a tag nested in a p tag
print(company_url.get('href'))

# select the same element using the id
company_url = soup.select_one(selector="#name")
print(company_url)

# select all elements in a class
headings = soup.select(selector=".heading")
print(headings)
