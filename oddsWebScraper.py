from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
import pandas as pd
import time


def oddsFinder():
    driver = Chrome("C:\Program Files (x86)\chromedriver.exe")
    driver.get('https://www.oddschecker.com/horse-racing/chepstow/16:00/winner')
    soup = BeautifulSoup(driver.page_source, 'lxml')
    table = soup.find('table', class_="eventTable")
    raceName = soup.title
    raceName = raceName.text.strip().split(' Betting')
    raceNameTime = raceName[0].split(':')
    df = pd.DataFrame(columns=['Number','Horse','bet365', 'Skybet', 'Paddypower', 'Hills', '888', 'Betfair', 'Betvictor', 'Coral', 'Unibet'])
    for row in table.tbody.find_all("tr"):
        columns = row.find_all('td')
        if columns != []:
            num = columns[0].text.strip()
            horse = columns[1].text.strip()
            horse = horse.split(' (')[0]
            bet = columns[2].text.strip()
            sky = columns[3].text.strip()
            pwr = columns[4].text.strip()
            hil = columns[5].text.strip()
            eig = columns[6].text.strip()
            fir = columns[7].text.strip()
            vic = columns[8].text.strip()
            cor = columns[9].text.strip()
            uni = columns[10].text.strip()
            df = df.append({'Number': num,'Horse': horse,'bet365': bet, 'Skybet': sky, 'Paddypower': pwr, "Hills": hil, "888": eig, "Betfair": fir, "Betvictor": vic, "Coral": cor, "Unibet": uni}, ignore_index=True)
    try:
        currentOdds = pd.read_excel('Odds.xlsx', sheet_name=raceNameTime[0]+raceNameTime[1],  engine='openpyxl')
    except:
        print('Odds do not current exist for race in system')
    file = pd.ExcelFile('Odds.xlsx', engine='openpyxl')


    df.loc[(df['bet365']) == '', 'bet365'] = 'Not Listed'
    df.loc[(df['Skybet']) == '', 'Skybet'] = 'Not Listed'
    df.loc[(df['Paddypower']) == '', 'Paddypower'] = 'Not Listed'
    df.loc[(df['Hills']) == '', 'Hills'] = 'Not Listed'
    df.loc[(df['888']) == '', '888'] = 'Not Listed'
    df.loc[(df['Betfair']) == '', 'Betfair'] = 'Not Listed'
    df.loc[(df['Betvictor']) == '', 'Betvictor'] = 'Not Listed'
    df.loc[(df['Coral']) == '', 'Coral'] = 'Not Listed'
    df.loc[(df['Unibet']) == '', 'Unibet'] = 'Not Listed'
    with pd.ExcelWriter('Odds.xlsx', mode='a', engine='openpyxl', if_sheet_exists='replace') as oddsWriter:
        df.to_excel(oddsWriter, sheet_name=raceNameTime[0]+raceNameTime[1], index=False)

    count = 0
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            try:
                currentMarketOdds = df.iat[i,j]
                oldOdds = currentOdds.iat[i, j]
            except:
                print('The odds have only just been added to the system, please run again for a comparison')
            if currentMarketOdds != oldOdds and j > 0:
                print("The odds for",df.iat[i, 1], "Have changed to", currentMarketOdds, "From", oldOdds, "On", df.columns[j])
                count = count+1
    print('The total number of odds that have fluctuated since your last search is', count)

if __name__ == '__main__':
    while True:
        oddsFinder()
        timeWait = 60
        print('Waiting 10 minutes until searching for updated odds')
        time.sleep(timeWait)



