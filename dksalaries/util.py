# dksalaries/dksalaries/util.py
# -*- coding: utf-8 -*-
# Copyright (C) 2021 Eric Truett
# Licensed under the MIT License

import re


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


def striptype(v):
    """Strips type information from repr of type(v)
    
    Args:
        v (Any): the value

    Returns:
        str

    Examples
    >>>striptype(3)
    'int'

    >>>striptype(None)
    'Any'

    """
    if v is None:
        return 'Any'
    return str(type(v)).replace('<class ', '').replace('>', '').replace("'", '')

