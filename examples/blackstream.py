import streamlit as st
import pandas as pd 
import requests as r
import bs4 as BeautifulSoup
import spacy


EW_BASE_URL = "https://www.bailii.org/ew/cases/"

HEADERS =  {
    'User-Agent': 'Chrome',
    'From': 'daniel.hoadley@iclr.co.uk' 
}

def process_request(response):
    """
    """
    content = response.text
    soup = BeautifulSoup.BeautifulSoup(content, "lxml")
    judgment = soup.find('ol')
    judgment_ = judgment.text
    title = soup.find('title').text
    return (judgment_, title)


@st.cache(ignore_hash=True)
def process_text(text):
    nlp = spacy.load('en_blackstone_proto')
    return nlp(text)


st.write("My first app!")

# court selector
court = st.sidebar.selectbox(
    "Select a court",
     ["Court of Appeal (Civil Division)", "Court of Appeal (Criminal Division)",])

# year selector
year = st.sidebar.selectbox(
    "Select a year", range(2000, 2020)
)

# case number text area
case_number = st.sidebar.text_input("Case number (e.g.  \"23\" for [2019] EWCA Crim 23.)")

if st.sidebar.button('Search'):
    if case_number:
        
        # Logic for CA (Civ)
        if court == "Court of Appeal (Civil Division)":
            target = EW_BASE_URL + "EWCA/Civ/" + str(year) + "/" + str(case_number) + ".html"
            response = r.get(target, headers=HEADERS)
            content = process_request(response)
            case_name = '<p style="font-size:0.7rem;">' + content[1] + '</p>'
            st.write(case_name, unsafe_allow_html=True)
            doc = process_text(content[0])
            if response.status_code == 200:
                pass
            else:
                st.sidebar.error("Unable to locate the requested case.")



            pass
        if court == "Court of Appeal (Criminal Division)":
            pass

    else:
        st.error("Please provide a case number to search for!")


