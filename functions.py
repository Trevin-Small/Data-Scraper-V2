import time, keyboard, random, sys
import lxml
from bs4 import BeautifulSoup

startDate = ""
endDate = ""

def setDates(start, end):
    global startDate
    global endDate
    startDate = start
    endDate = end

def wait(x = 1):
    randTime = random.uniform(0,0.75)
    time.sleep((0.25 + randTime) * x)

def getAgencies(user, titleAgencies, windows, selenBrowser):
    agencyList = []

    selenBrowser.get('https://rightdata.driggstitle.com/prv/site.new_confirm?name=' + user.get_username() + '&password=' + user.get_password())
    wait(3)
    selenBrowser.get('https://rightdata.driggstitle.com/prv/mta_dta.title_comps')
    wait()
    html = selenBrowser.page_source
    soup = BeautifulSoup(html, 'lxml')
    agencyList = soup.find('table')
    agencyList = agencyList.find_all('input', {'size':'100'})

    for i in range(len(agencyList)):

        currentAgency = agencyList[i]['value']

        if '\xa0' in currentAgency or 'value="293"' in currentAgency or "'" in currentAgency:

            currentAgency = currentAgency.replace(u'\xa0', u' ')
            currentAgency = currentAgency.replace(u'value="293">', u'')
            currentAgency = currentAgency.replace(u"'", u'')

        if currentAgency != '':

            titleAgencies.add_long_agency(currentAgency.lower())
            titleAgencies.add_short_agency(currentAgency[:5].lower())

    print(titleAgencies.get_title_agencies())

    selenBrowser.get('https://rightdata.driggstitle.com/prv/mta_dta.file_mta_rpt')
    windows.switchWindows(0)
    windows.addWindowToDict(0, 'driggsAgentList')
    openMta(user, windows, selenBrowser)
    windows.switchWindowByDict('driggsAgentList')

def openMta(user, windows, selenBrowser):

    selenBrowser.execute_script("window.open('about:blank', 'secondtab');")
    selenBrowser.switch_to.window("secondtab")
    windows.updateWindows()
    wait()
    selenBrowser.get("https://www.mymta.com/")
    wait(3)
    selenBrowser.find_element_by_name("user").send_keys(user.get_mta_username())
    wait()
    selenBrowser.find_element_by_name("pw").send_keys(user.get_mta_password())
    wait(3)
    selenBrowser.find_element_by_name("button").click()
    wait()
    selenBrowser.find_element_by_xpath('//input[@type="submit"]').click()
    wait(3)
    selenBrowser.get("https://www.mymta.com/agent_mktshare.php?print=1")
    wait()
    windows.addWindowToDict(1, 'mtaSearch')

def enterData(agent, titleAgencies, windows, selenBrowser):
    global startDate
    global endDate

    skippedName = enterDataForDate(agent, titleAgencies, windows, selenBrowser, startDate, endDate, True)
    if skippedName:
        return False
    dates = getNextDates(selenBrowser, startDate, endDate)
    for date in dates:
        date = str.split(date)
        startDate = date[0]
        endDate = date[len(date) - 1]
        enterDataForDate(agent, titleAgencies, windows, selenBrowser, startDate, endDate, False)

    windows.switchWindowByDict('agentPageOne')
    selenBrowser.close()
    wait()
    windows.switchWindowByDict('agentPageTwo')
    selenBrowser.close()
    wait()
    windows.switchWindowByDict('driggsAgentList')
    wait()
    selenBrowser.refresh()
    wait()
    return True

