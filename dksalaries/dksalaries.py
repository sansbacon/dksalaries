# dksalaries/dksalaries/dksalaries.py
# -*- coding: utf-8 -*-
# Copyright (C) 2021 Eric Truett
# Licensed under the MIT License

"""
dksalaries

library to scrape/parse/analyze draftkings salaries

Example:

    s = Scraper()
    p = Parser()
    c = s.contests(sport='NFL')
    mm = [i for i in c if 'Millionaire' in i['n']][0]
    dgid = mm['dg']
    dt = s.draftables(dgid)
    pool = p.draftables(dt)
    sals = {i['name]: i['salary] for i in pool}

"""

import logging
import re
from typing import Dict, List

import browser_cookie3
import cattr
from requests_html import HTMLSession

from .constants import *
from .util import *



class Scraper:
    """Scrape DK site for data
    
    Examples:
        s = Scraper()
        c = s.contests(sport='NFL')
        mm = [i for i in c if 'Millionaire' in i['n']][0]
        dgid = mm['dg']
        dt = s.draftables(dgid)

    """

    def __init__(self):
        logging.getLogger(__file__).addHandler(logging.NullHandler())
        self.s = HTMLSession()
        self.s.headers.update({
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
            'DNT': '1',
            'Accept': '*/*',
            'Origin': 'https://www.draftkings.com',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.draftkings.com/',
            'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
        })
        self.s.cookies = browser_cookie3.firefox()

    @property
    def api_url(self):
        return 'https://api.draftkings.com/'

    @property
    def base_params(self):
        return {'format': 'json'}

    def _embed_params(self, embed_type):
        return dict(**self.base_params, **{'embed': embed_type})

    def contests(self, sport='NFL'):
        """
        Gets dk contests

        Args:
            sport(str): default 'nfl'

        Returns:
            dict

        """
        url = "https://www.draftkings.com/lobby/getcontests"
        return self.get_json(url, params={'sport': sport})

    def draftables(self, dgid):
        """
        Gets draftables JSON

        Args:
            dgid(int): draftgroup ID

        Returns:
            dict

        """
        url = self.api_url + f'draftgroups/v1/draftgroups/{dgid}/draftables?'
        return self.get_json(url, params=self.base_params)

    def get_json(self, url, params, headers=None, response_object=False):
        """Gets json resource"""
        headers = headers if headers else {}
        r = self.s.get(url, params=params, headers=headers)
        if response_object:
            return r
        return r.json()


class Parser:
    """Parse DK site for data"""

    GAME_TYPES = {
        "Showdown Captain Mode": 96,
        "Classic": 1,
    }

    PLAYERPOOL_FIELDS = [
        'draftableId', 'playerId', 'firstName', 'lastName', 
        'displayName',  'position', 'teamAbbreviation', 'salary']

    def __init__(self):
        logging.getLogger(__file__).addHandler(logging.NullHandler())
        self.c = cattr.GenConverter(forbid_extra_keys=True)

    def _competition(self, competition):
        """Parses competition"""
        wanted = ['GameId', 'StartDate', 'HomeTeamId', 'HomeTeamName', 'AwayTeamId', 'AwayTeamName']
        return {k: v for k, v in competition.items() if k in wanted}

    def _gameset(self, gameset):
        """Parses gameset"""
        # get top-level keys
        wanted = ['GameSetKey', 'MinStartTime', 'ContestStartTimeSuffix', 'Tag']
        gset = {k: v for k, v in gameset.items() if k in wanted}
    
        # parse gamestyles subresource
        gset['gamestyles'] = [self._gamestyle(item) for item in gameset['GameStyles']]

        # parse competitions subresource
        gset['competitions'] = [self._competition(item) for item in gameset['Competitions']]

        return gset

    def _gamestyle(self, gamestyle):
        """Parses gamestyle"""
        wanted = ['GameStyleId', 'Name', 'Abbreviation']
        return {k: v for k, v in gamestyle.items() if k in wanted}

    def classic_contests(self, contests: List[dict]) -> List[dict]:
        """Gets classic contests
        
        Args:
            contests (List[dict]): the contests resource

        Returns:
            List[dict]

        """
        return [c for c in contests if c['gameType'] == 'Classic']

    def cattr_example(self, contests):
        """Example of how to use cattr
        
        """
        odata = {camel_to_snake(k): v for k, v in contests.items()}
        o = self.c.structure_attrs_fromdict(odata, Contests)



    def contest_draftgroups(self, data):
        """Parses contests JSON for draftgroup_ids
        
        Args:
            data (dict): parsed contest resource JSON
            
        Returns:
            list [int]: each item is a draftgroup id

        """
        # STEP ONE: parse the gamesets
        gamesets = [self._gameset(item) for item in data['GameSets']]

        # STEP TWO: get the GameSetKey for gamesets of interest
        # Here, I want tag of featured, this will get main slate and showdown
        gameset_keys = [gs['GameSetKey'] 
                        for gs in gamesets 
                        if gs['Tag'] == 'Featured']
        
        # STEP THREE: get the draftgroups
        return [dg['DraftGroupId'] 
                for dg in data['DraftGroups']
                if dg['GameSetKey'] in gameset_keys]
        
    def draftables(self, draftables):
        """Parses draftables resource"""
        return [{k: item.get(k, None) for k in self.PLAYERPOOL_FIELDS}
                       for item in draftables['draftables']]
        
    def find_contest(self, contests: List[dict], filters: dict) -> dict:
        """Finds contests according to filters
        
        Args:
            contests (List[dict]): the contests
            filters (dict): the filters for the find

        Returns:
            dict

        """
        for k, v in filters.items():
            comp, val = v
            if comp == 'eq':
                contests = [c for c in contests if c[k] == val]
            if comp == 'like':
                contests = [c for c in contests if val in c[k]]
            if comp == 'lte':
                contests = [c for c in contests if c[k] <= val]
            if comp == 'gte':
                contests = [c for c in contests if c[k] >= val]    
        return contests

    def find_milly(self, contests, return_all=True):
        """Finds Millionaire Maker contest
        
        Args:
            contests (List[dict]): the contests resource
            return_all (bool): default True, if Fals only return cheapest milly

        """
        mm = [c for c in contests if 'Millionaire' in c['n'] and c['sdstring'] == 'Sun 1:00PM']
        if len(mm) == 1:
            return mm[0]
        if return_all:
            return mm
        entry_fees = [i['a'] for i in contests]
        return mm[entry_fees.index(min(entry_fees))]

    def player_pool_dict(self, draftables=None):
        """Takes parsed draftables (from file or request) and
           creates player pool dict with key of draftableId

        Args:
            draftables (dict): parsed JSON resource

        Returns:
            dict of dict: key is draftableId,
            value is dict with keys 'displayName', 'playerId', 'playerDkId',
                                    'position', 'teamAbbreviation'
        """
        wanted = self.PLAYERPOOL_FIELDS.copy()
        key = wanted.pop(0)
        return {item[key]: {k: item[k] for k in wanted} for item in self.draftables(draftables)}

    def salary_draftgroups(self, data, sport='NFL', game_type='Classic'):
        """Parses draftgroups for salary contests"""
        return [i for i in data['DraftGroups'] if i['Sport'] == sport and i['GameTypeId'] == 1]