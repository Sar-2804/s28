import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="SIR Simulation", layout="wide")

# -------------------------------
# TITLE
# -------------------------------
st.title("🦠 Advanced Flu Outbreak Simulator (SIR Model)")
st.markdown("### Interactive Epidemiology Dashboard with Scenario Comparison")

# -------------------------------
# SIDEBAR INPUTS
# -------------------------------
st.sidebar.header("🔧 Adjust Parameters")

population = st.sidebar.slider("Population (N)", 100, 5000, 1000)
initial_infected = st.sidebar.slider("Initial Infected", 1, 100, 10)

beta = st.sidebar.slider("Infection Rate (β)", 0.0, 1.0, 0.3)
gamma = st.sidebar.slider("Recovery Rate (γ)", 0.01, 1.0, 0.1)
vaccination = st.sidebar.slider("Vaccination Rate (v)", 0.0, 0.5, 0.05)

days = st.sidebar.slider("Simulation Days", 10, 200, 100)

# -------------------------------
# SIR FUNCTION
# -------------------------------
def run_sir(beta, gamma, v):
    S = population - initial_infected
    I = initial_infected
    R = 0

    S_list, I_list, R_list = [S], [I], [R]

    for _ in range(days):
        new_S = S - (beta * S * I / population) - (v * S)
        new_I = I + (beta * S * I / population) - (gamma * I)
        new_R = R + (gamma * I) + (v * S)

        S, I, R = new_S, new_I, new_R

        S_list.append(S)
        I_list.append(I)
        R_list.append(R)

    return S_list, I_list, R_list

# -------------------------------
# MAIN SCENARIO
# -------------------------------
S, I, R = run_sir(beta, gamma, vaccination)

# -------------------------------
# SCENARIO COMPARISON
# -------------------------------
st.subheader("📊 Scenario Comparison")

S_no, I_no, R_no = run_sir(beta, gamma, 0)           # No vaccination
S_low, I_low, R_low = run_sir(beta*0.5, gamma, vaccination)  # Reduced contact

fig, ax = plt.subplots()

ax.plot(I, label="Current Scenario")
ax.plot(I_no, linestyle="--", label="No Vaccination")
ax.plot(I_low, linestyle=":", label="With Prevention")

ax.set_xlabel("Days")
ax.set_ylabel("Infected Population")
ax.set_title("Comparison of Infection Spread")
ax.legend()

st.pyplot(fig)

# -------------------------------
# METRICS + R0
# -------------------------------
st.subheader("📈 Key Metrics")

R0 = beta / gamma

peak = max(I)
peak_day = I.index(peak)

col1, col2, col3, col4 = st.columns(4)

col1.metric("R₀ Value", f"{R0:.2f}")
col2.metric("Peak Infected", int(peak))
col3.metric("Peak Day", peak_day)
col4.metric("Final Recovered", int(R[-1]))

# -------------------------------
# FLATTEN THE CURVE INDICATOR
# -------------------------------
st.subheader("📉 Flatten the Curve Analysis")

if peak < population * 0.2:
    st.success("✅ Curve is Flattened (Low infection peak)")
elif peak < population * 0.5:
    st.warning("⚠️ Moderate Spread")
else:
    st.error("❌ High Peak - Severe Outbreak")

# -------------------------------
# FULL GRAPH (SIR)
# -------------------------------
st.subheader("📊 Full SIR Graph")

fig2, ax2 = plt.subplots()

ax2.plot(S, label="Susceptible")
ax2.plot(I, label="Infected")
ax2.plot(R, label="Recovered")

ax2.set_xlabel("Days")
ax2.set_ylabel("Population")
ax2.legend()

st.pyplot(fig2)

# -------------------------------
# THEORY SECTION
# -------------------------------
st.subheader("📘 Mathematical Theory")

st.markdown("""
### SIR Model Equations:

- dS/dt = −βSI/N − vS  
- dI/dt = βSI/N − γI  
- dR/dt = γI + vS  

### Basic Reproduction Number (R₀):

R₀ = β / γ  

- If R₀ > 1 → Disease spreads  
- If R₀ < 1 → Disease dies out  

### Insights:

- Higher β increases spread  
- Higher γ improves recovery  
- Vaccination reduces susceptible population  
- Preventive measures reduce β (contact rate)
""")

# -------------------------------
# INSIGHTS / INTERPRETATION
# -------------------------------
st.subheader("🧠 Insights")

if R0 > 1:
    st.write("The infection is likely to spread in the population.")
else:
    st.write("The infection will gradually die out.")

st.write("Vaccination and preventive measures significantly reduce the outbreak impact.")
