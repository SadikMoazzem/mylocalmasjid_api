from datetime import datetime, timedelta
import math
from pydantic import BaseModel

class IslamicDate(BaseModel):
    day: str
    date: int
    year: int
    month: str
    string: str

class HijriDate(BaseModel):
    @staticmethod
    def __gmod(n: int, m: int) -> int:
        return ((n % m) + m) % m
    
    @classmethod
    def __kuwaiticalendar(cls, date: datetime, adjust: int) -> list:
        today = date
        if adjust:
            adjust_mili = 1000 * 60 * 60 * 24 * adjust
            today_mili = today + timedelta(milliseconds=adjust_mili)
            today = today_mili
        
        day = today.day
        month = today.month
        year = today.year

        m = month
        y = year

        if m < 3:
            y -= 1
            m += 12
        
        a = math.floor(y / 100)
        b = 2 - a + math.floor(a / 4)
        if y < 1583:
            b = 0
        if y == 1582 and m > 10:
            b = -10
        if y == 1582 and m == 10 and day > 4:
            b = -10
        
        jd = math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + day + b - 1524

        b = 0
        if jd > 2299160:
            a = math.floor((jd - 1867216.25) / 36524.25)
            b = 1 + a - math.floor(a / 4)
        bb = jd + b + 1524
        cc = math.floor((bb - 122.1) / 365.25)
        dd = math.floor(365.25 * cc)
        ee = math.floor((bb - dd) / 30.6001)
        day = bb - dd - math.floor(30.6001 * ee)
        month = ee - 1
        if ee > 13:
            cc += 1
            month = ee - 13
        
        year = cc - 4716

        if adjust:
            wd = cls.__gmod(jd + 1 - adjust, 7) + 1
        else:
            wd = cls.__gmod(jd + 1, 7) + 1

        iyear = 10631 / 30
        epochastro = 1948084
        epochcivil = 1948085

        shift1 = 8.01 / 60

        z = jd - epochastro
        cyc = math.floor(z / 10631)
        z = z - 10631 * cyc
        j = math.floor((z - shift1) / iyear)
        iy = 30 * cyc + j
        z = z - math.floor(j * iyear + shift1)
        im = math.floor((z + 28.5001) / 29.5)
        if im == 13:
            im = 12
        id = z - math.floor(29.5001 * im - 29)

        myRes = [None] * 8

        myRes[0] = day  # calculated day (CE)
        myRes[1] = month - 1  # calculated month (CE)
        myRes[2] = year  # calculated year (CE)
        myRes[3] = jd - 1  # julian day number
        myRes[4] = wd - 1  # weekday number
        myRes[5] = id  # islamic date
        myRes[6] = im - 1  # islamic month
        myRes[7] = iy  # islamic year

        return myRes

    @classmethod
    def writeIslamicDate(cls, date: datetime = datetime.now(), adjustment: int = 0) -> IslamicDate:
        """
        Translates the Gregorian Date into the Hijri Date taking into account the adjustment
        :return:
        """
        wdNames = [
            "Ahad",
            "Ithnin",
            "Thulatha",
            "Arbaa",
            "Khams",
            "Jumuah",
            "Sabt"
        ]
        iMonthNames = [
            "Muharram",
            "Safar",
            "Rabi'ul Awwal",
            "Rabi'ul Akhir",
            "Jumadal Ula",
            "Jumadal Akhira",
            "Rajab",
            "Sha'ban",
            "Ramadan",
            "Shawwal",
            "Dhul Qa'ada",
            "Dhul Hijja"
        ]

        iDate = cls.__kuwaiticalendar(date, adjustment)
        outputIslamicDateString = f"{iDate[5]} {iMonthNames[iDate[6]]} {iDate[7]}"
        # wdNames[iDate[4]] + ", "
        res: IslamicDate = {
            'day': wdNames[iDate[4]],
            'date': iDate[5],
            'year': iDate[7],
            'month': iMonthNames[iDate[6]],
            'string': outputIslamicDateString
        }

        return res
