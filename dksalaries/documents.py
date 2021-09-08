# dksalaries/dksalaries/documents.py
# -*- coding: utf-8 -*-
# Copyright (C) 2021 Eric Truett
# Licensed under the MIT License

"""documents.py: object model for draftkings API"""

import datetime
import functools
import logging
from typing import Any, Dict, List, Sequence, Set, Tuple

import attr, cattr

from .util import flatten, parse_dktime
from nflnames import standardize_team_code, standardize_team_name


CONTEST_TYPE_IDS = {
  1: ('Classic', 'SalaryCap'),
  96: ('Showdown Captain Mode', 'SalaryCap'),
  159: ('Madden Showdown Captain Mode', 'SalaryCap'),
  192: ('Snake Showdown', 'SnakeDraft'),
  145: ('Best Ball', 'SnakeDraft'),
  189: ('Snake', 'SnakeDraft'),
}

GAME_TYPE_IDS = {
  1: 'Classic',
  158: 'Classic',
  50: 'Tiers',
  51: 'Tiers',
  52: 'Tiers',
  53: 'Tiers',
  54: 'Tiers',
  55: 'Tiers',
  101: 'Tiers',
  102: 'Tiers',
  103: 'Tiers',
  104: 'Tiers',
  105: 'Tiers',
  96: 'Showdown Captain Mode',
  159: 'Showdown Captain Mode',
  108: 'In-Game Showdown H2',
  110: 'In-Game Showdown Q4',
  58: 'Showdown',
  99: 'QB Gunslinger',
  107: 'Non Late Swap',
  124: 'Sunday Night Series',
  145: 'Best Ball',
  162: 'Best Ball',
  157: 'Dark Horse Value Pick',
  163: 'Snake',
  189: 'Snake',
  164: 'Snake Showdown',
  192: 'Snake Showdown',
}

BEST_BALL_TYPES = tuple([k for k, v in GAME_TYPE_IDS.items() if v == 'Best Ball'])
CAPTAIN_GAME_TYPES = tuple([k for k, v in GAME_TYPE_IDS.items() if 'Captain' in v])
CLASSIC_GAME_TYPES = tuple([k for k, v in GAME_TYPE_IDS.items() if v == 'Classic'])
TIERS_GAME_TYPES = tuple([k for k, v in GAME_TYPE_IDS.items() if v == 'Tiers'])


@attr.s(auto_attribs=True)
class AttributesDocument:
    type: str = None
    type_id: int = None
    id: int = None
    name: str = None
    value: str = None
    filterable: bool = True
    sort_value: str = None
    prompt: str = None


@attr.s(auto_attribs=True)
class DraftStatsDocument:
    id: int
    abbr: str
    name: str
    order: int
    

@attr.s(auto_attribs=True)
class TournamentDocument:   
    tournament_key: str
    name: str
    draft_group_id: int
    is_visible: bool
    sort_order: int
    status: int
    entrants: int
    contest_attributes: List
    maximum_entries: int
    maximum_entries_per_user: int
    entry_fee: float
    accepted_tickets: List
    total_payouts: float
    payout_descriptions: List
    fpp_award: int
    payout_summaries: List
    sport_id: int
    crown_amount: int
    ticket_only_entry: bool
    start_time: str
    start_time_type: str
    game_set_key: str


@attr.s(auto_attribs=True)
class CompetitionDocument:
    game_id: int = None
    away_team_id: int = None
    home_team_id: int = None
    home_team_score: int = None
    away_team_score: int = None
    home_team_city: str = None
    away_team_city: str = None
    home_team_name: str = None
    away_team_name: str = None
    start_date: str = None
    location: str = None
    last_play: Any = None
    team_with_possession: int = None
    time_remaining_status: str = None
    sport: str = None
    status: str = None
    description: str = None
    full_description: str = None
    exceptional_messages: List = attr.Factory(list)
    series_type: int = None
    number_of_games_in_series: int = None
    series_info: Any = None
    home_team_competition_ordinal: int = None
    away_team_competition_ordinal: int = None
    home_team_competition_count: int = None
    away_team_competition_count: int = None

    @property
    def team_codes(self):
        return [standardize_team_code(t.strip()) for t in self.description.split(' @ ')]

    @property
    def team_names(self):
        return [standardize_team_name(self.away_team_city + ' ' + self.away_team_name), 
                standardize_team_name(self.home_team_city + ' ' + self.home_team_name)]


@attr.s(auto_attribs=True)
class GameStyleDocument:   
    game_id: int = None
    game_style_id: int = None
    sport_id: int = None
    sort_order: int = None
    name: str = None
    abbreviation: str = None
    description: str = None
    is_enabled: bool = None
    attributes: Any = None


@attr.s(auto_attribs=True)
class GameTypeDocument:   
    game_type_id: int
    sport_id: int
    name: str
    description: str = None
    tag: str = None
    draft_type: str = None
    game_style: List[GameStyleDocument] = attr.Factory(list)
    is_season_long: bool = False


