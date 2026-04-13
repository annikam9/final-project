"""
app.py — Green Death: Environmental Defenders & Organized Crime
Run with: streamlit run app.py
Requirements: pip install streamlit plotly pandas
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Green Death", page_icon="",
                   layout="wide", initial_sidebar_state="collapsed")

if "lang" not in st.session_state:
    st.session_state.lang = "EN"

# ─────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────
LATAM = ["Argentina","Bolivia","Brazil","Chile","Colombia","Costa Rica",
         "Dominican Republic","Ecuador","Guatemala","Honduras","Mexico",
         "Nicaragua","Panama","Paraguay","Peru","Venezuela"]

STATS = {"Argentina":{"total":8,"oc_share":0.0,"murders":8,"disappearances":0,"attacks_2024":1},"Bolivia":{"total":2,"oc_share":0.0,"murders":2,"disappearances":0,"attacks_2024":0},"Brazil":{"total":413,"oc_share":8.0,"murders":407,"disappearances":6,"attacks_2024":12},"Chile":{"total":5,"oc_share":0.0,"murders":4,"disappearances":1,"attacks_2024":1},"Colombia":{"total":509,"oc_share":14.5,"murders":498,"disappearances":11,"attacks_2024":48},"Costa Rica":{"total":4,"oc_share":25.0,"murders":4,"disappearances":0,"attacks_2024":0},"Dominican Republic":{"total":4,"oc_share":0.0,"murders":4,"disappearances":0,"attacks_2024":1},"Ecuador":{"total":9,"oc_share":0.0,"murders":8,"disappearances":1,"attacks_2024":3},"Guatemala":{"total":106,"oc_share":6.6,"murders":105,"disappearances":1,"attacks_2024":20},"Honduras":{"total":155,"oc_share":1.3,"murders":149,"disappearances":6,"attacks_2024":6},"Mexico":{"total":222,"oc_share":14.0,"murders":183,"disappearances":39,"attacks_2024":19},"Nicaragua":{"total":74,"oc_share":17.6,"murders":71,"disappearances":3,"attacks_2024":4},"Panama":{"total":5,"oc_share":0.0,"murders":5,"disappearances":0,"attacks_2024":0},"Paraguay":{"total":18,"oc_share":11.1,"murders":18,"disappearances":0,"attacks_2024":0},"Peru":{"total":62,"oc_share":17.7,"murders":58,"disappearances":4,"attacks_2024":4},"Venezuela":{"total":23,"oc_share":52.2,"murders":23,"disappearances":0,"attacks_2024":1}}

OCI = {"Argentina":{"c23":5.0,"r23":5.96,"c25":5.25,"r25":5.67},"Bolivia":{"c23":4.95,"r23":4.83,"c25":5.12,"r25":4.63},"Brazil":{"c23":6.77,"r23":4.92,"c25":7.07,"r25":5.04},"Chile":{"c23":5.18,"r23":6.17,"c25":5.48,"r25":6.17},"Colombia":{"c23":7.75,"r23":5.63,"c25":7.82,"r25":5.46},"Costa Rica":{"c23":5.53,"r23":5.63,"c25":5.9,"r25":5.63},"Dominican Republic":{"c23":5.02,"r23":4.79,"c25":5.17,"r25":4.92},"Ecuador":{"c23":7.07,"r23":4.88,"c25":7.48,"r25":4.46},"Guatemala":{"c23":6.6,"r23":4.08,"c25":6.77,"r25":4.0},"Honduras":{"c23":7.05,"r23":4.08,"c25":7.1,"r25":3.92},"Mexico":{"c23":7.57,"r23":4.21,"c25":7.68,"r25":4.5},"Nicaragua":{"c23":5.72,"r23":2.08,"c25":5.73,"r25":2.0},"Panama":{"c23":6.98,"r23":4.67,"c25":6.93,"r25":4.71},"Paraguay":{"c23":7.52,"r23":3.42,"c25":7.48,"r25":3.29},"Peru":{"c23":6.4,"r23":4.38,"c25":6.62,"r25":4.46},"Venezuela":{"c23":6.72,"r23":1.88,"c25":6.97,"r25":1.88}}

PERP = {"Argentina":[{"label":"Police","pct":50.0,"color":"#2980b9"},{"label":"Hitmen","pct":25.0,"color":"#922b21"},{"label":"Private security","pct":12.5,"color":"#16a085"},{"label":"Others","pct":12.5,"color":"#555"}],"Bolivia":[{"label":"Others","pct":50.0,"color":"#555"},{"label":"Hitmen","pct":50.0,"color":"#922b21"}],"Brazil":[{"label":"Unknown","pct":37.4,"color":"#555"},{"label":"Hitmen","pct":22.3,"color":"#922b21"},{"label":"Landowners","pct":11.6,"color":"#27ae60"},{"label":"Others","pct":8.4,"color":"#444"},{"label":"Organised crime","pct":7.7,"color":"#c0392b"}],"Chile":[{"label":"Unknown","pct":40.0,"color":"#555"},{"label":"Landowners","pct":20.0,"color":"#27ae60"},{"label":"Armed forces","pct":20.0,"color":"#1a5276"},{"label":"Police","pct":20.0,"color":"#2980b9"}],"Colombia":[{"label":"Hitmen","pct":28.9,"color":"#922b21"},{"label":"Private military","pct":27.9,"color":"#7f8c8d"},{"label":"Unknown","pct":24.4,"color":"#555"},{"label":"Organised crime","pct":14.5,"color":"#c0392b"},{"label":"Police","pct":1.8,"color":"#2980b9"}],"Costa Rica":[{"label":"Unknown","pct":50.0,"color":"#555"},{"label":"Organised crime","pct":25.0,"color":"#c0392b"},{"label":"Poachers","pct":25.0,"color":"#f39c12"}],"Dominican Republic":[{"label":"Unknown","pct":75.0,"color":"#555"},{"label":"Corporations","pct":25.0,"color":"#d35400"}],"Ecuador":[{"label":"Unknown","pct":66.7,"color":"#555"},{"label":"Hitmen","pct":22.2,"color":"#922b21"},{"label":"Gov. officials","pct":11.1,"color":"#8e44ad"}],"Guatemala":[{"label":"Unknown","pct":42.1,"color":"#555"},{"label":"Hitmen","pct":31.8,"color":"#922b21"},{"label":"Organised crime","pct":6.5,"color":"#c0392b"},{"label":"Police","pct":5.6,"color":"#2980b9"},{"label":"Private security","pct":4.7,"color":"#16a085"}],"Honduras":[{"label":"Hitmen","pct":41.9,"color":"#922b21"},{"label":"Unknown","pct":34.1,"color":"#555"},{"label":"Police","pct":5.4,"color":"#2980b9"},{"label":"Armed forces","pct":5.4,"color":"#1a5276"},{"label":"Private security","pct":3.1,"color":"#16a085"}],"Mexico":[{"label":"Hitmen","pct":33.0,"color":"#922b21"},{"label":"Unknown","pct":32.1,"color":"#555"},{"label":"Organised crime","pct":14.0,"color":"#c0392b"},{"label":"Police","pct":6.8,"color":"#2980b9"},{"label":"Private military","pct":6.3,"color":"#7f8c8d"}],"Nicaragua":[{"label":"Others","pct":57.1,"color":"#555"},{"label":"Organised crime","pct":16.9,"color":"#c0392b"},{"label":"Hitmen","pct":11.7,"color":"#922b21"},{"label":"Private military","pct":6.5,"color":"#7f8c8d"},{"label":"Unknown","pct":5.2,"color":"#555"}],"Panama":[{"label":"Others","pct":60.0,"color":"#555"},{"label":"Unknown","pct":40.0,"color":"#555"}],"Paraguay":[{"label":"Police","pct":55.6,"color":"#2980b9"},{"label":"Hitmen","pct":16.7,"color":"#922b21"},{"label":"Private security","pct":11.1,"color":"#16a085"},{"label":"Organised crime","pct":11.1,"color":"#c0392b"},{"label":"Others","pct":5.6,"color":"#555"}],"Peru":[{"label":"Police","pct":37.1,"color":"#2980b9"},{"label":"Unknown","pct":29.0,"color":"#555"},{"label":"Organised crime","pct":17.7,"color":"#c0392b"},{"label":"Hitmen","pct":8.1,"color":"#922b21"},{"label":"Others","pct":8.1,"color":"#555"}],"Venezuela":[{"label":"Organised crime","pct":35.3,"color":"#c0392b"},{"label":"Armed forces","pct":23.5,"color":"#1a5276"},{"label":"Hitmen","pct":17.6,"color":"#922b21"},{"label":"Private military","pct":8.8,"color":"#7f8c8d"},{"label":"Landowners","pct":8.8,"color":"#27ae60"}]}

TIMELINE = {"Argentina":[{"y":2012,"t":3,"oc_n":0,"oc_pct":0.0},{"y":2013,"t":0,"oc_n":0,"oc_pct":0},{"y":2014,"t":0,"oc_n":0,"oc_pct":0},{"y":2015,"t":0,"oc_n":0,"oc_pct":0},{"y":2016,"t":0,"oc_n":0,"oc_pct":0},{"y":2017,"t":2,"oc_n":0,"oc_pct":0.0},{"y":2018,"t":0,"oc_n":0,"oc_pct":0},{"y":2019,"t":0,"oc_n":0,"oc_pct":0},{"y":2020,"t":1,"oc_n":0,"oc_pct":0.0},{"y":2021,"t":1,"oc_n":0,"oc_pct":0.0},{"y":2022,"t":0,"oc_n":0,"oc_pct":0},{"y":2023,"t":0,"oc_n":0,"oc_pct":0},{"y":2024,"t":1,"oc_n":0,"oc_pct":0.0}],"Bolivia":[{"y":2012,"t":0,"oc_n":0,"oc_pct":0},{"y":2013,"t":0,"oc_n":0,"oc_pct":0},{"y":2014,"t":0,"oc_n":0,"oc_pct":0},{"y":2015,"t":0,"oc_n":0,"oc_pct":0},{"y":2016,"t":0,"oc_n":0,"oc_pct":0},{"y":2017,"t":0,"oc_n":0,"oc_pct":0},{"y":2018,"t":0,"oc_n":0,"oc_pct":0},{"y":2019,"t":1,"oc_n":0,"oc_pct":0.0},{"y":2020,"t":0,"oc_n":0,"oc_pct":0},{"y":2021,"t":1,"oc_n":0,"oc_pct":0.0},{"y":2022,"t":0,"oc_n":0,"oc_pct":0},{"y":2023,"t":0,"oc_n":0,"oc_pct":0},{"y":2024,"t":0,"oc_n":0,"oc_pct":0}],"Brazil":[{"y":2012,"t":36,"oc_n":0,"oc_pct":0.0},{"y":2013,"t":32,"oc_n":0,"oc_pct":0.0},{"y":2014,"t":29,"oc_n":0,"oc_pct":0.0},{"y":2015,"t":48,"oc_n":0,"oc_pct":0.0},{"y":2016,"t":49,"oc_n":1,"oc_pct":2.0},{"y":2017,"t":58,"oc_n":17,"oc_pct":29.3},{"y":2018,"t":20,"oc_n":1,"oc_pct":5.0},{"y":2019,"t":24,"oc_n":5,"oc_pct":20.8},{"y":2020,"t":20,"oc_n":8,"oc_pct":40.0},{"y":2021,"t":26,"oc_n":0,"oc_pct":0.0},{"y":2022,"t":34,"oc_n":0,"oc_pct":0.0},{"y":2023,"t":25,"oc_n":1,"oc_pct":4.0},{"y":2024,"t":12,"oc_n":0,"oc_pct":0.0}],"Chile":[{"y":2012,"t":0,"oc_n":0,"oc_pct":0},{"y":2013,"t":0,"oc_n":0,"oc_pct":0},{"y":2014,"t":0,"oc_n":0,"oc_pct":0},{"y":2015,"t":0,"oc_n":0,"oc_pct":0},{"y":2016,"t":1,"oc_n":0,"oc_pct":0.0},{"y":2017,"t":0,"oc_n":0,"oc_pct":0},{"y":2018,"t":2,"oc_n":0,"oc_pct":0.0},{"y":2019,"t":0,"oc_n":0,"oc_pct":0},{"y":2020,"t":0,"oc_n":0,"oc_pct":0},{"y":2021,"t":1,"oc_n":0,"oc_pct":0.0},{"y":2022,"t":0,"oc_n":0,"oc_pct":0},{"y":2023,"t":0,"oc_n":0,"oc_pct":0},{"y":2024,"t":1,"oc_n":0,"oc_pct":0.0}],"Colombia":[{"y":2012,"t":9,"oc_n":0,"oc_pct":0.0},{"y":2013,"t":15,"oc_n":1,"oc_pct":6.7},{"y":2014,"t":25,"oc_n":0,"oc_pct":0.0},{"y":2015,"t":26,"oc_n":0,"oc_pct":0.0},{"y":2016,"t":36,"oc_n":1,"oc_pct":2.8},{"y":2017,"t":24,"oc_n":1,"oc_pct":4.2},{"y":2018,"t":25,"oc_n":3,"oc_pct":12.0},{"y":2019,"t":64,"oc_n":4,"oc_pct":6.2},{"y":2020,"t":65,"oc_n":0,"oc_pct":0.0},{"y":2021,"t":33,"oc_n":1,"oc_pct":3.0},{"y":2022,"t":60,"oc_n":0,"oc_pct":0.0},{"y":2023,"t":79,"oc_n":39,"oc_pct":49.4},{"y":2024,"t":48,"oc_n":24,"oc_pct":50.0}],"Costa Rica":[{"y":2012,"t":0,"oc_n":0,"oc_pct":0},{"y":2013,"t":1,"oc_n":0,"oc_pct":0.0},{"y":2014,"t":1,"oc_n":0,"oc_pct":0.0},{"y":2015,"t":0,"oc_n":0,"oc_pct":0},{"y":2016,"t":0,"oc_n":0,"oc_pct":0},{"y":2017,"t":0,"oc_n":0,"oc_pct":0},{"y":2018,"t":0,"oc_n":0,"oc_pct":0},{"y":2019,"t":1,"oc_n":0,"oc_pct":0.0},{"y":2020,"t":1,"oc_n":1,"oc_pct":100.0},{"y":2021,"t":0,"oc_n":0,"oc_pct":0},{"y":2022,"t":0,"oc_n":0,"oc_pct":0},{"y":2023,"t":0,"oc_n":0,"oc_pct":0},{"y":2024,"t":0,"oc_n":0,"oc_pct":0}],"Dominican Republic":[{"y":2012,"t":0,"oc_n":0,"oc_pct":0},{"y":2013,"t":0,"oc_n":0,"oc_pct":0},{"y":2014,"t":0,"oc_n":0,"oc_pct":0},{"y":2015,"t":0,"oc_n":0,"oc_pct":0},{"y":2016,"t":0,"oc_n":0,"oc_pct":0},{"y":2017,"t":2,"oc_n":0,"oc_pct":0.0},{"y":2018,"t":0,"oc_n":0,"oc_pct":0},{"y":2019,"t":0,"oc_n":0,"oc_pct":0},{"y":2020,"t":0,"oc_n":0,"oc_pct":0},{"y":2021,"t":0,"oc_n":0,"oc_pct":0},{"y":2022,"t":1,"oc_n":0,"oc_pct":0.0},{"y":2023,"t":0,"oc_n":0,"oc_pct":0},{"y":2024,"t":1,"oc_n":0,"oc_pct":0.0}],"Ecuador":[{"y":2012,"t":0,"oc_n":0,"oc_pct":0},{"y":2013,"t":0,"oc_n":0,"oc_pct":0},{"y":2014,"t":1,"oc_n":0,"oc_pct":0.0},{"y":2015,"t":0,"oc_n":0,"oc_pct":0},{"y":2016,"t":0,"oc_n":0,"oc_pct":0},{"y":2017,"t":0,"oc_n":0,"oc_pct":0},{"y":2018,"t":0,"oc_n":0,"oc_pct":0},{"y":2019,"t":0,"oc_n":0,"oc_pct":0},{"y":2020,"t":0,"oc_n":0,"oc_pct":0},{"y":2021,"t":3,"oc_n":0,"oc_pct":0.0},{"y":2022,"t":1,"oc_n":0,"oc_pct":0.0},{"y":2023,"t":1,"oc_n":0,"oc_pct":0.0},{"y":2024,"t":3,"oc_n":0,"oc_pct":0.0}],"Guatemala":[{"y":2012,"t":6,"oc_n":0,"oc_pct":0.0},{"y":2013,"t":6,"oc_n":1,"oc_pct":16.7},{"y":2014,"t":5,"oc_n":0,"oc_pct":0.0},{"y":2015,"t":10,"oc_n":0,"oc_pct":0.0},{"y":2016,"t":6,"oc_n":0,"oc_pct":0.0},{"y":2017,"t":3,"oc_n":0,"oc_pct":0.0},{"y":2018,"t":15,"oc_n":0,"oc_pct":0.0},{"y":2019,"t":12,"oc_n":0,"oc_pct":0.0},{"y":2020,"t":13,"oc_n":0,"oc_pct":0.0},{"y":2021,"t":4,"oc_n":0,"oc_pct":0.0},{"y":2022,"t":2,"oc_n":0,"oc_pct":0.0},{"y":2023,"t":4,"oc_n":0,"oc_pct":0.0},{"y":2024,"t":20,"oc_n":6,"oc_pct":30.0}],"Honduras":[{"y":2012,"t":25,"oc_n":0,"oc_pct":0.0},{"y":2013,"t":10,"oc_n":0,"oc_pct":0.0},{"y":2014,"t":12,"oc_n":0,"oc_pct":0.0},{"y":2015,"t":8,"oc_n":0,"oc_pct":0.0},{"y":2016,"t":14,"oc_n":0,"oc_pct":0.0},{"y":2017,"t":5,"oc_n":0,"oc_pct":0.0},{"y":2018,"t":4,"oc_n":0,"oc_pct":0.0},{"y":2019,"t":14,"oc_n":0,"oc_pct":0.0},{"y":2020,"t":17,"oc_n":0,"oc_pct":0.0},{"y":2021,"t":8,"oc_n":0,"oc_pct":0.0},{"y":2022,"t":14,"oc_n":0,"oc_pct":0.0},{"y":2023,"t":18,"oc_n":1,"oc_pct":5.6},{"y":2024,"t":6,"oc_n":1,"oc_pct":16.7}],"Mexico":[{"y":2012,"t":10,"oc_n":2,"oc_pct":20.0},{"y":2013,"t":3,"oc_n":0,"oc_pct":0.0},{"y":2014,"t":3,"oc_n":0,"oc_pct":0.0},{"y":2015,"t":4,"oc_n":0,"oc_pct":0.0},{"y":2016,"t":3,"oc_n":0,"oc_pct":0.0},{"y":2017,"t":15,"oc_n":1,"oc_pct":6.7},{"y":2018,"t":14,"oc_n":2,"oc_pct":14.3},{"y":2019,"t":18,"oc_n":2,"oc_pct":11.1},{"y":2020,"t":30,"oc_n":1,"oc_pct":3.3},{"y":2021,"t":54,"oc_n":9,"oc_pct":16.7},{"y":2022,"t":31,"oc_n":0,"oc_pct":0.0},{"y":2023,"t":18,"oc_n":4,"oc_pct":22.2},{"y":2024,"t":19,"oc_n":10,"oc_pct":52.6}],"Nicaragua":[{"y":2012,"t":0,"oc_n":0,"oc_pct":0},{"y":2013,"t":1,"oc_n":0,"oc_pct":0.0},{"y":2014,"t":0,"oc_n":0,"oc_pct":0},{"y":2015,"t":12,"oc_n":0,"oc_pct":0.0},{"y":2016,"t":8,"oc_n":0,"oc_pct":0.0},{"y":2017,"t":4,"oc_n":0,"oc_pct":0.0},{"y":2018,"t":0,"oc_n":0,"oc_pct":0},{"y":2019,"t":5,"oc_n":0,"oc_pct":0.0},{"y":2020,"t":12,"oc_n":0,"oc_pct":0.0},{"y":2021,"t":15,"oc_n":13,"oc_pct":86.7},{"y":2022,"t":3,"oc_n":0,"oc_pct":0.0},{"y":2023,"t":10,"oc_n":0,"oc_pct":0.0},{"y":2024,"t":4,"oc_n":0,"oc_pct":0.0}],"Panama":[{"y":2012,"t":0,"oc_n":0,"oc_pct":0},{"y":2013,"t":1,"oc_n":0,"oc_pct":0.0},{"y":2014,"t":0,"oc_n":0,"oc_pct":0},{"y":2015,"t":0,"oc_n":0,"oc_pct":0},{"y":2016,"t":0,"oc_n":0,"oc_pct":0},{"y":2017,"t":0,"oc_n":0,"oc_pct":0},{"y":2018,"t":0,"oc_n":0,"oc_pct":0},{"y":2019,"t":0,"oc_n":0,"oc_pct":0},{"y":2020,"t":0,"oc_n":0,"oc_pct":0},{"y":2021,"t":0,"oc_n":0,"oc_pct":0},{"y":2022,"t":0,"oc_n":0,"oc_pct":0},{"y":2023,"t":4,"oc_n":0,"oc_pct":0.0},{"y":2024,"t":0,"oc_n":0,"oc_pct":0}],"Paraguay":[{"y":2012,"t":10,"oc_n":0,"oc_pct":0.0},{"y":2013,"t":0,"oc_n":0,"oc_pct":0},{"y":2014,"t":3,"oc_n":2,"oc_pct":66.7},{"y":2015,"t":0,"oc_n":0,"oc_pct":0},{"y":2016,"t":0,"oc_n":0,"oc_pct":0},{"y":2017,"t":0,"oc_n":0,"oc_pct":0},{"y":2018,"t":0,"oc_n":0,"oc_pct":0},{"y":2019,"t":0,"oc_n":0,"oc_pct":0},{"y":2020,"t":0,"oc_n":0,"oc_pct":0},{"y":2021,"t":0,"oc_n":0,"oc_pct":0},{"y":2022,"t":3,"oc_n":0,"oc_pct":0.0},{"y":2023,"t":2,"oc_n":0,"oc_pct":0.0},{"y":2024,"t":0,"oc_n":0,"oc_pct":0}],"Peru":[{"y":2012,"t":9,"oc_n":0,"oc_pct":0.0},{"y":2013,"t":3,"oc_n":0,"oc_pct":0.0},{"y":2014,"t":9,"oc_n":0,"oc_pct":0.0},{"y":2015,"t":12,"oc_n":0,"oc_pct":0.0},{"y":2016,"t":2,"oc_n":0,"oc_pct":0.0},{"y":2017,"t":2,"oc_n":2,"oc_pct":100.0},{"y":2018,"t":0,"oc_n":0,"oc_pct":0},{"y":2019,"t":1,"oc_n":1,"oc_pct":100.0},{"y":2020,"t":6,"oc_n":0,"oc_pct":0.0},{"y":2021,"t":7,"oc_n":3,"oc_pct":42.9},{"y":2022,"t":3,"oc_n":0,"oc_pct":0.0},{"y":2023,"t":4,"oc_n":3,"oc_pct":75.0},{"y":2024,"t":4,"oc_n":2,"oc_pct":50.0}],"Venezuela":[{"y":2012,"t":0,"oc_n":0,"oc_pct":0},{"y":2013,"t":1,"oc_n":0,"oc_pct":0.0},{"y":2014,"t":0,"oc_n":0,"oc_pct":0},{"y":2015,"t":0,"oc_n":0,"oc_pct":0},{"y":2016,"t":0,"oc_n":0,"oc_pct":0},{"y":2017,"t":1,"oc_n":0,"oc_pct":0.0},{"y":2018,"t":3,"oc_n":0,"oc_pct":0.0},{"y":2019,"t":8,"oc_n":8,"oc_pct":100.0},{"y":2020,"t":0,"oc_n":0,"oc_pct":0},{"y":2021,"t":4,"oc_n":4,"oc_pct":100.0},{"y":2022,"t":4,"oc_n":0,"oc_pct":0.0},{"y":2023,"t":1,"oc_n":0,"oc_pct":0.0},{"y":2024,"t":1,"oc_n":0,"oc_pct":0.0}]}

WORLD = [{"country":"Argentina","total":8,"lat":-26.52,"lon":-62.58,"attacks_2024":1},{"country":"Australia","total":1,"lat":-29.15,"lon":150.30,"attacks_2024":0},{"country":"Bangladesh","total":7,"lat":23.07,"lon":90.68,"attacks_2024":0},{"country":"Bolivia","total":2,"lat":-16.07,"lon":-61.02,"attacks_2024":0},{"country":"Brazil","total":413,"lat":-5.63,"lon":-49.27,"attacks_2024":12},{"country":"Burkina Faso","total":2,"lat":13.38,"lon":0.67,"attacks_2024":0},{"country":"Cambodia","total":11,"lat":13.08,"lon":104.24,"attacks_2024":1},{"country":"Cameroon","total":2,"lat":8.40,"lon":14.17,"attacks_2024":1},{"country":"Canada","total":1,"lat":43.65,"lon":-79.38,"attacks_2024":0},{"country":"Chad","total":5,"lat":10.89,"lon":19.82,"attacks_2024":0},{"country":"Chile","total":5,"lat":-39.71,"lon":-72.75,"attacks_2024":1},{"country":"Colombia","total":509,"lat":4.57,"lon":-74.30,"attacks_2024":48},{"country":"Costa Rica","total":4,"lat":9.07,"lon":-83.29,"attacks_2024":0},{"country":"Democratic Republic of the Congo","total":78,"lat":-9.15,"lon":25.84,"attacks_2024":4},{"country":"Dominican Republic","total":4,"lat":18.91,"lon":-70.74,"attacks_2024":1},{"country":"Ecuador","total":9,"lat":0.81,"lon":-78.97,"attacks_2024":3},{"country":"France","total":1,"lat":43.85,"lon":1.81,"attacks_2024":0},{"country":"Gabon","total":1,"lat":1.01,"lon":13.95,"attacks_2024":0},{"country":"Gambia","total":2,"lat":13.26,"lon":-16.52,"attacks_2024":0},{"country":"Ghana","total":2,"lat":5.64,"lon":0.02,"attacks_2024":0},{"country":"Guatemala","total":106,"lat":14.14,"lon":-90.01,"attacks_2024":20},{"country":"Honduras","total":155,"lat":15.92,"lon":-85.96,"attacks_2024":6},{"country":"India","total":87,"lat":17.42,"lon":78.45,"attacks_2024":1},{"country":"Indonesia","total":25,"lat":3.56,"lon":98.74,"attacks_2024":5},{"country":"Iran","total":9,"lat":35.69,"lon":51.39,"attacks_2024":0},{"country":"Kenya","total":6,"lat":-1.23,"lon":36.84,"attacks_2024":0},{"country":"Liberia","total":6,"lat":7.01,"lon":-11.12,"attacks_2024":3},{"country":"Madagascar","total":3,"lat":-19.19,"lon":48.01,"attacks_2024":1},{"country":"Mexico","total":222,"lat":23.63,"lon":-102.55,"attacks_2024":19},{"country":"Myanmar","total":8,"lat":21.92,"lon":95.96,"attacks_2024":0},{"country":"Nicaragua","total":74,"lat":12.87,"lon":-85.21,"attacks_2024":4},{"country":"Pakistan","total":5,"lat":30.38,"lon":69.35,"attacks_2024":0},{"country":"Panama","total":5,"lat":8.54,"lon":-80.78,"attacks_2024":0},{"country":"Paraguay","total":18,"lat":-23.44,"lon":-58.44,"attacks_2024":0},{"country":"Peru","total":62,"lat":-9.19,"lon":-75.02,"attacks_2024":4},{"country":"Philippines","total":306,"lat":12.88,"lon":121.77,"attacks_2024":8},{"country":"Romania","total":2,"lat":45.94,"lon":24.97,"attacks_2024":0},{"country":"Russia","total":5,"lat":61.52,"lon":105.32,"attacks_2024":1},{"country":"South Africa","total":6,"lat":-30.56,"lon":22.94,"attacks_2024":0},{"country":"Thailand","total":13,"lat":15.87,"lon":100.99,"attacks_2024":0},{"country":"Türkiye","total":3,"lat":38.96,"lon":35.24,"attacks_2024":1},{"country":"Uganda","total":5,"lat":1.37,"lon":32.29,"attacks_2024":0},{"country":"Ukraine","total":4,"lat":48.38,"lon":31.17,"attacks_2024":0},{"country":"United States of America","total":2,"lat":37.09,"lon":-95.71,"attacks_2024":0},{"country":"Venezuela","total":23,"lat":6.42,"lon":-66.59,"attacks_2024":1}]

COL_PTS = [{"name":"Álvaro Javier Morales Flor","lat":2.623652,"lon":-76.569014,"act":"Murder","perp":"Organised crime / mafias"},{"name":"Alexander Pilcué Tenorio","lat":2.981277,"lon":-76.464849,"act":"Murder","perp":"Unknown"},{"name":"Anderson David Murillo","lat":2.567736,"lon":-72.634028,"act":"Murder","perp":"Private military actors"},{"name":"Bruno Pambelé Moreno","lat":6.85992,"lon":-71.16642,"act":"Murder","perp":"Organised crime / mafias"},{"name":"Carlos Alberto Aristizábal Morales","lat":4.815109,"lon":-75.694278,"act":"Murder","perp":"Organised crime / mafias"},{"name":"Carlos Andrés Ascué Tumbo","lat":2.783248,"lon":-76.549478,"act":"Murder","perp":"Organised crime / mafias"},{"name":"Carmelina Yule Paví","lat":2.958055,"lon":-76.27139,"act":"Murder","perp":"Organised crime / mafias"},{"name":"Dairo Yobani Aquite","lat":2.926664,"lon":-76.463493,"act":"Murder","perp":"Organised crime / mafias"},{"name":"Daniel Nolavita","lat":10.773785,"lon":-73.980969,"act":"Murder","perp":"Private military actors"},{"name":"Dino Ul Musicué","lat":3.016836,"lon":-76.400963,"act":"Murder","perp":"Unknown"},{"name":"Emanuel José Oca Cuspián","lat":2.555573,"lon":-76.067058,"act":"Murder","perp":"Organised crime / mafias"},{"name":"Erney Noa Papa","lat":-0.170979,"lon":-74.80204,"act":"Murder","perp":"Organised crime / mafias"},{"name":"Evangelina Quiguanás Quebrada","lat":2.777092,"lon":-76.324678,"act":"Murder","perp":"Organised crime / mafias"},{"name":"Eyber Danilo Poto Pazú","lat":3.035556,"lon":-76.40778,"act":"Murder","perp":"Private military actors"},{"name":"Eywar Yamid Morán Campo","lat":2.999014,"lon":-76.495341,"act":"Murder","perp":"Organised crime / mafias"},{"name":"Fernando Pérez Beltrán (Child)","lat":2.567736,"lon":-72.634028,"act":"Murder","perp":"Private military actors"},{"name":"Ferney Aponte","lat":3.331469,"lon":-76.244463,"act":"Murder","perp":"Unknown"},{"name":"Fidel Antonio Hernández Correa","lat":7.882413,"lon":-76.621602,"act":"Murder","perp":"Private military actors"},{"name":"Graciel Mendoza Valencia","lat":6.462877,"lon":-71.7274,"act":"Murder","perp":"Organised crime / mafias"},{"name":"Gustavo Taquinás","lat":2.777092,"lon":-76.324678,"act":"Murder","perp":"Organised crime / mafias"},{"name":"Harrison Okí Valencia","lat":5.28139,"lon":-76.629997,"act":"Murder","perp":"Unknown"},{"name":"Heber Rivera Méndez","lat":4.035009,"lon":-76.077656,"act":"Murder","perp":"Organised crime / mafias"},{"name":"Hilton Eduardo Barrios Jara","lat":4.091929,"lon":-72.814964,"act":"Murder","perp":"Private military actors"},{"name":"Isidoro Bautista Ortiz","lat":2.685259,"lon":-75.326884,"act":"Murder","perp":"Hitmen"},{"name":"Jaime Ernesto Páez Devia","lat":3.529167,"lon":-75.64472,"act":"Murder","perp":"Hitmen"},{"name":"Javier Condía Cárdenas","lat":5.452598,"lon":-72.456757,"act":"Murder","perp":"Organised crime / mafias"},{"name":"José Alirio Chocué Molano","lat":2.633965,"lon":-76.484074,"act":"Murder","perp":"Organised crime / mafias"},{"name":"José Antonio Lozano Puentes","lat":3.534722,"lon":-76.29556,"act":"Murder","perp":"Organised crime / mafias"},{"name":"José Elver Giraldo Villada","lat":4.092226,"lon":-76.212897,"act":"Murder","perp":"Unknown"},{"name":"José Enrique Roa Cruz","lat":2.1975,"lon":-75.98,"act":"Murder","perp":"Private military actors"},{"name":"José Naín Barón","lat":2.891944,"lon":-72.13361,"act":"Murder","perp":"Organised crime / mafias"},{"name":"Josué Castellanos Pérez","lat":6.460706,"lon":-71.728574,"act":"Murder","perp":"Organised crime / mafias"},{"name":"Lorenzo Pascal Guanga","lat":1.312205,"lon":-78.409099,"act":"Murder","perp":"Unknown"},{"name":"Ludivia Galindez Jiménez","lat":1.616317,"lon":-75.614865,"act":"Murder","perp":"Unknown"},{"name":"Luis Eduardo Sterling","lat":2.1975,"lon":-75.98,"act":"Murder","perp":"Private military actors"},{"name":"Luis Eduardo Vivas","lat":2.715266,"lon":-76.173848,"act":"Murder","perp":"Unknown"},{"name":"Luis Obdulio Ramón","lat":6.955672,"lon":-71.875802,"act":"Murder","perp":"Organised crime / mafias"},{"name":"Marián Rodríguez Camelo","lat":2.891944,"lon":-72.13361,"act":"Murder","perp":"Organised crime / mafias"},{"name":"Narciso Beleño","lat":10.445444,"lon":-75.370907,"act":"Murder","perp":"Private military actors"},{"name":"Nelson Javier Pérez Vargas","lat":3.650442,"lon":-75.58343,"act":"Murder","perp":"Organised crime / mafias"},{"name":"Segundo Virgilio Imbachí Noguera","lat":2.112028,"lon":-77.216092,"act":"Murder","perp":"Organised crime / mafias"},{"name":"Tiberio Domicó Bailarín","lat":8.172778,"lon":-76.05945,"act":"Murder","perp":"Private military actors"},{"name":"Víctor Alfonso Yule Medina","lat":2.955563,"lon":-76.269716,"act":"Murder","perp":"Organised crime / mafias"},{"name":"Víctor Manuel Vargas","lat":2.567736,"lon":-72.634028,"act":"Murder","perp":"Private military actors"},{"name":"William Ramírez Muñoz","lat":2.610742,"lon":-76.378777,"act":"Murder","perp":"Unknown"},{"name":"Willis Guillermo Robinson Sánchez","lat":6.28,"lon":-71.10028,"act":"Murder","perp":"Organised crime / mafias"},{"name":"Yilber Silva","lat":2.1975,"lon":-75.98,"act":"Murder","perp":"Private military actors"},{"name":"Yofri Heraldo Vázquez Medina","lat":2.567736,"lon":-72.634028,"act":"Murder","perp":"Private military actors"}]

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def tx(key):
    return T.get(st.session_state.lang, T["EN"]).get(key, key)

def g(word, tip):
    """Inline glossary tooltip using native browser title attribute."""
    return f'<span class="gloss" title="{tip}">{word}</span>'

def oci_arrow(v25, v23, lang="EN"):
    if v25 is None or v23 is None: return ""
    d = v25 - v23
    a = abs(d)
    vs = "vs. 2023" if lang == "EN" else "vs. 2023"
    if a < 0.05: return f'<span class="oci-arrow flat">→ {vs}</span>'
    if d > 0:    return f'<span class="oci-arrow up">↑ +{a:.2f} {vs}</span>'
    return           f'<span class="oci-arrow dn">↓ −{a:.2f} {vs}</span>'

def perp_bars_html(perps):
    rows = ""
    for p in perps:
        rows += f"""<div class="perp-row">
  <div class="perp-nm">{p['label']}</div>
  <div class="perp-bg"><div class="perp-fill" style="width:{p['pct']}%;background:{p['color']}"></div></div>
  <div class="perp-pct">{p['pct']}%</div>
