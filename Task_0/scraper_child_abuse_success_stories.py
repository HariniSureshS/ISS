import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
soup = BeautifulSoup(urllib.request.urlopen('https://www.boltburdonkemp.co.uk/child-abuse/success-stories/'), "html.parser")

folderpath='child_abuse_success_caseStories/'
f=open(folderpath+f'case_story0.txt', 'w')
count=0
dicForFiles={}
dicForFiles['title']=[]
dicForFiles['text']=[]
temp=''

##basically modified a bit one of the answers here
## https://stackoverflow.com/questions/25216598/print-heading-and-corresponding-paragraph-in-beautiful-soup
for header in soup.find_all(['h3']):
    f.write(header.get_text() + u'\n')
    dicForFiles['title'].append(header.get_text())
    
    for elem in header.next_siblings:
        
        if elem.name and elem.name.startswith('h'):
            f.close()
            count = count+1
            dicForFiles['text'].append(temp)
            temp=''
            f=open(folderpath+f'case_story{count}.txt', 'w')
            break
            
        if elem.name == 'p':
            f.write(elem.get_text() + u'\n')
            temp += elem.get_text()
dicForFiles['text'].append(temp)
f.close()

##some cleaning
del dicForFiles['title'][0],dicForFiles['text'][0]
dicForFiles['title']=dicForFiles['title'][:-2]

##save collated files
pd.DataFrame(data=dicForFiles).to_csv(folderpath+'allCaseFile.csv',index=None)