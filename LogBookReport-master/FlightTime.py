"""
Структура даних, для зберігання обробленої інформації
"""

from datetime import datetime
from datetime import time


class FlightTime:
    # data structure for collect and sum time by month
    MONTHS_DIGITS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    main_data = {}  # main data structure

    # create main data structure
    def __init__(self):
        self.main_data = {ind: {'month': mon,
                                'flight_time': {'single_engine': {'hour': [], 'min': [], 'sum': ''},
                                                'multi_engine': {'hour': [], 'min': [], 'sum': ''},
                                                'multi_pilot': {'hour': [], 'min': [], 'sum': ''},
                                                'jet': {'hour': [], 'min': [], 'sum': ''},
                                                'turboprop': {'hour': [], 'min': [], 'sum': ''},
                                                'total_flight_time': {'hour': [], 'min': [], 'sum': ''},
                                                'night_cond': {'hour': [], 'min': [], 'sum': ''},
                                                'ifr_cond': {'hour': [], 'min': [], 'sum': ''},
                                                'PIC': {'hour': [], 'min': [], 'sum': ''},
                                                'Co-Pilot': {'hour': [], 'min': [], 'sum': ''},
                                                'dual': {'hour': [], 'min': [], 'sum': ''},
                                                'INSTRUCTOR': {'hour': [], 'min': [], 'sum': ''},
                                                'SIMULATOR': {'hour': [], 'min': [], 'sum': ''}
                                                },
                                'landings': {'day': [],
                                             'night': [],
                                             'total': 0},
                                'flight_by_plane': {}
                                } for ind, mon in zip(self.MONTHS_DIGITS, self.MONTHS)}
        self.main_data['total_6mo'] = {'single_engine': '',
                                       'multi_engine': '',
                                       'multi_pilot': '',
                                       'jet': '',
                                       'turboprop': '',
                                       'total_flight_time': '',
                                       'day_land': 0,
                                       'night_land': 0,
                                       'total_land': 0,
                                       'night_cond': '',
                                       'ifr_cond': '',
                                       'PIC': '',
                                       'Co-Pilot': '',
                                       'dual': '',
                                       'INSTRUCTOR': ''}
        self.main_data['total_year'] = {'single_engine': '',
                                        'multi_engine': '',
                                        'multi_pilot': '',
                                        'jet': '',
                                        'turboprop': '',
                                        'total_flight_time': '',
                                        'day_land': 0,
                                        'night_land': 0,
                                        'total_land': 0,
                                        'night_cond': '',
                                        'ifr_cond': '',
                                        'PIC': '',
                                        'Co-Pilot': '',
                                        'dual': '',
                                        'INSTRUCTOR': ''}

    # co-methods
    # if value is link to another cell - evaluate link and get final cell.value
    def _isformula(self, value):    # cel is value of cell
        if isinstance(value, str) and value[0] == '=':
            if '+' in value or '-' in value or '*' in value or '/' in value:
                return True
        else:
            return False

    def _islink(self, value):
        if isinstance(value, str) and value[0] == '=':
            if ('+' not in value) or ('-' not in value) or ('*' not in value) or ('/' not in value):
                return True
        else:
            return False

    def _isdata(self, value):
        if isinstance(value, datetime):
            return True
        elif isinstance(value, int):
            return True
        else:
            return False

    def get_data(self, cel, workbook, sheet):   # cel is string as adress of cell 'A11'
        while self._islink(workbook[sheet][cel].value):
            cel = workbook[sheet][cel].value[1:]
        return workbook[sheet][cel].value

    # methods that filling all summary values
    # calculate flight_time by months - using by another function
    def month_sum(self, current_month, topic):
        minutes = sum(self.main_data[current_month]['flight_time'][topic]['min'])
        calc_min = minutes % 60
        calc_hour = minutes // 60
        calc_hour = calc_hour + sum(self.main_data[current_month]['flight_time'][topic]['hour'])
        month_result = str(calc_hour) + ':' + str('%02d' % calc_min)
        return month_result

    # collect all single_engine values from sheets to main data structure - main_data
    # single_engine. data column = 10, condition if col=7 is not empty and col=9 is empty
    # multi_engine. data column = 10, condition if col=8 is not empty and col=9 is empty
    # multi_pilot. data column = 10, condition if col=9 is not empty
    # name = 'single_engine'
    #        'multi_engine'
    #        'multi_pilot'

    def collect_topic(self, name_sheets, workbook, yr, topic, cond_column_1, cond_column_2, data_column, end='0'):
        end_sheet = end                                # worksheet for stop calculating
        year = yr[2:]                                  # default year for calculating
        for sheet in name_sheets:
            # if title is not report and not later 2019 (reverse counting)
            if sheet.isdigit() and int(sheet) > int(end_sheet):
                # starting work in rows
                for row in workbook[sheet].iter_rows(min_row=5, max_row=17):  # next row in worksheet, range[5:17]
                    col_0 = row[0].value               # date in row
                    if isinstance(col_0, datetime):    # try to find date type
                        if col_0.strftime('%y') != year:  # collect only 1 year, if trying collect another year - break
                            continue
                        month = col_0.strftime('%m')   # '07' - month
                        if row[cond_column_1].value and not row[cond_column_2].value:
                            data = str(self.get_data(row[data_column].coordinate, workbook, sheet))
                            h, m, s = data.split(':')
                            self.main_data[month]['flight_time'][topic]['hour'].append(int(h))
                            self.main_data[month]['flight_time'][topic]['min'].append(int(m))
            # stop counting, when out of old date
            elif sheet < end_sheet:
                break
        # count total time for month
        for month in self.MONTHS_DIGITS:
            self.main_data[month]['flight_time']['total_flight_time']['hour'].extend(
                self.main_data[month]['flight_time'][topic]['hour'])
            self.main_data[month]['flight_time']['total_flight_time']['min'].extend(
                self.main_data[month]['flight_time'][topic]['min'])
            self.main_data[month]['flight_time'][topic]['sum'] = self.month_sum(month, topic)










    def collect_single_engine(self, name_sheets, workbook, yr, topic, end='0'):
        end_sheet = end                                # worksheet for stop calculating
        year = yr[2:]                                  # default year for calculating
        for sheet in name_sheets:
            # if title is not report and not later 2019 (reverse counting)
            if sheet.isdigit() and int(sheet) > int(end_sheet):

                # starting work in rows
                for row in workbook[sheet].iter_rows(min_row=5, max_row=17):  # next row in worksheet, range[5:17]
                    col_0 = row[0].value               # date in row
                    if isinstance(col_0, datetime):    # try to find date type
                        if col_0.strftime('%y') != year:  # collect only 1 year, if trying collect another year - break
                            continue

                        month = col_0.strftime('%m')   # '07' - month
                        if row[7].value and not row[9].value:
                            data = str(self.get_data(row[10].coordinate, workbook, sheet))
                            h, m, s = data.split(':')
                            self.main_data[month]['flight_time'][topic]['hour'].append(int(h))
                            self.main_data[month]['flight_time'][topic]['min'].append(int(m))

            # stop counting, when out of old date
            elif sheet < end_sheet:
                break

        # count total time for month
        for month in self.MONTHS_DIGITS:
            self.main_data[month]['flight_time']['total_flight_time']['hour'].extend(
                self.main_data[month]['flight_time'][topic]['hour'])
            self.main_data[month]['flight_time']['total_flight_time']['min'].extend(
                self.main_data[month]['flight_time'][topic]['min'])
            self.main_data[month]['flight_time'][topic]['sum'] = self.month_sum(month, topic)

    # collect all multi_engine values from sheets to main data structure - main_data
    def collect_multi_engine(self, name_sheets, workbook, yr, end='56'):
        end_sheet = end  # worksheet for stop calculating
        year = yr[2:]  # default year for calculating
        for sheet in name_sheets:  # list of sheet names
            if sheet.isdigit() and sheet >= end_sheet:
                for row in workbook[sheet].iter_rows(min_row=4):  # next row in worksheet, row[0] - date, row[10] - time
                    col_0 = row[0].value
                    if isinstance(col_0, datetime):
                        if col_0.strftime('%y') != year:
                            continue
                        month = col_0.strftime('%m')  # '07' - month
                        if row[8].value and not row[9].value:
                            data = str(row[10].value)  # take col'J', "time of flight'
                            h, m, s = data.split(':')
                            self.main_data[month]['flight_time']['multi_engine']['hour'].append(int(h))
                            self.main_data[month]['flight_time']['multi_engine']['min'].append(int(m))
            elif sheet < end_sheet:  # stop counting, when date of sheet too old
                break
        for month in self.MONTHS_DIGITS:  # count total time for month
            self.main_data[month]['flight_time']['total_flight_time']['hour'].extend(
                self.main_data[month]['flight_time']['multi_engine']['hour'])
            self.main_data[month]['flight_time']['total_flight_time']['min'].extend(
                self.main_data[month]['flight_time']['multi_engine']['min'])
            self.main_data[month]['flight_time']['multi_engine']['sum'] = self.month_sum(month, 'multi_engine')

    # collect all multi_pilot values from sheets to main data structure - main_data
    def collect_multi_pilot(self, name_sheets, workbook, yr, end='56'):
        end_sheet = end  # worksheet for stop calculating
        year = yr[2:]  # default year for calculating
        for sheet in name_sheets:  # list of sheet names
            if sheet.isdigit() and sheet >= end_sheet:
                for row in workbook[sheet].iter_rows(min_row=4):  # next row in worksheet, row[0] - date, row[10] - time
                    col_0 = row[0].value
                    if isinstance(col_0, datetime):
                        if col_0.strftime('%y') != year:
                            continue
                        month = col_0.strftime('%m')  # '07' - month
                        if row[9].value:
                            data = str(row[10].value)  # take col'J', "time of flight'
                            h, m, s = data.split(':')
                            self.main_data[month]['flight_time']['multi_pilot']['hour'].append(int(h))
                            self.main_data[month]['flight_time']['multi_pilot']['min'].append(int(m))
            elif sheet < end_sheet:
                break
        for month in self.MONTHS_DIGITS:  # count total time for month
            self.main_data[month]['flight_time']['total_flight_time']['hour'].extend(
                self.main_data[month]['flight_time']['multi_pilot']['hour'])
            self.main_data[month]['flight_time']['total_flight_time']['min'].extend(
                self.main_data[month]['flight_time']['multi_pilot']['min'])
            # count sum for 'multi_pilot'
            self.main_data[month]['flight_time']['multi_pilot']['sum'] = self.month_sum(month, 'multi_pilot')

    # calculate total flight time by month
    def calc_total_fltime_month(self):
        for month in self.MONTHS_DIGITS:
            self.main_data[month]['flight_time']['total_flight_time']['sum'] = self.month_sum(month,
                                                                                              'total_flight_time')

    # collect all landings values from sheets to main data structure - main_data
    def collect_landings(self, name_sheets, workbook, yr, end='56'):
        end_sheet = end  # worksheet for stop calculating
        year = yr[2:]  # default year for calculating
        for sheet in name_sheets:  # list of sheet names
            if sheet.isdigit() and sheet >= end_sheet:
                for row in workbook[sheet].iter_rows(min_row=4):  # next row in worksheet, row[0] - date, row[10] - time
                    col_0 = row[0].value
                    if isinstance(col_0, datetime):
                        if col_0.strftime('%y') != year:
                            continue
                        day_landing = row[12].value  # take col'L', "day landings'
                        night_landing = row[13].value  # take col'M', "night landings'
                        month = col_0.strftime('%m')  # '07' - month
                        self.main_data[month]['landings']['day'].append(day_landing)
                        self.main_data[month]['landings']['night'].append(night_landing)
            elif sheet < end_sheet:
                break
        for month in self.MONTHS_DIGITS:  # count total landings by month
            dland = self.main_data[month]['landings']['day']
            dayl = [x if x else 0 for x in dland]  # when None - change to 0
            nland = self.main_data[month]['landings']['night']
            nightl = [x if x else 0 for x in nland]  # when None - change to 0
            self.main_data[month]['landings']['total'] = sum(dayl) + sum(nightl)

    # collect night condition time from sheets to main data structure - main_data
    def collect_night_cond(self, name_sheets, workbook, yr, end='56'):
        end_sheet = end  # worksheet for stop calculating
        year = yr[2:]  # default year for calculating
        for sheet in name_sheets:  # list of sheet names
            if sheet.isdigit() and sheet >= end_sheet:
                for row in workbook[sheet].iter_rows(min_row=4):
                    col_0 = row[0].value  # date in row --> cell row-any, col-0
                    if isinstance(col_0, datetime) and row[14].value:  # якщо перша колонка-дата і в 14й колонці НЕпусто
                        if col_0.strftime('%y') != year:  # if date of data is not current year
                            continue
                        month = col_0.strftime('%m')  # '07' - month
                        data = row[14].value  # night_time condition
                        if data[0] == '=':  # its reference to another cell
                            data = workbook[sheet][data[1:]].value
                        data = str(data)
                        h, m, s = data.split(':')
                        self.main_data[month]['flight_time']['night_cond']['hour'].append(int(h))
                        self.main_data[month]['flight_time']['night_cond']['min'].append(int(m))
        # put daily night_condition_time to total_month night condition time
        for month in self.MONTHS_DIGITS:
            self.main_data[month]['flight_time']['night_cond']['sum'] = self.month_sum(month, 'night_cond')

    # collect pilot-in-command time from sheets to main data structure - main_data
    def collect_pic(self, name_sheets, workbook, yr, end='56'):
        end_sheet = end  # worksheet for stop calculating
        year = yr[2:]  # default year for calculating
        for sheet in name_sheets:  # list of sheet names
            if sheet.isdigit() and sheet >= end_sheet:
                for row in workbook[sheet].iter_rows(min_row=4):
                    col_0 = row[0].value  # date in row --> cell row-any, col-0
                    if isinstance(col_0, datetime) and row[16].value:  # якщо перша колонка-дата і в 14й колонці НЕпусто
                        if col_0.strftime('%y') != year:  # if date of data is not current year
                            continue
                        month = col_0.strftime('%m')  # '07' - month
                        data = row[16].value  # night_time condition
                        if data[0] == '=':  # its reference to another cell
                            data = workbook[sheet][data[1:]].value
                        data = str(data)
                        h, m, s = data.split(':')
                        self.main_data[month]['flight_time']['PIC']['hour'].append(int(h))
                        self.main_data[month]['flight_time']['PIC']['min'].append(int(m))
        # put daily night_condition_time to total_month night condition time
        for month in self.MONTHS_DIGITS:
            self.main_data[month]['flight_time']['PIC']['sum'] = self.month_sum(month, 'PIC')

    # collect co-pilot time from sheets to main data structure - main_data
    def collect_co_pilot(self, name_sheets, workbook, yr, end='56'):
        end_sheet = end  # worksheet for stop calculating
        year = yr[2:]  # default year for calculating
        for sheet in name_sheets:  # list of sheet names
            if sheet.isdigit() and sheet >= end_sheet:
                for row in workbook[sheet].iter_rows(min_row=4):
                    col_0 = row[0].value  # date in row --> cell row-any, col-0
                    if isinstance(col_0, datetime) and row[17].value:  # якщо перша колонка-дата і в 14й колонці НЕпусто
                        if col_0.strftime('%y') != year:  # if date of data is not current year
                            continue
                        month = col_0.strftime('%m')  # '07' - month
                        data = row[17].value  # night_time condition
                        if data[0] == '=':
                            data = workbook[sheet][data[1:]].value
                        data = str(data)
                        h, m, s = data.split(':')
                        self.main_data[month]['flight_time']['Co-Pilot']['hour'].append(int(h))
                        self.main_data[month]['flight_time']['Co-Pilot']['min'].append(int(m))
        # put daily night_condition_time to total_month night condition time
        for month in self.MONTHS_DIGITS:
            self.main_data[month]['flight_time']['Co-Pilot']['sum'] = self.month_sum(month, 'Co-Pilot')

    # collect dual time from sheets to main data structure - main_data
    def collect_dual(self, name_sheets, workbook, yr, end='56'):
        end_sheet = end  # worksheet for stop calculating
        year = yr[2:]  # default year for calculating
        for sheet in name_sheets:  # list of sheet names
            if sheet.isdigit() and sheet >= end_sheet:
                for row in workbook[sheet].iter_rows(min_row=4):
                    col_0 = row[0].value  # date in row --> cell row-any, col-0
                    if isinstance(col_0, datetime) and row[18].value:  # якщо перша колонка-дата і в 14й колонці НЕпусто
                        if col_0.strftime('%y') != year:  # if date of data is not current year
                            continue
                        month = col_0.strftime('%m')  # '07' - month
                        data = row[18].value  # night_time condition
                        if data[0] == '=':
                            data = workbook[sheet][data[1:]].value
                        data = str(data)
                        h, m, s = data.split(':')
                        self.main_data[month]['flight_time']['dual']['hour'].append(int(h))
                        self.main_data[month]['flight_time']['dual']['min'].append(int(m))
        # put daily night_condition_time to total_month night condition time
        for month in self.MONTHS_DIGITS:
            self.main_data[month]['flight_time']['dual']['sum'] = self.month_sum(month, 'dual')

    # collect dual time from sheets to main data structure - main_data
    def collect_instructor(self, name_sheets, workbook, yr, end='56'):
        end_sheet = end  # worksheet for stop calculating
        year = yr[2:]  # default year for calculating
        for sheet in name_sheets:  # list of sheet names
            if sheet.isdigit() and sheet >= end_sheet:  # if title not report and not later 2019
                for row in workbook[sheet].iter_rows(min_row=4):
                    col_0 = row[0].value  # date in row --> cell row-any, col-0
                    if isinstance(col_0, datetime) and row[19].value:  # якщо перша колонка-дата і в 14й колонці НЕпусто
                        if col_0.strftime('%y') != year:  # if date of data is not current year
                            continue
                        month = col_0.strftime('%m')  # '07' - month
                        data = row[19].value  # night_time condition
                        if data[0] == '=':
                            data = workbook[sheet][data[1:]].value
                        if not isinstance(data, time) and data[0] == '=':
                            data = workbook[sheet][data[1:]].value
                        data = str(data)
                        h, m, s = data.split(':')
                        self.main_data[month]['flight_time']['INSTRUCTOR']['hour'].append(int(h))
                        self.main_data[month]['flight_time']['INSTRUCTOR']['min'].append(int(m))
        for month in self.MONTHS_DIGITS:  # put daily night_condition_time to total_month night condition time
            self.main_data[month]['flight_time']['INSTRUCTOR']['sum'] = self.month_sum(month, 'INSTRUCTOR')

    # calculate months_time by start-stop period - use to get 6 months/year total flight time
    def total_period(self, start, stop, topic):
        minutes = []
        hours = []
        for month in self.MONTHS_DIGITS[start:stop]:
            h, m = self.main_data[month]['flight_time'][topic]['sum'].split(':')
            minutes.append(int(m))
            hours.append(int(h))
        minutes_total = sum(minutes)
        calc_m = minutes_total % 60
        calc_h = minutes_total // 60
        calc_h = calc_h + sum(hours)
        period = str(calc_h) + ':' + str('%02d' % calc_m)
        return period

    # calculate flight time for 6/12 months period
    def calc_fltime_period(self, end_month, period):
        list_topics = ['single_engine', 'multi_engine', 'multi_pilot', 'total_flight_time',
                       'night_cond', 'PIC', 'Co-Pilot', 'dual', 'INSTRUCTOR']
        for topic in list_topics:
            self.main_data[period][topic] = self.total_period(0, end_month, topic)

    # calculate landings for 6/12 months period
    def calc_land_period(self, end_month, topic):
        day = 0
        night = 0
        tot = 0
        for month in self.MONTHS_DIGITS[0:end_month]:
            dland = self.main_data[month]['landings']['day']
            dayland = [x if x else 0 for x in dland]
            day += sum(dayland)
            nland = self.main_data[month]['landings']['night']
            nightland = [x if x else 0 for x in nland]
            night += sum(nightland)
            tot += self.main_data[month]['landings']['total']
        self.main_data[topic]['day_land'] = day
        self.main_data[topic]['night_land'] = night
        self.main_data[topic]['total_land'] = tot
