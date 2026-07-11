import streamlit as st


def logging() :
  if "access" not in st.session_state :
    st.session_state.access = False
    st.session_state.count = 0
    
  if st.session_state.access == True :
    return

  modal_pw()


@st.dialog("Log", dismissible=False)
def modal_pw() :
  if st.session_state.count >= 3 :
    st.error("Too mony tries")

  
  with st.form("pws", border=False) :
    pw1 = st.text_input("Password 1", None, type="password")
    pw2 = st.text_input("Password 2", None, type="password")
    if st.form_submit_button(":material/check: Submit", type="primary") :
      if pw1 == st.secrets["pw1"] and pw2 == st.secrets["pw2"] :
        st.session_state.access = True
        st.rerun()
      else :
        st.error("Wrong passwords")    
  