</div>"""
    return rows

def oci_html(oc, lang="EN"):
    c_pct = (oc['c25'] or 0) * 10
    r_pct = (oc['r25'] or 0) * 10
    c_s = f"{oc['c25']:.2f}/10" if oc['c25'] else "—"
    r_s = f"{oc['r25']:.2f}/10" if oc['r25'] else "—"
    cr_lbl = "Criminality" if lang == "EN" else "Criminalidad"
    re_lbl = "Resilience" if lang == "EN" else "Resiliencia"
    return f"""
<div class="oci-row">
  <div class="oci-hdr">
    <span class="oci-lbl">{cr_lbl}</span>
    <div class="oci-vals"><span class="oci-score" style="color:#e74c3c">{c_s}</span>{oci_arrow(oc['c25'],oc['c23'],lang)}</div>
  </div>
  <div class="oci-bg"><div class="oci-fill" style="width:{c_pct}%;background:#e74c3c"></div></div>
</div>
<div class="oci-row" style="margin-top:12px">
  <div class="oci-hdr">
    <span class="oci-lbl">{re_lbl}</span>
    <div class="oci-vals"><span class="oci-score" style="color:#1abc9c">{r_s}</span>{oci_arrow(oc['r25'],oc['r23'],lang)}</div>
  </div>
  <div class="oci-bg"><div class="oci-fill" style="width:{r_pct}%;background:#1abc9c"></div></div>
