import streamlit as st
import numpy as np
import pandas as pd
import warnings
import pickle
import os

# Basic Functions
warnings.filterwarnings("ignore")
basedir = os.path.join(os.getcwd(), "model")

# Defining Constants and Protected Variables
FONTS = ["cursive", "monospace"]

# Defining Models PATH
TossWinner = pickle.load(open(os.path.join(basedir, "TossWinner", "block_1", "tosswin.pkl"), mode="rb"))
TossDecision = pickle.load(open(os.path.join(basedir, "TossDecision", "classifier.pkl"), mode="rb"))
Winner = pickle.load(open(os.path.join(basedir, "Winner", "best", "best.pkl"), "rb"))


WinnerDecoder = pickle.load(open(os.path.join(basedir, "TossDecision", "Winner.pkl"), mode="rb"))
City = pickle.load(open(os.path.join(basedir, "TossWinner", "City.pkl"), mode="rb"))
Venue = pickle.load(open(os.path.join(basedir, "TossWinner", "Venue.pkl"), mode="rb"))
Teams = pickle.load(open(os.path.join(basedir, "TossWinner", "Team.pkl"), mode="rb"))

STADIUMS = []
for (i, j) in Venue.items():
    if i not in ["punjab cricket association is bindra stadium", "m chinnaswamy stadium", "arun jaitley stadiumi"]:
        STADIUMS.append((i, j))

STADIUMS = dict(STADIUMS)
del Venue

# Defining Decorator Source Code
st.markdown(f'<h1 style="color:magenta;justify-content:center;display:grid;font-family:{str(np.random.choice(FONTS))}">The IPL Predictor</h1>',
            unsafe_allow_html=True)

# Input Values By Users
TEAM_1 = Teams[str(st.selectbox("Team 1", [str(i).capitalize() for (i, j) in Teams.items()])).lower()]
TEAM_2 = Teams[str(st.selectbox("Team 2", [str(i).capitalize() for (i, j) in Teams.items()])).lower()]
VENUE = STADIUMS[str(st.selectbox("Stadium/Venue", [str(i).capitalize() for (i, j) in STADIUMS.items()])).lower()]
CITY = City[str(st.selectbox("City", [str(i).capitalize() for (i, j) in City.items()])).lower()]

# Output_Button
if st.button("Predict"):
    TW = str(WinnerDecoder[
        TEAM_1 if TossWinner.predict([[
            TEAM_1, TEAM_2, CITY, VENUE
        ]])[0] else TEAM_2
    ]).capitalize()

    TD = str({1: "field", 0: "bat"}[
                 int(
                     TossDecision.predict([[
                         TEAM_1, TEAM_2, CITY, VENUE, Teams[TW.lower()]
                     ]])
                 )
             ]).capitalize()

    TX = Winner.predict([[TEAM_1, TEAM_2, VENUE, CITY, Teams[TW.lower()], {"field": 1, "bat": 0}[TD.lower()]]])

    st.success(f"May be, The Winning Team is {str(WinnerDecoder[TEAM_1] if TX else WinnerDecoder[TEAM_2]).capitalize()}.")

    st.table(
            pd.DataFrame({
                "Toss Winner": [str(WinnerDecoder[TEAM_2]).capitalize() if Teams[TW.lower()] == TEAM_1 else str(WinnerDecoder[TEAM_1]).capitalize()],
                "Toss Decision": ["Bat" if TD == "Field" else "Bowl".capitalize()],
                "Prediction": [str(WinnerDecoder[TEAM_1] if TX else WinnerDecoder[TEAM_2]).capitalize()]
            })
        )
