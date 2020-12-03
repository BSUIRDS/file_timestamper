import re
import time
import pathlib
import datetime
import dateutil.parser


def parse_argos(string):
    """Parse timestamp from string
    
    For simplicity, assumes timestamps are as recent as the year 2000

    Parameters
    ----------
    string : str
        String containing timestamp substring with format YYYYmmdd_HHMMSS
        where
            YYYY = year
            mm = month
            dd = day
            HH = hour (24-hour format)
            MM = minute
            SS = second
        Example: 20200102_140203 -> 2:02:03 pm on Jan 2nd, 2020

    Returns
    -------
    ctime
        time.struct_time object of timestamp or None if not found
    """
    assert isinstance(string, str)

    search_str = r"([12][0-9]{3})([0-9]{2})([0-9]{2})_([0-9]{2})([0-9]{2})([0-9]{2})"
    matches = re.findall(search_str, string)
    assert len(matches) <= 1, f"found more than one timestamp: {string}"
    if matches:
        Y, m, d, H, M, S = map(int, matches[0])

        assert m in range(1, 13), f"invalid month: {m} in {string}"
        if m == 2:
            # Feb
            if Y % 4 == 0:
                # leap year
                assert d in range(1, 30), f"invalid day: {d} in {string}"
            else:
                assert d in range(1, 29), f"invalid day: {d} in {string}"
        elif m in (1, 3, 5, 7, 8, 10, 12):
            assert d in range(1, 32), f"invalid day: {d} in {string}"
        else:
            assert d in range(1, 31), f"invalid day: {d} in {string}"
        assert H in range(24), f"invalid hour: {H} in {string}"
        assert M in range(60), f"invalid minute: {M} in {string}"
        assert S in range(60), f"invalid second: {S} in {string}"
        # ctime = time.strptime(time_str[0], r"%Y%m%d_%H%M%S")
        ctime = time.struct_time((Y, m, d, H, M, S, 0, 0, 0))
    else:
        ctime = None
    return ctime


def format(ctime, fmt=r"%Y%m%d_%H%M%S"):
    """Format time into file timestamp

    Parameters
    ----------
    ctime : time.struct_time or datetime.datetime
        Time to format into string

    Returns
    -------
    str
        Time formatted as string"""
    assert isinstance(ctime, time.struct_time) or isinstance(
        ctime, datetime.datetime
    ), "argument not struct_time or datetime.datetime: reference"

    if hasattr(ctime, "timetuple"):
        return time.strftime(fmt, ctime.timetuple())
    else:
        return time.strftime(fmt, ctime)


def parse(filename):
    """Parse timestamp from filename
    
    Parameters
    ----------
    filename : str, pathlib.Path
        Path or string of file
    """
    if isinstance(filename, str):
        t = dateutil.parser.parse(filename, fuzzy=True)
    elif isinstance(filename, pathlib.Path):
        t = dateutil.parser.parse(filename.name, fuzzy=True)
    else:
        raise ValueError(f"Cannot parse: {filename}")
    return t


def out_of_date(reference, target):
    """Returns True if reference is newer than target

    Parameters
    ----------
    reference : time.struct_time or datetime.datetime
        Time associated with reference
    target : time.struct_time or datetime.datetime
        Time associated with target

    Returns
    -------
    outdated : bool or None
        Indicates if target is nonexistent or not as recent. None
        if reference and target are None.
    """

    if isinstance(reference, str) or isinstance(reference, pathlib.Path):
        reference = parse(reference)

    if isinstance(target, str) or isinstance(target, pathlib.Path):
        target = parse(target)

    assert (
        isinstance(reference, time.struct_time)
        or isinstance(reference, datetime.datetime)
        or (reference is None)
    ), "argument not struct_time or datetime.datetime: reference"
    assert (
        isinstance(target, time.struct_time)
        or isinstance(target, datetime.datetime)
        or (target is None)
    ), "argument not struct_time or datetime.datetime: target"

    if target:
        if reference:
            if target >= reference:
                outdated = False
            else:
                outdated = True
        else:
            outdated = False
    else:
        if reference:
            outdated = True
        else:
            outdated = None
    return outdated


def filepaths(directory, file_stem, stamp_fmt=r"\d{8}_\d{6}"):
    """Generate all filenames with matching stem

    Parameters
    ----------
    directory : pathlib.Path
        Path to directory holding file
    file_stem : str
        Filename without timestamp and extension
    stamp_fmt : str
        Regular expression

    Returns
    ------
    list of pathlib.Path
        Path of file in directory matching stem
    """
    stamp = re.compile(stamp_fmt)
    paths = [p for p in directory.glob(f"{file_stem}*") if stamp.search(p.name)]
    return paths


def filenames(directory, file_stem, stamp_fmt=r"\d{8}_\d{6}"):
    """Generate all filenames with matching stem

    Parameters
    ----------
    directory : pathlib.Path
        Path to directory holding file
    file_stem : str
        File stem, filename without timestamp and extension

    Yields
    ------
    str
        Name of file in directory matching stem
    """
    return (x.name for x in filepaths(directory, file_stem, stamp_fmt=stamp_fmt))


def latest_version(directory, file_stem, stamp_fmt=r"\d{8}_\d{6}"):
    """Gets latest creation time of files sharing stem

    Parameters
    ----------
    directory : pathlib.Path
        Path to directory holding file
    file_stem : str
        File stem, filename without timestamp and extension

    Returns
    -------
    str
        Filename of file with most recent creation time
    """
    sort_by = lambda s: dateutil.parser.parse(s, fuzzy=True)
    sorted_fnames = sorted(
        filenames(directory, file_stem, stamp_fmt=stamp_fmt), key=sort_by
    )
    if sorted_fnames:
        return sorted_fnames[-1]
    else:
        return None
