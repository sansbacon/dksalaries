# dksalaries/dksalaries/documents.py
# -*- coding: utf-8 -*-
# Copyright (C) 2021 Eric Truett
# Licensed under the MIT License

"""documents.py: object model for draftkings API"""

from typing import Any, Dict, List

import attr


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
    exceptional_messages: List = None
    series_type: int = None
    number_of_games_in_series: int = None
    series_info: Any = None
    home_team_competition_ordinal: int = None
    away_team_competition_ordinal: int = None
    home_team_competition_count: int = None
    away_team_competition_count: int = None


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
class GameSetDocument:   
    game_set_key: str
    competitions: List[CompetitionDocument] = attr.Factory(list)
    game_styles: List[GameStyleDocument] = attr.Factory(list)
    contest_start_time_suffix: Any = None
    sort_order: int = None
    min_start_time: str = None
    tag: str = None


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
    draft_stat_attributes: List = None
    player_attributes: List = None
    team_league_season_attributes: List = None
    player_game_attributes: List = None
    draft_alerts: List = None
    player_game_hash: str = None
    competition: List = None
    competitions: List = None


@attr.s(auto_attribs=True)
class DraftablesDocument:   
    draftables: List[PlayerDocument] = attr.Factory(list)
    competitions: List[CompetitionDocument] = attr.Factory(list)
    teams_without_competitions: List = attr.Factory(list)
    draft_alerts: List = attr.Factory(list)
    draft_stats: List = attr.Factory(list)
    player_game_attributes: List = attr.Factory(list)
    error_status: List = attr.Factory(list)


