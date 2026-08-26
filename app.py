import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="IPL Dashboard",
    layout="wide"
)

st.markdown("""
<style>

/* Sidebar background */
[data-testid="stSidebar"]{
    background: linear-gradient(
        180deg,
        #0f172a,
        #1e3a8a,
        #0f172a
    );
}

/* Sidebar text */
[data-testid="stSidebar"] *{
    color:white;
}

/* Selectbox styling */
.stSelectbox > div > div{
    background-color:#0b1220;
    border-radius:15px;
}

/* Sidebar title */
[data-testid="stSidebar"] h1{
    color:#00c6ff;
}

/* Add blur glass effect */
[data-testid="stSidebar"]{
    backdrop-filter: blur(20px);
    border-right:1px solid rgba(255,255,255,0.1);
}

/* Scrollbar */
::-webkit-scrollbar{
    width:8px;
}

::-webkit-scrollbar-thumb{
    background:#2196f3;
    border-radius:10px;
}

/* Main app background */
[data-testid="stAppViewContainer"]{
    background: linear-gradient(
        135deg,
        #020617,
        #06152f,
        #0a1f44,
        #020617
    );
}

/* Main content transparency */
[data-testid="stHeader"]{
    background: rgba(0,0,0,0);
}

/* Container padding + glass feel */
.block-container{
    padding-top:2rem;
    border-radius:20px;
}

/* Progress bar background */
.stProgress > div > div{
    background-color:#1e3a8a !important;
}

/* Progress fill color */
.stProgress > div > div > div{
    background:linear-gradient(
    90deg,
    #00c6ff,
    #0072ff
    ) !important;
}


/* Dataframe / table background */
[data-testid="stDataFrame"]{
    background:rgba(18,35,75,0.85) !important;
    border-radius:15px;
    border:1px solid rgba(255,255,255,0.1);
    padding:10px;
}

/* Table cells */
[data-testid="stDataFrame"] div{
    color:white !important;
}

/* Header row */
thead tr th{
    background:#1e3a8a !important;
    color:white !important;
}


</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h5 style='color:gray;'>Made with ❤️ by Priyanshu Maurya</h5>",
    unsafe_allow_html=True
)

# -----------------------------------
# LOAD DATA
# -----------------------------------



deliveries = pd.read_csv(
    "deliveries_updated_mens_ipl.csv"
)

batter_stats = pd.read_csv(
    "batter_stats.csv"
)

season_batter_stats = pd.read_csv(
    "season_batter_stats.csv"
)

match_batter_stats = pd.read_csv(
    "match_batter_stats.csv"
)

ball_data = pd.read_csv(
    "IPL_ball_by_ball_updated.csv"
)

bowler_stats = pd.read_csv(
    "bowler_stats.csv"
)

season_bowler_stats = pd.read_csv(
    "season_bowler_stats.csv"
)

match_bowler_stats = pd.read_csv(
    "match_bowler_stats.csv"
)

match_bowler_stats['economy']=round(
    (match_bowler_stats['runs_conceded']*6)/
    match_bowler_stats['balls'],
    2
)

ball_data["over"] = ball_data["ball"].astype(int)

ball_data["phase"]="Middle Overs"

ball_data.loc[
    ball_data["over"]<=6,
    "phase"
]="Powerplay"

ball_data.loc[
    ball_data["over"]>=16,
    "phase"
]="Death Overs"


matches = pd.read_csv(
    "matches_updated_mens_ipl.csv"
)

matches = matches.rename(
    columns={
        'matchId':'match_id'
    }
)


# -----------------------------------
# TITLE
# -----------------------------------

st.title("🏏 IPL Batter Analytics Dashboard")

# -----------------------------------
# SIDEBAR
# -----------------------------------

mode = st.sidebar.radio(
    "Analysis Type",
    [
        "Batting",
        "Bowling"
    ]
)

st.sidebar.header("Filters")

# players = sorted(
#     season_batter_stats['striker'].unique()
# )

if mode=="Batting":

    players = sorted(
        season_batter_stats[
            'striker'
        ].unique()
    )

else:

    players = sorted(
        season_bowler_stats[
            'bowler'
        ].unique()
    )

# PLAYER LIST

if mode=="Batting":

    players = sorted(
        season_batter_stats[
            'striker'
        ].unique()
    )

    player_title="Select Batter"

else:

    players = sorted(
        season_bowler_stats[
            'bowler'
        ].unique()
    )

    player_title="Select Bowler"



# selected_player = st.sidebar.selectbox(
#     player_title,
#     players
# )


if mode=="Batting":

    selected_player = st.sidebar.selectbox(
        "Select Batter",
        players,
        key="batter_box"
    )

else:

    selected_player = st.sidebar.selectbox(
        "Select Bowler",
        players,
        key="bowler_box"
    )




# SEASON LIST

if mode=="Batting":

    seasons=["All"] + sorted(
        season_batter_stats[
            'season'
        ]
        .unique()
        .tolist(),

        reverse=True
    )

else:

    seasons=["All"] + sorted(
        season_bowler_stats[
            'season'
        ]
        .unique()
        .tolist(),

        reverse=True
    )



selected_season = st.sidebar.selectbox(
    "Select Season",
    seasons
)

selected_team = st.sidebar.selectbox(
    "Opponent Team",
    ["All"] +
    sorted(
        ball_data["bowling_team"]
        .dropna()
        .unique()
        .tolist()
    )
)

selected_venue = st.sidebar.selectbox(
    "Venue",
    ["All"] +
    sorted(
        ball_data["venue"]
        .dropna()
        .unique()
        .tolist()
    )
)

selected_phase = st.sidebar.selectbox(
    "Match Phase",
    [
        "All",
        "Powerplay",
        "Middle Overs",
        "Death Overs"
    ]
)

# Match analysis toggle

st.sidebar.markdown("---")
show_match_analysis = st.sidebar.checkbox(
    "Enable Match Analysis"
)

show_season_analysis = st.sidebar.checkbox(
    "Enable Season Analytics"
)

filtered_ball = ball_data[
    ball_data["striker"] == selected_player
]

if selected_season != "All":
    filtered_ball = filtered_ball[
        filtered_ball["season"] == selected_season
    ]

if selected_team != "All":
    filtered_ball = filtered_ball[
        filtered_ball["bowling_team"] == selected_team
    ]

if selected_venue != "All":
    filtered_ball = filtered_ball[
        filtered_ball["venue"] == selected_venue
    ]

if selected_phase != "All":
    filtered_ball = filtered_ball[
        filtered_ball["phase"] == selected_phase
    ]

# -----------------------------------
# CAREER STATS
# -----------------------------------
# st.subheader("📊 Career Snapshot")


# career = batter_stats[
#     batter_stats.iloc[:,0] == selected_player
# ]

# st.header("Career Stats")

# col1,col2,col3,col4,col5 = st.columns(5)

# col1.metric(
#     "Runs",
#     int(career['runs'].values[0])
# )

# col2.metric(
#     "Strike Rate",
#     round(career['SR'].values[0],2)
# )

# # st.progress(
# #     min(
# #         int(career['SR'].values[0]/2),
# #         100
# #     )
# # )

# progress=career['runs'].values[0]/4000

# st.progress(
# min(progress,1.0)
# )

# col3.metric(
#     "Average",
#     round(career['average'].values[0],2)
# )

# col4.metric(
#     "4s",
#     int(career['4s'].values[0])
# )

# col5.metric(
#     "6s",
#     int(career['6s'].values[0])
# )

# ------------------------------------
# CAREER STATS
# ------------------------------------

st.subheader("📊 Career Snapshot")

if mode=="Batting":

    career = batter_stats[
        batter_stats.iloc[:,0]==selected_player
    ]

    st.header("Career Stats")

    col1,col2,col3,col4,col5=st.columns(5)

    col1.metric(
        "Runs",
        int(career['runs'].values[0])
    )

    col2.metric(
        "Strike Rate",
        round(career['SR'].values[0],2)
    )

    progress=career['runs'].values[0]/4000

    st.progress(
        min(progress,1.0)
    )

    col3.metric(
        "Average",
        round(career['average'].values[0],2)
    )

    col4.metric(
        "4s",
        int(career['4s'].values[0])
    )

    col5.metric(
        "6s",
        int(career['6s'].values[0])
    )


else:

    career = bowler_stats[
        bowler_stats['bowler']==selected_player
    ]

    st.header("Career Stats")

    col1,col2,col3,col4,col5=st.columns(5)

    col1.metric(
        "Wickets",
        int(career['wickets'].values[0])
    )

    col2.metric(
        "Economy",
        round(career['economy'].values[0],2)
    )

    progress=career['wickets'].values[0]/150

    st.progress(
        min(progress,1.0)
    )

    col3.metric(
        "Average",
        round(career['average'].values[0],2)
    )

    col4.metric(
        "Strike Rate",
        round(career['SR'].values[0],2)
    )

    col5.metric(
        "Overs",
        round(career['overs'].values[0],1)
    )

# -----------------------------------
# SEASON STATS
# -----------------------------------

# st.header("Season Stats")

# season_data = season_batter_stats[
#     (season_batter_stats['striker']==selected_player)
#     &
#     (season_batter_stats['season']==selected_season)
# ]

# st.dataframe(season_data)

# ------------------------------------
# SEASON STATS
# ------------------------------------

st.header("Season Stats")

if mode=="Batting":

    season_data = season_batter_stats[
        season_batter_stats['striker']
        ==selected_player
    ]

else:

    season_data = season_bowler_stats[
        season_bowler_stats['bowler']
        ==selected_player
    ]


if selected_season!="All":

    season_data = season_data[
        season_data['season']
        ==selected_season
    ]


st.dataframe(
    season_data,
    use_container_width=True,
    height=300
)

# -----------------------------------
# RUNS BY SEASON
# -----------------------------------

# st.header("Runs By Season")

# if selected_season=="All":

#     player_season=season_batter_stats[
#         season_batter_stats["striker"]
#         ==selected_player
#     ]

# else:

#     player_season=season_batter_stats[
#         (season_batter_stats["striker"]
#         ==selected_player)
#         &
#         (season_batter_stats["season"]
#         ==selected_season)
#     ]
   
    
# # fig = px.bar(
# #     player_season,
# #     x='season',
# #     y='runs',
# #     text='runs',
# #     title='Season Runs'
# # )

# # st.plotly_chart(
# #     fig,
# #     use_container_width=True
# # )

# season_stats = season_batter_stats[
#     season_batter_stats['striker']==selected_player
# ]

# # yahi niche add karo
# season_stats['season'] = season_stats['season'].astype(str)

# fig = px.bar(
#     season_stats,
#     x='season',
#     y='runs',
#     text='runs',
#     color='runs',
#     title='Season Runs'
# )

# fig.update_xaxes(type='category')

# st.plotly_chart(
#     fig,
#     use_container_width=True
# )

# ------------------------------------
# RUNS / WICKETS BY SEASON
# ------------------------------------

if mode=="Batting":

    st.header("Runs By Season")

    if selected_season=="All":

        player_season=season_batter_stats[
            season_batter_stats["striker"]
            ==selected_player
        ]

    else:

        player_season=season_batter_stats[
            (season_batter_stats["striker"]
            ==selected_player)

            &

            (season_batter_stats["season"]
            ==selected_season)
        ]

else:

    st.header("Wickets By Season")

    if selected_season=="All":

        player_season=season_bowler_stats[
            season_bowler_stats["bowler"]
            ==selected_player
        ]

    else:

        player_season=season_bowler_stats[
            (season_bowler_stats["bowler"]
            ==selected_player)

            &

            (season_bowler_stats["season"]
            ==selected_season)
        ]


player_season['season']=player_season[
    'season'
].astype(str)


if mode=="Batting":

    fig=px.bar(
        player_season,
        x='season',
        y='runs',
        text='runs',
        color='runs',
        title='Season Runs'
    )

else:

    fig=px.bar(
        player_season,
        x='season',
        y='wickets',
        text='wickets',
        color='wickets',
        title='Season Wickets'
    )


fig.update_xaxes(type='category')

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# STRIKE RATE TREND
# -----------------------------------

# st.header("Strike Rate Trend")

# fig2 = px.line(
#     player_season,
#     x='season',
#     y='SR',
#     markers=True
# )

# st.plotly_chart(
#     fig2,
#     use_container_width=True
# )

# ------------------------------------
# STRIKE RATE / ECONOMY TREND
# ------------------------------------

if mode=="Batting":

    st.header("Strike Rate Trend")

    trend_data = season_batter_stats[
        season_batter_stats["striker"]
        ==selected_player
    ]

    y_col='SR'
    title='Strike Rate Trend'


else:

    st.header("Economy Trend")

    trend_data = season_bowler_stats[
        season_bowler_stats["bowler"]
        ==selected_player
    ]

    y_col='economy'
    title='Economy Trend'


if selected_season!="All":

    trend_data=trend_data[
        trend_data["season"]
        ==selected_season
    ]


trend_data['season']=trend_data[
    'season'
].astype(str)


fig=px.line(
    trend_data,
    x='season',
    y=y_col,
    markers=True,
    text=y_col,
    title=title
)

fig.update_xaxes(
    type='category'
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# VENUE ANALYSIS
# -----------------------------------

# st.header("Venue-wise Runs")

# venue_data = match_batter_stats[
#     match_batter_stats['striker']
#     == selected_player
# ]

# if selected_season != "All":
#     venue_data = venue_data[
#         venue_data['season']
#         == selected_season
#     ]

# venue_data = venue_data.groupby(
#     'venue'
# )['runs'].sum().reset_index()

# fig3 = px.bar(
#     venue_data,
#     x='venue',
#     y='runs'
# )

# st.plotly_chart(fig3, use_container_width=True)

# --------------------------------
# VENUE ANALYSIS
# --------------------------------

st.header("Venue-wise Performance")

# -------- Batting --------

if mode=="Batting":

    venue_data = match_batter_stats[
        match_batter_stats['striker']
        == selected_player
    ]

    # season filter
    if selected_season!="All":
        venue_data=venue_data[
            venue_data['season']
            == selected_season
        ]

    # opponent filter
    if selected_team!="All":
        venue_data=venue_data[
            venue_data['bowling_team']
            == selected_team
        ]

    # venue filter
    if selected_venue!="All":
        venue_data=venue_data[
            venue_data['venue']
            == selected_venue
        ]

    # group
    venue_data=venue_data.groupby(
        'venue',
        as_index=False
    )['runs'].sum()

    venue_data=venue_data.sort_values(
        by='runs',
        ascending=False
    )

    fig3=px.bar(
        venue_data,
        x='venue',
        y='runs',
        text='runs',
        color='runs',
        title='Venue-wise Runs'
    )


# -------- Bowling --------

else:

    venue_data = match_bowler_stats[
        match_bowler_stats['bowler']
        == selected_player
    ]

    # season filter
    if selected_season!="All":
        venue_data=venue_data[
            venue_data['season']
            == selected_season
        ]

    # opponent filter
    if selected_team!="All":
        venue_data=venue_data[
            venue_data['batting_team']
            == selected_team
        ]

    # venue filter
    if selected_venue!="All":
        venue_data=venue_data[
            venue_data['venue']
            == selected_venue
        ]

    venue_data=venue_data.groupby(
        'venue',
        as_index=False
    )['wickets'].sum()

    venue_data=venue_data.sort_values(
        by='wickets',
        ascending=False
    )

    fig3=px.bar(
        venue_data,
        x='venue',
        y='wickets',
        text='wickets',
        color='wickets',
        title='Venue-wise Wickets'
    )


st.plotly_chart(
    fig3,
    use_container_width=True
)

# -----------------------------------
# TEAM ANALYSIS
# -----------------------------------

# st.header("Runs Against Teams")

# team_data = match_batter_stats[
#     match_batter_stats['striker']
#     == selected_player
# ]

# if selected_season != "All":
#     team_data = team_data[
#         team_data['season']
#         == selected_season
#     ]

# team_data = team_data.groupby(
#     'bowling_team'
# )['runs'].sum().reset_index()

# fig4 = px.bar(
#     team_data,
#     x='bowling_team',
#     y='runs'
# )

# st.plotly_chart(fig4, use_container_width=True)

# --------------------------------
# TEAM ANALYSIS
# --------------------------------

st.header("Team-wise Performance")


# ---------- BATTING ----------

if mode=="Batting":

    team_data = match_batter_stats[
        match_batter_stats['striker']
        == selected_player
    ]

    # season
    if selected_season!="All":
        team_data=team_data[
            team_data['season']
            == selected_season
        ]

    # venue
    if selected_venue!="All":
        team_data=team_data[
            team_data['venue']
            == selected_venue
        ]

    # opponent
    if selected_team!="All":
        team_data=team_data[
            team_data['bowling_team']
            == selected_team
        ]


    team_data=team_data.groupby(
        'bowling_team',
        as_index=False
    )['runs'].sum()

    team_data=team_data.sort_values(
        by='runs',
        ascending=False
    )

    fig4=px.bar(
        team_data,
        x='bowling_team',
        y='runs',
        text='runs',
        color='runs',
        title='Runs Against Teams'
    )


# ---------- BOWLING ----------

else:

    team_data = match_bowler_stats[
        match_bowler_stats['bowler']
        == selected_player
    ]

    # season
    if selected_season!="All":
        team_data=team_data[
            team_data['season']
            == selected_season
        ]

    # venue
    if selected_venue!="All":
        team_data=team_data[
            team_data['venue']
            == selected_venue
        ]

    # opponent
    if selected_team!="All":
        team_data=team_data[
            team_data['batting_team']
            == selected_team
        ]



    team_data=team_data.groupby(
        'batting_team',
        as_index=False
    )['wickets'].sum()

    team_data=team_data.sort_values(
        by='wickets',
        ascending=False
    )

    fig4=px.bar(
        team_data,
        x='batting_team',
        y='wickets',
        text='wickets',
        color='wickets',
        title='Wickets Against Teams'
    )


st.plotly_chart(
    fig4,
    use_container_width=True
)

# -------------------------------
# TREND ANALYSIS
# -------------------------------

st.header("📈 Trend Analysis")

if mode=="Batting":

    trend_data=season_batter_stats[
        season_batter_stats['striker']
        == selected_player
    ]

    trend_data=trend_data.sort_values(
        by='season'
    )

    trend_data['season'] = trend_data['season'].astype(str)
    
    fig=px.line(
        trend_data,
        x='season',
        y=['runs','SR','average'],
        markers=True,
        title='Batting Trends'
    )

else:

    trend_data=season_bowler_stats[
        season_bowler_stats['bowler']
        == selected_player
    ]

    trend_data=trend_data.sort_values(
        by='season'
    )

    trend_data['season'] = trend_data['season'].astype(str)

    fig=px.line(
        trend_data,
        x='season',
        y=['wickets','economy','average'],
        markers=True,
        title='Bowling Trends'
    )

fig.update_xaxes(type='category')

st.plotly_chart(
    fig,
    use_container_width=True
)


# -----------------------------------
# TOP INNINGS
# -----------------------------------



# st.header("Top Innings")

# # minimum score filter
# search_runs = st.slider(
#     "Minimum Runs",
#     0,
#     150,
#     50
# )

# player_matches = match_batter_stats[
#     (match_batter_stats['striker'] == selected_player)
#     &
#     (match_batter_stats['season'] == selected_season)
# ]

# if selected_team != "All":
#     player_matches = player_matches[
#         player_matches['bowling_team'] == selected_team
#     ]

# if selected_venue != "All":
#     player_matches = player_matches[
#         player_matches['venue'] == selected_venue
#     ]



# # filter score
# player_matches = player_matches[
#     player_matches['runs'] >= search_runs
# ]

# player_matches = player_matches.sort_values(
#     by='runs',
#     ascending=False
# ).head(10)

# # st.dataframe(
# #     player_matches,
# #     use_container_width=True,
# #     height=400
# # )

# st.data_editor(
# player_matches,
# use_container_width=True
# )

# bubble chart
# fig = px.scatter(
#     player_matches,
#     x='balls',
#     y='runs',
#     size='6s',
#     color='SR',
#     hover_data=[
#         'bowling_team',
#         'venue'
#     ],
#     title="Top Innings Analysis"
# )

# st.plotly_chart(
#     fig,
#     use_container_width=True
# )

# ------------------------------------
# TOP INNINGS / TOP SPELLS
# ------------------------------------

if mode=="Batting":

    st.header("🔥 Top Innings")

    search_runs=st.slider(
        "Minimum Runs",
        0,
        150,
        50
    )

    player_matches=match_batter_stats[
        match_batter_stats['striker']
        ==
        selected_player
    ]

    if selected_season!="All":

        player_matches=player_matches[
            player_matches['season']
            ==
            selected_season
        ]

    if selected_team!="All":

        player_matches=player_matches[
            player_matches['bowling_team']
            ==
            selected_team
        ]

    if selected_venue!="All":

        player_matches=player_matches[
            player_matches['venue']
            ==
            selected_venue
        ]


    player_matches=player_matches[
        player_matches['runs']
        >=
        search_runs
    ]


    player_matches=player_matches.sort_values(
        by='runs',
        ascending=False
    ).head(10)


else:

    st.header("🎯 Top Bowling Spells")

    min_wickets=st.slider(
        "Minimum Wickets",
        0,
        6,
        1
    )


    player_matches=match_bowler_stats[
        match_bowler_stats['bowler']
        ==
        selected_player
    ]


    if selected_season!="All":

        player_matches=player_matches[
            player_matches['season']
            ==
            selected_season
        ]


    if selected_team!="All":

        player_matches=player_matches[
            player_matches['batting_team']
            ==
            selected_team
        ]


    if selected_venue!="All":

        player_matches=player_matches[
            player_matches['venue']
            ==
            selected_venue
        ]


    player_matches=player_matches[
        player_matches['wickets']
        >=
        min_wickets
    ]


    player_matches=player_matches.sort_values(
        by=['wickets','economy'],
        ascending=[False,True]
    ).head(10)
    
   



st.data_editor(
    player_matches,
    use_container_width=True
)

# fig=px.scatter(
# player_matches,
# x='balls',
# y='runs',
# size='6s',
# color='SR',
# hover_name='bowling_team',
# animation_frame='season',
# title='🔥 Top Innings Analysis'
# )

# st.plotly_chart(
# fig,
# use_container_width=True
# )

player_matches['season']=player_matches['season'].astype(str)

if mode=="Batting":

    fig=px.scatter(
        player_matches,
        x='balls',
        y='runs',
        size='6s',
        color='SR',
        hover_name='bowling_team',
        animation_frame='season',
        title='🔥 Top Innings Analysis'
    )

else:

    fig=px.scatter(
        player_matches,
        x='overs',
        y='wickets',
        size='wickets',
        color='economy',
        hover_name='batting_team',
        animation_frame='season',
        title='🎯 Bowling Spell Analysis'
    )


st.plotly_chart(
    fig,
    use_container_width=True
)

# Performace breakdown

# st.subheader("Performance Breakdown")

# col1,col2 = st.columns(2)

# with col1:

#     team_runs = player_matches.groupby(
#         'bowling_team',
#         as_index=False
#     )['runs'].sum()

#     fig = px.treemap(
#         team_runs,
#         path=['bowling_team'],
#         values='runs',
#         color='runs',
#         title='Runs Distribution vs Teams'
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )


# with col2:

#     venue_runs = player_matches.groupby(
#         'venue',
#         as_index=False
#     )['runs'].sum()

#     venue_runs = venue_runs.sort_values(
#         by='runs',
#         ascending=False
#     )

#     fig = px.funnel(
#         venue_runs,
#         x='runs',
#         y='venue',
#         title='Venue Performance'
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )
    

# Performance breakdown

st.subheader("Performance Breakdown")

col1,col2=st.columns(2)

with col1:

    if mode=="Batting":

        team_data=player_matches.groupby(
            'bowling_team',
            as_index=False
        )['runs'].sum()

        fig=px.treemap(
            team_data,
            path=['bowling_team'],
            values='runs',
            color='runs',
            title='Runs Distribution vs Teams'
        )

    else:

        team_data=player_matches.groupby(
            'batting_team',
            as_index=False
        )['wickets'].sum()

        fig=px.treemap(
            team_data,
            path=['batting_team'],
            values='wickets',
            color='wickets',
            title='Wickets Distribution vs Teams'
        )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    if mode=="Batting":

        venue_data=player_matches.groupby(
            'venue',
            as_index=False
        )['runs'].sum()

        venue_data=venue_data.sort_values(
            by='runs',
            ascending=False
        )

        fig=px.funnel(
            venue_data,
            x='runs',
            y='venue',
            title='Venue Performance'
        )

    else:

        venue_data=player_matches.groupby(
            'venue',
            as_index=False
        )['wickets'].sum()

        venue_data=venue_data.sort_values(
            by='wickets',
            ascending=False
        )

        fig=px.funnel(
            venue_data,
            x='wickets',
            y='venue',
            title='Venue Wicket Performance'
        )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

# Match analysis

def generate_points_table(season_matches):

        teams = pd.unique(
            season_matches[["team1", "team2"]].values.ravel()
        )

        points = []

        for team in teams:

            played = len(
                season_matches[
                    (season_matches["team1"] == team)
                    |
                    (season_matches["team2"] == team)
                ]
            )

            won = len(
                season_matches[
                    season_matches["winner"] == team
                ]
            )

            lost = played - won

            pts = won * 2

            points.append({
                "Team": team,
                "Played": played,
                "Won": won,
                "Lost": lost,
                "Points": pts
            })

        table = pd.DataFrame(points)

        table = table.sort_values(
            ["Points", "Won"],
            ascending=False
        )

        table.reset_index(drop=True, inplace=True)

        table.index += 1

        return table

if show_match_analysis:

    st.header("🏏 Match Analysis")

    # season selector
    seasons = sorted(
        matches['season'].unique(),
        reverse=True
    )

    selected_match_season = st.selectbox(
        "Select Season",
        seasons
    )


    # selected season ka data
    season_matches = matches[
        matches['season']
        ==
        selected_match_season
    ].copy()


    # readable match name
    season_matches['match_label'] = (
        season_matches['team1']
        + " vs "
        + season_matches['team2']
        + " | "
        + season_matches['date'].astype(str)
    )


    # dropdown
    selected_match_label = st.selectbox(
        "Select Match",
        season_matches['match_label']
    )


    # label se match id nikalna
    selected_match_id = season_matches[
        season_matches['match_label']
        ==
        selected_match_label
    ]['match_id'].values[0]


    # match data
    match_info = season_matches[
        season_matches['match_id']
        ==
        selected_match_id
    ]


     # ---------------------------
    # Extract Values
    # ---------------------------

    winner = match_info[
        'winner'
    ].values[0]


    potm = match_info[
        'player_of_match'
    ].values[0]


    venue = match_info[
        'venue'
    ].values[0]


    toss = match_info[
        'toss_winner'
    ].values[0]



    # ---------------------------
    # Margin
    # ---------------------------

    if match_info[
        'winner_runs'
    ].values[0] > 0:

        margin = str(

            match_info[
                'winner_runs'
            ].values[0]

        ) + " runs"

    else:

        margin = str(

            match_info[
                'winner_wickets'
            ].values[0]

        ) + " wickets"



    st.markdown("---")

    col1,col2,col3,col4,col5 = st.columns(5)

    with col1:
        st.markdown("🏆 **Winner**")
        st.info(winner)

    with col2:
        st.markdown("⭐ **POTM**")
        st.info(potm)

    with col3:
        st.markdown("🎯 **Margin**")
        st.info(margin)

    with col4:
        st.markdown("🏟 **Venue**")
        st.info(venue)

    with col5:
        st.markdown("🪙 **Toss Winner**")
        st.info(toss)


    # Match score summary
    # st.write(selected_match_id)

    st.header("📊 Match Score Summary")

    # selected match ka ball-by-ball data
    match_ball = ball_data[
        ball_data['match_id'] == selected_match_id
    ]

    # innings 1
    innings1 = match_ball[
        match_ball['innings'] == 1
    ]

    team1 = innings1['batting_team'].iloc[0]

    score1 = (
        innings1['runs_off_bat'].sum()
        +
        innings1['extras'].sum()
    )

    wickets1 = innings1['player_dismissed'].notna().sum()

    # overs1 = innings1['over'].max()
    overs1 = round(innings1['ball'].max(),1)
    # innings 2
    innings2 = match_ball[
        match_ball['innings'] == 2
    ]

    team2 = innings2['batting_team'].iloc[0]

    score2 = (
        innings2['runs_off_bat'].sum()
        +
        innings2['extras'].sum()
    )

    wickets2 = innings2['player_dismissed'].notna().sum()

    # overs2 = innings2['over'].max()
    overs2 = round(innings2['ball'].max(),1)
    # top scorer innings 1
    top_batter1 = innings1.groupby(
        'striker'
    )['runs_off_bat'].sum().reset_index()

    top_batter1 = top_batter1.sort_values(
        by='runs_off_bat',
        ascending=False
    )

    top_batter1_name = top_batter1.iloc[0]['striker']

    top_batter1_runs = top_batter1.iloc[0]['runs_off_bat']


    # top scorer innings 2
    top_batter2 = innings2.groupby(
        'striker'
    )['runs_off_bat'].sum().reset_index()

    top_batter2 = top_batter2.sort_values(
        by='runs_off_bat',
        ascending=False
    )

    top_batter2_name = top_batter2.iloc[0]['striker']

    top_batter2_runs = top_batter2.iloc[0]['runs_off_bat']


    # display
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        ### {team1}
        🏏 **{score1}/{wickets1}**
        
        Overs: {overs1}
        
        🔥 Top Scorer:
        {top_batter1_name} ({top_batter1_runs})
        """)

    with col2:
        st.markdown(f"""
        ### {team2}
        🏏 **{score2}/{wickets2}**
        
        Overs: {overs2}

        🔥 Top Scorer:
        {top_batter2_name} ({top_batter2_runs})
        """)


    st.header("📈 Worm Chart")
    # Innings 1 over-wise runs
    worm1 = match_ball[
        match_ball['innings'] == 1
    ].groupby('over')[
        ['runs_off_bat', 'extras']
    ].sum()

    worm1['runs'] = (
        worm1['runs_off_bat']
        + worm1['extras']
    )

    worm1['cumulative_runs'] = worm1['runs'].cumsum()


    # Innings 2 over-wise runs
    worm2 = match_ball[
        match_ball['innings'] == 2
    ].groupby('over')[
        ['runs_off_bat', 'extras']
    ].sum()

    worm2['runs'] = (
        worm2['runs_off_bat']
        + worm2['extras']
    )

    worm2['cumulative_runs'] = worm2['runs'].cumsum()
    
    worm_fig = px.line()

    worm_fig.add_scatter(
        x=worm1.index,
        y=worm1['cumulative_runs'],
        mode='lines+markers',
        name=team1
    )

    worm_fig.add_scatter(
        x=worm2.index,
        y=worm2['cumulative_runs'],
        mode='lines+markers',
        name=team2
    )

    worm_fig.update_layout(
        xaxis_title="Overs",
        yaxis_title="Runs",
        height=500
    )

    st.plotly_chart(
        worm_fig,
        use_container_width=True
    )

    st.header("🏙️ Manhattan Chart")

    manhattan1 = match_ball[
        match_ball['innings'] == 1
    ].groupby('over')[
        ['runs_off_bat', 'extras']
    ].sum()

    manhattan1['runs'] = (
        manhattan1['runs_off_bat']
        + manhattan1['extras']
    )

    manhattan2 = match_ball[
        match_ball['innings'] == 2
    ].groupby('over')[
        ['runs_off_bat', 'extras']
    ].sum()

    manhattan2['runs'] = (
        manhattan2['runs_off_bat']
        + manhattan2['extras']
    )


    manhattan_fig = go.Figure()

    manhattan_fig.add_bar(
        x=manhattan1.index,
        y=manhattan1['runs'],
        name=team1
    )

    manhattan_fig.add_bar(
        x=manhattan2.index,
        y=manhattan2['runs'],
        name=team2
    )

    manhattan_fig.update_layout(
        barmode='group',
        xaxis_title='Overs',
        yaxis_title='Runs'
    )

    st.plotly_chart(
        manhattan_fig,
        use_container_width=True
    )

    # Fall of Wickets

    st.header("🏏 Fall of Wickets")

    fow1 = innings1[
        innings1['player_dismissed'].notna()
    ].copy()

    fow1['wicket_no'] = range(1, len(fow1)+1)

    scores = []
    for _, row in fow1.iterrows():

        score = innings1[
            (innings1['over'] < row['over']) |
            (
                (innings1['over'] == row['over']) &
                (innings1['ball'] <= row['ball'])
            )
        ]

        scores.append(
            score['runs_off_bat'].sum()
            + score['extras'].sum()
        )

    fow1['score'] = scores

    fow1['over_ball'] = fow1['over']
    
    fow2 = innings2[
        innings2['player_dismissed'].notna()
    ].copy()

    fow2['wicket_no'] = range(1, len(fow2)+1)

    scores = []
    for _, row in fow2.iterrows():

        score = innings2[
            (innings2['over'] < row['over']) |
            (
                (innings2['over'] == row['over']) &
                (innings2['ball'] <= row['ball'])
            )
        ]

        scores.append(
            score['runs_off_bat'].sum()
            + score['extras'].sum()
        )

    fow2['score'] = scores

    fow2['over_ball'] = fow2['over']

    fow_fig = go.Figure()

    fow_fig.add_scatter(
        x=fow1['over'],
        y=fow1['score'],
        mode='markers+text',

        marker=dict(
            size=10,
            color='gold'
        ),

        text=[
            f"{score}/{wk}"
            for score, wk in zip(
                fow1['score'],
                fow1['wicket_no']
            )
        ],

        textposition=[
            'top left',
            'top right',
            'bottom left',
            'bottom right',
            'top center'
        ] * 10,

        name=team1,

        customdata=list(
            zip(
                fow1['player_dismissed'],
                fow1['bowler'],
                fow1['wicket_no'],
                fow1['ball']
            )
        ),

        hovertemplate=
        "<b>Wicket %{customdata[2]}</b><br>" +
        "Batsman: %{customdata[0]}<br>" +
        "Bowler: %{customdata[1]}<br>" +
        "Score: %{y}<br>" +
        "Over: %{customdata[3]}<extra></extra>"
    )

    fow_fig.add_scatter(
        x=fow2['over'],
        y=fow2['score'],
        mode='markers+text',

        marker=dict(
            size=10,
            color='deepskyblue'
        ),

        text=[
            f"{score}/{wk}"
            for score, wk in zip(
                fow2['score'],
                fow2['wicket_no'],
            )
        ],

        textposition=[
            'top left',
            'top right',
            'bottom left',
            'bottom right',
            'top center'
        ] * 10,

        name=team2,

        customdata=list(
            zip(
                fow2['player_dismissed'],
                fow2['bowler'],
                fow2['wicket_no'],
                fow2['ball']
            )
        ),

        hovertemplate=
        "<b>Wicket %{customdata[2]}</b><br>" +
        "Batsman: %{customdata[0]}<br>" +
        "Bowler: %{customdata[1]}<br>" +
        "Score: %{y}<br>" +
        "Over: %{customdata[3]}<extra></extra>"
    )

    fow_fig.update_layout(
        title="Fall of Wickets",
        xaxis_title="Overs",
        yaxis_title="Team Score",
        height=600,
        hovermode="closest"
    )
    st.plotly_chart(
        fow_fig,
        use_container_width=True
    ) 

    # Scorecard(Batting+Bowling)
    
    st.header("📋 Scorecards")

    # =====================
    # Batting Scorecards
    # =====================

    batting1 = innings1.groupby(
        'striker'
    ).agg(
        Runs=('runs_off_bat','sum'),
        Balls=('runs_off_bat','count')
    ).reset_index()

    batting1.rename(
        columns={'striker':'Batsman'},
        inplace=True
    )

    batting1['SR'] = round(
        batting1['Runs'] * 100 / batting1['Balls'],
        2
    )

    # Fours
    fours1 = innings1[
        innings1['runs_off_bat'] == 4
    ].groupby('striker').size()

    batting1['4s'] = batting1['Batsman'].map(
        fours1
    ).fillna(0).astype(int)


    # Sixes
    sixes1 = innings1[
        innings1['runs_off_bat'] == 6
    ].groupby('striker').size()

    batting1['6s'] = batting1['Batsman'].map(
        sixes1
    ).fillna(0).astype(int)

    batting2 = innings2.groupby(
        'striker'
    ).agg(
        Runs=('runs_off_bat','sum'),
        Balls=('runs_off_bat','count')
    ).reset_index()

    batting2.rename(
        columns={'striker':'Batsman'},
        inplace=True
    )

    batting2['SR'] = round(
        batting2['Runs'] * 100 / batting2['Balls'],
        2
    )

    # Fours
    fours2 = innings2[
        innings2['runs_off_bat'] == 4
    ].groupby('striker').size()

    batting2['4s'] = batting2['Batsman'].map(
        fours2
    ).fillna(0).astype(int)


    # Sixes
    sixes2 = innings2[
        innings2['runs_off_bat'] == 6
    ].groupby('striker').size()

    batting2['6s'] = batting2['Batsman'].map(
        sixes2
    ).fillna(0).astype(int)

    dismissal1 = innings1[
        innings1['player_dismissed'].notna()
    ][
        ['player_dismissed','bowler']
    ].drop_duplicates()

    dismissal_dict1 = dict(
        zip(
            dismissal1['player_dismissed'],
            dismissal1['bowler']
        )
    )

    batting1['Dismissal'] = batting1['Batsman'].map(
        dismissal_dict1
    )

    batting1['Dismissal'] = batting1['Dismissal'].fillna(
        'Not Out'
    )

    batting1 = batting1[
        [
            'Batsman',
            'Dismissal',
            'Runs',
            'Balls',
            '4s',
            '6s',
            'SR'
        ]
    ]

    batting1 = batting1.sort_values(
        'Runs',
        ascending=False
    )

    dismissal2 = innings2[
        innings2['player_dismissed'].notna()
    ][
        ['player_dismissed','bowler']
    ].drop_duplicates()

    dismissal_dict2 = dict(
        zip(
            dismissal2['player_dismissed'],
            dismissal2['bowler']
        )
    )

    batting2['Dismissal'] = batting2['Batsman'].map(
        dismissal_dict2
    )

    batting2['Dismissal'] = batting2['Dismissal'].fillna(
        'Not Out'
    )

    batting2 = batting2[
        [
            'Batsman',
            'Dismissal',
            'Runs',
            'Balls',
            '4s',
            '6s',
            'SR'
        ]
    ]

    batting2 = batting2.sort_values(
        'Runs',
        ascending=False
    )

    # =====================
    # Bowling Scorecards
    # =====================

    bowling1 = innings2.groupby(
        'bowler'
    ).agg(
        Runs=('runs_off_bat','sum'),
        Extras=('extras','sum')
    ).reset_index()

    bowling1['Runs'] = (
        bowling1['Runs']
        + bowling1['Extras']
    )

    runs1 = innings2.groupby('bowler').apply(
        lambda x:
            x['runs_off_bat'].sum()
            + x['wides'].fillna(0).sum()
            + x['noballs'].fillna(0).sum()
    )

    bowling1['Runs'] = (
        bowling1['bowler']
        .map(runs1)
        .fillna(0)
        .astype(int)
    )

    wickets1 = innings2[
        innings2['player_dismissed'].notna()
    ].groupby(
        'bowler'
    ).size()

    bowling1['Wickets'] = bowling1[
        'bowler'
    ].map(
        wickets1
    ).fillna(0).astype(int)

    # overs1 = innings2.groupby(
    #     'bowler'
    # ).size()

    legal_balls1 = innings2[
        innings2['wides'].isna()
        &
        innings2['noballs'].isna()
    ]

    overs1 = legal_balls1.groupby(
        'bowler'
    ).size()
    # st.write("OVERS1")
    # st.write(overs1)
    bowling1['Balls'] = bowling1[
        'bowler'
    ].map(
        overs1
    )

    # st.dataframe(
    #     bowling1[['bowler','Balls']]
    # )
    nb1 = innings2.groupby(
        'bowler'
    )['noballs'].sum()

    bowling1['NB'] = (
        bowling1['bowler']
        .map(nb1)
        .fillna(0)
        .astype(int)
    )
    
    wd1 = innings2.groupby(
        'bowler'
    )['wides'].sum()

    bowling1['WD'] = (
        bowling1['bowler']
        .map(wd1)
        .fillna(0)
        .astype(int)
    )
    
    bowling1['M'] = 0
    
    bowling1['Overs'] = (
        (bowling1['Balls'] // 6).astype(str)
        + "."
        + (bowling1['Balls'] % 6).astype(str)
    )

    bowling1['Economy'] = round(
        bowling1['Runs']
        /
        (bowling1['Balls'] / 6),
        2
    )

    maiden1 = {}

    for bowler in innings2['bowler'].dropna().unique():

        bowler_df = innings2[
            innings2['bowler'] == bowler
        ]

        over_runs = bowler_df.groupby('over').apply(
            lambda x:
            x['runs_off_bat'].sum()
            + x['wides'].fillna(0).sum()
            + x['noballs'].fillna(0).sum()
        )

        maiden1[bowler] = (over_runs == 0).sum()

    bowling1['M'] = (
        bowling1['bowler']
        .map(maiden1)
        .fillna(0)
        .astype(int)
    )

    bowling1.rename(
        columns={
            'bowler':'Bowler'
        },
        inplace=True
    )

    bowling1 = bowling1[
        [
            'Bowler',
            'Overs',
            'M',
            'Runs',
            'Wickets',
            'NB',
            'WD',
            'Economy'
        ]
    ]

    bowling1 = bowling1.sort_values(
        'Wickets',
        ascending=False
    )

    bowling2 = innings1.groupby(
        'bowler'
    ).agg(
        Runs=('runs_off_bat','sum'),
        Extras=('extras','sum')
    ).reset_index()

    bowling2['Runs'] = (
        bowling2['Runs']
        + bowling2['Extras']
    )

    runs2 = innings1.groupby('bowler').apply(
        lambda x:
            x['runs_off_bat'].sum()
            + x['wides'].fillna(0).sum()
            + x['noballs'].fillna(0).sum()
    )

    bowling2['Runs'] = (
        bowling2['bowler']
        .map(runs2)
        .fillna(0)
        .astype(int)
    )

    wickets2 = innings1[
        innings1['player_dismissed'].notna()
    ].groupby(
        'bowler'
    ).size()

    bowling2['Wickets'] = bowling2[
        'bowler'
    ].map(
        wickets2
    ).fillna(0).astype(int)

    # Legal balls only
    legal_balls2 = innings1[
        innings1['wides'].isna()
        &
        innings1['noballs'].isna()
    ]

    # Balls bowled by each bowler
    overs2 = legal_balls2.groupby(
        'bowler'
    ).size()

    # Balls column
    bowling2['Balls'] = bowling2[
        'bowler'
    ].map(
        overs2
    )

    nb2 = innings1.groupby(
        'bowler'
    )['noballs'].sum()

    bowling2['NB'] = (
        bowling2['bowler']
        .map(nb2)
        .fillna(0)
        .astype(int)
    )

    wd2 = innings1.groupby(
        'bowler'
    )['wides'].sum()

    bowling2['WD'] = (
        bowling2['bowler']
        .map(wd2)
        .fillna(0)
        .astype(int)
    )
    bowling2['M'] = 0
    # Overs in cricket format
    bowling2['Overs'] = (
        (bowling2['Balls'] // 6).astype(int).astype(str)
        + "."
        + (bowling2['Balls'] % 6).astype(int).astype(str)
    )

    # Economy
    bowling2['Economy'] = round(
        bowling2['Runs']
        /
        (bowling2['Balls'] / 6),
        2
    )

    maiden2 = {}

    for bowler in innings1['bowler'].dropna().unique():

        bowler_df = innings1[
            innings1['bowler'] == bowler
        ]

        over_runs = bowler_df.groupby('over').apply(
            lambda x:
            x['runs_off_bat'].sum()
            + x['wides'].fillna(0).sum()
            + x['noballs'].fillna(0).sum()
        )

        maiden2[bowler] = (over_runs == 0).sum()

    bowling2['M'] = (
        bowling2['bowler']
        .map(maiden2)
        .fillna(0)
        .astype(int)
    )

    bowling2.rename(
        columns={
            'bowler':'Bowler'
        },
        inplace=True
    )

    bowling2 = bowling2[
        [
            'Bowler',
            'Overs',
            'M',
            'Runs',
            'Wickets',
            'NB',
            'WD',
            'Economy'
        ]
    ]

    bowling2 = bowling2.sort_values(
        ['Wickets','Economy'],
        ascending=[False,True]
    )

    def calculate_partnerships(innings):

        partnerships = []

        current_runs = 0
        current_balls = 0

        batter1 = innings.iloc[0]['striker']
        batter2 = innings.iloc[0]['non_striker']

        for _, row in innings.iterrows():

            if batter1 is None or batter2 is None:

                players = [row['striker'], row['non_striker']]

                if batter1 is None:
                    batter1 = players[0] if players[0] != batter2 else players[1]

                if batter2 is None:
                    batter2 = players[0] if players[0] != batter1 else players[1]

            current_runs += (
                row['runs_off_bat']
                + row['extras']
            )

            current_balls += 1

            if pd.notna(row['player_dismissed']):

                partnerships.append({
                    "Batter1": batter1,
                    "Batter2": batter2,
                    "Runs": current_runs,
                    "Balls": current_balls
                })

                current_runs = 0
                current_balls = 0

                dismissed = row['player_dismissed']

                if dismissed == batter1:
                    batter1 = None

                elif dismissed == batter2:
                    batter2 = None

                continue

        if current_runs > 0:

            partnerships.append({
                "Batter1": batter1,
                "Batter2": batter2,
                "Runs": current_runs,
                "Balls": current_balls
            })

        return pd.DataFrame(partnerships)

    def phase_analysis(innings):

        powerplay = innings[innings['over'] < 6]

        middle = innings[
            (innings['over'] >= 6)
            & (innings['over'] < 16)
        ]

        death = innings[innings['over'] >= 16]

        return pd.DataFrame({
            "Phase": ["Powerplay", "Middle Overs", "Death Overs"],

            "Runs": [
                (powerplay['runs_off_bat'] + powerplay['extras']).sum(),
                (middle['runs_off_bat'] + middle['extras']).sum(),
                (death['runs_off_bat'] + death['extras']).sum()
            ],

            "Wickets": [
                powerplay['player_dismissed'].notna().sum(),
                middle['player_dismissed'].notna().sum(),
                death['player_dismissed'].notna().sum()
            ]
        })

    tab1, tab2 = st.tabs(
        [team1, team2]
    )

    with tab1:

        st.subheader(f"🏏 {team1} Batting")

        st.dataframe(
            batting1,
            use_container_width=True,
            hide_index=True
        )
        
        st.subheader(f"🎯 {team2} Bowling")

        st.dataframe(
            bowling2,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("🤝 Partnerships")

        partnerships1 = calculate_partnerships(innings1)

        partnerships_display1 = pd.DataFrame({
            "Batter 1": partnerships1["Batter1"],
            "Partnership": partnerships1["Runs"].astype(str)
                        + "("
                        + partnerships1["Balls"].astype(str)
                        + ")",
            "Batter 2": partnerships1["Batter2"]
        })

        st.dataframe(
            partnerships_display1,
            use_container_width=True,
            hide_index=True
        )

        # st.subheader("📊 Phase Analysis")
        # phase_df1 = phase_analysis(innings1)
        # st.bar_chart(
        #     phase_df1.set_index("Phase")
        # )



    with tab2:

        st.subheader(f"🏏 {team2} Batting")

        st.dataframe(
            batting2,
            use_container_width=True,
            hide_index=True
        )
        
        st.subheader(f"🎯 {team1} Bowling")

        st.dataframe(
            bowling1,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("🤝 Partnerships")

        partnerships2 = calculate_partnerships(innings2)

        partnerships_display2 = pd.DataFrame({
            "Batter 1": partnerships2["Batter1"],
            "Partnership": partnerships2["Runs"].astype(str)
                        + "("
                        + partnerships2["Balls"].astype(str)
                        + ")",
            "Batter 2": partnerships2["Batter2"]
        })

        st.dataframe(
            partnerships_display2,
            use_container_width=True,
            hide_index=True
        )

        # st.subheader("📊 Phase Analysis")
        # phase_df2 = phase_analysis(innings2)
        # st.bar_chart(
        #     phase_df2.set_index("Phase")
        # )
    phase1 = phase_analysis(innings1)
    phase2 = phase_analysis(innings2)
    fig = go.Figure()

    fig.add_bar(
        name=team1,
        x=phase1["Phase"],
        y=phase1["Runs"],
        customdata=phase1["Wickets"],
        hovertemplate=
        "<b>Runs:</b> %{y}<br>"
        "<b>Wickets:</b> %{customdata}<br>"
        "<extra></extra>"
    )

    fig.add_bar(
        name=team2,
        x=phase2["Phase"],
        y=phase2["Runs"],
        customdata=phase2["Wickets"],
        hovertemplate=
        "<b>Runs:</b> %{y}<br>"
        "<b>Wickets:</b> %{customdata}<br>"
        "<extra></extra>"
    )

    fig.update_layout(
        barmode="group",
        title="Runs Scored by Phase",
        xaxis_title="Phase",
        yaxis_title="Runs",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")
    st.subheader("⚔️ Head-to-Head") 

    team1 = match_info.iloc[0]['team1']
    team2 = match_info.iloc[0]['team2']

    h2h_matches = matches[
        (
            (matches['team1'] == team1)
            &
            (matches['team2'] == team2)
        )
        |
        (
            (matches['team1'] == team2)
            &
            (matches['team2'] == team1)
        )
    ]

    team1_wins = (h2h_matches['winner'] == team1).sum()
    team2_wins = (h2h_matches['winner'] == team2).sum()
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(
            "Matches",
            len(h2h_matches)
        )

    with c2:
        st.metric(
            team1,
            team1_wins
        )

    with c3:
        st.metric(
            team2,
            team2_wins
        )

# Season analysis
def team_card(team, color):
    return f"""
    <div style="
        background:{color};
        color:white;
        padding:15px;
        border-radius:12px;
        text-align:center;
        font-weight:bold;
        margin:5px;
        min-width:220px;
        ">
        {team}
    </div>
    """


if show_season_analysis:

    st.header("📊 Season Analytics")

    selected_season_sa = st.selectbox(
        "Select Season",
        sorted(matches["season"].dropna().unique(), reverse=True),
        key="season_analytics_dropdown"
    )

    season_matches = matches[
        matches["season"] == selected_season_sa
    ]
    st.write("Selected Season:", selected_season_sa)
    st.write("Matches:", len(season_matches))
    
    st.subheader("🏆 Season Summary")

    st.write(
        season_matches[
            season_matches["match_number"].isna()
        ][[
            "team1",
            "team2",
            "winner",
            "match_number",
            "eliminator",
            "date"
        ]]
    )

    playoffs = season_matches.tail(4)

    final_match = playoffs.iloc[-1]

    winner = final_match["winner"]

    if final_match["team1"] == winner:
        runner_up = final_match["team2"]
    else:
        runner_up = final_match["team1"]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🏆 Winner",
            winner
        )

    with col2:
        st.metric(
            "🥈 Runner Up",
            runner_up
        )
    
    st.markdown("---")
    st.subheader("📊 Points Table")
    points_table = generate_points_table(
        season_matches
    )

    points_table.loc[
        points_table.index[:4],
        "Team"
    ] = (
        points_table.loc[
            points_table.index[:4],
            "Team"
        ] + "  (Q)"
    )

    st.dataframe(
        points_table,
        use_container_width=True
    )

    st.markdown("---")
    st.subheader("🏆 Playoffs")

    playoffs = season_matches.tail(4)

    st.dataframe(
        playoffs[
            [
                "team1",
                "team2",
                "winner",
                "date"
            ]
        ],
        use_container_width=True
    )

    q1 = playoffs.iloc[0]
    elim = playoffs.iloc[1]
    q2 = playoffs.iloc[2]
    final = playoffs.iloc[3]
    st.markdown("### 🏆 Playoff Bracket")
    st.markdown("---")

    # st.info(f"""
    # 🏆 Qualifier 1
    # {q1['team1']}
    # VS
    # {q1['team2']}
    # Winner: {q1['winner']}

    # -------------------------

    # ❌ Eliminator

    # {elim['team1']}
    # VS
    # {elim['team2']}

    # Winner: {elim['winner']}



    # -------------------------

    # 🏏 Qualifier 2

    # {q2['team1']}
    # VS
    # {q2['team2']}

    # Winner: {q2['winner']}

    # -------------------------

    # 👑 Final

    # {final['team1']}
    # VS
    # {final['team2']}

    # Champion: {final['winner']}
    # """)    
    
    bracket_html = f"""
    <div style="
    background:#002b5b;
    padding:30px;
    border-radius:15px;
    color:white;
    font-family:Arial;
    ">

    <h1 style="text-align:center;">🏆 IPL Playoff Bracket</h1>

    <div style="
    display:flex;
    justify-content:space-between;
    align-items:center;
    ">

    <div>
    <h2>🏆 Qualifier 1</h2>
    <div style="background:#1976d2;padding:15px;border-radius:10px;margin:10px 0;">
    {q1['team1']}
    </div>

    <div style="background:#009688;padding:15px;border-radius:10px;">
    {q1['team2']}
    </div>

    <br><br>

    <h2>❌ Eliminator</h2>
    <div style="background:#e53935;padding:15px;border-radius:10px;margin:10px 0;">
    {elim['team1']}
    </div>

    <div style="background:#8e24aa;padding:15px;border-radius:10px;">
    {elim['team2']}
    </div>
    </div>

    <div>
    <h2>🏏 Qualifier 2</h2>
    <div style="background:#ff9800;padding:25px;border-radius:10px;margin-top:20px;">
    {q2['team1']}<br>
    VS<br>
    {q2['team2']}
    </div>
    </div>

    <div>
    <h2>👑 Final</h2>
    <div style="background:#fbc02d;padding:25px;border-radius:10px;">
    {final['team1']}<br>
    VS<br>
    {final['team2']}
    </div>

    <br><br>

    <div style="
    background:#2e7d32;
    padding:25px;
    border-radius:10px;
    font-size:22px;
    font-weight:bold;
    text-align:center;
    margin-top:30px;
    ">
    🏆 Champion<br>
    {final['winner']}
    </div>
    </div>

    </div>
    </div>
    """
    components.html(bracket_html, height=700)
    # st.write(season_batter_stats.columns)
    # st.subheader("🟠 Orange Cap")

    # if selected_season_sa == "All":

    #     orange_cap = (
    #         season_batter_stats
    #         .sort_values("runs", ascending=False)
    #         .iloc[0]
    #     )

    # else:

    #     season_data = season_batter_stats[
    #         season_batter_stats["season"].astype(str)
    #         == str(selected_season_sa)
    #     ]

    #     if len(season_data) > 0:

            # orange_cap = (
            #     season_data
            #     .sort_values("runs", ascending=False)
            #     .iloc[0]
            # )

    #         st.markdown(f"""
    #         <div style="
    #         background:#ff9800;
    #         padding:40px;
    #         border-radius:20px;
    #         text-align:center;
    #         color:white;
    #         ">

    #         <h1>🟠 Orange Cap Winner</h1>

    #         <h1>{orange_cap['striker']}</h1>

    #         <div style="
    #         display:flex;
    #         justify-content:center;
    #         gap:80px;
    #         margin-top:30px;
    #         font-size:24px;
    #         font-weight:bold;
    #         ">

    #         <div>
    #         Runs<br>
    #         {int(orange_cap['runs'])}
    #         </div>

    #         <div>
    #         SR<br>
    #         {round(orange_cap['SR'],2)}
    #         </div>

    #         <div>
    #         AVG<br>
    #         {round(orange_cap['average'],2)}
    #         </div>

    #         </div>

    #         </div>
    #         """, unsafe_allow_html=True)

    #     else:
    #         st.error(f"No data found for season {selected_season}")
    mm_2023 = deliveries[
        (deliveries["season"] == 2023) &
        (deliveries["bowler"] == "MM Sharma")
    ]

    valid_wickets = [
        "bowled",
        "caught",
        "lbw",
        "stumped",
        "hit wicket",
        "caught and bowled"
    ]

    wickets = mm_2023[
        mm_2023["dismissal_kind"].isin(valid_wickets)
    ]

    print("MM Sharma wickets in 2023:", len(wickets))

    st.dataframe(
        wickets[
            ["matchId", "over", "ball", "player_dismissed", "dismissal_kind"]
        ]
    )

    orange_cap_player = (
        season_batter_stats[
            season_batter_stats["season"].astype(str)
            == str(selected_season_sa)
        ]
        .sort_values("runs", ascending=False)
        .iloc[0]
    )
    purple_cap_player = (
        season_bowler_stats[
            season_bowler_stats["season"].astype(str)
            == str(selected_season_sa)
        ]
        .sort_values("wickets", ascending=False)
        .iloc[0]
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="
        background:#ff9800;
        padding:15px;
        border-radius:15px;
        text-align:center;
        color:white;
        min-height:180px;
        width:90%;
        margin:auto;
        ">

        <h2>🟠 Orange Cap</h2>

        <h2 style="font-size:30px;">
        {orange_cap_player['striker']}
        </h2>

        <hr>

        <div style="
        display:flex;
        justify-content:space-evenly;
        margin-top:20px;
        font-size:18px;
        font-weight:bold;
        ">

        <div>
        Runs<br>
        {int(orange_cap_player['runs'])}
        </div>

        <div>
        SR<br>
        {round(orange_cap_player['SR'],1)}
        </div>

        <div>
        AVG<br>
        {round(orange_cap_player['average'],1)}
        </div>

        </div>

        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="
        background:#800080;
        padding:15px;
        border-radius:15px;
        text-align:center;
        color:white;
        min-height:180px;
        width:90%;
        margin:auto;
        ">

        <h2>🟣 Purple Cap</h2>

        <h2 style="font-size:30px;">
        {purple_cap_player['bowler']}
        </h2>

        <hr>

        <div style="
        display:flex;
        justify-content:space-evenly;
        margin-top:20px;
        font-size:18px;
        font-weight:bold;
        ">

        <div>
        Wickets<br>
        {int(purple_cap_player['wickets'])}
        </div>

        <div>
        Economy<br>
        {round(purple_cap_player['economy'],1)}
        </div>

        <div>
        Avg<br>
        {round(purple_cap_player['average'],1)}
        </div>

        </div>

        </div>
        """, unsafe_allow_html=True)

st.markdown("---")


st.markdown("---")

st.markdown(
"""
<div style='text-align:center;color:gray'>

Made by Priyanshu Maurya 

</div>
""",
unsafe_allow_html=True
)