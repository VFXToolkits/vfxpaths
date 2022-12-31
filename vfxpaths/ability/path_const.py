#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import enum


class FileMatchModel(enum.Enum):
    style1 = '$F'
    style2 = '%0'
    style3 = "#"
