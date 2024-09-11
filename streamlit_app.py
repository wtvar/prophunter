import time
import pandas as pd
import streamlit as st
import db_oddsapi as db
from datetime import datetime

from config import TEXT_LANDING_PAGE

min_val = st.sidebar.slider(label='Min Value Percentage', min_value=0.00, max_value=25.0, value=2.5, step=0.5)

unique_leagues = db.get_leagues()
selected_leagues = st.sidebar.multiselect(label='Leagues', options=sorted(unique_leagues), default=unique_leagues)
selected_leagues = [f"'{s}'" for s in selected_leagues]
selected_leagues = f"({','.join(selected_leagues)})"

bets = db.get_bets(leagues=selected_leagues, min_val=float(min_val) / 100)

dataframe = pd.DataFrame(bets)

st.write(dataframe) 
