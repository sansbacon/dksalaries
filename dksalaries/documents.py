# dksalaries/dksalaries/documents.py
# -*- coding: utf-8 -*-
# Copyright (C) 2021 Eric Truett
# Licensed under the MIT License

"""documents.py: object model for draftkings API"""

import logging
from typing import Any, Dict, List

import attr

logging.getLogger(__file__).addHandler(logging.NullHandler())


@attr.s(auto_attribs=True)
class AttributesDocument:
    id: int = None
    name: str = None
    type_id: int = None
    type: str
    value: str = None
    filterable: bool = True
    sort_value: str = None
    prompt: str = None


@attr.s(auto_attribs=True)
class CompetitionDocument:
    game_id: int
    away_team_id: int
    home_team_id: int
    home_team_score: int
    away_team_score: int
    home_team_city: str
    away_team_city: str
    home_team_name: str
    away_team_name: str
    start_date: str
    location: str
    last_play: Any
    team_with_possession: int
    time_remaining_status: str
    sport: str
    status: str
    description: str
    full_description: str
    exceptional_messages: List
    series_type: int
    number_of_games_in_series: int
    series_info: Any
    home_team_competition_ordinal: int
    away_team_competition_ordinal: int
    home_team_competition_count: int
    away_team_competition_count: int


@attr.s(auto_attribs=True)
class ContestsDocument:   
    contests: List[ContestDocument]
    tournaments: List[TournamentDocument]
    draft_groups: List[DraftGroupsDocument]
    game_sets: List[GameSetDocument]
    game_types: List[GameTypeDocument]


@attr.s(auto_attribs=True)
class ContestDocument:   
	uc: int
	ec: int
	mec: int
	fpp: int
	s: int
	n: str
	attr: Dict
	nt: int
	m: int
	a: int
	po: float
	pd: Dict
	tix: bool
	sdstring: str
	sd: str
	id: int
	tmpl: int
	pt: int
	so: int
	fwt: bool
	is_owner: bool
	start_time_type: int
	dg: int
	ulc: int
	cs: int
	game_type: str
	ssd: None
	dgpo: float
	cso: int
	ir: int
	rl: bool
	rlc: int
	rll: int
	sa: bool
	free_with_crowns: bool
	crown_amount: int
	is_bonus_finalized: bool
	is_snake_draft: bool


@attr.s(auto_attribs=True)
class DraftablesDocument:   
    draftables: List[PlayerDocument]
    competitions: List[CompetitionDocument]
    teams_without_competitions: List
    draft_alerts: List
    draft_stats: List
    player_game_attributes: List
    error_status: List


@attr.s(auto_attribs=True)
class DraftGroupDocument:   
    draft_group_id: int
    contest_type_id: int
    start_date: str
    start_date_est: str
    sort_order: int
    draft_group_tag: str
    game_type_id: int
    game_type: Any
    sport_sort_order: int
    sport: str
    game_count: int
    contest_start_time_suffix: Any
    contest_start_time_type: int
    games: Any
    draft_group_series_id: int
    game_set_key: str
    allow_ugc: bool


@attr.s(auto_attribs=True)
class DraftStatsDocument:
    id: int
    abbr: str
    name: str
    order: int
    

@attr.s(auto_attribs=True)
class GameSetDocument:   
    game_set_key: str
    contest_start_time_suffix: Any
    competitions: List[CompetitionDocument]
    game_styles: List[GameStyleDocument]
    sort_order: int
    min_start_time: str
    tag: str


@attr.s(auto_attribs=True)
class GameStyleDocument:   
    game_style_id: int
    sport_id: int
    sort_order: int
    name: str
    abbreviation: str
    description: str
    is_enabled: bool
    attributes: Any


@attr.s(auto_attribs=True)
class GameTypeDocument:   
    game_type_id: int
    name: str
    description: str
    tag: str
    sport_id: int
    draft_type: str
    game_style: List[GameStyleDocument]
    is_season_long: bool


@attr.s(auto_attribs=True)
class PlayerDocument:   
    draftable_id: int
    first_name: str
    last_name: str
    display_name: str
    short_name: str
    player_id: int
    player_dk_id: int
    position: str
    roster_slot_id: int
    salary: int
    status: str
    is_swappable: bool
    is_disabled: bool
    news_status: str
    player_image50: str
    player_image160: str
    alt_player_image50: str
    alt_player_image160: str
    competition: List
    competitions: List
    draft_stat_attributes: List
    player_attributes: List
    team_league_season_attributes: List
    player_game_attributes: List
    team_id: int
    team_abbreviation: str
    draft_alerts: List
    player_game_hash: str


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



