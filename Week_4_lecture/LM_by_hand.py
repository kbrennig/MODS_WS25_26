# create conda environment: conda create -n mods python=3.11
# run streamlit app: streamlit run LM_by_hand.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Read data    
path = "./Advertising.csv"
df = pd.read_csv(path)

# Sliders for beta0 and beta1
beta0 = st.slider("Select a value for beta 0", -20.0, 20.0, 12.0)
beta1 = st.slider("Select a value for beta 1", -1.0, 1.0, -0.1)

# Calculate the prediction and the residuals
df["Prediction"] = beta0 + beta1 * df["TV"]
df["Epsilon"] = df["Prediction"] - df["Sales"]

# Calculate the RSS
RSS = (df["Epsilon"]**2).sum()

# Plotting with Pyplot
fig, ax = plt.subplots()
ax.scatter(df["TV"], df["Sales"])
ax.plot(df["TV"], df["Prediction"], color="red")
# fix limits of the y-axis to -100 and 100
ax.set_ylim(-10, 40)
fig.suptitle("Sales ~ beta0 + beta1*TV")
plt.title(f"RSS: {str(round(RSS, 2))}")

# Display the plot in Streamlit
st.pyplot(fig)