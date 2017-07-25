# Gather NBA Data

# Shooting data scraper

import requests, bs4, openpyxl,time
import pandas as pd

players = []
playerID = []
startTime = time.time()
for year in range(2012,2017):
    workbook = filename = str(year)+'-'+str(year+1)+' Total.xlsx'
    print(workbook)
    
    wb = openpyxl.load_workbook(workbook, read_only=True, data_only=True)
    ws = wb['Sheet1']
    for row in range(2,ws.max_row+1):
        playCell = 'B'+str(row)
        IDcell = 'C'+str(row)
        if ws[IDcell].value not in playerID:
            players.append(ws[playCell].value)
            playerID.append(ws[IDcell].value)

print('Reading Finished')
wb = openpyxl.Workbook()
ws = wb.create_sheet()
destFilename = 'TotalCareer.xlsx'
count = 0

for x in range(0,len(players)):
    url='http://www.basketball-reference.com/players/'+playerID[x][:1]+'/'+playerID[x]+'.html'
    res = requests.get(url)
    html = res.content
    soup = bs4.BeautifulSoup(html, 'html.parser')
    step1 = str(soup.find('div',attrs={'id':'all_shooting'})).split('<!--')[1]
    step1 = step1.split('<tbody>')[1].split('</tfoot>')[0]
    b2s = bs4.BeautifulSoup(step1,'html.parser')
    shootSplits = b2s.findAll('tr')
    headers = len(shootSplits[0].findAll('td'))
    posCol = {}
    for i in range(0,len(shootSplits)):
        if str(shootSplits[i]).split('scope=\"row">')[1].split('</th>')[0] != 'Career':
            pos = str(shootSplits[i]).split('data-stat=\"pos">')[1].split('</td')[0]
            if pos in posCol:
                posCol[pos] += 1
            else:
                posCol[pos] = 1
                
            count += 1
##            for j in range(0,len(splits[i].findAll('td'))):
##                ioi = splits[i].findAll('td')[j]
##                col = str(ioi).split('data-stat=\"')[1].split('\">')[0]
##                val = str(ioi).split('\">')[1].split('</td')[0]
        else:
            for j in range(0,headers):
                
                ioi = shootSplits[i].findAll('td')[j]
                
                if x == 0:
                    ws['A1']='Player'
                    ws[openpyxl.utils.get_column_letter(j+2)+str(1)] = (str(ioi).split('data-stat=\"')[1].split('\">')[0])
                
                ws['A'+str(x+2)]=players[x]

                if str(shootSplits[i-1]).split('scope=\"row">')[1].split('</th>')[0].split('/">')[1].split('</a>')[0] == '2016-17':
                    ws['B'+str(x+2)]='Active'
                else:
                    ws['B'+str(x+2)]='Inactive' 

                ws['C'+str(x+2)]=max(posCol, key=posCol.get)
                cell = openpyxl.utils.get_column_letter(j+4)+str(x+2)
                ws[cell] = str(ioi).split('\">')[1].split('</td')[0]
                
                count += 1

            
            break

    step1 = str(soup.find('div',attrs={'id':'all_per_poss'})).split('<!--')[1]
    step1 = step1.split('<tbody>')[1].split('</tfoot>')[0]
    b2s = bs4.BeautifulSoup(step1,'html.parser')
    splits100 = b2s.findAll('tr')

    for i in range(0,len(splits100)):
        if str(splits100[i]).split('scope=\"row">')[1].split('</th>')[0] != 'Career':
            count += 1

        else:
            for j in range(0,len(splits100[i].findAll('td'))):
                if i == 0:
                    ws['A'+str(j+2+headers)] = (str(ioi).split('data-stat=\"')[1].split('\">')[0])
                
                ioi = splits100[i].findAll('td')[j]
                cell = openpyxl.utils.get_column_letter(j+4+headers)+str(x+2)
                ws[cell] = str(ioi).split('\">')[1].split('</td')[0]
                
                count += 1

    
    step1 = str(soup.find('div',attrs={'id':'all_advanced'})).split('<!--')[1]
    step1 = step1.split('<tbody>')[1].split('</tfoot>')[0]
    b2s = bs4.BeautifulSoup(step1,'html.parser')
    advSplits = b2s.findAll('tr')
    headers += len(splits100[0].findAll('td'))
    for i in range(0,len(advSplits)):
        if str(advSplits[i]).split('scope=\"row">')[1].split('</th>')[0] != 'Career':
            count += 1

        else:
            for j in range(0,len(advSplits[i].findAll('td'))):
                if i == 0:
                    ws['A'+str(j+2+headers)] = (str(ioi).split('data-stat=\"')[1].split('\">')[0])
                
                ioi = advSplits[i].findAll('td')[j]
                cell = openpyxl.utils.get_column_letter(j+4+headers)+str(x+2)
                ws[cell] = str(ioi).split('\">')[1].split('</td')[0]
                
                count += 1

    print(x)

print(count)
wb.save(filename = destFilename)

print(time.time()-startTime)
