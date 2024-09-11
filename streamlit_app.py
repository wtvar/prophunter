import time
import tools
import db_imr
import pandas as pd
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt

from config import TEXT_LANDING_PAGE

# Switch to wide-mode for better view
st.set_page_config(layout="wide")

# Display name & widgets in side bar

min_val = st.sidebar.slider(label='Min Diff Percentage', min_value=0, max_value=25, value=2.5, step=0.5)

unique_leagues = db.get_leagues()
selected_leagues = st.sidebar.multiselect(label='Leagues', options=sorted(unique_leagues), default=unique_leagues)
selected_leagues = [f"'{s}'" for s in selected_leagues]
selected_leagues = f"({','.join(selected_leagues)})"

bets = db.get_bets(leagues=selected_leagues, min_val=float(min_diff) / 100)

dataframe = pd.DataFrame(bets)

st.write(dataframe) 
