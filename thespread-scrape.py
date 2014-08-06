from bs4 import BeautifulSoup
import mechanize
import re
import urlparse
import time
from datetime import datetime
from xlwt import Workbook, Style

# construct the output Excel filename from current date/time
today = datetime.today()
excelFilename = 'mlb_pitchers_%4d-%02d-%02d.xls' % (today.year, today.month, today.day)

BASE_URL = 'http://www.thespread.com'
wb = Workbook(encoding='utf-8')
sheet1 = wb.add_sheet('Compiled Data')
sheet2 = wb.add_sheet('Data Output')
sheet3 = wb.add_sheet('Backtest')

style_bold = Style.easyxf('font: bold 1')
style_over = Style.easyxf('pattern: pattern solid, fore_colour green;')
style_under = Style.easyxf('pattern: pattern solid, fore_colour red;')
style_push = Style.easyxf('pattern: pattern solid, fore_colour yellow;')
pitchers = {}

def makeSoup(url):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Firefox')]
    try:
        response = br.open(url)
    except:
        return None

    return BeautifulSoup(response.read())

def process_pitcher(name, url):
    soup = makeSoup(url)
    num_try = 1
    while soup is None:
        print "\t",'None'
        if num_try == 6:
            break;

        time.sleep(10)
        soup = makeSoup(url)
        num_try = num_try + 1

    stat = soup.find(text=stat_regexp)
    match = re.search(reg_ck, stat)
    ck_param = match.group(1)

    stat_url = urlparse.urljoin(BASE_URL, 'statwrapper.php')
    stat_url = stat_url + "?ck=" + ck_param
    stat_soup = makeSoup(stat_url)

    stat_tbl = stat_soup.find('table', attrs={'class':'datatable', 'cellspacing':'1'})

    try:
        for row in stat_tbl.findAll('tr')[4:]:
            cols = row.findAll('td')
            cell_value = cols[7].get_text()
            pitchers[name]['stat'].append(cell_value)
    except AttributeError:
        pass


def saveToExcel():
    writeSheet1()
    writeSheet2_3()

def writeSheet1():
    rowNum = 1
    for name in sorted(pitchers, key=lambda x : pitchers[x]['numberOfGames'], reverse=True): 
        sheet1.write(rowNum, 0, name)
        colNum = 1
        for stat in pitchers[name]['stat']:
            if stat == 'Un':
                style = style_under
            elif stat == 'Ov':
                style = style_over
            else:
                style = style_push

            sheet1.write(rowNum, colNum, stat, style)
            colNum = colNum + 1

        rowNum = rowNum + 1

