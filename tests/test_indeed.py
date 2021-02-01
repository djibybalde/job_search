# -*- coding: utf-8 -*-

"""
    Script to make test
"""

from indeed import params


def test_indeed_params():
    assert params('my_username', 'my_password') == ('my_username', 'my_password')
    assert params('your_username', 'your_password') == ('your_username', 'your_password')
