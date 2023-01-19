from datetime import date
import streamlit as st
from contestlib import ContestLib

cl = ContestLib("config/contestinfo.json")

st.set_page_config(
   page_title=cl.get_contestname(),
   page_icon=None,
   layout="centered",
)

st.markdown('''
<style>
.stApp [data-testid="stToolbar"]{
    display:none;
}
</style>
''', unsafe_allow_html=True)

if "button_disabled" not in st.session_state:
    st.session_state.button_disabled = True
if "form_msg" not in st.session_state:
    st.session_state.form_msg = ""

def check_callsign():
    if cl.is_callsign(st.session_state.input_participant):
        st.session_state.button_disabled = False
    else:
        st.session_state.button_disabled = True

def submit_entry():
    res = cl.submit_entry(day, participant, callsign, bands)
    if res == None:
        st.session_state.form_msg = "Erfolgreich eingetragen!"
        st.session_state.input_bands = []
        return
    st.session_state.form_msg = res


st.title(cl.get_contestname())

tab0, tab1, tab2 = st.tabs(["Informationen", "Eingabe", "Ergebnis"])

with tab0:
    f = open("config/description.md")
    st.markdown(f.read())

with tab1:
    if st.session_state.form_msg != "":
        st.info(st.session_state.form_msg)
    participant = st.text_input("Eigenes Rufzeichen",
                  key="input_participant",
                  on_change=check_callsign)
    callsign = st.selectbox("Call",
                 options=cl.get_callsigns())
    bands = st.multiselect("Bänder/Specials",
                   options=cl.get_bands(),
                   key="input_bands")
    day = st.date_input("Datum",
                  min_value=date(2023,1,1),
                  max_value=date(2023,12,31))
    st.button("Eintragen",
              on_click=submit_entry,
              disabled=st.session_state.button_disabled)

with tab2:
    # CSS to inject contained in a string
    hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    option_list = ["all"]
    option_list.extend(cl.get_participants())
    st.selectbox("Call", options=option_list, key="input_score_select")

    if st.session_state.input_score_select == "all":
        st.table(cl.get_score_table_all())
    else:
        st.markdown("Punktzahl: " + str(cl.get_score(st.session_state.input_score_select)))
        st.table(cl.get_score_table(st.session_state.input_score_select))
