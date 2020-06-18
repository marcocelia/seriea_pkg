import pandas_validator as pv
from seriea_pkg.data import constants

class RoundsValidator(pv.DataFrameValidator):
    column_num = 5
    l_round = pv.IntegerColumnValidator(constants.ROUND, min_value=1, max_value=38)
    l_ghome = pv.IntegerColumnValidator(constants.GOALS_HOME, min_value=0)
    l_gaway = pv.IntegerColumnValidator(constants.GOALS_AWAY, min_value=0)