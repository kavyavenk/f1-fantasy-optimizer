import streamlit as st
from itertools import combinations
from PIL import Image

st.set_page_config(page_title="F1 Fantasy League Optimizer", layout="wide", page_icon="icon.png")

st.image("logo.png", width=1000)

st.markdown(
    """
    <style>
        body {
            background-color: #000000;
            color: white;
        }
        .css-18e3th9 {
            background-color: #00000;
        }
        .stButton>button {
            background-color: #ff1801;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)
drivers = [
    {"name": "Max Verstappen", "team": "Red Bull", "price": 30.0, "points": 550},
    {"name": "Liam Lawson", "team": "Red Bull", "price": 24.0, "points": 320},
    {"name": "Lewis Hamilton", "team": "Ferrari", "price": 23.0, "points": 300},
    {"name": "Charles Leclerc", "team": "Ferrari", "price": 21.0, "points": 270},
    {"name": "George Russell", "team": "Mercedes", "price": 20.0, "points": 260},
    {"name": "Andrea Kimi Antonelli", "team": "Mercedes", "price": 19.0, "points": 250},
    {"name": "Lando Norris", "team": "McLaren", "price": 18.0, "points": 240},
    {"name": "Oscar Piastri", "team": "McLaren", "price": 16.0, "points": 220},
    {"name": "Fernando Alonso", "team": "Aston Martin", "price": 15.0, "points": 210},
    {"name": "Lance Stroll", "team": "Aston Martin", "price": 14.0, "points": 200},
    {"name": "Pierre Gasly", "team": "Alpine", "price": 13.5, "points": 190},
    {"name": "Jack Doohan", "team": "Alpine", "price": 12.0, "points": 180},
    {"name": "Alex Albon", "team": "Williams", "price": 11.5, "points": 170},
    {"name": "Carlos Sainz", "team": "Williams", "price": 11.0, "points": 160},
    {"name": "Yuki Tsunoda", "team": "VCARB", "price": 10.5, "points": 150},
    {"name": "Isack Hadjar", "team": "VCARB", "price": 10.0, "points": 140},
    {"name": "Nico Hulkenberg", "team": "Sauber/Audi", "price": 9.5, "points": 130},
    {"name": "Gabriel Bortoleto", "team": "Sauber/Audi", "price": 9.0, "points": 120},
    {"name": "Oliver Bearman", "team": "Haas", "price": 8.5, "points": 110},
    {"name": "Esteban Ocon", "team": "Haas", "price": 8.0, "points": 100}
]

constructors = [
    {"name": "Red Bull", "price": 30.0, "points": 650},
    {"name": "Ferrari", "price": 27.0, "points": 550},
    {"name": "Mercedes", "price": 24.0, "points": 500},
    {"name": "McLaren", "price": 21.0, "points": 450},
    {"name": "Aston Martin", "price": 19.0, "points": 400},
    {"name": "Alpine", "price": 16.0, "points": 350},
    {"name": "Williams", "price": 13.0, "points": 300},
    {"name": "Visa Cash App RB", "price": 11.0, "points": 250},
    {"name": "Sauber/Audi", "price": 10.0, "points": 220},
    {"name": "Haas", "price": 9.0, "points": 200}
]

st.sidebar.header("User Preferences")
preferred_drivers = st.sidebar.multiselect("Select up to 3 preferred drivers:", [driver["name"] for driver in drivers], max_selections=3)
preferred_constructors = st.sidebar.multiselect("Select up to 3 preferred constructors:", [constructor["name"] for constructor in constructors], max_selections=3)
priority = st.sidebar.radio("What would you like to prioritize?", ["Drivers", "Constructors"], index=0)

budget = st.sidebar.slider("Select your budget:", min_value=50, max_value=100, value=100)

st.write("The algorithm selects the best combinations of drivers and constructors within the budget constraints. It prioritizes either drivers or constructors based on user input and ensures that the selected team maximizes points while adhering to the budget. The algorithm works by generating all possible combinations of 5 drivers and 2 constructors. It calculates the total cost and points for each combination, filters out those exceeding the budget, and prioritizes the combinations based on user preferences. The top 3 optimal teams are displayed.")

def generate_teams(drivers, constructors, budget, preferred_drivers, preferred_constructors, priority):
    optimal_teams = []

    for driver_combo in combinations(drivers, 5):
        driver_cost = sum(driver["price"] for driver in driver_combo)
        driver_points = sum(driver["points"] for driver in driver_combo)

        for constructor_combo in combinations(constructors, 2):
            constructor_cost = sum(constructor["price"] for constructor in constructor_combo)
            constructor_points = sum(constructor["points"] for constructor in constructor_combo)

            total_cost = driver_cost + constructor_cost
            total_points = driver_points + constructor_points

            if total_cost <= budget:
                team = {
                    "drivers": driver_combo,
                    "constructors": constructor_combo,
                    "cost": total_cost,
                    "points": total_points
                }
                optimal_teams.append(team)

    optimal_teams.sort(key=lambda x: x["points"], reverse=True)
    filtered_teams = []
    for team in optimal_teams:
        if priority == "Drivers":
            if sum(driver["name"] in preferred_drivers for driver in team["drivers"]) >= 1:
                filtered_teams.append(team)
        elif priority == "Constructors":
            if any(constructor["name"] in preferred_constructors for constructor in team["constructors"]):
                filtered_teams.append(team)

    return filtered_teams[:3] 

optimal_teams = generate_teams(drivers, constructors, budget, preferred_drivers, preferred_constructors, priority)

if optimal_teams:
    col1, col2, col3 = st.columns(3)

    for idx, team in enumerate(optimal_teams, 1):
        col = [col1, col2, col3][idx - 1]
        with col:
            st.subheader(f"Team {idx}")
            st.write(f"**Cost:** ${team['cost']}M | **Points:** {team['points']}")

            st.write("**Drivers:**")
            for driver in team["drivers"]:
                st.write(f"- {driver['name']} ({driver['team']}) - ${driver['price']}M, {driver['points']} points")

            st.write("**Constructors:**")
            for constructor in team["constructors"]:
                st.write(f"- {constructor['name']} - ${constructor['price']}M, {constructor['points']} points")
else:
    st.write("Enter preferences to generate optimal teams within the budget:")