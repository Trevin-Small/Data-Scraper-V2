class TitleAgencies:
 
    def __init__(self):
        self.titleAgenciesLong = []
        self.titleAgenciesShort = []

    def get_title_agencies(self):
        return self.titleAgenciesShort
 
    def add_long_agency(self, agency):
        self.titleAgenciesLong.append(agency)
 
    def add_short_agency(self, agency):
        self.titleAgenciesShort.append(agency)
 
    def agency_count(self):
        return len(self.titleAgenciesLong)
 
    def short_agency(self, index, start = None, end = None):
        return self.titleAgenciesShort[index][start:end]
 
    def long_agency(self, index, start = None, end = None):
        return self.titleAgenciesLong[index][start:end]
 