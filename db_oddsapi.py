import streamlit as st
from sqlalchemy import text
from config import TABLE_BETS

conn = st.connection('oddsapi', type='sql')


@st.cache_data(ttl=10)
def get_bets(leagues: str, min_val: float):

  return conn.query(f"SELECT starts, league, runner_home, runner_away, market, selection, side, line, odds, fair_odds, book, value, timestamp FROM {TABLE_BETS} WHERE league IN {leagues} AND value >= {min_val} ORDER BY starts", ttl=600).to_dict('records')


@st.cache_data(ttl=10)
def get_leagues():

  return conn.query(f"SELECT DISTINCT(league) FROM {TABLE_BETS} WHERE starts >= NOW()", ttl=600)['league'].tolist()
