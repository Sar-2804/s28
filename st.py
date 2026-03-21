import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("📈 Fitness App Growth Simulation")

# -------------------------------
# Function
# -------------------------------
def fitness_app_growth(initial_dau, initial_new_users, growth_rate, retention_rate,
                       days=4, retention_boost_day=None, boost_amount=0.1):

    dau = [initial_dau]
    new_users = [initial_new_users]
    dropouts = [0]

    for t in range(1, days):

        current_retention = retention_rate

        if retention_boost_day is not None and t == retention_boost_day:
            current_retention = min(1.0, retention_rate + boost_amount)

        new_users_t = new_users[-1] * growth_rate
        new_users.append(new_users_t)

        retained = dau[-1] * current_retention
        dropouts_t = dau[-1] * (1 - current_retention)
        dau_t = retained + new_users_t

        dau.append(dau_t)
        dropouts.append(dropouts_t)

    return dau, new_users, dropouts


# -------------------------------
# Sidebar Inputs
# -------------------------------
st.sidebar.header("🔧 Input Parameters")

initial_dau = st.sidebar.number_input("Initial DAU", value=100)
initial_new_users = st.sidebar.number_input("Initial New Users", value=50)
growth_rate = st.sidebar.number_input("Growth Rate", value=1.2)
retention_rate = st.sidebar.number_input("Retention Rate", value=0.8)
days = st.sidebar.slider("Number of Days", 2, 10, 4)

st.sidebar.subheader("Retention Boost (Scenario 2)")
retention_boost_day = st.sidebar.number_input("Boost Day", value=2)
boost_amount = st.sidebar.number_input("Boost Amount", value=0.1)

# -------------------------------
# Run Simulation
# -------------------------------
if st.button("Run Simulation"):

    # Scenario 1
    dau1, new_users1, dropouts1 = fitness_app_growth(
        initial_dau, initial_new_users, growth_rate, retention_rate, days
    )

    # Scenario 2
    dau2, new_users2, dropouts2 = fitness_app_growth(
        initial_dau, initial_new_users, growth_rate, retention_rate,
        days, retention_boost_day, boost_amount
    )

    # -------------------------------
    # Display Results
    # -------------------------------
    st.subheader("📊 Scenario 1 Results")
    for day in range(days):
        st.write(f"Day {day+1}: DAU={dau1[day]:.0f}, "
                 f"New Users={new_users1[day]:.0f}, "
                 f"Dropouts={dropouts1[day]:.0f}")

    st.subheader("📊 Scenario 2 Results")
    for day in range(days):
        st.write(f"Day {day+1}: DAU={dau2[day]:.0f}, "
                 f"New Users={new_users2[day]:.0f}, "
                 f"Dropouts={dropouts2[day]:.0f}")

    # -------------------------------
    # Plot Graph
    # -------------------------------
    days_list = list(range(1, days + 1))

    fig, ax = plt.subplots()
    ax.plot(days_list, dau1, label='DAU (Scenario 1)', marker='o')
    ax.plot(days_list, new_users1, label='New Users (Scenario 1)', marker='s')
    ax.plot(days_list, dropouts1, label='Dropouts (Scenario 1)', marker='^')

    ax.plot(days_list, dau2, label='DAU (Scenario 2)', linestyle='--', marker='o')

    ax.set_title("Fitness App User Growth")
    ax.set_xlabel("Day")
    ax.set_ylabel("Users")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
