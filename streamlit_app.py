import time
import pandas as pd
import streamlit as st
from st_paywall import add_auth

st.set_page_config(page_title="PropHunter by BettingIsCool", page_icon="🍀", layout="wide", initial_sidebar_state="expanded")

import db_oddsapi as db
from datetime import datetime

from config import TEXT_LANDING_PAGE

placeholder1 = st.empty()
placeholder1.markdown(TEXT_LANDING_PAGE)

add_auth(required=True)

st.write(st.session_state.subscriptions)

placeholder1.empty()


def refresh_table():

  st.cache_data.clear()


def color_cells(val):

  color = 'white'
  if val is not None:
    
    if val > 0.05:
        color = 'green'
    elif val > 0.025:
      color = 'yellow'

  return f'color: {color}'


def highlight_outdated_odds(val):

 if (datetime.now() - val).total_seconds() > 600:
  color = 'red' 
 else:
  color = 'green'
 return f'color: {color}'


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

st.button('Refresh Table', on_click=refresh_table)
bets_df = pd.DataFrame(bets)
bets_df = bets_df.rename(columns={'starts': 'STARTS', 'league': 'LEAGUE', 'runner_home': 'HOME_TEAM', 'runner_away': 'AWAY_TEAM', 'market': 'MARKET', 'selection': 'SELECTION', 'line': 'LINE', 'odds': 'ODDS', 'fair_odds': 'FAIR_ODDS', 'book': 'BOOKMAKER', 'value': 'VALUE', 'timestamp': 'LAST_UPDATE'})
bets_df = bets_df[['STARTS', 'LEAGUE', 'HOME_TEAM', 'AWAY_TEAM', 'MARKET', 'SELECTION', 'LINE', 'ODDS', 'FAIR_ODDS', 'VALUE', 'BOOKMAKER', 'LAST_UPDATE']]
styled_df = bets_df.style.applymap(color_cells, subset=['VALUE']).applymap(highlight_outdated_odds, subset=['LAST_UPDATE']).format({'LINE': '{:g}'.format, 'ODDS': '{:,.3f}'.format, 'FAIR_ODDS': '{:,.3f}'.format, 'VALUE': '{:,.2%}'.format})

if len(bets_df) > 0:
  st.write(styled_df) 