def enterDataForDate(agent, titleAgencies, windows, selenBrowser, startDate, endDate, fullYearRecord):

    startDateEntry = startDate.replace("/","")
    endDateEntry = endDate.replace("/","")

    if fullYearRecord:
        wait()
        windows.switchWindowByDict('driggsAgentList')
        agentName = selenBrowser.find_element_by_xpath('//a[@href]').text
        names = str.split(agentName.lower())
        try:
            lastName = names[len(names) - 1]
        except IndexError:
            # Name not found, skip name and return function.
            windows.switchWindowByDict('driggsAgentList')
            wait()
            selenBrowser.find_element_by_name('skipBtn').click()
            wait()
            return True

        if lastName == "" or lastName == " ":
            # Name not found, skip name and return function.
            windows.switchWindowByDict('driggsAgentList')
            wait()
            selenBrowser.find_element_by_name('skipBtn').click()
            wait()
            return True

        wait()
        windows.switchWindowByDict('mtaSearch')
        wait()
        selenBrowser.find_element_by_xpath('//input[@value="<<"]').click()
        wait()
        nameField = selenBrowser.find_element_by_name("agentsearch")
        wait()
        nameField.clear()
        wait()
        nameField.send_keys(lastName)

    windows.switchWindowByDict('mtaSearch')
    wait()
    dateField = selenBrowser.find_element_by_name("date1")
    wait()
    dateField.clear()
    wait()
    dateField.send_keys(startDate)
    wait()
    dateField = selenBrowser.find_element_by_name("date2")
    wait()
    dateField.clear()
    wait()
    dateField.send_keys(endDate)
    wait()

    if fullYearRecord:
        nameFound = False
        selenBrowser.find_element_by_xpath('//input[@value="Go"]').click()
        wait()
        nameResults = selenBrowser.find_elements_by_xpath('//option[@value]')
        wait()

        for name in nameResults:
            nameString = name.text
            nameString = nameString.lower()
            nameString = str.split(nameString)
            if len(nameString) >= 1:
                if names[0] == nameString[0] and names[len(names) - 1] == nameString[len(nameString) - 1]:
                    nameFound = True
                    name.click()
                    selenBrowser.find_element_by_name("Right").click()
                    wait()
                    break

        if not nameFound:
            # Name not found, skip name and return function.
            windows.switchWindowByDict('driggsAgentList')
            wait()
            selenBrowser.find_element_by_name('skipBtn').click()
            wait()
            return True


    selenBrowser.find_element_by_xpath('//input[@value="View HTML"]').click()
    time.sleep(5)
    windows.updateWindows()
    windows.addWindowToDict(len(windows.windows) - 1, 'mtaData')
    windows.switchWindowByDict('mtaData')
    wait(6)
    getData(agent, selenBrowser)
    wait()
    selenBrowser.close()
    wait()

    if fullYearRecord:
        windows.switchWindowByDict('driggsAgentList')
        wait()
        selenBrowser.find_element_by_xpath('//a[@href]').click()
        wait()
        windows.updateWindows()
        windows.addWindowToDict(len(windows.windows) - 1, 'agentPageOne')
        windows.switchWindowByDict('agentPageOne')
        buttons = selenBrowser.find_elements_by_xpath('//a[@href]')
        buttons[len(buttons) - 1].click()
        wait(3)
        windows.updateWindows()
        windows.addWindowToDict(len(windows.windows) - 1, 'agentPageTwo')
        windows.switchWindowByDict('agentPageTwo')
        wait(3)
        selenBrowser.find_element_by_name('beg_dt_p').send_keys(startDateEntry)
        wait()
        selenBrowser.find_element_by_name('end_dt_p').send_keys(endDateEntry)
        wait()
        selenBrowser.find_element_by_name('mta_yr_type_p').click()
        wait()
        selenBrowser.find_element_by_name("sub").click()
        wait(4)
    else:
        windows.switchWindowByDict('agentPageTwo')
        dateLinks = selenBrowser.find_elements_by_xpath('//a[@href]')
        lastEntry = selenBrowser.find_element_by_link_text(startDate + " - " + endDate)

        for i in range(len(dateLinks)):
            if dateLinks[i] == lastEntry:
                dateLinks[i].click()

    wait()
    agencyEntry = selenBrowser.find_element_by_name("title_comp_id_p1")
    wait()
    agencyEntry.click()
    wait()
    agencyEntry.click()
    wait(3)
    pasteData(agent, titleAgencies, selenBrowser)
    wait(3)
    selenBrowser.find_element_by_name("sub").click()
    wait()


def getNextDates(selenBrowser, startDate, endDate):
    dateLinks = selenBrowser.find_elements_by_xpath('//a[@href]')
    lastEntry = selenBrowser.find_element_by_link_text(startDate + " - " + endDate)

    for i in range(len(dateLinks)):
        if dateLinks[i] == lastEntry:
            dateLinks = dateLinks[:i]
            break

        dateLinks[i] = dateLinks[i].text

    return dateLinks


