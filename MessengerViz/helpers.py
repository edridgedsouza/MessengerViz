#!/usr/bin/env python3
import pandas as pd
from ggplot import *


class Helpers:
    def __init__():
        pass

    def makeDatetime(df):
        return pd.to_datetime(df.Year*10000+df.Month*100+df.Day,
                              format='%Y%m%d')

    def ggplot_theme():
        return theme(axis_text_x = element_text(angle=10))
