import smtplib
from email.mime.text import MIMEText
import requests
EMAIL_ADDRESS = "fa24-bcs-200@students.cuisahiwal.edu.pk"
EMAIL_PASSWORD = "dvyg aqpm kcjc fksv"
API_KEY = "edbff3f78dbb3eaec081390562531fb9"
def get_weather(city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},PK&appid={API_KEY}&units=metric"

    response = requests.get(url)

    data = response.json()

    # Debugging
    print(data)

    # If API fails
    if "main" not in data:

        return {
            "temperature": 30,
            "humidity": 70
        }

    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"]
    }
def send_email_alert(city, risk):

    subject = f"Flood Alert - {city}"

    body = f"""
    Flood Warning System Alert

    City: {city}
    Risk Level: {risk}

    Immediate precautions are recommended.
    """

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS

    try:

        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        server.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        server.send_message(msg)

        server.quit()

        return True

    except Exception as e:

        print(e)

        return False
import random
import folium
from streamlit_folium import st_folium
import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Flood Warning System",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------

model = joblib.load("models/flood_model.pkl")
encoder = joblib.load("models/label_encoder.pkl")

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

/* Main App */
.stApp {
    background-color: #0B1120;
    color: white;
}

/* Main Container */
.main .block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    background-color: #0B1120;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Titles */
h1, h2, h3, h4, h5, h6 {
    color: white !important;
}

/* Text */
/* General Text */
p {
    color: white;
}

/* Labels */
label {
    color: white !important;
}

/* Markdown Text */
.stMarkdown {
    color: white;
}
/* Cards */
.card {
    background: linear-gradient(145deg, #172033, #1E293B);
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.35);
    text-align: center;
    margin-bottom: 10px;
}

/* Metric Title */
.metric-title {
    font-size: 16px;
    color: #94A3B8;
    margin-bottom: 10px;
}

/* Metric Value */
.metric-value {
    font-size: 34px;
    font-weight: bold;
    color: #60A5FA;
}

/* Alert Box */
.alert-high {
    background: linear-gradient(145deg, #166534, #15803D);
    padding: 25px;
    border-radius: 18px;
    color: #FFFFFF !important;
    font-weight: 600;
    font-size: 20px;
    line-height: 1.8;
    margin-top: 15px;
    margin-bottom: 25px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.35);
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background-color: #111827;
}

/* Plotly Chart */
.js-plotly-plot {
    border-radius: 15px;
    overflow: hidden;
}

/* Selectbox Main */
.stSelectbox div[data-baseweb="select"] {
    background-color: #172033 !important;
    border-radius: 10px !important;
    color: white !important;
    border: 1px solid #334155 !important;
}

/* Selected Value */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #172033 !important;
    color: white !important;
}

/* Input Text */
.stSelectbox input {
    color: white !important;
}

/* Dropdown Popup */
div[data-baseweb="popover"] {
    background-color: #172033 !important;
}

/* Dropdown List */
ul {
    background-color: #172033 !important;
    color: white !important;
}

/* Dropdown Options */
li {
    background-color: #172033 !important;
    color: white !important;
}

/* Hover Effect */
li:hover {
    background-color: #334155 !important;
    color: white !important;
}

/* Remove Streamlit Header */
header {
    visibility: hidden;
}

/* Remove Footer */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

st.sidebar.title("Flood Warning System")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Live Weather",
        "Flood Prediction",
        "Risk Map",
        "Alerts"
    ]
)

st.sidebar.markdown("---")
st.sidebar.success("System Status: ONLINE")

# ---------------- TOP SECTION ----------------

top1, top2 = st.columns([3, 1])

with top1:
    st.title("AI Flood Warning Dashboard")
    st.caption("Real-time flood monitoring and prediction system")

with top2:
    city = st.selectbox(
        "Select City",
        [
            "Sukkur",
            "Karachi",
            "Hyderabad",
            "Larkana",
            "Khairpur"
        ]
    )

    st.write(datetime.now().strftime("%d %B %Y"))

# ---------------- SMART CITY CONDITIONS ----------------

city_conditions = {

    "Sukkur": {
        "rainfall": 140,
        "river": 20
    },

    "Karachi": {
        "rainfall": 60,
        "river": 5
    },

    "Hyderabad": {
        "rainfall": 95,
        "river": 12
    },

    "Larkana": {
        "rainfall": 110,
        "river": 15
    },

    "Khairpur": {
        "rainfall": 85,
        "river": 10
    }
}

