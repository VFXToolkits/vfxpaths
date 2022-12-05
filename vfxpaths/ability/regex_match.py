#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import enum
import re


class RegexCompile(enum.Enum):
    field_match: re.compile = re.compile(r'{(.+?)}')
    env_match: re.compile = re.compile(r'\[(.+?)\]')
    split_path: re.compile = re.compile(r"([\w_.\-]+)")
    str_path_split = r"([\w_.\-:]+)"
    str_field = r'{(.+?)}'


class MatchModel(enum.Enum):
    stat: int = 0
    center: int = 1
    end: int = 2
    full: int = 3
