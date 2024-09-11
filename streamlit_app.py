import time
import pandas as pd
import streamlit as st
import db_oddsapi as db
from datetime import datetime

st.set_page_config(page_title="PropHunter by BettingIsCool", page_icon="🍀", layout="wide", initial_sidebar_state="expanded")

import db_pinnacle as db

from config import TEXT_LANDING_PAGE

min_val = st.sidebar.slider(label='Min Value Percentage', min_value=0.00, max_value=25.0, value=2.5, step=0.5)

unique_leagues = db.get_leagues()
selected_leagues = st.sidebar.multiselect(label='Leagues', options=sorted(unique_leagues), default=unique_leagues)
selected_leagues = [f"'{s}'" for s in selected_leagues]
selected_leagues = f"({','.join(selected_leagues)})"

unique_books = db.get_books()
selected_books = st.sidebar.multiselect(label='Bookmakers', options=sorted(unique_books), default=unique_books)
selected_books = [f"'{s}'" for s in selected_books]
selected_books = f"({','.join(selected_books)})"

bets = db.get_bets(leagues=selected_leagues, books=selected_books, min_val=float(min_val) / 100)

dataframe = pd.DataFrame(bets)

st.write(dataframe) 