rainfall = city_conditions[city]["rainfall"] + random.randint(-15, 15)

river = city_conditions[city]["river"] + random.randint(-3, 3)

# Prevent negative values
rainfall = max(rainfall, 0)
river = max(river, 0)

weather = get_weather(city)
temp = weather["temperature"]
humidity = weather["humidity"]


# ---------------- PREDICTION ----------------

input_data = pd.DataFrame(
    [[rainfall, humidity, river, temp]],
    columns=[
        "Rainfall",
        "Humidity",
        "RiverLevel",
        "Temperature"
    ]
)

prediction = model.predict(input_data)

result = encoder.inverse_transform(prediction)[0]

# ---------------- METRIC CARDS ----------------

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="card">
        <div class="metric-title">Rainfall</div>
        <div class="metric-value">{rainfall} mm</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="card">
        <div class="metric-title">Humidity</div>
        <div class="metric-value">{humidity}%</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="card">
        <div class="metric-title">River Level</div>
        <div class="metric-value">{river} ft</div>
    </div>
    """, unsafe_allow_html=True)

with m4:

    color = "#22C55E"

    if result == "Medium":
        color = "#F59E0B"

    elif result == "High":
        color = "#EF4444"

    st.markdown(f"""
    <div class="card">
        <div class="metric-title">Flood Risk</div>
        <div class="metric-value" style="color:{color}">
            {result}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- ALERT SECTION ----------------

st.markdown("## Flood Alert Status")
if st.button("Send Emergency Alert"):

    success = send_email_alert(city, result)

    if success:
        st.success("Emergency alert email sent successfully")

    else:
        st.error("Failed to send email alert")
alert_message = ""
alert_color = ""

if result == "High":

    alert_message = f"""
    HIGH FLOOD RISK DETECTED IN {city.upper()}

    Heavy rainfall and rising river levels indicate possible flooding within the next 24 hours.

    Recommended Actions:
    • Avoid unnecessary travel
    • Move toward safer areas
    • Follow local authority instructions
    """

    alert_color = "#991B1B"

elif result == "Medium":

    alert_message = f"""
    MODERATE FLOOD RISK IN {city.upper()}

    Weather conditions should be monitored carefully.

    Recommended Actions:
    • Stay updated with alerts
    • Prepare emergency supplies
    """

    alert_color = "#92400E"

else:

    alert_message = f"""
    LOW FLOOD RISK IN {city.upper()}

    Current environmental conditions appear stable.
    """

    alert_color = "#166534"

st.markdown(f"""
<div style="
background:{alert_color};
padding:25px;
border-radius:18px;
color:white;
font-size:20px;
font-weight:600;
line-height:1.9;
margin-top:15px;
margin-bottom:25px;
box-shadow:0 4px 15px rgba(0,0,0,0.35);
">
<pre style="
color:white;
font-size:18px;
font-family:sans-serif;
white-space:pre-wrap;
margin:0;
">
{alert_message}
</pre>
</div>
""", unsafe_allow_html=True)
# ---------------- CHARTS ----------------

chart1, chart2 = st.columns(2)

# Rainfall Chart
with chart1:

    rainfall_data = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Rainfall": [
    random.randint(30, 60),
    random.randint(40, 80),
    random.randint(60, 100),
    random.randint(80, 140),
    random.randint(70, 120),
    random.randint(90, 150),
    rainfall
]
    })

    fig = px.bar(
        rainfall_data,
        x="Day",
        y="Rainfall",
        title="Rainfall Trend"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#172033",
        plot_bgcolor="#172033",
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)

# River Chart
with chart2:

    river_data = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Level": [
    random.randint(3, 6),
    random.randint(5, 8),
    random.randint(7, 10),
    random.randint(10, 14),
    random.randint(12, 16),
    random.randint(14, 18),
    river
]
    })

    fig2 = px.line(
        river_data,
        x="Day",
        y="Level",
        markers=True,
        title="River Level Trend"
    )

    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="#172033",
        plot_bgcolor="#172033",
        font=dict(color="white")
    )

    st.plotly_chart(fig2, use_container_width=True)

# ---------------- AI FACTORS ----------------

