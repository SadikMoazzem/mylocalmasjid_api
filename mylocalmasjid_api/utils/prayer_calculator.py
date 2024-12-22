# -*- coding: utf-8 -*-
from math import pi, atan, sqrt, tan, floor
from datetime import time, datetime
from pyIslam.hijri import HijriDate
from pyIslam.baselib import dcos, dsin, equation_of_time, gregorian_to_julian

class FixedTime:
    """
    A class to represent a fixed prayer time in minutes for all year and during Ramadan.

    Attributes:
        _all_year_time (int): Fixed time for all year in minutes.
        _ramadan_time (int): Fixed time for Ramadan in minutes.
    """

    def __init__(self, all_year_time_min, ramadan_time_min):
        self._all_year_time = all_year_time_min
        self._ramadan_time = ramadan_time_min

    @property
    def ramadan_time_hr(self):
        """Returns the Ramadan time in hours."""
        return self._ramadan_time / 60.0

    @property
    def all_year_time_hr(self):
        """Returns the all-year time in hours."""
        return self._all_year_time / 60.0


class MethodInfo:
    """
    A class to hold information about a prayer calculation method.

    Attributes:
        _id (int): Identifier for the method.
        _organizations (tuple): Organizations that endorse this method.
        _fajr_angle (float): Angle for Fajr calculation.
        _ishaa_angle (float): Angle for Ishaa calculation.
        _applicability (tuple): Applicability of the method, e.g., regions it is valid for.
    """

    def __init__(self, method_id, organizations, fajr_angle, ishaa_angle, applicability=()):
        self._id = method_id
        self._organizations = organizations if isinstance(organizations, (list, tuple)) else (organizations,)
        self._fajr_angle = fajr_angle
        self._ishaa_angle = ishaa_angle
        self._applicability = applicability if isinstance(applicability, (list, tuple)) else (applicability,)

    @property
    def id(self):
        """Returns the identifier for the method."""
        return self._id

    @property
    def organizations(self):
        """Returns the organizations that endorse this method."""
        return self._organizations

    @property
    def fajr_angle(self):
        """Returns the Fajr angle for calculation."""
        return self._fajr_angle

    @property
    def ishaa_angle(self):
        """Returns the Ishaa angle for calculation."""
        return self._ishaa_angle

    @property
    def applicability(self):
        """Returns the applicability of the method."""
        return self._applicability


# List of predefined Fajr and Ishaa methods
LIST_FAJR_ISHA_METHODS = (
    MethodInfo(1, ("University of Islamic Sciences, Karachi (UISK)", 
                    "Ministry of Religious Affaires, Tunisia", 
                    "Grande Mosquée de Paris, France"), 
                18.0, 18.0, ()),
    MethodInfo(2, ("Muslim World League (MWL)", 
                    "Ministry of Religious Affaires and Awqaf, Algeria", 
                    "Presidency of Religious Affairs, Turkey"), 
                18.0, 17.0, ()),
    MethodInfo(3, "Egyptian General Authority of Survey (EGAS)", 
                19.5, 17.5, ()),
    MethodInfo(4, "Umm al-Qura University, Makkah (UMU)", 
                18.5, FixedTime(90, 120), ()),
    MethodInfo(5, ("Islamic Society of North America (ISNA)", 
                    "France - Angle 15°"), 
                15.0, 15.0, ()),
    MethodInfo(6, "French Muslims (ex-UOIF)", 12.0, 12.0, ()),
    MethodInfo(7, ("Islamic Religious Council of Singapore (MUIS)", 
                    "Department of Islamic Advancements of Malaysia (JAKIM)", 
                    "Ministry of Religious Affairs of Indonesia (KEMENAG)"), 
                20.0, 18.0, ()),
    MethodInfo(8, "Spiritual Administration of Muslims of Russia", 
                16.0, 15.0, ()),
    MethodInfo(9, "Fixed Ishaa Time Interval, 90min", 
                19.5, FixedTime(90, 90), ()),
)


