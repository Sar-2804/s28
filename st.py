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
# SIR FUNCTION (FIXED)
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

        # ✅ Prevent negative values
        new_S = max(0, new_S)
        new_I = max(0, new_I)
        new_R = max(0, new_R)

        # ✅ Maintain total population
        total = new_S + new_I + new_R
        if total > 0:
            new_S *= population / total
            new_I *= population / total
            new_R *= population / total

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

S_no, I_no, R_no = run_sir(beta, gamma, 0)
S_low, I_low, R_low = run_sir(beta * 0.5, gamma, vaccination)

fig, ax = plt.subplots()

ax.plot(I, label="Current Scenario", color="red")
ax.plot(I_no, linestyle="--", label="No Vaccination")
ax.plot(I_low, linestyle=":", label="With Prevention")

ax.set_xlabel("Days")
ax.set_ylabel("Infected Population")
ax.set_title("Comparison of Infection Spread")
ax.legend()

st.pyplot(fig, use_container_width=True)

# -------------------------------
# METRICS + R0
# -------------------------------
st.subheader("📈 Key Metrics")

R0 = beta / gamma if gamma != 0 else 0

peak = max(I)
peak_day = int(np.argmax(I))

col1, col2, col3, col4 = st.columns(4)

col1.metric("R₀ Value", f"{R0:.2f}")
col2.metric("Peak Infected", round(peak))
col3.metric("Peak Day", peak_day)
col4.metric("Final Recovered", round(R[-1]))

# -------------------------------
# FLATTEN THE CURVE
# -------------------------------
st.subheader("📉 Flatten the Curve Analysis")

if peak < population * 0.2:
    st.success("✅ Curve is Flattened (Low infection peak)")
elif peak < population * 0.5:
    st.warning("⚠️ Moderate Spread")
else:
    st.error("❌ High Peak - Severe Outbreak")

# -------------------------------
# FULL SIR GRAPH
# -------------------------------
st.subheader("📊 Full SIR Graph")

fig2, ax2 = plt.subplots()

ax2.plot(S, label="Susceptible", color="blue")
ax2.plot(I, label="Infected", color="red")
ax2.plot(R, label="Recovered", color="green")

ax2.set_xlabel("Days")
ax2.set_ylabel("Population")
ax2.legend()

st.pyplot(fig2, use_container_width=True)

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
# INSIGHTS
# -------------------------------
st.subheader("🧠 Insights")

if R0 > 1:
    st.write("The infection is likely to spread in the population.")
else:
    st.write("The infection will gradually die out.")

st.write("Vaccination and preventive measures significantly reduce the outbreak impact.")
