# dksalaries/dksalaries/util.py
# -*- coding: utf-8 -*-
# Copyright (C) 2021 Eric Truett
# Licensed under the MIT License
import collections
import datetime
import re
from typing import Any, Callable, Dict, List

from dateutil.parser import parse
import pytz


def attr_boiler(d: dict) -> None:
    """Generates attr boilerplate for nested dict
    
    Args:
        d (dict):

    Returns:
        None

    """
    for k, v in d.items():
        if isinstance(v, list):
            print(f'{camel_to_snake(k)}: List')
        elif isinstance(v, dict):
            print(f'{camel_to_snake(k)}: List')
        elif isinstance(v, tuple):
            print(f'{camel_to_snake(k)}: List')
        else:
            print(f'{camel_to_snake(k)}: {striptype(v)}')

            
def camel_to_snake(s: str) -> str:
    """Converts camel-case string to snake string
    
    Args:
        s (str): the camel-cased string

    Returns:
        str

    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()


def flatten(t: List[List[Any]]) -> List[Any]:
    """Flattens nested lists
    
    Args:
        t (List[List]): the nested lists

    Returns:
        List[Any]

    """
    return [item for sublist in t for item in sublist]


def map_nested_dicts(ob: Dict[str, Any], func: Callable) -> Dict[str, Any]:
    """Applies functions to all keys in nested dict"""
    if isinstance(ob, collections.Mapping):
        return {func(k): v for k, v in ob.items()}
    else:
        return func(ob)


def parse_dktime(s: str, as_local: bool = False, tz: str = None) -> datetime.datetime:
    """Parses dk time strings
    
    Args:
        s (str): the datestring
        as_local (bool): UTC or localtime
        tz (str): timezone str, e.g. 'America/Chicago'

    Returns:
        datetime.datetime

    """
    if s.endswith('Z'):
        dt = parse(s)
    elif s.startswith('/Date'):
        epoch = int(''.join([c for c in s if c.isnumeric()])) / 1000
        dt = datetime.datetime.fromtimestamp(epoch, tz=pytz.utc)
    else:
        raise ValueError(f'Invalid datestring: {s}')
    if as_local:
        local_tz = pytz.timezone(tz)
        return dt.astimezone(local_tz)
    return dt


def striptype(v):
    """Strips type information from repr of type(v)
    
    Args:
        v (Any): the value

    Returns:
        str

    """
    if v is None:
        return 'Any'
    return str(type(v)).replace('<class ', '').replace('>', '').replace("'", '')

