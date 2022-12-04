#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import enum
import re


class RegexCompile(enum.Enum):
    field_match: re.compile = re.compile(r'{(.+?)}')
    env_match: re.compile = re.compile(r'\[(.+?)\]')
    split_path: re.compile = re.compile(r"([\w_.\-]+)")


class MatchModel(enum.Enum):
    stat: int = 0
    center: int = 1
    end: int = 2
    full: int = 3
