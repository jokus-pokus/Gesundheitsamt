import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame(data=[0,1,2,3])

chart = st.line_chart(df.values)