def getData(agent, selenBrowser):
    agent.reset_deal_count()
    NONE = []
    titleNamesHTML = []

    try:
        html = selenBrowser.page_source
        soup = BeautifulSoup(html, 'lxml')
    except:
        print(' No URL found! Try reselecting web page before copying data. \n')
        return

    # Store data on agent Deals as lists
    titleNamesHTML = soup.find_all('div', attrs={'class':'a78'})
    listingSideHTML = soup.find_all('div', attrs={'class':'a119'})
    MS1HTML = soup.find_all('div', attrs={'class':'a127'})
    buySideHTML = soup.find_all('div', attrs={'class':'a135'})
    MS2HTML = soup.find_all('div', attrs={'class':'a143'})
    doubleDipHTML = soup.find_all('div', attrs={'class':'a151'})
    MS3HTML = soup.find_all('div', attrs={'class':'a159'})
    NONE = str(soup.find_all('a', href = True))

    # Set count equal to the length of the list
    count = len(titleNamesHTML)

    if '<a href="mailto:info@mymta.com">info@mymta.com</a>' in NONE:
        agent.add_deal('none', '1', '1', '1', '1')
        count = 1
    elif count == 0:
        print(" We couldn't find any data, are you sure you are copying a MyMTA Market Share Report?")
        sys.exit(1)
    else:
        if count > 0:
            for i in range(count):
                currentTitleName = str(titleNamesHTML[i])
                currentTitleName = currentTitleName[17:-6]

                currentListingSideSTR = str(listingSideHTML[i])
                currentListingSideSTR = currentListingSideSTR[19:-6]

                currentMS1STR = str(MS1HTML[i])
                currentMS1STR = currentMS1STR[18:-6]

                currentBuySideSTR = str(buySideHTML[i])
                currentBuySideSTR = currentBuySideSTR[19:-6]

                currentMS2STR = str(MS2HTML[i])
                currentMS2STR = currentMS2STR[18:-6]

                currentDoubleDipSTR = str(doubleDipHTML[i])
                currentDoubleDipSTR = currentDoubleDipSTR[19:-6]

                currentMS3STR = str(MS3HTML[i])
                currentMS3STR = currentMS3STR[18:-6]

                currentListingSideSTR = currentListingSideSTR.replace(',' , '')
                currentBuySideSTR = currentBuySideSTR.replace(',' , '')
                currentDoubleDipSTR = currentDoubleDipSTR.replace(',' , '')

                currentListingSide = int(currentListingSideSTR)
                currentMS1 = int(currentMS1STR)
                currentBuySide = int(currentBuySideSTR)
                currentMS2 = int(currentMS2STR)
                currentDoubleDip = int(currentDoubleDipSTR)
                currentMS3 = int(currentMS3STR)

                currentMS1 += currentMS3
                currentMS1STR = str(currentMS1)

                currentMS2 += currentMS3
                currentMS2STR = str(currentMS2)

                if currentDoubleDip > 0 and currentListingSide == 0:

                    currentListingSide = currentDoubleDip
                    currentListingSideSTR = str(currentListingSide)

                if currentDoubleDip > 0 and currentBuySide == 0:

                    currentBuySide = currentDoubleDip
                    currentBuySideSTR = str(currentBuySide)

                agent.add_deal(currentTitleName[0:17].lower(), currentListingSideSTR.lower(), currentMS1STR.lower(), currentBuySideSTR.lower(), currentMS2STR.lower())
                time.sleep(0.01)

def pasteData(agent, titleAgencies, selenBrowser):
    MAX_NUM_DEALS = 30

    numDeals = agent.deal_count() if agent.deal_count() <= MAX_NUM_DEALS else MAX_NUM_DEALS
    for x in range(numDeals):

        matchFound = True
        arrowKeyCount = 0
        shortDuplicate = 0
        fullDuplicate = 0
        occurences = 0
        nameLength = 17

        for i in range(titleAgencies.agency_count()):

            if agent.title_name(x, 0, 5) in titleAgencies.short_agency(i):

                occurences += 1

        if occurences > 1:

            matchFound = False

            for i in range(titleAgencies.agency_count()):

                if agent.title_name(x, 0, 5) in titleAgencies.short_agency(i) and agent.title_name(x, 0, 4) in titleAgencies.short_agency(i, 0, 5):

                    shortDuplicate = i
                    break

            for i in range(10):

                for i in range(titleAgencies.agency_count()):

                    if agent.title_name(x) in titleAgencies.long_agency(i) and agent.title_name(x, 0, 5) in titleAgencies.long_agency(i, 0, 5):

                        fullDuplicate = i
                        matchFound = True
                        break

                if nameLength > 7 and matchFound == False:

                    nameLength -= 1
                    agent.update_title_name(x, agent.title_name(x, 0, nameLength))

        if occurences == 0 or matchFound == False:

            agent.update_title_name(x, 'othe')
            shortDuplicate = 0
            fullDuplicate = 0

        arrowKeyCount = shortDuplicate - fullDuplicate

        keyboard.write(agent.title_name(x, 0, 4), 0.05)
        wait()

        if (abs(arrowKeyCount) > 0):

            keyboard.press_and_release('down arrow')
            wait(0.3)

            for i in range(abs(arrowKeyCount)):

                keyboard.press_and_release('down arrow')
                wait(0.3)

            wait()
            keyboard.press_and_release('enter')
            wait()

        keyboard.press_and_release('tab')
        wait(0.3)
        keyboard.write(agent.listing_side(x), 0.05)
        wait(0.3)
        keyboard.press_and_release('tab')
        wait(0.3)
        keyboard.write(agent.ms1(x), 0.05)
        wait(0.3)
        keyboard.press_and_release('tab')
        wait(0.3)
        keyboard.write(agent.buy_side(x), 0.05)
        wait(0.3)
        keyboard.press_and_release('tab')
        wait(0.3)
        keyboard.write(agent.ms2(x), 0.05)
        wait(0.3)
        keyboard.press_and_release('tab')
        wait(0.3)


    if agent.deal_count() > MAX_NUM_DEALS:
        selenBrowser.find_element_by_name("sub").click()
        agent.remove_deals(MAX_NUM_DEALS)
        pasteData(agent, titleAgencies, selenBrowser)
