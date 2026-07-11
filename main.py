import streamlit as st
import qrcode
import log

log.logging()

st.image("img/Zero white title.png", width="stretch")

"# Zero licenses"
st.caption("GENERATE A NEW LICENSE", text_alignment="center")

with st.form("new lic") :
  st.caption("Geologist", text_alignment="center")
  c = st.columns(2)
  fname = c[0].text_input(":material/person: First name", "")
  name = c[1].text_input(":material/person: Name", "")
  cie = st.text_input(":material/person: Company", "")
  
  st.caption("License", text_alignment="center")
  c = st.columns(2)
  license_type = c[0].selectbox(":material/license: License type", ["PC","server"])
  license_cover = c[1].selectbox(":material/license: License cover", ["Trial","Premium"])
  expiry = st.date_input("Expiry", "today", format="YYYY-MM-DD")
  st.form_submit_button(":material/check: Submit", type="primary")

license_data = {
    "geologist_fname": fname,
    "geologist_name" : name,
    "geologist_cie"  : cie,
    "expires": expiry,
    "license_type" : license_type,
    "license_cover" : license_cover,
}

key = st.file_uploader("Private password key", type=["pem"])

