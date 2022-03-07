import users, title_agencies, agents, browser_windows, functions
from selenium import webdriver

def main():
    user = users.UserCredentials()
    titleAgencies = title_agencies.TitleAgencies()
    agent = agents.DriggsAgent()
    selenBrowser = webdriver.Chrome('./chromedriver')
    windows = browser_windows.BrowserWindows(selenBrowser)

    functions.setDates("01/31/2021", "01/31/2022")
    functions.getAgencies(user, titleAgencies, windows, selenBrowser)

    NUMBER_OF_NAMES = 200
    namesCompleted = 0
    namesSkipped = 0

    for i in range(NUMBER_OF_NAMES):
        dataEntered = functions.enterData(agent, titleAgencies, windows, selenBrowser)
        if dataEntered:
            namesCompleted += 1
        else:
            namesSkipped += 1

        print("Names Completed: " + namesCompleted + ", Names Skipped: " + namesSkipped)

    print("Program Complete. Names Completed: " + str(namesCompleted))

main()
