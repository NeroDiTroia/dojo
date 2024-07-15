import streamlit as st
import numpy as np
import pandas as pd


# remove empty top space
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)
    
# remove header banner   
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
#st.markdown(hide_st_style, unsafe_allow_html=True)

# Inject custom CSS to set the width of the sidebar
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 350px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def read_google_sheet(url):
    return pd.read_csv(url,sep=',')
    
url_sheet = f"https://docs.google.com/spreadsheets/d/1etDAH3M2Rl7743EEEWCH-TfOAJW06OPQs38Ipxx52ig/export?format=csv&gid=0" 
#url = 'master_list_of_study_chapters.csv'
df = read_google_sheet(url_sheet)
# pass down opening names:
for iii in range(len(df)):
    df['opening'][iii] = str(df['opening'][iii])
    if df['opening'][iii] == 'nan':
        df['opening'][iii] = df['opening'][iii-1]
# only keep rows with a URL
df = df[df['url'].notnull()]
#st.dataframe(df)

list_boards = [
    "blue",
    "blue2",
    "blue3",
    "blue-marble",
    "canvas",
    "wood",
    "wood2",
    "wood3",
    "wood4",
    "maple",
    "maple2",
    "brown",
    "leather",
    "green",
    "marble",
    "green-plastic",
    "grey",
    "metal",
    "olive",
    "newspaper",
    "purple",
    "purple-diag",
    "pink",
    "ic",
    "horsey",
]
list_pieces = [
    "cburnett",
    "merida",
    "alpha",
    "pirouetti",
    "chessnut",
    "chess7",
    "reillycraig",
    "companion",
    "riohacha",
    "kosal",
    "leipzig",
    "fantasy",
    "spatial",
    "california",
    "pixel",
    "maestro",
    "fresca",
    "cardinal",
    "gioco",
    "tatiana",
    "staunty",
    "governor",
    "dubrovny",
    "icpieces",
    "shapes",
    "letter",
    "horsey",
    "anarcandy",
    "cooke",
    "monarchy",
]

# Filter studies in sidebar:
all_openings = sorted(set(list(df['opening'])))
selected_opening = [True for ooo in all_openings]
for iii,ooo in enumerate(all_openings):
    selected_opening[iii] = st.sidebar.checkbox( ooo , value=True )

# Pick a random study:
allowed_openings = [ooo for ooo,sss in zip(all_openings,selected_opening) if sss==True]
if allowed_openings==[]:
    allowed_openings = all_openings
urls_to_pick_from = [uuu for uuu,ooo in zip(df['url'],df['opening']) if ooo in allowed_openings]
study_pick = np.random.choice( urls_to_pick_from )
study_URL = study_pick.replace('/study/','/study/embed/')


board_pick = np.random.choice( list_boards )
pieces_pick = np.random.choice( list_pieces )
params = '?bg=dark&pieceSet=%s&theme=%s' % (pieces_pick,board_pick)

st.components.v1.iframe(study_URL+params, width=350, height=480, scrolling=False)

col1, col2 = st.columns([0.3,0.7])
col1.button("Refresh", type="primary")
col2.write(study_pick)
