# The MIT License (MIT)
# Copyright (c) 2016 Alireza Aghamohammadi

from __future__ import division


def div(a, b):
    """Helper function for division

    :param a: first parameter
    :type a: int
    :param b: second parameter
    :type b: int
    :return: integer division result
    :rtype: int
    """
    return int(a / b)


def mod(a, b):
    """Helper function for modulo

    :param a: first parameter
    :type a: int
    :param b: second parameter
    :type b: int
    :return: modulo result
    :rtype: int
    """
    return a - div(a, b) * b


class Jalaali:
    @staticmethod
    def to_jalaali(gy, gm, gd):
        """Convert a Gregorian date to Jalaali

        :param gy: Gregorian Year
        :type gy: int
        :param gm: Gregorian Month
        :type gm: int
        :param gd: Gregorian Day
        :type gd: int
        :return: the converted Jalaali date
        :rtype: dict
        """
        return Jalaali.d2j(Jalaali.g2d(gy, gm, gd))

    @staticmethod
    def to_gregorian(jy, jm, jd):
        """Convert a Jalaali date to Gregorian

        :param jy: Jalaali Year
        :type jy: int
        :param jm: Jalaali Moth
        :type jm: int
        :param jd: Jalaali Day
        :type jd: int
        :return: the converted Gregorian date
        :rtype: dict
        """

        return Jalaali.d2g(Jalaali.j2d(jy, jm, jd))

    @staticmethod
    def is_valid_jalaali_date(jy, jm, jd):
        """Checks whether a Jalaali date is valid or not.

        :param jy: Jalaali Year
        :type jy: int
        :param jm: Jalaali Month
        :type jm: int
        :param jd: Jalaali Day
        :type jd: int
        :return: is date valid?
        :rtype: bool
        """

        year_is_valid = (-61 <= jy <= 3177)
        month_is_valid = (1 <= jm <= 12)
        day_is_valid = (1 <= jd <= Jalaali.jalaali_month_length(jy, jm))

        return year_is_valid and month_is_valid and day_is_valid

    @staticmethod
    def is_leap_jalaali_year(jy):
        """Checks whether this is a leap year or not.

        :param jy: Jalaali Year
        :type jy: int
        :return: is leap year?
        :rtype: bool
        """
        return Jalaali.jal_cal(jy)['leap'] == 0

    @staticmethod
    def jalaali_month_length(jy, jm):
        """Number of days in a given month in a Jalaali year.

        :param jy: Jalaali Year
        :type jy: int
        :param jm: Jalaali Month
        :type jm: int
        :return: number of days in month
        :rtype: int
        """
        if jm <= 6:
            return 31
        if jm <= 11:
            return 30
        if Jalaali.is_leap_jalaali_year(jy):
            return 30
        return 29

    @staticmethod
    def jal_cal(jy):
        """This function determines if the Jalaali (persian) year is
        leap(366-day long) or is the common year (365-days), and
        finds the day in March (Gregorian calendar) of the first
        day of the Jalaali year (jy).

        :param jy: Jalaali Year (-61 to 3177).
        :type jy: int
        :return:
            leap: number of years since the last leap year(0 to 4)
            gy: Gregorian year of the beginning of Jalaali year
            march: the March day of farvardin the 1st (1st day of jy)
        :rtype: dict
        """
        breaks = [-61, 9, 38, 199, 426, 686, 756, 818, 1111, 1181, 1210, 1635, 2060, 2097, 2192, 2262, 2324,
                  2394, 2456,
                  3178]
        b1 = len(breaks)
        gy = jy + 621
        leap_j = -14
        jp = breaks[0]
        jump = None
        if jy < jp or jy >= breaks[b1 - 1]:
            raise Exception('Invalid Jalaali year ' + str(jy))
        # Find the limiting years for the Jalaali year jy.

        for i in range(1, b1):
            jm = breaks[i]
            jump = jm - jp
            if jy < jm:
                break
            leap_j = leap_j + div(jump, 33) * 8 + div(mod(jump, 33), 4)
            jp = jm
        n = jy - jp

        # Find the number of leap years from AD 621 to the beginning of the current
        # Jalaali year in the persian calendar
        leap_j = leap_j + div(n, 33) * 8 + div(mod(n, 33) + 3, 4)
        if mod(jump, 33) == 4 and jump - n == 4:
            leap_j += 1

        # And the same in the Gregorian calendar (until the year gy)
        leap_g = div(gy, 4) - div((div(gy, 100) + 1) * 3, 4) - 150

        # Determine the Gregorian date of farvardin the 1st
        march = 20 + leap_j - leap_g

        # Find how many years have passed since the last year
        if jump - n < 6:
            n = n - jump + div(jump + 4, 33) * 33
        leap = mod(mod(n + 1, 33) - 1, 4)
        if leap == -1:
            leap = 4
        return {'leap': leap, 'gy': gy, 'march': march}

    @staticmethod
    def j2d(jy, jm, jd):
        """Converts a date of the Jalaali calendar to the julian day number.

        :param jy: Jalaali Year (1 to 3100)
        :type jy: int
        :param jm: Jalaali Month (1 to 12)
        :type jm: int
        :param jd: Jalaali Day (1 to 29/31)
        :type jd: int
        :return: Julian Day number
        :rtype: int
        """
        r = Jalaali.jal_cal(jy)
        return Jalaali.g2d(r['gy'], 3, r['march']) + (jm - 1) * 31 - div(jm, 7) * (jm - 7) + jd - 1

    @staticmethod
    def d2j(jdn):
        """Converts the Julian day number to a date in the jalaali calendar.

        :param jdn: Julian day number
        :type jdn: int
        :return: dictionary containing jy, jm, jd
        :rtype: dict
        """
        gy = Jalaali.d2g(jdn)['gy']  # calculate gregorian year (gy)
        jy = gy - 621
        r = Jalaali.jal_cal(jy)
        jdn1f = Jalaali.g2d(gy, 3, r['march'])
        # find number of days that passed since 1 farvardin
        k = jdn - jdn1f
        if k >= 0:
            if k <= 185:
                # the first 6 months
                jm = div(k, 31) + 1
                jd = mod(k, 31) + 1
                return {'jy': jy, 'jm': jm, 'jd': jd}
            else:
                # the remaining months.
                k -= 186
        else:
            # previous jalaali year
            jy -= 1
            k += 179
            k = k + 1 if r['leap'] == 1 else k
        jm = 7 + div(k, 30)
        jd = mod(k, 30) + 1
        return {'jy': jy, 'jm': jm, 'jd': jd}

    @staticmethod
    def g2d(gy, gm, gd):
        """Calculates the Julian Day number from Gregorian or Julian
        calendar dates. This integer number corresponds to the noon of
        the date(i.e.12 hours of Universal Time).
        The procedure was tested to be good since 1 March, -100100 (of both
        calendars) up to few million years into the future

        :param gy: Gregorian Year
        :type gy: int
        :param gm: Gregorian Month (1 to 12)
        :type gm: int
        :param gd: Gregorian Day (1 to 28/29/30/31)
        :type gd: int
        :return: Julian Day Number
        :rtype: int
        """
        d = div((gy + div(gm - 8, 6) + 100100) * 1461, 4) + div(153 * mod(gm + 9, 12) + 2, 5) + gd - 34840408
        d = d - div(div(gy + 100100 + div(gm - 8, 6), 100) * 3, 4) + 752
        return d

    @staticmethod
    def d2g(jdn):
        """Calculates Gregorian and Julian calendar dates from the Julian day number
        (jdn) for the period since jdn=-34839655 (i.e. the year -100100 of both calendars)
        to some millions years ahead of the present.

        :param jdn: Julian Day Number
        :type jdn: int
        :return: dictionary containing gy, gm, gd
        :rtype: dict
        """
        j = 4 * jdn + 139361631 + div(div(4 * jdn + 183187720, 146097) * 3, 4) * 4 - 3908
        i = div(mod(j, 1461), 4) * 5 + 308
        gd = div(mod(i, 153), 5) + 1
        gm = mod(div(i, 153), 12) + 1
        gy = div(j, 1461) - 100100 + div(8 - gm, 6)
        return {'gy': gy, 'gm': gm, 'gd': gd}