def writeSheet2_3():
    rowNumCol2 = 1
    rowNumCol3 = 1
    rowNumCol4 = 1
    rowNumCol5 = 1

    # variables for the count of pitchers who have satisfied the Overcriteria
    totalLast10_ov = 0
    totalUnit1_ov = 0
    totalUnit2_ov = 0
    totalUnit3_ov = 0

    backtestLast10_ov = 0
    backtestUnit1_ov = 0
    backtestUnit2_ov = 0
    backtestUnit3_ov = 0

    # print the Over data
    sheet2.write(0,0, 'Over', style_bold)
    sheet2.write(0,1, '70% Last 10', style_bold)
    sheet2.write(0,2, '1Unit', style_bold)
    sheet2.write(0,3, '2Unit', style_bold)
    sheet2.write(0,4, '3Unit', style_bold)
    for name in sorted(pitchers, key=lambda x : pitchers[x]['numberOfGames'], reverse=True):
        last10 = calcLastGames(name, 'Ov', 10)                                                  # compute percentage of 'Ov' for the last 10 games
        unit1 = calcLastGames(name, 'Ov', 3)                                                    # compute percentage of 'Ov' for the last 3 games
        unit2 = calcLastGames(name, 'Ov', 4)
        unit3 = calcLastGames(name, 'Ov', 5)
        if last10 >= 0.70:
            sheet2.write(rowNumCol2, 1, name)
            totalLast10_ov = totalLast10_ov + 1
            if len(pitchers[name]['stat']) > 10 and pitchers[name]['stat'][10] == 'Ov':
                backtestLast10_ov = backtestLast10_ov + 1
            rowNumCol2 = rowNumCol2 + 1

        if unit1 == 1:                                                                          # last 3 games are all 'Ov'
            sheet2.write(rowNumCol3, 2, name)
            totalUnit1_ov = totalUnit1_ov + 1
            if len(pitchers[name]['stat']) > 3 and pitchers[name]['stat'][3] == 'Ov':
                backtestUnit1_ov = backtestUnit1_ov + 1
            rowNumCol3 = rowNumCol3 + 1

        if unit2 == 1:                                                                          # last 4 games are all 'Ov'
            sheet2.write(rowNumCol4, 3, name)
            totalUnit2_ov = totalUnit2_ov + 1
            if len(pitchers[name]['stat']) > 4 and pitchers[name]['stat'][4] == 'Ov':
                backtestUnit2_ov = backtestUnit2_ov + 1
            rowNumCol4 = rowNumCol4 + 1

        if unit3 == 1:                                                                          # last 5 games are all 'Ov'
            sheet2.write(rowNumCol5, 4, name)
            totalUnit3_ov = totalUnit3_ov + 1
            if len(pitchers[name]['stat']) > 5 and pitchers[name]['stat'][5] == 'Ov':
                backtestUnit3_ov = backtestUnit3_ov + 1
            rowNumCol5 = rowNumCol5 + 1


    # print the Under data
    rowNum = max(rowNumCol2, rowNumCol3, rowNumCol4, rowNumCol5) + 3                            # get the highest row from the 'Over' data and add 3 blank lines
    rowNumCol2 = rowNum + 1
    rowNumCol3 = rowNum + 1
    rowNumCol4 = rowNum + 1
    rowNumCol5 = rowNum + 1

    # variables for the count of pitchers who have satisfied the Under criteria
    totalLast10_un = 0
    totalUnit1_un = 0
    totalUnit2_un = 0
    totalUnit3_un = 0

    backtestLast10_un = 0
    backtestUnit1_un = 0
    backtestUnit2_un = 0
    backtestUnit3_un = 0

    # write header for Under data
    sheet2.write(rowNum,0, 'Under', style_bold)
    sheet2.write(rowNum,1, '70% Last 10', style_bold)
    sheet2.write(rowNum,2, '1Unit', style_bold)
    sheet2.write(rowNum,3, '2Unit', style_bold)
    sheet2.write(rowNum,4, '3Unit', style_bold)
    for name in sorted(pitchers, key=lambda x : pitchers[x]['numberOfGames'], reverse=True):
        last10 = calcLastGames(name, 'Un', 10)                                                  # compute percentage of 'Un' for the last 10 games
        unit1 = calcLastGames(name, 'Un', 3)                                                    # compute percentage of 'Un' for the last 3 games
        unit2 = calcLastGames(name, 'Un', 4)
        unit3 = calcLastGames(name, 'Un', 5)
        if last10 >= 0.70:
            sheet2.write(rowNumCol2, 1, name)
            totalLast10_un = totalLast10_un + 1
            if len(pitchers[name]['stat']) > 10 and pitchers[name]['stat'][10] == 'Un':
                backtestLast10_un = backtestLast10_un + 1
            rowNumCol2 = rowNumCol2 + 1

        if unit1 == 1:                                                                          # last 3 games are all 'Un'
            sheet2.write(rowNumCol3, 2, name)
            totalUnit1_un = totalUnit1_un + 1
            if len(pitchers[name]['stat']) > 3 and pitchers[name]['stat'][3] == 'Un':
                backtestUnit1_un = backtestUnit1_un + 1
            rowNumCol3 = rowNumCol3 + 1

        if unit2 == 1:                                                                          # last 4 games are all 'Un'
            sheet2.write(rowNumCol4, 3, name)
            totalUnit2_un = totalUnit2_un + 1
            if len(pitchers[name]['stat']) > 4 and pitchers[name]['stat'][4] == 'Un':
                backtestUnit2_un = backtestUnit2_un + 1
            rowNumCol4 = rowNumCol4 + 1

        if unit3 == 1:                                                                          # last 5 games are all 'Un'
            sheet2.write(rowNumCol5, 4, name)
            totalUnit3_un = totalUnit3_un + 1
            if len(pitchers[name]['stat']) > 5 and pitchers[name]['stat'][5] == 'Un':
                backtestUnit3_un = backtestUnit3_un + 1
            rowNumCol5 = rowNumCol5 + 1


    # write the sheet3
    sheet3.write(0, 0, 'Over', style_bold)
    sheet3.write(1, 0, '70% Last 10')
    sheet3.write(2, 0, '1 Unit')
    sheet3.write(3, 0, '2 Unit')
    sheet3.write(4, 0, '3 Unit')

    backtestLast10 = (float(backtestLast10_ov) / totalLast10_ov) * 100
    backtestUnit1 = (float(backtestUnit1_ov) / totalUnit1_ov) * 100
    backtestUnit2 = (float(backtestUnit2_ov) / totalUnit2_ov) * 100
    backtestUnit3 = (float(backtestUnit3_ov) / totalUnit3_ov) * 100

    sheet3.write(1, 1, '{0:.0f}%'.format(backtestLast10))
    sheet3.write(2, 1, '{0:.0f}%'.format(backtestUnit1))
    sheet3.write(3, 1, '{0:.0f}%'.format(backtestUnit2))
    sheet3.write(4, 1, '{0:.0f}%'.format(backtestUnit3))


    # Under backtest
    rowNum = 7
    sheet3.write(rowNum, 0, 'Under', style_bold)
    sheet3.write(rowNum+1, 0, '70% Last 10')
    sheet3.write(rowNum+2, 0, '1 Unit')
    sheet3.write(rowNum+3, 0, '2 Unit')
    sheet3.write(rowNum+4, 0, '3 Unit')

    backtestLast10 = (float(backtestLast10_un) / totalLast10_un) * 100
    backtestUnit1 = (float(backtestUnit1_un) / totalUnit1_un) * 100
    backtestUnit2 = (float(backtestUnit2_un) / totalUnit2_un) * 100
    backtestUnit3 = (float(backtestUnit3_un) / totalUnit3_un) * 100

    sheet3.write(rowNum+1, 1, '{0:.0f}%'.format(backtestLast10))
    sheet3.write(rowNum+2, 1, '{0:.0f}%'.format(backtestUnit1))
    sheet3.write(rowNum+3, 1, '{0:.0f}%'.format(backtestUnit2))
    sheet3.write(rowNum+4, 1, '{0:.0f}%'.format(backtestUnit3))