@attr.s(auto_attribs=True)
class GameSetDocument:   
    game_set_key: str
    competitions: List[CompetitionDocument] = attr.Factory(list)
    game_styles: List[GameStyleDocument] = attr.Factory(list)
    contest_start_time_suffix: Any = None
    sort_order: int = None
    min_start_time: str = None
    tag: str = None
    tz: str = 'America/New_York'

    @property
    def has_classic(self) -> bool:
        return 'Classic' in self.game_style_names

    @property
    def game_style_names(self) -> Set[str]:
        return set([i.name for i in self.game_styles])

    @property
    def n_games(self) -> int:
        return len(self.competitions)

    @functools.cached_property
    def slate_teams(self) -> List[str]:
        return [standardize_team_code(item) 
                for item in flatten([c.team_codes for c in self.competitions])]

    @functools.cached_property
    def start_end_time(self) -> Tuple[datetime.datetime, datetime.datetime]:
        """Gets the min and max start time for a gameset
        
        Args:
            None

        Returns:
            Tuple[datetime.datetime, datetime.datetime]

        """
        times = [parse_dktime(comp.start_date, True, self.tz) for comp in self.competitions]
        return (min(times), max(times))


@attr.s(auto_attribs=True)
class ContestDocument:   
    uc: int = None
    ec: int = None
    mec: int = None
    fpp: int = None
    s: int = None
    n: str = None
    attr: Dict = None
    nt: int = None
    m: int = None
    a: int = None
    po: float = None
    pd: Dict = None
    tix: bool = None
    sdstring: str = None
    sd: str = None
    id: int = None
    tmpl: int = None
    pt: int = None
    so: int = None
    fwt: bool = None
    is_owner: bool = None
    start_time_type: int = None
    dg: int = None
    ulc: int = None
    cs: int = None
    game_type: str = None
    ssd: Any = None
    dgpo: float = None
    cso: int = None
    ir: int = None
    rl: bool = None
    rlc: int = None
    rll: int = None
    sa: bool = None
    free_with_crowns: bool = None
    crown_amount: int = None
    is_bonus_finalized: bool = None
    is_snake_draft: bool = None


@attr.s(auto_attribs=True)
class DraftGroupDocument:   
    draft_group_id: int
    contest_type_id: int = None
    start_date: str = None
    start_date_est: str = None
    sort_order: int = None
    draft_group_tag: str = None
    game_type_id: int = None
    game_type: Any = None
    sport_sort_order: int = None
    sport: str = None
    game_count: int = None
    contest_start_time_suffix: Any = None
    contest_start_time_type: int = None
    games: Any = None
    draft_group_series_id: int = None
    game_set_key: str = None
    allow_ugc: bool = None


@attr.s(auto_attribs=True)
class PlayerDocument:   
    draftable_id: int
    first_name: str
    last_name: str
    display_name: str
    short_name: str
    player_id: int
    player_dk_id: int
    team_id: int
    team_abbreviation: str
    position: str
    roster_slot_id: int
    salary: int
    status: str
    is_swappable: bool = False
    is_disabled: bool = False
    news_status: str = None
    player_image50: str = None
    player_image160: str = None
    alt_player_image50: str = None
    alt_player_image160: str = None
    draft_stat_attributes: List = attr.Factory(list)
    player_attributes: List = attr.Factory(list)
    team_league_season_attributes: List = attr.Factory(list)
    player_game_attributes: List = attr.Factory(list)
    draft_alerts: List = attr.Factory(list)
    player_game_hash: str = None
    competition: List = attr.Factory(list)
    competitions: List = attr.Factory(list)


@attr.s(auto_attribs=True)
class PlayerSalaryDocument:
    draftable_id: int
    player_id: int
    player_dk_id: int
    first_name: str
    last_name: str
    display_name: str
    team_abbreviation: str
    position: str
    salary: int


@attr.s(auto_attribs=True)
class SlateDocument:
    """Document that represents main slate information"""
    sport: str
    n_games: int
    dg: int
    game_set_key: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    is_main_slate: bool
    slate_teams: List[str] = attr.Factory(list)
    slate_players: List[PlayerSalaryDocument] = attr.Factory(list)

 
