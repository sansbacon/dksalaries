# -*- coding: utf-8 -*-
# test_dksalaries.py

from dksalaries.util import camel_to_snake
import json
import random
from typing import List

import cattr
import pandas as pd
import pytest

from dksalaries import Parser
from dksalaries.documents import *


@pytest.fixture
def draftables_document(test_directory):
    return json.loads((test_directory / 'data' / 'draftables.json').read_text())


@pytest.fixture
def getcontests_document(test_directory):
    return json.loads((test_directory / 'data' / 'getcontests.json').read_text())


def test_contests(getcontests_document):
    """Testing structure of contest"""
    contests = getcontests_document['Contests']
    for contest in contests:
        d = {camel_to_snake(k): v for k, v in contest.items() if v is not None}
        converter = cattr.GenConverter(forbid_extra_keys=True)
        assert isinstance(converter.structure(d, ContestDocument), ContestDocument)


def test_getcontests(getcontests_document):
    """Testing structure of getcontest"""
    p = Parser()
    o = p.getcontests(getcontests_document)
    assert isinstance(o, GetContestsDocument)


def test_draftables(draftables_document, tprint):
    """Testing structure of getcontest"""
    p = Parser()
    o = p.draftables(draftables_document)
    assert isinstance(o, DraftablesDocument)


def test_draftables_player_salary(draftables_document, tprint):
    """Tests draftables.player_salaries"""
    p = Parser()
    o = p.draftables(draftables_document)
    ps = o.player_salaries()
    assert isinstance(ps, list)
    assert isinstance(random.choice(ps), PlayerSalaryDocument)
    tprint(random.choice(ps))


def test_player_salary_document(draftables_document, tprint):
    """Testing structure of getcontest"""
    p = Parser()
    o = p.draftables(draftables_document)
    pl = random.choice(o.draftables)
    ps = cattr.structure_attrs_fromdict(cattr.unstructure(pl), PlayerSalaryDocument)
    assert isinstance(ps, PlayerSalaryDocument)