</div>"""

# ─────────────────────────────────────────────────────────────
# TRANSLATIONS (minimal — article text injected directly)
# ─────────────────────────────────────────────────────────────
T = {
    "EN": {
        "kicker":       "Data report · Environmental violence",
        "byline":       "Story by Caroline Chaffiotte, Annika Mösl, Fernanda Gándara Marchant",
        "dash_title":   "Lethal attacks against Environmental Defenders and Organized Crime in Latin American countries",
        "dash_sub":     "Violence and criminality in numbers: Select a Latin American country to explore the full scale of attacks against environmental defenders and the organized crime scores from 2025 with comparison from 2023.",
        "dash_source":  "Source: Global Witness (2025) and Global Initiative Against Transnational Organized Crime (2023–2025).",
        "select_cty":   "Select country",
        "total_lbl":    "Total attacks",
        "since_lbl":    "since 2012",
        "oc_lbl":       "Organised crime share",
        "pct_lbl":      "% of all attacks",
        "att24_lbl":    "Attacks in 2024",
        "latest_lbl":   "latest full year",
        "perp_lbl":     "Top perpetrator types",
        "oci_lbl":      "Organized Crime Index 2025",
        "map_title":    "A global issue, concentrated in Latin America",
        "map_sub":      "Total recorded attacks against environmental defenders by country, 2012–2024. Hover for details, change zoom to Latin America or Colombia.",
        "map_source":   "Source: Global Witness (2012–2024).",
        "view_world":   "World view",
        "view_latam":   "Latin America",
        "view_col":     "Colombia (2024)",
        "tt_total":     "Total attacks",
        "tt_2024":      "Attacks 2024",
        "tt_act":       "Attack type",
        "tt_perp":      "Perpetrator",
        "chart_title":  "A rising threat: Attacks and Organized Crime over time",
        "chart_sub":    "Annual attacks against environmental defenders, from 2012 to 2024. Bar height = total attacks. Toggle to show organized crime share.",
        "chart_source": "Source: Global Witness (2012–2024).",
        "chart_cty":    "Select country",
        "total_att":    "Total attacks",
        "oc_att":       "OC-attributed attacks",
        "other_att":    "Other attacks",
        "show_oc":      "Show OC share",
        "method_title": "Methodology & Data Sources",
    },
    "ES": {
        "kicker":       "Reportaje de datos · Violencia ambiental",
        "byline":       "Reportaje de Caroline Chaffiotte, Annika Mösl, Fernanda Gándara Marchant",
        "dash_title":   "Ataques letales contra Defensores Ambientales y Crimen Organizado en países latinoamericanos",
        "dash_sub":     "Violencia y criminalidad en cifras: Selecciona un país latinoamericano para explorar la magnitud de los ataques contra defensores ambientales y los índices de crimen organizado de 2025 con comparación de 2023.",
        "dash_source":  "Fuente: Global Witness (2025) e Iniciativa Global contra el Crimen Organizado Transnacional (2023–2025).",
        "select_cty":   "Seleccionar país",
        "total_lbl":    "Ataques totales",
        "since_lbl":    "desde 2012",
        "oc_lbl":       "Participación del crimen organizado",
        "pct_lbl":      "% del total",
        "att24_lbl":    "Ataques en 2024",
        "latest_lbl":   "último año completo",
        "perp_lbl":     "Principales perpetradores",
        "oci_lbl":      "Índice de Crimen Organizado 2025",
        "map_title":    "Un problema global, concentrado en América Latina",
        "map_sub":      "Total de ataques registrados contra defensores ambientales por país, 2012–2024. Pasa el cursor para más detalles.",
        "map_source":   "Fuente: Global Witness (2012–2024).",
        "view_world":   "Vista global",
        "view_latam":   "América Latina",
        "view_col":     "Colombia (2024)",
        "tt_total":     "Ataques totales",
        "tt_2024":      "Ataques 2024",
        "tt_act":       "Tipo de ataque",
        "tt_perp":      "Perpetrador",
        "chart_title":  "Una amenaza creciente: Ataques y Crimen Organizado a lo largo del tiempo",
        "chart_sub":    "Ataques anuales contra defensores ambientales, de 2012 a 2024. Altura = total de ataques. Activa el botón para ver la participación del crimen organizado.",
        "chart_source": "Fuente: Global Witness (2012–2024).",
        "chart_cty":    "Seleccionar país",
        "total_att":    "Ataques totales",
        "oc_att":       "Ataques atribuidos al CO",
        "other_att":    "Otros ataques",
        "show_oc":      "Mostrar participación CO",
        "method_title": "Metodología y Fuentes de Datos",
    },
}

# ─────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,400&family=Source+Serif+4:opsz,wght@8..60,300;8..60,400&family=IBM+Plex+Mono:wght@400;500&display=swap');

html,body,[class*="css"]{font-family:'Source Serif 4',Georgia,serif}

.art-kicker{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.2em;color:#c0392b;text-transform:uppercase;margin-bottom:16px}
.art-title{font-family:'Playfair Display',serif;font-size:clamp(1.6rem,3vw,2.4rem);font-weight:900;line-height:1.1;color:#fff;margin-bottom:16px}
.art-subtitle{font-size:1.1rem;font-weight:300;color:#a09880;line-height:1.7;margin-bottom:24px;border-left:3px solid #c0392b;padding-left:16px}
.art-byline{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.1em;color:#6a6050;padding-top:20px;border-top:1px solid rgba(255,255,255,.08)}

.article-text{max-width:680px;margin:0 auto;font-size:1.05rem;line-height:1.85;color:#d8d0c0;font-weight:300;padding:32px 0}
.article-text p{margin-bottom:1.4em}
.section-head{font-family:'IBM Plex Mono',monospace;font-size:13px;letter-spacing:.25em;color:#c0392b;text-transform:uppercase;margin:36px 0 12px;font-weight:700;display:block}

.gloss{border-bottom:1px dashed rgba(230,126,34,.7);cursor:help}

.viz-wrap{background:#141414;border:1px solid rgba(255,255,255,.08);border-radius:8px;padding:28px;margin:16px 0}
.viz-title{font-family:'Playfair Display',serif;font-size:1.25rem;font-weight:700;color:#fff;margin-bottom:6px}
.viz-sub{font-size:.95rem;color:#a09880;margin-bottom:20px;font-weight:600}
.viz-src{font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:.08em;color:#5a5040;text-align:right;margin-top:10px}

.stat-card{background:#1c1c1c;border:1px solid rgba(255,255,255,.07);border-radius:6px;padding:16px 18px;height:100%}
.stat-lbl{font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:.15em;text-transform:uppercase;color:#6a6050;margin-bottom:8px}
.stat-val{font-family:'Playfair Display',serif;font-size:1.9rem;font-weight:700;line-height:1;margin-bottom:3px}
.stat-note{font-size:.7rem;color:#6a6050}
.red{color:#e74c3c}.amber{color:#f39c12}.teal{color:#1abc9c}

.perp-row{display:flex;align-items:center;gap:8px;margin-bottom:7px}
.perp-nm{font-family:'IBM Plex Mono',monospace;font-size:9px;color:#a09880;width:110px;flex-shrink:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.perp-bg{flex:1;height:7px;background:#252525;border-radius:3px;overflow:hidden}
.perp-fill{height:100%;border-radius:3px}
.perp-pct{font-family:'IBM Plex Mono',monospace;font-size:9px;color:#6a6050;width:32px;text-align:right}

.oci-row{display:flex;flex-direction:column;gap:5px}
.oci-hdr{display:flex;justify-content:space-between;align-items:center}
.oci-lbl{font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:.1em;text-transform:uppercase;color:#6a6050}
.oci-vals{display:flex;align-items:center;gap:6px}
.oci-score{font-family:'Playfair Display',serif;font-size:1.2rem;font-weight:700}
.oci-arrow{font-family:'IBM Plex Mono',monospace;font-size:10px;white-space:nowrap}
.up{color:#e74c3c}.dn{color:#1abc9c}.flat{color:#6a6050}
.oci-bg{height:5px;background:#252525;border-radius:3px;overflow:hidden}
.oci-fill{height:100%;border-radius:3px}

[data-testid="stAppViewContainer"]{background:#0d0d0d}
[data-testid="stHeader"]{background:#0d0d0d}
footer{visibility:hidden}
div[data-testid="stVerticalBlock"]>div{background:transparent}
.stSelectbox label{color:#fff!important;font-family:'IBM Plex Mono',monospace!important;font-size:13px!important}
.stSelectbox>div>div{background:#1c1c1c!important;border-color:rgba(255,255,255,.2)!important;color:#e8e0d0!important}
.stRadio label{color:#fff!important;font-family:'IBM Plex Mono',monospace!important;font-size:12px!important}
.stToggle label{color:#fff!important;font-family:'IBM Plex Mono',monospace!important;font-size:12px!important}
.stExpander{background:#141414!important;border-color:rgba(255,255,255,.15)!important}
.stExpander summary{color:#e8e0d0!important;font-family:'IBM Plex Mono',monospace!important;font-size:13px!important;font-weight:600!important;letter-spacing:.08em}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# LANGUAGE TOGGLE
# ─────────────────────────────────────────────────────────────
_, lc = st.columns([8, 1])
with lc:
    lang = st.radio("", ["EN", "ES"],
                    index=0 if st.session_state.lang == "EN" else 1,
                    horizontal=True, label_visibility="collapsed", key="lang_radio")
    st.session_state.lang = lang

L = st.session_state.lang

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
title_en = 'Green Death: How Organized Crime <span style="color:#e74c3c">Threatens</span> Environmental Defenders'
title_es = 'Muerte verde: cómo el crimen organizado <span style="color:#e74c3c">amenaza</span> a los defensores ambientales'
sub_en   = "Standing between nature and destruction comes at a deadly price — especially in Latin America."
sub_es   = "Defender la naturaleza tiene un precio mortal, especialmente en Latinoamérica."

import base64

def img_to_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""

header_img = img_to_b64("defenders_project/header.jpeg")  # Pfad ggf. anpassen
header_src = f"data:image/jpeg;base64,{header_img}" if header_img else ""

st.markdown(f"""
<div style="position:relative;overflow:hidden;min-height:280px;padding:32px 24px 32px">
  {"" if not header_src else f'<img src="{header_src}" style="position:absolute;right:0;top:0;height:100%;width:70%;object-fit:cover;object-position:center;opacity:0.30;mask-image:linear-gradient(to left,rgba(0,0,0,0.9) 0%,rgba(0,0,0,0) 100%);-webkit-mask-image:linear-gradient(to left,rgba(0,0,0,0.9) 0%,rgba(0,0,0,0) 100%)">'}
  <div style="position:relative;z-index:1;max-width:640px">
    <div class="art-kicker">{tx('kicker')}</div>
    <div class="art-title">{title_en if L=="EN" else title_es}</div>
    <div class="art-subtitle">{sub_en if L=="EN" else sub_es}</div>
    <div class="art-byline">{tx('byline')}</div>
  </div>
  <div style="position:absolute;bottom:8px;right:10px;font-family:'IBM Plex Mono',monospace;font-size:9px;color:rgba(255,255,255,0.3);text-align:right;z-index:2;max-width:320px;line-height:1.4">
    Picture: "kilimanjaro - rainforest canopy" by tommorphy, licensed under CC BY-SA 2.0.<br>Color and frame change done by Caroline Chaffiotte.
  </div>
