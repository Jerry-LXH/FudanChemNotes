import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from dataBase import FilterDatabaseSQLite
from importSpectrum import *
from dealWithSpectrum import *

### Run with [streamlit run SmilE/Optics_exp/Database_of_filters/filter_viewer.py], use your own directory.

step = 0.5
db = FilterDatabaseSQLite("/Users/jerryling/Documents/Research/Department_of_chemistry/SmilE/Optics_exp/Database_of_filters/filters.db")

# layout of page
st.set_page_config(layout="wide")
st.title("Browser of Filter Database")

# Seraching
keyword = st.text_input("Search for Filters: (name/type/manufacturer/notes)", "")

if keyword.strip():
    filters = db.search(keyword)
else:
    filters = db.list_all_filters(order_by='manufacturer')

# Mode of Units
mode = st.radio("Mode of Units", ["Transmission (%)", "Optical Density (OD)"], horizontal=True)

selected_filters = []

st.sidebar.header("Display Settings")
wl_range = st.sidebar.text_input("Wavelength Range (nm, 例如 400-700)", "300-900")
try:
    wl_min, wl_max = [float(x) for x in wl_range.split("-")]
except:
    wl_min, wl_max = 300, 900

# Showing the results
for f in filters:
    fid, name, ftype, manufacturer, notes = f
    wl, tr = db.get_filter_spectrum(name)

    # --- 裁剪数据 ---
    wl = np.asarray(wl, dtype=float)
    tr = np.asarray(tr, dtype=float)
    mask = (wl >= wl_min) & (wl <= wl_max)
    if not np.any(mask):
        continue
    new_wl, new_tr = wl[mask], tr[mask]

    col1, col2, col3, col4 = st.columns([2,4,1,2])

    with col1:
        st.markdown(f"**{name}**")
        st.text(f"Type: {ftype}\nManu: {manufacturer}\nNotes: {notes}")

    with col2:
        fig, ax = plt.subplots()
        if mode.startswith("Transmission"):
            y = new_tr * (100 if np.max(new_tr) <= 1.5 else 1)
            ax.plot(new_wl, y, label=name)
            ax.set_ylabel("Transmission (%)")
        else:
            frac = new_tr / 100 if np.max(new_tr) > 1.5 else new_tr
            frac = np.clip(frac, 1e-6, 1.0)
            y = -np.log10(frac)
            ax.plot(new_wl, y, label=name)
            ax.set_ylabel("Optical Density (OD)")

        ax.set_xlabel("Wavelength (nm)")
        ax.set_xlim(wl_min, wl_max)   # <<< 固定横坐标范围
        ax.legend()
        ax.grid(alpha=0.3)
        st.pyplot(fig)

    with col3:
        if st.checkbox("SELECT", key=name):
            selected_filters.append((name, new_wl, new_tr))

    with col4:
        st.write("Edit Notes:")
        new_notes = st.text_area("", notes, key=f"notes_{name}", height=80)
        if st.button("Update", key=f"update_{name}"):
            db.update_notes(name, new_notes)
            st.success(f"Notes for {name} updated!")

# Combining Filters
if len(selected_filters) >= 2:
    st.subheader("Combining Filters")

    new_wl = np.arange(wl_min, wl_max + step, step)
    combo_tr = np.ones_like(new_wl)
    
    for name, wl, tr in selected_filters:
        new_wl, new_tr = resample_spectrum(wl,tr,wl_min=wl_min,wl_max=wl_max,step=step)
        combo_tr *= new_tr /100

    fig, ax = plt.subplots()
    if mode.startswith("Transmission"):
        ax.plot(new_wl, combo_tr*100, 'r', linewidth=2, label="Comb.")
        ax.set_ylabel("Transmission (%)")
    else:
        frac = np.clip(combo_tr, 1e-6, 1.0)
        ax.plot(new_wl, -np.log10(frac), 'r', linewidth=2, label="Comb.")
        ax.set_ylabel("Optical Density (OD)")

    ax.set_xlabel("Wavelength (nm)")
    ax.legend()
    ax.grid(alpha=0.3)
    st.pyplot(fig)