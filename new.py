import polars as pl
import soccerdata as sd
import matplotlib.pyplot as plt
import sklearn as skl

fbref = sd.FBref()
season_stats = fbref.read_team_season_stats(stat_type='shooting')
