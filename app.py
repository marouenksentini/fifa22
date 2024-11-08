import streamlit as st
from statsbombpy import sb
import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt

# Set up the Streamlit app title
st.title("FIFA World Cup 2022 - Passes into Final 3rd")

# Fetch all available competitions
free_comps = sb.competitions()
fifa_male = free_comps[(free_comps['country_name'] == 'International') & 
                       (free_comps['competition_gender'] == 'male') & 
                       (free_comps['match_available_360'].notnull())]

# Dropdown to select a competition and season
competition_id = st.selectbox("Select Competition", fifa_male['competition_id'].unique())
season_id = st.selectbox("Select Season", fifa_male[fifa_male['competition_id'] == competition_id]['season_id'].unique())

# Get matches for the selected competition and season
matches = sb.matches(competition_id=competition_id, season_id=season_id)

# Dropdown to select a match
match_id = st.selectbox("Select Match", matches['match_id'])
match_info = matches[matches['match_id'] == match_id]
team1, team2 = match_info.iloc[0]['home_team'], match_info.iloc[0]['away_team']

# Dropdown to select a team (home or away)
team = st.selectbox("Select Team", [team1, team2])

# Load events for the selected match
events = sb.events(match_id=match_id)

# Extract x, y locations for passes
events[['x', 'y']] = events['location'].apply(pd.Series)
events[['pass_end_x', 'pass_end_y']] = events['pass_end_location'].apply(pd.Series)

# Filter passes for the selected team
passes_df = events[(events.team == team) & 
                   (events.type == "Pass") & 
                   (events.x < 80) & 
                   (events.pass_end_x > 80) & 
                   (events.pass_outcome.isna())]

# Set up the pitch and plot
pass_colour = '#e21017'
pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2, line_color='black')
fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
fig.set_facecolor('white')

# Plot the passes
pitch.arrows(passes_df.x, passes_df.y, passes_df.pass_end_x, passes_df.pass_end_y,
             width=3, headwidth=8, headlength=5, color=pass_colour, ax=ax, zorder=2, label="Pass")
ax.legend(facecolor='white', handlelength=5, edgecolor='None', fontsize=20, loc='best')
ax.set_title(f'{team} Progressions into Final 3rd', fontsize=30, color='black')

# Display the plot in Streamlit
st.pyplot(fig)