</div>
<hr style="border-color:rgba(255,255,255,.07);margin:0">
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ARTICLE — INTRO
# ─────────────────────────────────────────────────────────────
if L == "EN":
    st.markdown(f"""
<div class="article-text">
<p>"My bodyguards had noticed motorcycle movements. A person from the community told me they had already sent two {g('pollos','Hitmen')} to track me, but I hadn't given them a shot. I always went out with guards. They said, 'If we can't get her this week, we'll just bomb the house,'" Jani Silva recalls.</p>
<p>Silva, a 63-year-old farmer and {g('environmental defender','Individuals who peacefully protect and promote human rights relating to the environment')}, lives in the Putumayo region of Colombia, in the Amazon rainforest.</p>
<p>"That was horrible for me. My grandkids come here, my children. I got so nervous; I couldn't speak. I called the guards to stay alert. Afterward, I locked myself in my room and broke down. They break you down bit by bit. Even if they don't kill you, they are killing you slowly."</p>
<p>For almost 50 years, she has put her life at risk defending her home against extractive industries like mining and logging, and more recently, {g('organized crime', 'Criminal enterprises that capitalize on political, social, and economic pressures for financial gain')}. Other environmental defenders in the region have been <strong>killed for the same work</strong>.</p>
</div>
""", unsafe_allow_html=True)
else:
    st.markdown(f"""
<div class="article-text">
<p>"Mis escoltas habían detectado movimiento de motos. Una persona de la comunidad me dijo que ya habían mandado dos {g('pollos','Sicarios')}, que me habían estado haciendo seguimiento, pero que no había dado tiro porque siempre salía con escoltas. Dijeron: 'si esta semana no podemos, le metemos un bombazo a esa casa'", recuerda Jani Silva.</p>
<p>Silva, una agricultora y {g('defensora ambiental','Personas que defienden y promueven pacíficamente los derechos humanos relacionados con el medio ambiente')}, de 63 años, vive en la región de Putumayo en Colombia, ubicada en la selva amazónica.</p>
<p>"Eso fue horrible para mí [...] Mis nietos vienen aquí, mis hijos. Me puse tan nerviosa que no podía hablar. Llamé a los escoltas y les dije 'estén pendientes' y pusimos la alerta. Después, me encerré en mi cuarto y me quebré. Poco a poco cómo lo van quebrando a uno. Incluso si no te matan, te van matando de a poquito."</p>
<p>Por casi 50 años, ha defendido su hogar frente a industrias extractivas como la minería y la tala, y más recientemente, frente al {g('crimen organizado', 'Organizaciones delictivas que se aprovechan de las presiones políticas, sociales y económicas para obtener beneficios económicos')}. Cientos de defensores en la región han sido <strong>asesinados por hacer lo mismo</strong>.</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# VIZ 1: DASHBOARD
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="viz-wrap">
<div class="viz-title">{tx('dash_title')}</div>
<div class="viz-sub">{tx('dash_sub')}</div>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="viz-wrap">', unsafe_allow_html=True)
    dash_cty = st.selectbox(tx("select_cty"), LATAM, index=LATAM.index("Colombia"), key="dash_cty")
    s   = STATS[dash_cty]
    oc  = OCI[dash_cty]
    perps = PERP.get(dash_cty, [])

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="stat-card">
  <div class="stat-lbl">{tx('total_lbl')}</div>
  <div class="stat-val red">{s['total']:,}</div>
  <div class="stat-note">{tx('since_lbl')}</div>
</div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="stat-card">
  <div class="stat-lbl">{tx('oc_lbl')}</div>
  <div class="stat-val amber">{s['oc_share']}%</div>
  <div class="stat-note">{tx('pct_lbl')}</div>
</div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="stat-card">
  <div class="stat-lbl">{tx('att24_lbl')}</div>
  <div class="stat-val red">{s['attacks_2024']}</div>
  <div class="stat-note">{tx('latest_lbl')}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    cp, co = st.columns(2)
    with cp:
        st.markdown(f"""<div class="stat-card">
  <div class="stat-lbl">{tx('perp_lbl')}</div>
  {perp_bars_html(perps)}
</div>""", unsafe_allow_html=True)
    with co:
        st.markdown(f"""<div class="stat-card">
  <div class="stat-lbl">{tx('oci_lbl')}</div>
  {oci_html(oc, L)}
</div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="viz-src">{tx("dash_source")}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ARTICLE — MID 1
# ─────────────────────────────────────────────────────────────
if L == "EN":
    st.markdown("""
<div class="article-text">
<span class="section-head">A DEADLY PATTERN</span>
<p><strong>The link between organized crime and environmental defenders is supported by numbers.</strong> Uncovering it required piecing together two independent sources: the Organized Crime Index by NGO <a href="https://globalinitiative.net/initiatives/ocindex/" target="_blank" style="color:#e74c3c">Global Initiative</a>, which scores the levels of criminal activity within countries (like drug-trafficking) and watchdog <a href="https://globalwitness.org/en/campaigns/land-and-environmental-defenders/in-numbers-lethal-attacks-against-defenders-since-2012/" target="_blank" style="color:#e74c3c">Global Witness</a>'s data on lethal incidents against defenders.</p>
<p>The merged data from 2021 and 2023 shows stark results worldwide: if a country's criminality score goes up by one, <strong>nine more environmental defenders could be killed</strong>. More realistically, a country's score would increase by 0.5, predicting around <strong>four additional deaths</strong>.</p>
<p>This suggests the international threat organized crime poses to people defending the environment. However, these results have to be put into perspective, given limitations regarding attack records and the small scope of the analysis.</p>
<span class="section-head">ON THE FRONTLINE</span>
<p>Since 2012, Global Witness has recorded <strong>2,223</strong> killings and disappearances across the world. Four out of five occurred in Latin America and <strong>a quarter of all defenders attacked were Colombian</strong>, a testament to its history of criminal violence. For decades, the country has struggled with guerrilla groups vying for political power. In 2016, <span class="gloss" title="Revolutionary Armed Forces of Colombia">FARC</span>, the largest and deadliest armed group, reached a peace treaty with the government.</p>
<p>Vanessa Torres, assistant director of the NGO Ambiente y Sociedad, explains how Colombia's conflict is related to environmental violence: "During [President] Ivan Duque's government, there was no follow-through on the treaty's implementation. Those four years led to <strong>new illegal armed groups that are focused on territorial control</strong>. It is a large criminal enterprise across the region."</p>
<p>These <strong>organized crime</strong> groups are drawn to rural, resource-rich lands to pursue unregulated financial profit with activities like gold mining and coca cultivation.</p>
<p>Competition for natural resources has intensified the situation. "There has been a lot more pressure for local communities to defend their territories," Pedro Cabezas, international coordinator for the Central American Alliance on Mining says, "As this pressure continues, there is more resistance, and <strong>with this resistance, there is more persecution of defenders</strong>." This pressure extends past the borders of Latin America, representing a global trend.</p>
</div>
""", unsafe_allow_html=True)
else:
    st.markdown("""
<div class="article-text">
<span class="section-head">UN PATRÓN MORTAL</span>
<p><strong>La relación entre el crimen organizado y los defensores ambientales está respaldada por los números.</strong> Para investigarla, fue necesario cruzar dos fuentes independientes: el Índice de Crimen Organizado de la ONG <a href="https://globalinitiative.net/initiatives/ocindex/" target="_blank" style="color:#e74c3c">Global Initiative</a>, que evalúa los niveles de actividad delictiva en los países (como el narcotráfico), y los datos de la organización <a href="https://globalwitness.org/en/campaigns/land-and-environmental-defenders/in-numbers-lethal-attacks-against-defenders-since-2012/" target="_blank" style="color:#e74c3c">Global Witness</a> sobre incidentes mortales contra defensores.</p>
<p>Los datos combinados de 2021 y 2023 son claros a nivel mundial: si la puntuación de criminalidad de un país aumenta en un punto, podrían morir <strong>nueve defensores más</strong>. Siendo más realistas, la puntuación de un país aumentaría en 0,5, lo que predice unas <strong>cuatro muertes adicionales</strong>.</p>
<p>Los números sugieren que el crimen organizado representa una amenaza real para quienes defienden el medio ambiente. Sin embargo, deben leerse con cautela dadas las limitaciones en cuanto a la documentación de ataques y el alcance del análisis.</p>
<span class="section-head">EN PRIMERA LÍNEA</span>
<p>Desde 2012, Global Witness ha registrado <strong>2.223</strong> asesinatos y desapariciones a defensores ambientales en todo el mundo. Cuatro de cada cinco tuvieron lugar en América Latina y <strong>una cuarta parte de todos los defensores atacados eran colombianos</strong>, lo que refleja su historia de violencia criminal. Durante décadas, el país ha luchado contra grupos guerrilleros que compiten por el poder político. En 2016, las <span class="gloss" title="Fuerzas Armadas Revolucionarias de Colombia">FARC</span> alcanzaron un acuerdo de paz con el gobierno.</p>
<p>Vanessa Torres, subdirectora de la ONG Ambiente y Sociedad, explica cómo el conflicto colombiano está relacionado con la violencia ambiental: "Durante el gobierno de Iván Duque, no hubo apoyo ni seguimiento a la continuidad del acuerdo. Esos cuatro años dieron lugar a la aparición de <strong>nuevos grupos ilegales armados que buscan control territorial</strong>. Se trata de una gran empresa criminal que opera en toda la región".</p>
<p>Atraídos por las ganancias que dejan actividades como la minería ilegal y el cultivo de coca, estos grupos de <strong>crimen organizado</strong> se expanden hacia territorios rurales donde el estado tiene poca presencia.</p>
<p>La competencia por los recursos naturales ha agravado la situación. "Ha aumentado considerablemente la presión sobre las comunidades locales para que defiendan sus territorios", afirma Pedro Cabezas. "A medida que esta presión continúa, aumenta la resistencia y, <strong>con esta resistencia, se intensifica la persecución de los defensores</strong>". Esta presión traspasa las fronteras de Latinoamérica, representando una tendencia global.</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# VIZ 2: MAP
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="viz-wrap">
<div class="viz-title">{tx('map_title')}</div>
<div class="viz-sub">{tx('map_sub')}</div>
</div>
""", unsafe_allow_html=True)

with st.container():
    map_view = st.radio("", [tx("view_world"), tx("view_latam"), tx("view_col")],
                        horizontal=True, key="map_view", label_visibility="collapsed")

    def build_map(view):
        fig = go.Figure()
        countries = [r["country"] for r in WORLD]
        z_vals    = [r["total"]   for r in WORLD]
        htexts    = [f"<b>{r['country']}</b><br>{tx('tt_total')}: {r['total']}<br>{tx('tt_2024')}: {r['attacks_2024']}" for r in WORLD]

        fig.add_trace(go.Choropleth(
            locations=countries, locationmode="country names",
            z=z_vals, text=htexts,
            hovertemplate="%{text}<extra></extra>",
            colorscale=[[0,"#4a4a4a"],[0.001,"#ffcccc"],[0.05,"#e87070"],
                        [0.15,"#c93030"],[0.40,"#9b1a1a"],[1.0,"#5c0000"]],
            zmin=0, zmax=520, showscale=False,
            marker=dict(line=dict(color="rgba(255,255,255,0.1)", width=0.4)),
        ))

        if view == "col":
            df_col = pd.DataFrame(COL_PTS)
            is_oc  = df_col["perp"].str.contains("Organised crime", na=False)
            for mask, color in [(~is_oc, "#546778"), (is_oc, "#e74c3c")]:
                sub = df_col[mask]
                if len(sub):
                    fig.add_trace(go.Scattergeo(
                        lat=sub["lat"], lon=sub["lon"], mode="markers",
                        marker=dict(symbol="cross", size=10, color=color,
                                    line=dict(width=2.5, color=color)),
                        text=sub["name"],
                        customdata=list(zip(sub["act"], sub["perp"])),
                        hovertemplate=f"<b>%{{text}}</b><br>{tx('tt_act')}: %{{customdata[0]}}<br>{tx('tt_perp')}: %{{customdata[1]}}<extra></extra>",
                        showlegend=False,
                    ))

        geo_cfgs = {
            "world": dict(scope="world", projection_type="natural earth",
                          center=dict(lat=10, lon=0), projection_scale=1),
            "latam": dict(scope="world", projection_type="mercator",
                          center=dict(lat=-15, lon=-75), projection_scale=1.2,
                          lonaxis=dict(range=[-115, -30]),
                          lataxis=dict(range=[-60, 35])),
            "col":   dict(scope="world", projection_type="mercator",
                          center=dict(lat=4.5, lon=-74.0), projection_scale=7),
        }
        fig.update_layout(
            geo=dict(showframe=False, showcoastlines=True,
                     coastlinecolor="rgba(255,255,255,.15)",
                     showland=True, landcolor="#3a3a3a",
                     showocean=True, oceancolor="#181818",
                     showcountries=True, countrycolor="rgba(255,255,255,.1)",
                     bgcolor="#0d0d0d", **geo_cfgs[view]),
            paper_bgcolor="#0d0d0d", plot_bgcolor="#0d0d0d",
            margin=dict(l=0,r=0,t=0,b=0), height=480,
            hoverlabel=dict(bgcolor="#141414", bordercolor="rgba(255,255,255,.2)",
                            font=dict(color="#e8e0d0", size=12)),
        )
        return fig

    vk = "world"
    if map_view == tx("view_latam"): vk = "latam"
    elif map_view == tx("view_col"):  vk = "col"

    st.plotly_chart(build_map(vk), use_container_width=True, config={"displayModeBar": False})

    # Legend
    st.markdown("""
<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:6px">
  <span style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#6a6050">Attacks →</span>
  <span style="display:inline-block;width:18px;height:8px;background:#4a4a4a;border:1px solid #666;border-radius:2px"></span><span style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#6a6050">0</span>
  <span style="display:inline-block;width:18px;height:8px;background:#ffcccc;border-radius:2px"></span><span style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#6a6050">1–10</span>
  <span style="display:inline-block;width:18px;height:8px;background:#e87070;border-radius:2px"></span><span style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#6a6050">11–50</span>
  <span style="display:inline-block;width:18px;height:8px;background:#c93030;border-radius:2px"></span><span style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#6a6050">51–150</span>
  <span style="display:inline-block;width:18px;height:8px;background:#9b1a1a;border-radius:2px"></span><span style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#6a6050">151–300</span>
  <span style="display:inline-block;width:18px;height:8px;background:#5c0000;border-radius:2px"></span><span style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#6a6050">300+</span>
  &nbsp;
  <span style="color:#e74c3c;font-size:13px">✕</span><span style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#6a6050">OC 2024</span>
  <span style="color:#546778;font-size:13px">✕</span><span style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#6a6050">Other 2024</span>
</div>
""", unsafe_allow_html=True)
    st.markdown(f'<div class="viz-src">{tx("map_source")}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ARTICLE — MID 2
# ─────────────────────────────────────────────────────────────
if L == "EN":
    st.markdown(f"""
<div class="article-text">
<p>Jani Silva and her organization, {g('ADISPA','Association for Sustainable Development of the Amazon Pearl')}, are currently threatened by an armed group. She says that due to their vocal opposition to organized crime, they're particularly vulnerable. Silva believes the group wants to take control of the organization to help leverage power. She says that two leaders close to her have already been killed.</p>
<span class="section-head">CRIMINAL EVOLUTION</span>
<p>Organized crime has appeared as a perpetrator of violence against defenders throughout the last decade. Its frequency varies across countries, with the highest concentration in Latin America.</p>
</div>
""", unsafe_allow_html=True)
else:
    st.markdown(f"""
<div class="article-text">
<p>Jani Silva y su organización, {g('ADISPA','Asociación para el Desarrollo Integral Sostenible de la Perla Amazónica')}, se encuentran actualmente amenazadas por un grupo armado. Afirma que, debido a su abierta oposición al crimen organizado, son especialmente vulnerables. Silva cree que el grupo quiere tomar el control de la organización para reforzar su poder. Afirma que ya han asesinado a dos líderes cercanos a ella.</p>
<span class="section-head">EVOLUCIÓN CRIMINAL</span>
<p>El crimen organizado ataca cada vez más a defensores ambientales. La presencia de estos grupos varía de un país a otro, con la mayor concentración en América Latina.</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# VIZ 3: BAR CHART
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="viz-wrap">
<div class="viz-title">{tx('chart_title')}</div>
<div class="viz-sub">{tx('chart_sub')}</div>
</div>
""", unsafe_allow_html=True)

with st.container():
    cc1, cc2 = st.columns([2, 2])
    with cc1:
        chart_cty = st.selectbox(tx("chart_cty"), LATAM,
                                  index=LATAM.index("Colombia"), key="chart_cty")
    with cc2:
        show_oc = st.toggle(tx("show_oc"), value=False, key="show_oc")

    tl      = TIMELINE[chart_cty]
    years   = [d["y"] for d in tl]
    totals  = [d["t"] for d in tl]
    oc_ns   = [d["oc_n"] for d in tl]
    others  = [d["t"] - d["oc_n"] for d in tl]
    oc_pcts = [d["oc_pct"] for d in tl]

    LAY = dict(
        paper_bgcolor="#141414", plot_bgcolor="#141414",
        font=dict(family="IBM Plex Mono, monospace", color="#6a6050", size=10),
        xaxis=dict(showgrid=False, tickmode="array", tickvals=years,
                   ticktext=[str(y) for y in years], color="#6a6050"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,.04)", color="#6a6050", title=""),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#a09880", size=10),
                    orientation="h", x=0, y=1.08),
        margin=dict(l=40, r=20, t=40, b=40), height=340,
        hoverlabel=dict(bgcolor="#141414", bordercolor="rgba(255,255,255,.15)",
                        font=dict(color="#e8e0d0", size=12)),
        bargap=0.25, transition=dict(duration=500, easing="cubic-in-out"),
    )

    fig_bar = go.Figure()
    if show_oc:
        fig_bar.add_trace(go.Bar(
            x=years, y=others, name=tx("other_att"),
            marker=dict(color="#e87070", line=dict(width=0)),
            hovertemplate=f"<b>%{{x}}</b><br>{tx('other_att')}: %{{y}}<extra></extra>",
        ))
        fig_bar.add_trace(go.Bar(
            x=years, y=oc_ns, name=tx("oc_att"),
            marker=dict(color="#7b0000", line=dict(width=0)),
            hovertemplate=f"<b>%{{x}}</b><br>{tx('oc_att')}: %{{y}}<br>OC share: %{{customdata:.1f}}%<extra></extra>",
            customdata=oc_pcts,
        ))
        fig_bar.update_layout(barmode="stack", **LAY)
    else:
        fig_bar.add_trace(go.Bar(
            x=years, y=totals, name=tx("total_att"),
            marker=dict(color="#e87070", line=dict(width=0)),
            hovertemplate=f"<b>%{{x}}</b><br>{tx('total_att')}: %{{y}}<extra></extra>",
        ))
        fig_bar.update_layout(barmode="group", **LAY)

    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
    st.markdown(f'<div class="viz-src">{tx("chart_source")}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ARTICLE — CLOSING
# ─────────────────────────────────────────────────────────────
if L == "EN":
    st.markdown("""
<div class="article-text">
<p>Colombia went from <strong>no recorded organized crime attacks</strong> in 2022 to <strong>39 in 2023 and 24 the following year</strong>. The cause of this is unknown, but Vladimir Pacheco, a professor at Aarhus University specializing in extractive industries, credits it to high levels of impunity, especially in Latin American countries:</p>
<p>"I think it is <strong>more dangerous for an environmental defender</strong> because nothing can stop a warlord [...] or a drug cartel because these governments, they're either abetting it or aiding it or they don't have the ability, even if they want to."</p>
<p>Pacheco points out that states are also benefiting from extractive markets, both legal and illegal, meaning that they are less incentivized to enforce consequences, which traps environmental defenders in a vicious, violent cycle.</p>
<p>"It's not that people don't know there's a problem," says Environmental Law Institute attorney Kristine Perry, "It's about the enforcement and compliance with laws, holding people to account when defenders are attacked, and cutting off the escalation because oftentimes it's not an isolated attack."</p>
<p>Latin America is not an exception; environmental violence is a global phenomenon. Nana Kwesi Osei Bonsu, an indigenous Ghanaian defender, knows this all too well, "I was forced to flee my homeland because of threats to my life." He credits this to the lack of enforcement from the state.</p>
<p>These international failures in political leadership and law enforcement could mean that the number of deaths and disappearances is higher. Also, the recorded attacks don't include other forms of violence like intimidation or threats, suggesting that <strong>deadly violence is only part of a larger issue</strong>.</p>
<p>However, the tide may be starting to turn. As Kristine Perry observes, countries are beginning to build "better protection mechanisms for defenders." While enforcement remains the missing link, international pressure is mounting. The upcoming UN Climate Change Conference will serve as a platform where organizations are set to demand the creation of an environmental justice group to safeguard the lives of those who protect the planet.</p>
<p>Despite knowing the cost, defenders like Jani Silva persist, "<strong>Why is defending what we should all be defending going to put me at risk?</strong> Not just me, but my family, my daily life, and my essence as a campesina [...] Seeing young people representing the youth and involving others keeps me going. <strong>I feel like I can <em>not</em> not be here</strong>."</p>
</div>
""", unsafe_allow_html=True)
else:
    st.markdown("""
<div class="article-text">
<p>Colombia pasó de <strong>no registrar ningún ataque efectuado por el crimen organizado</strong> en 2022 a <strong>39 en 2023 y 24 al año siguiente</strong>. No hay una explicación clara, pero Vladimir Pacheco, profesor de la Universidad de Aarhus y especialista en industrias extractivas, lo atribuye a los altos niveles de impunidad en la región.</p>
<p>"Creo que es mucho <strong>más peligroso para un defensor ambiental</strong> porque nada puede detener a un cabecilla [...] o a un cartel, ya que estos gobiernos, o están metidos en eso o lo encubren, o bien no tienen la capacidad de detenerlo aunque quieran".</p>
<p>Pacheco señala que los estados también se benefician de los mercados extractivos, tanto legales como ilegales. Por ello, tienen menos incentivos para aplicar sanciones, lo que atrapa a los defensores en un círculo vicioso y violento.</p>
<p>"No es que la gente no sepa que hay un problema", afirma Kristine Perry, abogada del Environmental Law Institute, "se trata de la aplicación y el cumplimiento de las leyes, de exigir responsabilidades cuando se ataca a los defensores y de frenar la escalada, porque a menudo no se trata de un ataque aislado".</p>
<p>América Latina no es la excepción. La violencia contra defensores ambientales es un problema global. Nana Kwesi Osei Bonsu, un defensor indígena ghanés, lo vivió en carne propia: "Me vi obligado a huir de mi tierra natal debido a las amenazas contra mi vida". Él culpa al estado por no hacer cumplir la ley.</p>
<p>Los números cuentan solo una parte de la historia. Los ataques documentados solo incluyen muertes y desapariciones, dejando de lado otras formas de violencia como la intimidación o las amenazas, lo que sugiere que <strong>la violencia letal es solo parte de un problema mayor</strong>.</p>
<p>Sin embargo, como observa Kristine Perry, los países están comenzando a crear "mejores mecanismos de protección para los defensores". La presión internacional crece y la próxima Conferencia de las Naciones Unidas sobre el Cambio Climático servirá de plataforma: algunas organizaciones exigirán la creación de un grupo de justicia ambiental que proteja las vidas de quienes protegen el planeta.</p>
<p>A pesar de conocer el costo, defensores como Jani Silva persisten: "<strong>¿Por qué defender lo que todos deberíamos defender me va a poner en peligro?</strong> No solo a mí, sino a mi familia, mi vida cotidiana y mi esencia como campesina [...] Ver a jóvenes que representan a la juventud e involucran a otros me da fuerzas para seguir adelante. <strong>Siento que <em>no</em> puedo no estar aquí"</strong>.</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# METHODOLOGY
# ─────────────────────────────────────────────────────────────
method_en = """<strong>Methodology</strong>

The analysis combines <a href="https://globalwitness.org/en/campaigns/land-and-environmental-defenders/in-numbers-lethal-attacks-against-defenders-since-2012/" target="_blank" style="color:#e74c3c">Global Witness</a>'s data on attacks against environmental defenders and the Organized Crime Index from <a href="https://globalinitiative.net/initiatives/ocindex/" target="_blank" style="color:#e74c3c">Global Initiative</a>. The merged dataset includes 35 cases with recorded attacks in 2021 and 2023. The relationship between the level of criminality and number of attacks was examined with a statistical regression model. Additional factors were included to isolate the effect, including population size, Corruption Perception Index, countries' resilience to organized crime, year, region, and country. The results indicate a positive relationship: countries that increase in criminality score also see an increase in attacks. However, the findings should be interpreted cautiously due to the limited sample size, possible underreporting of cases, and less consistent results for changes within individual countries over time.

**Data sources**

Global Organized Crime Index. (2021-2025). The Organized Crime Index. Ocindex.net; Global Initiative Against Transnational Organized Crime. https://ocindex.net/ 

Global Witness. (2012-2024). In numbers: Lethal attacks against defenders since 2012. Global Witness.org. Global Witness.https://globalwitness.org/en/campaigns/land-and-environmental-defenders/in-numbers-lethal-attacks-against-defenders-since-2012/
"""

method_es = """<strong>Metodología</strong>

El análisis combina los datos de <a href="https://globalwitness.org/en/campaigns/land-and-environmental-defenders/in-numbers-lethal-attacks-against-defenders-since-2012/" target="_blank" style="color:#e74c3c">Global Witness</a> sobre ataques contra defensores ambientales y el Índice de Crimen Organizado de <a href="https://globalinitiative.net/initiatives/ocindex/" target="_blank" style="color:#e74c3c">Global Initiative</a>. El conjunto de datos combinado incluye 35 casos con ataques registrados en 2021 y 2023. La relación entre el nivel de criminalidad y el número de ataques se examinó con un modelo de regresión estadística. Se incluyeron factores adicionales para aislar el efecto, como el tamaño de la población, el Índice de Percepción de la Corrupción, la resiliencia de los países ante el crimen organizado, el año, la región y el país. Los resultados indican una relación positiva. Sin embargo, los hallazgos deben interpretarse con cautela.

**Fuentes de datos**

Global Organized Crime Index. (2021-2025). The Organized Crime Index. Ocindex.net; Global Initiative Against Transnational Organized Crime. https://ocindex.net/ 

Global Witness. (2012-2024). In numbers: Lethal attacks against defenders since 2012. Global Witness.org; Global Witness. https://globalwitness.org/en/campaigns/land-and-environmental-defenders/in-numbers-lethal-attacks-against-defenders-since-2012/
"""

with st.expander(tx("method_title")):
    st.markdown(
        f'<div style="font-family:\'Source Serif 4\',serif;font-size:.9rem;color:#a09880;line-height:1.8">{method_en if L=="EN" else method_es}</div>',
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
footer_en = "Global Witness (2012–2024) · Organized Crime Index (2021–2025) (GI-TOC) · Caroline Chaffiotte, Annika Mösl, Fernanda Gándara Marchant"
footer_es = "Global Witness (2012–2024) · Índice de Crimen Organizado (2021–2025) (GI-TOC) · Caroline Chaffiotte, Annika Mösl, Fernanda Gándara Marchant"
st.markdown(f"""
<div style="border-top:1px solid rgba(255,255,255,.07);margin-top:48px;padding:24px 0;text-align:center;font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.1em;color:#5a5040">
{footer_en if L=="EN" else footer_es}
</div>
""", unsafe_allow_html=True)