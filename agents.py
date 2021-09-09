class DriggsAgent:
 
    def __init__(self): 
        self.deals = []
        self.dealCount = 0
 
    def add_deal(self, titleName, listingSide, MS1, buySide, MS2): 
        self.new_deal = [titleName, listingSide, MS1, buySide, MS2]
        self.deals.append(self.new_deal)
        self.dealCount += 1

    def reset_deal_count(self):
        self.clear_deals()
 
    def update_title_name(self, x, name):
        self.deals[x][0] = name

    def remove_deals(self, dealIndex):
        self.deals = self.deals[dealIndex:]

    def title_name(self, dealIndex, start = None, end = None):
        current_title_name = self.deals[dealIndex][0]
        if end != None:
            if end > len(current_title_name) - 1:
                end -= 1
        return current_title_name[start:end]
 
    def deal_count(self):
        return len(self.deals)

    def listing_side(self, x):
        return self.deals[x][1]
 
    def ms1(self, x):
        return self.deals[x][2]
 
    def buy_side(self, x):
        return self.deals[x][3]
 
    def ms2(self, x):
        return self.deals[x][4]
 
    def clear_deals(self):
        self.deals.clear()
        