class PrayerConf:
    """
    Configuration class for prayer calculations.

    Attributes:
        longitude (float): Geographical longitude of the location.
        latitude (float): Geographical latitude of the location.
        timezone (float): Time zone in hours from GMT.
        angle_ref (Union[int, MethodInfo]): Reference for Fajr and Ishaa angles.
        asr_madhab (int): 1 for Jomhor method, 2 for Hanafi method.
        enable_summer_time (bool): Flag to indicate if summer time is used.
    """

    def __init__(self, longitude, latitude, timezone, angle_ref=2, asr_madhab=1, enable_summer_time=False):
        """
        Initialize the PrayerConf object.

        :param longitude: Geographical longitude of the given location.
        :param latitude: Geographical latitude of the given location.
        :param timezone: The time zone GMT (+/-timezone).
        :param angle_ref: The reference method for Fajr and Ishaa angles, can be MethodInfo object or ID.
        :param asr_madhab: 1 for Jomhor (default) or 2 for Hanafi.
        :param enable_summer_time: True if summer time is used, False by default.
        """
        self.longitude = longitude
        self.latitude = latitude
        self.timezone = timezone
        self.sherook_angle = 90.83333  # Constant for sunrise
        self.maghreb_angle = 90.83333  # Constant for sunset
        self.asr_madhab = asr_madhab if asr_madhab == 2 else 1
        
        self.middle_longitude = self.timezone * 15
        self.longitude_difference = (self.middle_longitude - self.longitude) / 15
        self.summer_time = enable_summer_time

        global LIST_FAJR_ISHA_METHODS
        if isinstance(angle_ref, int):
            method = LIST_FAJR_ISHA_METHODS[angle_ref - 1 if angle_ref <= len(LIST_FAJR_ISHA_METHODS) else 2]
        elif isinstance(angle_ref, MethodInfo):
            method = angle_ref
        else:
            raise TypeError("angle_ref must be an instance of int or MethodInfo")

        self.fajr_angle = (method.fajr_angle + 90.0) if not isinstance(method.fajr_angle, FixedTime) else method.fajr_angle
        self.ishaa_angle = (method.ishaa_angle + 90.0) if not isinstance(method.ishaa_angle, FixedTime) else method.ishaa_angle


