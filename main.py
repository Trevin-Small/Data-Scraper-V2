import users, title_agencies, agents, browser_windows, functions
from selenium import webdriver

def main():
    user = users.UserCredentials()
    titleAgencies = title_agencies.TitleAgencies()
    agent = agents.DriggsAgent()
    selenBrowser = webdriver.Chrome('./chromedriver')
    windows = browser_windows.BrowserWindows(selenBrowser)

    NUMBER_OF_NAMES = 50
    functions.getAgencies(user, titleAgencies, windows, selenBrowser)
    nameCountAdjusted = NUMBER_OF_NAMES
    for nameNumber in range(NUMBER_OF_NAMES):
        dataEntered = functions.enterData(agent, titleAgencies, windows, selenBrowser)
        if dataEntered:
            print("Name Completed: #" + str(nameNumber +1))
        else:
            print("Name Skipped: #" + str(nameNumber + 1))
            nameCountAdjusted -= 1
    print("Program Complete. Names Completed: " + str(nameCountAdjusted))

main()
