# Streamlit
import streamlit as st
import os
# Get all folders (teams) in t3
teams = os.listdir('t3')

st.header("Let's see what you draw!")
for i, team in enumerate(teams):
    st.subheader(f"Team #{i+1}: {team}")
    if st.checkbox("Show?"):
        st.image([f"t3/{team}/{f}" for f in os.listdir(f't3/{team}')])

    st.markdown("---")