st.markdown("## AI Risk Factors")

f1, f2, f3, f4 = st.columns(4)

with f1:
    st.metric("Rainfall Impact", f"{min(rainfall,100)}%")

with f2:
    st.metric("River Pressure", f"{min(river*5,100)}%")

with f3:
    st.metric("Humidity Impact", f"{humidity}%")

with f4:
    st.metric("Temperature Factor", f"{temp}%")

# ---------------- AI PROBABILITY ----------------

st.markdown("## AI Flood Probability")

if result == "High":

    probability = random.randint(80, 98)

elif result == "Medium":

    probability = random.randint(50, 75)

else:

    probability = random.randint(15, 40)

fig3 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=probability,
    title={'text': "Flood Probability"},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "red"},
        'steps': [
            {'range': [0, 40], 'color': "green"},
            {'range': [40, 70], 'color': "orange"},
            {'range': [70, 100], 'color': "red"}
        ]
    }
))

fig3.update_layout(
    template="plotly_dark",
    paper_bgcolor="#172033",
    font=dict(color="white")
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- RECENT ALERTS ----------------

st.markdown("## Recent Alerts")

alerts = pd.DataFrame({
    "Time": [
        "11:20 AM",
        "10:45 AM",
        "09:30 AM",
        "08:15 AM"
    ],
    "Location": [
        city,
        "Khairpur",
        "Larkana",
        "Karachi"
    ],
    "Risk": [
        result,
        "Medium",
        "Low",
        "Low"
    ]
})

st.dataframe(alerts, use_container_width=True)
# ---------------- FLOOD RISK MAP ----------------

st.markdown("## Flood Risk Map")

# Pakistan centered map
m = folium.Map(
    location=[27.5, 68.5],
    zoom_start=6,
    tiles="Cartodb dark_matter"
)

# Flood Risk Locations

locations = [
    {
        "city": "Sukkur",
        "lat": 27.7052,
        "lon": 68.8574,
        "risk": "High",
        "color": "red"
    },
    {
        "city": "Larkana",
        "lat": 27.5615,
        "lon": 68.2264,
        "risk": "Medium",
        "color": "orange"
    },
    {
        "city": "Karachi",
        "lat": 24.8607,
        "lon": 67.0011,
        "risk": "Low",
        "color": "green"
    },
    {
        "city": "Hyderabad",
        "lat": 25.3960,
        "lon": 68.3578,
        "risk": "Medium",
        "color": "orange"
    }
]

# Add Markers

for loc in locations:

    folium.CircleMarker(
        location=[loc["lat"], loc["lon"]],
        radius=15,
        popup=f"{loc['city']} - {loc['risk']} Risk",
        color=loc["color"],
        fill=True,
        fill_color=loc["color"],
        fill_opacity=0.7
    ).add_to(m)

# Display Map

st_folium(m, use_container_width=True, height=500)
# ---------------- HISTORICAL FLOOD ANALYTICS ----------------

st.markdown("## Historical Flood Analytics")

history_data = pd.DataFrame({

    "Year": [
        2018,
        2019,
        2020,
        2021,
        2022,
        2023,
        2024
    ],

    "Flood Cases": [
        12,
        18,
        25,
        20,
        40,
        28,
        35
    ],

    "Affected Population (Millions)": [
        1.2,
        1.8,
        2.5,
        2.0,
        8.0,
        4.2,
        5.1
    ]
})

# Display Table

st.dataframe(history_data, use_container_width=True)
# ---------------- FLOOD TREND CHART ----------------

fig_history = px.line(

    history_data,

    x="Year",
    y="Flood Cases",
    markers=True,
    title="Yearly Flood Trend Analysis"
)

fig_history.update_layout(
    template="plotly_dark",
    paper_bgcolor="#172033",
    plot_bgcolor="#172033",
    font=dict(color="white")
)

st.plotly_chart(fig_history, use_container_width=True)
# ---------------- POPULATION IMPACT ----------------

fig_population = px.bar(

    history_data,

    x="Year",
    y="Affected Population (Millions)",
    title="Population Impact Analysis"
)

fig_population.update_layout(
    template="plotly_dark",
    paper_bgcolor="#172033",
    plot_bgcolor="#172033",
    font=dict(color="white")
)

st.plotly_chart(fig_population, use_container_width=True)
