"""
for delineate GUI and Controller

onclick-methods
"""

from FlightTime import FlightTime
from Report import Report


class Wrapper:
    def __init__(self, filename, period):
        self.filename = filename
        self.period = period
        self.rpt = Report(filename, period)
        self.ft = FlightTime()

    # тут - що зробити під час натискання 'calculate'
    def onclick_calculate(self):
        self.ft.collect_topic(self.rpt.Name_Sheets, self.rpt.workb, self.period, 'single_engine', 7, 9, 10)
        self.ft.collect_topic(self.rpt.Name_Sheets, self.rpt.workb, self.period, 'multi_engine', 8, 9, 10)
        self.ft.collect_topic(self.rpt.Name_Sheets, self.rpt.workb, self.period, 'multi_pilot', 9, 8, 10)

    #    self.ft.collect_single_engine(self.rpt.Name_Sheets, self.rpt.workb, self.period, 'single_engine', '56')
    #    self.ft.collect_multi_engine(self.rpt.Name_Sheets, self.rpt.workb, self.period)
    #   self.ft.collect_multi_pilot(self.rpt.Name_Sheets, self.rpt.workb, self.period)
    #   self.ft.collect_landings(self.rpt.Name_Sheets, self.rpt.workb, self.period)
    #    self.ft.collect_night_cond(self.rpt.Name_Sheets, self.rpt.workb, self.period)
     #   self.ft.collect_pic(self.rpt.Name_Sheets, self.rpt.workb, self.period)
      #  self.ft.collect_co_pilot(self.rpt.Name_Sheets, self.rpt.workb, self.period)
       # self.ft.collect_dual(self.rpt.Name_Sheets, self.rpt.workb, self.period)
        #self.ft.collect_instructor(self.rpt.Name_Sheets, self.rpt.workb, self.period)

        self.ft.calc_total_fltime_month()
    #    self.ft.calc_fltime_period(6, 'total_6mo')
     #   self.ft.calc_fltime_period(12, 'total_year')
      #  self.ft.calc_land_period(6, 'total_6mo')
       # self.ft.calc_land_period(12, 'total_year')

        self.rpt.create_workspace_page1(self.ft.main_data)
        self.rpt.create_workspace_page2(self.ft.main_data)
        self.rpt.set_print_option()
        self.rpt.save_summaries()