@attr.s(auto_attribs=True)
class GetContestsDocument:   
    contests: List[ContestDocument] = attr.Factory(list)
    tournaments: List[TournamentDocument] = attr.Factory(list)
    draft_groups: List[DraftGroupDocument] = attr.Factory(list)
    game_sets: List [GameSetDocument] = attr.Factory(list)
    game_types: List [GameTypeDocument] = attr.Factory(list)
    user_prizes: List[Any] = attr.Factory(list)
    marketing_offers: Any = None
    direct_challenge_modal: Any = None
    deposit_transaction: Any = None
    show_raf_link: Any = None
    prize_redemption_model: Any = None
    prize_redemption_pop: Any = None
    use_raptor_head_to_head: Any = None
    use_js_web_lobby_modals: Any = None
    show_game_style_filter: Any = None
    sport_menu_items: Any = None
    user_geo_location: Any = None
    show_ads: Any = None
    is_vip: Any = None
    ads_enabled: Any = None

    @functools.cached_property
    def classic_slates(self) -> List[SlateDocument]:
        """Gets classic slates from GetContestDocument"""
        slate_documents = []

        # step one: need to iterate over slates (game_sets)
        for gset in [item for item in self.game_sets if item.has_classic]:
            # step one: find qualifying draft groups
            draft_groups = [dg for dg in self.draft_groups if
                            dg.game_set_key == gset.game_set_key and
                            dg.game_type_id == 1]
            start, end = gset.start_end_time
            ims = all((start.hour == 13, end.hour == 16, start.weekday() == 6, end.weekday() == 6))

            o = SlateDocument(
                sport='NFL',
                n_games=gset.n_games,
                dg=draft_groups,
                game_set_key=gset.game_set_key,
                start_date=start,
                end_date=end,
                is_main_slate=ims,
                slate_teams=gset.slate_teams,
                slate_players=None
            )

            slate_documents.append(o)

        return slate_documents

    def find_contest(self, filters: dict, contests: List[ContestDocument] = None) -> List[ContestDocument]:
        """Finds contests according to filters
    
        Args:
            filters (dict): the filters for the find
            contests (List[dict]): the contests

        Returns:
            List[ContestDocument]

        """
        contests = self.contests if not contests else contests
        for k, v in filters.items():
            comp, val = v
            if comp == 'eq':
                contests = [c for c in contests if getattr(c, k) == val]
            if comp == 'like':
                contests = [c for c in contests if val in getattr(c, k)]
            if comp == 'lte':
                contests = [c for c in contests if getattr(c, k) <= val]
            if comp == 'gte':
                contests = [c for c in contests if getattr(c, k) >= val]   
        return contests

    def find_main_slate(self) -> Tuple[str, int]:
        """Finds the game_set_key and draft_group of the main slate
        
        Args:
            None

        Returns:
            Tuple[str, int]

        """
        # step one: get the draft group of contests that start Sunday at 1:00 PM
        dgid = self.find_milly().dg
        gskey = [i.game_set_key for i in self.draft_groups if i.draft_group_id == dgid][0]
        return (dgid, gskey)

    def find_milly(self, contests: List[ContestDocument] = None) -> List[ContestDocument]:
        """Finds Millionaire Makers"""
        l = contests if contests else self.contests
        return [i for i in l if 
                i.sdstring == 'Sun 1:00PM' and 
                i.game_type == 'Classic'and
                'Million' in i.n][0]


@attr.s(auto_attribs=True)
class DraftablesDocument:   
    draftables: List[PlayerDocument] = attr.Factory(list)
    competitions: List[CompetitionDocument] = attr.Factory(list)
    teams_without_competitions: List = attr.Factory(list)
    draft_alerts: List = attr.Factory(list)
    draft_stats: List = attr.Factory(list)
    player_game_attributes: List = attr.Factory(list)
    error_status: List = attr.Factory(list)

    def find_player_by_name(self, first_name: str = None, last_name: str = None, full_name: str = None, players: List[Any] = None) -> List[Any]:
        """Finds player by first, last, or full name
        
        Args:
            first_name (str): the player first_name, default None
            last_name (str): the player last_name, default None
            full_name (str): the player full_name, default None
            players (List[Any]): the players, default None

        Returns:
            List[Any]

        """
        l = self.draftables if not players else players
        if first_name:
            l = [i for i in l if first_name == i.first_name]
        if last_name:
            l = [i for i in l if last_name == i.last_name]
        if full_name:
            l = [i for i in l if full_name == i.full_name]
        return l

    def find_player_by_position(self, pos: str, players: List[Any] = None) -> List[Any]:
        """Finds player by position
        
        Args:
            pos (str): the player position
            players (List[Any]): the players, default None

        Returns:
            List[Any]

        """
        l = self.draftables if not players else players
        return [i for i in l if pos == i.position]

    def find_player_by_team(self, team: str, players: List[Any] = None) -> List[Any]:
        """Finds player by team
        
        Args:
            team (str): the player team
            players (List[Any]): the players, default None

        Returns:
            List[Any]

        """
        l = self.draftables if not players else players
        return [i for i in l if team == i.team_abbreviation]

    def player_salaries(self, players: List[PlayerDocument] = None) -> List[PlayerSalaryDocument]:
        """Converts PlayerDocument to PlayerSalaryDocument
        
        Args:
            players (List[PlayerDocument]): default None

        Returns:
            List[PlayerSalaryDocument]

        """
        l = self.draftables if not players else players
        return [cattr.structure(cattr.unstructure(o), PlayerSalaryDocument) for o in l]
