import streamlit as st
import qrcode
import log

log.logging()

"# Zero licenses"
"Generate a new license"

c = st.columns(2)
fname = c[0].text_input("First name", "")
name = c[1].text_input("Name", "")

cie = c[0].text_input("Company", "")
expiry = c[1].date_input("Expiry", "today")
