# -*- coding: utf-8 -*-
'''Timecode config'''

import re 
from proxi.models.timecodeComponents import FrameDelimeter


class Timecode:
    '''Timecode related settings'''

    defaultFrameDelimiter = FrameDelimeter.semiColon
    timecodePattern = re.compile(r"^(\d{2,3}):(\d{2}):(\d{2})[:;](\d{2,3})$")