class Prayer:
    """
    A class for calculating prayer times and Qibla direction.
    """

    def __init__(self, conf, dat, correction_val=0):
        """
        Initialize the Prayer object with configuration and date.

        :param conf: PrayerConf object containing configuration.
        :param dat: Date for which prayer times are to be calculated.
        :param correction_val: Correction value for the date.
        """
        self._conf = conf
        self._date = dat
        self._jd = gregorian_to_julian(dat)

        if correction_val not in range(-2, 3):
            raise Exception('Correction value exception')

        self._correction_val = correction_val

        # Calculate prayer times
        self._dohr_time = self._get_dohr_time()
        self._fajr_time = self._get_fajr_time()
        self._sherook_time = self._get_sherook_time()
        self._asr_time = self._get_asr_time()
        self._maghreb_time = self._get_maghreb_time()
        self._ishaa_time = self._get_ishaa_time()

        # Calculate midnight and thirds of the night
        self._midnight = self._get_midnight()
        self._second_third_of_night = self._get_second_third_of_night()
        self._last_third_of_night = self._get_last_third_of_night()

    def _get_asr_angle(self):
        """Calculate the angle for Asr based on the chosen Madhab (doctrine)."""
        delta = self._sun_declination()
        x = (dsin(self._conf.latitude) * dsin(delta) + dcos(self._conf.latitude) * dcos(delta))
        a = atan(x / sqrt(-x * x + 1))
        x = self._conf.asr_madhab + (1 / tan(a))
        return 90 - (180 / pi) * (atan(x) + 2 * atan(1))

    def _sun_declination(self):
        """Calculate the sun declination angle."""
        n = self._jd - 2451544.5
        epsilon = 23.44 - 0.0000004 * n
        l = 280.466 + 0.9856474 * n
        g = 357.528 + 0.9856003 * n
        lamda = l + 1.915 * dsin(g) + 0.02 * dsin(2 * g)
        x = dsin(epsilon) * dsin(lamda)
        return (180 / (4 * atan(1))) * atan(x / sqrt(-x * x + 1))

    def _get_time_for_angle(self, angle):
        """Calculate times for prayer angles (Fajr, Sherook, Asr, Maghreb, Ishaa)."""
        delta = self._sun_declination()
        s = ((dcos(angle) - dsin(self._conf.latitude) * dsin(delta)) / (dcos(self._conf.latitude) * dcos(delta)))
        return (180 / pi * (atan(-s / sqrt(-s * s + 1)) + pi / 2)) / 15

    def _hours_to_time(self, val, shift):
        """
        Convert a decimal hour value to a time object.

        :param val: Value in decimal hours.
        :param shift: Time shift in seconds to apply to the calculated time.
        :return: A time object representing the calculated time.
        """
        if not isinstance(shift, (float, int)):
            raise ValueError("shift's value must be an int or a float")
        
        st = 1 if self._conf.summer_time else 0
        hours = val + shift / 3600
        minutes = (hours - floor(hours)) * 60
        seconds = (minutes - floor(minutes)) * 60
        hours = floor(hours + st) % 24
        return time(hours, floor(minutes), floor(seconds))

    def fajr_time(self, shift=0.0):
        """Get the Fajr time with an optional shift."""
        return self._hours_to_time(self._fajr_time, shift)

    def _get_fajr_time(self):
        """Calculate the Fajr time."""
        return self._dohr_time - self._get_time_for_angle(self._conf.fajr_angle)

    def sherook_time(self, shift=0.0):
        """Get the Sherook (Sunrise) time with an optional shift."""
        return self._hours_to_time(self._sherook_time, shift)

    def _get_sherook_time(self):
        """Calculate the Sherook time."""
        return self._dohr_time - self._get_time_for_angle(self._conf.sherook_angle)

    def dohr_time(self, shift=0.0):
        """Get the Dohr (Zenith) time with an optional shift."""
        return self._hours_to_time(self._dohr_time, shift)

    def _get_dohr_time(self):
        """Calculate the Dohr time (internal use only)."""
        ld = self._conf.longitude_difference
        time_eq = equation_of_time(self._jd)
        duhr_t = 12 + ld + time_eq / 60
        return duhr_t

    def asr_time(self, shift=0.0):
        """Get the Asr time with an optional shift."""
        return self._hours_to_time(self._asr_time, shift)

    def _get_asr_time(self):
        """Calculate the Asr time."""
        return self._dohr_time + self._get_time_for_angle(self._get_asr_angle())

    def maghreb_time(self, shift=0.0):
        """Get the Maghreb time with an optional shift."""
        return self._hours_to_time(self._maghreb_time, shift)

    def _get_maghreb_time(self):
        """Calculate the Maghreb time."""
        return self._dohr_time + self._get_time_for_angle(self._conf.maghreb_angle)

    def ishaa_time(self, shift=0.0):
        """Get the Ishaa time with an optional shift."""
        return self._hours_to_time(self._ishaa_time, shift)

    def _get_ishaa_time(self):
        """Calculate the Ishaa time."""
        if isinstance(self._conf.ishaa_angle, FixedTime):
            is_ramadan = HijriDate.get_hijri(self._date, self._correction_val).month == 9
            time_after_maghreb = self._conf.ishaa_angle.ramadan_time_hr if is_ramadan else self._conf.ishaa_angle.all_year_time_hr
            ishaa_t = time_after_maghreb + self._dohr_time + self._get_time_for_angle(self._conf.maghreb_angle)
        else:
            ishaa_t = self._dohr_time + self._get_time_for_angle(self._conf.ishaa_angle)
        
        return ishaa_t

    def midnight(self, shift=0.0):
        """Get the midnight time with an optional shift."""
        return self._hours_to_time(self._midnight, shift)

    def _get_midnight(self):
        """Calculate the midnight time (internal use only)."""
        return self._maghreb_time + ((24.0 - (self._maghreb_time - self._fajr_time)) / 2.0)

    def second_third_of_night(self, shift=0.0):
        """Get the second third of the night time with an optional shift."""
        return self._hours_to_time(self._second_third_of_night, shift)

    def _get_second_third_of_night(self):
        """Calculate the second third of the night time (internal use only)."""
        return self._maghreb_time + ((24.0 - (self._maghreb_time - self._fajr_time)) / 3.0)

    def last_third_of_night(self, shift=0.0):
        """Get the last third of the night time with an optional shift."""
        return self._hours_to_time(self._last_third_of_night, shift)

    def _get_last_third_of_night(self):
        """Calculate the last third of the night time (internal use only)."""
        return self._maghreb_time + (2 * (24.0 - (self._maghreb_time - self._fajr_time)) / 3.0)