def calcLastGames(name, stat, numGames):
    cnt_stat = 0
    for i in range(0, numGames): 

        if i >= len(pitchers[name]['stat']):
            break
        
        if pitchers[name]['stat'][i] == stat:
            cnt_stat = cnt_stat + 1

    return (cnt_stat * 1.0) / numGames


def write_header():
    sheet1.write(0,0, 'PitcherName', style_bold)
    sheet1.write(0,1, 'Start #1', style_bold)
    sheet1.write(0,2, 'Start #2', style_bold)
    sheet1.write(0,3, 'Start #3', style_bold)
    sheet1.write(0,4, 'Start #4', style_bold)
    sheet1.write(0,5, 'Start #5', style_bold)
    sheet1.write(0,6, 'Start #6', style_bold)
    sheet1.write(0,7, 'Start #7', style_bold)
    sheet1.write(0,8, 'Start #8', style_bold)
    sheet1.write(0,9, 'Start #9', style_bold)
    sheet1.write(0,10, 'Start #10', style_bold)
    sheet1.write(0,11, 'Start #11', style_bold)
    sheet1.write(0,12, 'Start #12', style_bold)
    sheet1.write(0,13, 'Start #13', style_bold)
    sheet1.write(0,14, 'Start #14', style_bold)
    sheet1.write(0,15, 'Start #15', style_bold)
    sheet1.write(0,16, 'Start #16', style_bold)
    sheet1.write(0,17, 'Start #17', style_bold)
    sheet1.write(0,18, 'Start #18', style_bold)
    sheet1.write(0,19, 'Start #19', style_bold)
    sheet1.write(0,20, 'Start #20', style_bold)



if __name__ == '__main__':
    # regular expression to search the statwrapper.php page
    stat_regexp = re.compile(r'statwrapper.php')

    # regular expression to get the ck parameter to the statwrapper.php page
    reg_ck = re.compile(r'"ck": "(.+)"')

    # main page of the mlb pitchers stats
    mainUrl = 'http://www.thespread.com/mlb-baseball-pitching-pitcher-stats'
    soup = makeSoup(mainUrl)

    # get the text of the JavaScript function that calls the statwrapper.php page
    stat = soup.find(text=stat_regexp)

    # get the statwrapper.php ck parameter value for the main page of pitcher stats
    match = re.search(reg_ck, stat)
    ck_param = match.group(1)

    # now load the main pitcher stats page, by load the statwrapper.php page 
    # with the correct ck parameter
    stat_url = urlparse.urljoin(BASE_URL, 'statwrapper.php')
    stat_url = stat_url + "?ck=" + ck_param
    stat_soup = makeSoup(stat_url)

    # get the pitchers list
    write_header()
    pitcher_tbl = stat_soup.find('table', attrs={'class':'datatable', 'cellpadding':'3'})
    rowNum = 1
    for row in pitcher_tbl.findAll('tr')[2:]:
        # get the url of each pitcher's page
        name = row.a.string
        pitcher_url = urlparse.urljoin(BASE_URL, row.a['href'])
        num_games = row.findAll('td')[1]
        pitchers[name] = {}                                                 # add current pitcher to the pitchers dictionary
        pitchers[name]['numberOfGames'] = int(num_games.get_text())         # add number of games
        pitchers[name]['stat'] = []                                         # add statistics list
        print "%d. %s => %s games" % (rowNum, name, num_games.get_text())
        process_pitcher(name, pitcher_url)
        time.sleep(2)                                                       # pause for 2 seconds before processing next pitcher
        rowNum = rowNum + 1


    saveToExcel()
    wb.save(excelFilename)
