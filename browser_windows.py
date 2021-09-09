class BrowserWindows:

    browser = None
    windows = []
    windowDict = {
        'driggsAgentList': None,
        'mtaSearch': None,
        'mtaData': None,
        'agentPageOne': None,
        'agentPageTwo': None
    }

    def __init__(cls, _browser):
        cls.browser = _browser

    def updateWindows(cls):
        cls.windows = cls.browser.window_handles

    def switchWindows(cls, numWindow):
        cls.updateWindows()
        cls.browser.switch_to.window(cls.windows[numWindow])

    def switchWindowByDict(cls, windowName):
        cls.browser.switch_to.window(cls.windowDict[windowName])

    def addWindowToDict(cls, windowNumber, windowName):
        cls.updateWindows()
        cls.windowDict[windowName] = cls.windows[windowNumber]
