# Gather NCAA Data

# College Career stats scrapers for players who played between 2008-2016
# A lot of garbage parsing in here

import requests, bs4, time
import pandas as pd
from string import ascii_lowercase as alphabet

startTime = time.time()
totalStats = []
firstName = False

for initial in alphabet:
    
    url='http://www.sports-reference.com/cbb/players/'+initial+'-index.html'
    res = requests.get(url)
    html = res.content
    soup = bs4.BeautifulSoup(html, 'html.parser')
    step1 = soup.find('div', attrs={'id':'content'})
    step2 = bs4.BeautifulSoup(str(step1.findAll('div')),'html.parser').findAll('p')
    
    for i in range(0,len(step2)):
        
        info = bs4.BeautifulSoup(str(step2[i]),'html.parser').findAll('a')
        
        if int(str(step2[i]).split('"note">(')[1].split(') <a')[0][:4]) in range(2008,2018): 
            if firstName == False:
                firstName = True
                
            totalLine = [];
            
            urlAndName = str(info[0]).split('href="')[1].split('">')
            
            newUrl = 'http://www.sports-reference.com'+urlAndName[0]
            
            while True:
                try:
                    newRes = requests.get(newUrl)
                    newHtml = newRes.content
                    newSoup = bs4.BeautifulSoup(newHtml, 'html.parser')
                    
                    totalLine.append(str(info[0]).split('">')[1].split('</a>')[0]) #name
                    print(str(info[0]).split('">')[1].split('</a>')[0])
                    totalLine.append(str(info[1]).split('/">')[1].split('</a>')[0]) #school
                    totalLine.append(str(newSoup.find('div', attrs={'id':'meta'}).findAll('p')).split('</strong>')[1].split('<p>')[0].strip(' \t\n\r')) #Pos
                    
                    if int(str(step2[i]).split('"note">(')[1].split(') <a')[0][5:]) == 2017:
                        totalLine.append('Active')
                    else:
                        totalLine.append('Inactive') #status

                    try:
                        #--------------------------- PER 100
                        step1 = str(newSoup.find('div',attrs={'id':'all_players_per_poss'})).split('<!--')[1]
                        step1 = step1.split('<tbody>')[1].split('</tfoot>')[0]
                        b2s = bs4.BeautifulSoup(step1,'html.parser')
                        splits100 = b2s.findAll('tr')
                        headers = len(splits100[0].findAll('td'))

                        for i in range(0,len(splits100)):
                            
                            if str(splits100[i]).split('scope=\"row">')[1].split('</th>')[0] != 'Career': 
                                pass #Only read Career totals
                            
                            else:
                                for j in range(0,headers):
                                    
                                    ioi = splits100[i].findAll('td')[j]
                                    
                                    if firstName and initial == 'a':
                                        totalHeaders=['Player', 'School', 'Status']
                                        totalHeaders.append(str(ioi).split('data-stat=\"')[1].split('\">')[0])

                                    totalLine.append(str(ioi).split('\">')[1].split('</td')[0])

                                    
                                break
                        #--------------------------- ADVANCED    
                        step1 = str(newSoup.find('div',attrs={'id':'all_players_advanced'})).split('<!--')[1]
                        step1 = step1.split('<tbody>')[1].split('</tfoot>')[0]
                        b2s = bs4.BeautifulSoup(step1,'html.parser')
                        advSplits = b2s.findAll('tr')
                        headers = len(advSplits[0].findAll('td'))

                        for i in range(0,len(advSplits)):
                            if str(advSplits[i]).split('scope=\"row">')[1].split('</th>')[0] != 'Career':
                                pass
                            else:
                                for j in range(0,headers):
                                    
                                    ioi = advSplits[i].findAll('td')[j]
                                    
                                    if firstName and initial == 'a':
                                        totalHeaders.append(str(ioi).split('data-stat=\"')[1].split('\">')[0])

                                    totalLine.append(str(ioi).split('\">')[1].split('</td')[0])

                                    
                                break
                    
                        totalStats.append(totalLine)
                        break

                    except IndexError:
                        break

                except:
                    pass
            
        else:
            pass
            
            

        
df = pd.DataFrame(totalStats)   
df.to_csv('ncaaStats.csv')
print(time.time()-startTime)
