import streamlit as st
import os,sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import plotly.express as px 
import json
import requests


@st.experimental_singleton
def installff():
  os.system('sbase install geckodriver chrome')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

_ = installff()

from selenium import webdriver
from selenium.webdriver import FirefoxOptions

st.title("PAA and Related Searches Analyzer")
st.caption ("View PAA's and Related Questions for a keyword")
input_keyword = st.text_input('Enter Keyword')
agree = st.checkbox('Enter keyword')
if agree:
    ####### Scrape related searches and questions

    url = "https://www.google.com/search?q="+input_keyword
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    driver = webdriver.Firefox(options=opts)

    # options = webdriver.ChromeOptions() 
    # options.add_argument('--headless') 
    # driver = webdriver.Chrome(options=options)
    driver.get(url)


    related_searches_list = []
    paa_questions_list = []
    related_searches = driver.find_elements(By.XPATH, "//div[@class='s75CSd OhScic AB4Wff']")
    questions = driver.find_elements(By.XPATH, "//div[@jsname='yEVEwb']")
    for search in related_searches:
        related_searches_list.append(search.text)
    for question in questions:
        paa_questions_list.append(question.text)


    related_searches_dict2 = {}
    questions_dict2 = {}
    for x in related_searches_list:
        driver.get('https://www.google.com/search?q='+x)
        related_searches2 = driver.find_elements(By.XPATH, "//div[@class='s75CSd OhScic AB4Wff']")
        questions2 = driver.find_elements(By.XPATH, "//div[@jsname='yEVEwb']")
        for search2 in related_searches2:
            related_searches_dict2[search2.text] = x
        for question in questions2:
            questions_dict2[question.text] = x

 




    df = pd.DataFrame(list(related_searches_dict2.items()), columns=['Level_2', 'Level_1'])
    df2 = pd.DataFrame(list(questions_dict2.items()), columns=['Level_2', 'Level_1'])


    st.header(f"Related Searches for {input_keyword}")

    fig_searches = px.treemap(df, path=['Level_1', 'Level_2'], color='Level_1')
    fig_searches.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(fig_searches, use_container_width=True)

    st.header(f"PAAs for {input_keyword}")

    fig_paa = px.treemap(df2, path=['Level_1', 'Level_2'], color='Level_1')
    fig_paa.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(fig_paa, use_container_width=True)
