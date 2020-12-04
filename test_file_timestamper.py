import datetime

import pytest
from hypothesis import given
import hypothesis.strategies as st

import file_timestamper


@given(
    st.from_regex(r"\w*"),
    st.integers(min_value=1990, max_value=2050),
    st.integers(min_value=0, max_value=13),
    st.integers(min_value=0, max_value=32),
    st.integers(min_value=0, max_value=25),
    st.integers(min_value=0, max_value=61),
    st.integers(min_value=0, max_value=61),
    st.from_regex(r"\w*"),
)
def test_parse(stem, Y, m, d, H, M, S, ext):

    if Y < 1000 or m == 0 or d == 0 or m > 12 or H > 23 or M > 59 or S > 59:
        valid = False
    else:
        if m == 2:
            # Feb
            if Y % 4 == 0:
                # leap year
                if d in range(1, 30):
                    valid = True
                else:
                    valid = False
            else:
                if d in range(1, 29):
                    valid = True
                else:
                    valid = False
        elif m in (1, 3, 5, 7, 8, 10, 12):
            if d in range(1, 32):
                valid = True
            else:
                valid = False
        else:
            if d in range(1, 31):
                valid = True
            else:
                valid = False

    pad0 = lambda x, y: ("{:0>" + str(x) + "}").format(y)
    string = (
        stem
        + pad0(4, Y)
        + pad0(2, m)
        + pad0(2, d)
        + "_"
        + pad0(2, H)
        + pad0(2, M)
        + pad0(2, S)
        + "."
        + ext
    )
    if valid:
        ctime = file_timestamper.parse_ctime(string)
    else:
        with pytest.raises(AssertionError):
            file_timestamper.parse_ctime(string)


# @given(
#     st.datetimes(
#         min_value=datetime.datetime(1000, 1, 1), max_value=datetime.datetime(2099, 1, 1)
#     )
# )
# def test_parse(ctime):
#     string = file_timestamper.format_ctime(ctime)
#     ctime2 = file_timestamper.parse_ctime(string)
#     assert ctime.timetuple()[:6] == ctime2[:6]


@given(
    st.datetimes(
        min_value=datetime.datetime(1000, 1, 1), max_value=datetime.datetime(2099, 1, 1)
    )
)
def test_format(ctime):
    string = file_timestamper.format(ctime)
    ctime2 = file_timestamper.parse(string)
    # only test (Year, Month, Day, Hour, Min, Sec)
    assert ctime.timetuple()[:6] == ctime2[:6]


@given(
    st.datetimes(
        min_value=datetime.datetime(1000, 1, 1), max_value=datetime.datetime(2099, 1, 1)
    ),
    st.datetimes(
        min_value=datetime.datetime(1000, 1, 1), max_value=datetime.datetime(2099, 1, 1)
    ),
)
def test_out_of_date(reference, target):
    outdated = file_timestamper.out_of_date(reference, target)
    assert outdated in (True, False, None)
    # assert (outdated is None and outdated2 is None) or (outdated != outdated2)
    if outdated:
        outdated2 = file_timestamper.out_of_date(target, reference)
        assert outdated2 != outdated


# functions below do IO operations, need to mock filesystem or something to test
# def test_filepaths(directory, fname_less_ctime):
#     pass


# def test_filenames(directory, fname_less_ctime):
#     pass


# def test_latest_version(directory, fname):
#     pass

