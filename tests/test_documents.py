# dksalaries/tests/test_documents.py
# -*- coding: utf-8 -*-
# Copyright (C) 2021 Eric Truett
# Licensed under the MIT License

import datetime
import random
from typing import List

import pandas as pd
import pytest

from dksalaries.documents import *
from dksalaries.util import camel_to_snake


########################################
# AttributesDocument
########################################
@pytest.mark.skip('AttributesDocument not implemented')
def test_attributes_document():
    pass


########################################
# DraftStatsDocument
########################################
@pytest.mark.skip('DraftStatsDocument not implemented')
def test_draftstats_document():
    pass


########################################
# TournamentDocument
########################################
@pytest.mark.skip('TournamentDocument not implemented')
def test_tournament_document():
    pass


########################################
# CompetitionDocument
########################################
def test_competition(gc: GetContestsDocument):
    """Testing structure of competition"""
    comp = gc.game_sets[0].competitions[0]
    assert comp.team_codes == ['PHI', 'ATL']
    assert comp.team_names == ['Philadelphia Eagles', 'Atlanta Falcons']
 

########################################
# GameStyleDocument
########################################
@pytest.mark.skip('GameStyleDocument not implemented')
def test_gamestyle_document():
    pass


########################################
# GameTypeDocument
########################################
@pytest.mark.skip('GameTypeDocument not implemented')
def test_gametype_document():
    pass


########################################
# GameSetDocument
########################################
def test_gameset_n_games(gc: GetContestsDocument):
    """Testing structure of game_set"""
    gs = gc.game_sets[0]
    assert gs.n_games == 13

    
def test_gameset_slate_starts(gc: GetContestsDocument):
    """Testing game_set.slate_starts"""
    gs = gc.game_sets[0]
    assert gs.slate_starts.date() == datetime.date(2021, 9, 12)

    
def test_gameset_slate_teams(gc):
    """Testing game_set.slate_teams"""
    gs = gc.game_sets[0]
    assert len(gs.slate_teams) == 26


########################################
# ContestDocument
########################################
def test_contest(gc: GetContestsDocument):
    """Tests contest document"""
    contest = random.choice(gc.contests)
    assert isinstance(contest, ContestDocument)


########################################
# DraftGroupDocument
########################################
def test_draftgroup(gc: GetContestsDocument):
    """Tests draftgroup document"""
    item = random.choice(gc.draft_groups)
    assert isinstance(item, DraftGroupDocument)


########################################
# GetContestsDocument
########################################
def test_getcontestsdocument(gc: GetContestsDocument):
    """Tests getcontests document"""
    assert isinstance(gc, GetContestsDocument)


def test_findcontest_nocontests(gc: GetContestsDocument) -> List[ContestDocument]:
    """Tests find_contest"""
    filters = {'n': ('like', 'Million')}
    contests = gc.find_contest(filters)
    assert len(contests) > 0
    assert isinstance(random.choice(contests), ContestDocument)


def test_findcontest_contests(gc: GetContestsDocument):
    """Tests find_contest"""
    filters = {'n': ('like', 'Million')}
    contests = gc.find_contest(filters, gc.contests[0:2])
    assert len(contests) > 0
    assert isinstance(random.choice(contests), ContestDocument)


def test_findmainslate(gc: GetContestsDocument, tprint):
    """Tests find_main_slate"""
    v = gc.find_main_slate()
    assert v == (53019, 'FBE061E5C4BADEC29A2BF302DE6DC97A')

