#!/usr/bin/env/ python

import pytest


@pytest.mark.general
def test_init():
    x = 5
    assert x == 5
