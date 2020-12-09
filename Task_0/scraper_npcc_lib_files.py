##first part is basically using this tutorial
##https://realpython.com/modern-web-automation-with-python-and-selenium/

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import os

##folders to save in
pdfFolderPath='npccLibFiles/pdf_files/'
htmlFolderPath='npccLibFiles/html_files/'
abstractFolderPath='npccLibFiles/abstract_files/'
keywordsFolderPath='npccLibFiles/keyword_files/'

os.mkdir('npccLibFiles')
os.mkdir(pdfFolderPath)
os.mkdir(htmlFolderPath)
os.mkdir(abstractFolderPath)
os.mkdir(keywordsFolderPath)


opts = Options()
opts.headless = True
assert opts.headless  # Operating in headless mode
browser = Firefox(options=opts)

##A starting website
browser.get('https://library.nspcc.org.uk/HeritageScripts/Hapi.dll/retrieve2?SetID=4F99D829-D113-439B-8BE2-5171E0F2BC47&LabelText=Case%20review&searchterm=%2A&Fields=%40&Media=SCR&Bool=AND&SearchPrecision=20&SortOrder=Y1&Offset=1&Direction=%2E&Dispfmt=F&Dispfmt_b=B27&Dispfmt_f=F13&DataSetName=LIVEDATA')

count=1

##save page: this function is there just for brevity and 
##removing the repeating code

def savePage(filename, content, writeType='w'):
    
    f=open(filename,writeType)
    f.write(content)
    f.close()

##save the first page 
savePage(htmlFolderPath + f'file{count}.html', browser.page_source)

##find the next button(following the tutorial)
clickButton = browser.find_element_by_class_name('navNext')

while clickButton:
    
    count=count+1    
    browser.find_element_by_class_name('navNext').click()
    savePage(htmlFolderPath + f'file{count}.html', browser.page_source)
    clickButton = browser.find_element_by_class_name('navNext')
        
browser.close()
##above code collects about 1466 files before crashing.
##which i felt were enough anyways 
numFiles=1466


##Handing over to beautiful soup

from bs4 import BeautifulSoup
import requests
import os.path

##this is a quick fix
def has_href(cont):
    try:
        cont['href']
        return True
    except:
        return False
    
##to check if link is broken 
def linkAvailable(link):
    try:
        response = requests.get(url)
        return response
    except:
        return False

##some links are from the nspcc website and need extension
def addLink(link):
    
    if '/HeritageScripts' in link:
        return 'https://library.nspcc.org.uk' + link
    else:
        return link

## find and download all htmls which have full case reports available

for ind in range(1, numFiles+1):
    f = open(htmlFolderPath + f'file{ind}.html','r')
    soup=BeautifulSoup(f)
    f.close()
    
    for header in soup.find_all(class_='fulllabel'):
        ##pdf links are generally attached to 'Others' string
        if('Other' in header.string):
            for content in header.next_siblings:
                
                if has_href(content):
                    
                    url=addLink(content['href'])
                    response = linkAvailable(url)
                    if response:
                        savePage(pdfFolderPath + f'caseReview{ind}.pdf',response.content, 'wb')

## this collects 754 files, as some links don't have pdfs(full case review reports) 
## and some links are dead

##finally add abstracts and keywords to files where full case report was found

def saveContent(filename, header):
    
    f=open(filename, 'w')
    
    for content in header.next_siblings:
        if content.string : f.write(content.string)
    
    f.close()

for ind in range(1, numFiles+1):
    
    fname = pdfFolderPath + f'caseReview{ind}.pdf'
    
    ##check if file exists
    if os.path.isfile(fname):
        f = open(htmlFolderPath + f'file{ind}.html','r')
        soup=BeautifulSoup(f)
        f.close()
        
        for header in soup.find_all(class_='fulllabel'):
            
            if('Abstract' in header.string):
                saveContent(abstractFolderPath+f'abstract{ind}.txt', header)
            
            elif('Keywords' in header.string):
                saveContent(keywordsFolderPath+f'keywords{ind}.txt', header)

