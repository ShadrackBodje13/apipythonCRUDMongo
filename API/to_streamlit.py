# Librairies
import streamlit as st 
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.backends.backend_agg import RendererAgg
import requests
import json

data = requests.get('http://10.92.2.163:5000/chems').json()
print(data)
# otherdata = requests.get('http://10.92.2.163:5000/chems').json()
# otherdata = requests.get('http://10.92.2.163:5000/chemises')
col = ["descripton", "newpricecol", "nom_chemise", "old-pricecol", ]
df = pd.DataFrame(data, columns=col, index=[0])

print(type(df))
# df["newpricecol"]
# df["nom_chemise"]
# df["pricecol"]
st.dataframe(df)
# st.dataframe(dataframe)
