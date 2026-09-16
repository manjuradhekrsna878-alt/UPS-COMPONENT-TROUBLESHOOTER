import streamlit as st

st.set_page_config(page_title="UPS Component Troubleshooter", page_icon="⚡", layout="wide")

st.title("⚡ UPS Component Troubleshooter")
st.caption("Component-level learning • fault isolation • troubleshooting logic")

st.warning("Safety: Educational use only. UPS systems contain lethal AC/DC voltages and stored energy. Use this tool for learning and de-energized equipment only. Follow LOTO, PPE and the OEM service manual. Never use this app as permission to probe a live UPS.")

COMP = {
"Rectifier / Converter":("Converts AC to DC for the DC link.",["Rectifier","DC link"],["Rectifier fault","DC bus abnormal","Input current distortion"],["Read OEM alarms/events.","With equipment isolated, inspect fuses, terminals and semiconductor modules.","Use OEM-specified input/output tests.","Separate input, power-stage, sensing and control faults."]),
"DC Link / DC Bus":("Energy-transfer DC node between front end and inverter.",["Rectifier","DC capacitors","Pre-charge","DC bus sensing","Inverter"],["DC undervoltage/overvoltage","Ripple alarm","Pre-charge failure","Inverter shutdown"],["Review the exact OEM DC-bus alarm.","After verified isolation/discharge, inspect capacitors and bus connections.","Check pre-charge components using the OEM procedure.","Treat the bus as energized until proven otherwise."]),
"Inverter":("Converts DC-link energy into controlled AC output.",["DC link","IGBT stage","Gate driver","Output filter","Load"],["Inverter fault","Output abnormal","Overcurrent","Transfer to bypass"],["Read inverter, overcurrent, gate-driver and thermal alarms.","With equipment isolated, inspect power modules, drivers, cooling and output connections.","Use OEM diagnostics.","Never bypass protection."]),
"IGBT Power Module":("High-power switching device used in many modern UPS power stages.",["DC terminals","IGBT","Gate","Heatsink"],["Immediate trip","Semiconductor fault","High current","Repeated module failure"],["Identify the exact module and OEM test limits.","Inspect for thermal/mechanical damage after isolation.","Use the manufacturer's approved semiconductor test.","Investigate gate driver, cooling, DC bus and load before replacement."]),
"Gate Driver":("Drives and protects the gate of a power semiconductor.",["Controller","Isolation","Gate driver","IGBT"],["Gate-driver alarm","One phase/module abnormal","Repeated IGBT failure"],["Review gate-driver diagnostics.","Inspect connectors and auxiliary supplies after isolation.","Compare affected and healthy channels only with OEM-approved tests."]),
"DC Capacitor":("Stores energy and reduces DC-link ripple.",["DC bus","Capacitor bank","Discharge circuit"],["High ripple","Bus instability","Temperature alarm","Reduced ride-through"],["Follow OEM capacitor maintenance criteria.","After isolation/discharge, inspect swelling, leakage and heat damage.","Use approved capacitance/ESR tests where specified.","Check cooling and ambient temperature."]),
"Battery / Battery String":("Provides stored DC energy during mains failure.",["Battery blocks","String","Protection","DC bus"],["Short backup","Battery alarm","String imbalance","Breaker trip"],["Review age and maintenance history.","Inspect for swelling, leakage, corrosion and damaged terminals.","Use OEM-approved impedance/conductance/string tests.","Never short or open a high-energy battery circuit without the approved procedure."]),
"Battery Charger":("Maintains and restores battery charge.",["Charging stage","Current control","Voltage sensing","Battery"],["Undercharge","Overcharge","Long recharge","Charger fault"],["Review charger alarms.","Compare charge voltage/current with OEM limits.","Inspect cooling and connections after isolation.","Separate charger faults from battery faults using history and approved tests."]),
"Static Bypass / SCR":("Transfers the load between inverter and bypass in many UPS architectures.",["Bypass","Static switch","Inverter output","Load"],["Bypass unavailable","Transfer failure","SCR alarm"],["Check bypass availability and synchronization.","Review static-switch diagnostics.","Inspect SCR modules, cooling and controls after isolation.","Use OEM semiconductor/gate tests."]),
"Output Filter":("Filters inverter switching to produce suitable AC output.",["Inverter","Inductor","Capacitor","Output"],["Waveform distortion","Abnormal current","Filter temperature"],["Review waveform/THD diagnostics if available.","Inspect inductors, capacitors and connections after isolation.","Consider both inverter switching and load characteristics."]),
"Cooling / Fan":("Removes heat from power semiconductors and magnetic components.",["Fan","Air path","Heatsink","Temperature sensor"],["Overtemperature","Fan fault","Thermal shutdown"],["Review temperature trend.","After isolation, inspect fans, filters, airflow and heatsinks.","Check fan replacement interval and ambient temperature."]),
"Control PCB / DSP":("Runs control, protection, monitoring and communications.",["Sensors","ADC","DSP","Gate drivers","HMI"],["Multiple alarms","Communication failure","Incorrect sensing","Unexpected shutdown"],["Capture the complete alarm sequence.","Check auxiliary supplies/connectors after isolation.","Validate sensor values and diagnostic flags.","Use event logs and firmware information with OEM support."]),
"Sensors / CT / PT":("Provides voltage, current and temperature feedback.",["Sensor","Signal conditioning","ADC","Controller"],["Wrong displayed values","False protection alarm","Phase imbalance"],["Compare values only using an approved procedure.","Inspect sensor wiring/connectors after isolation.","Check calibration/diagnostic status.","Validate sensing before replacing major power components."])
}

FAULTS = {
"UPS will not start":["Read the event history and startup sequence.","Check input/bypass availability in the HMI.","Check battery/DC availability according to OEM procedure.","Consider control power, pre-charge/contactor, DC bus and controller faults."],
"UPS transfers to bypass":["Determine whether transfer was commanded or protective.","Review inverter overcurrent, overload, thermal and synchronization alarms.","Check output/load conditions.","Consider inverter, gate driver, sensing, cooling and control faults."],
"Short backup time":["Check load level and runtime history.","Review battery age and maintenance records.","Check battery condition/string health using OEM-approved methods.","Separate battery capacity loss from charging problems."],
"DC bus alarm":["Identify undervoltage vs overvoltage.","Review rectifier/converter alarms.","Review the pre-charge sequence.","Consider capacitors, sensing, semiconductor stage and control."],
"Inverter overcurrent":["Determine whether it occurs at startup, load step or steady state.","Review load/short-circuit information.","Review IGBT, gate-driver and thermal alarms.","Check output filter and sensing diagnostics."],
"Overtemperature":["Identify the alarm source and temperature trend.","Check fan/airflow/filter condition after isolation.","Check heatsink and thermal interface.","Consider load, ambient temperature and switching stress."],
"Bypass unavailable":["Check bypass source and synchronization.","Review static-switch and bypass alarms.","Check sensing/control path.","Inspect SCR/static-switch components using OEM procedure."],
"Output voltage abnormal":["Determine magnitude, phase-balance or frequency issue.","Review inverter and output-filter alarms.","Check sensing chain.","Consider load characteristics and inverter control."],
"Multiple unrelated alarms":["Do not assume multiple component failures.","Find the first alarm chronologically.","Check control power and sensing.","Use the event log to separate primary from consequential alarms."]
}

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to",["Home","Learning Path","Component Lab","Fault Isolation","Quiz","Reference"])

if page=="Home":
    st.header("Learn UPS troubleshooting from the component level")
    st.write("Build a mental model of the UPS power path, connect symptoms to components, and practise root-cause isolation.")
    st.code("AC INPUT → PROTECTION → RECTIFIER/CONVERTER → DC LINK → INVERTER/IGBT → OUTPUT FILTER → LOAD\n                         ↑                         ↓\n                    BATTERY/CHARGER          STATIC BYPASS → LOAD")
    a,b,c=st.columns(3)
    a.metric("Component modules",len(COMP)); b.metric("Fault scenarios",len(FAULTS)); c.metric("Learning modes",5)
    st.info("Recommended order: Learning Path → Component Lab → Fault Isolation → Quiz.")

elif page=="Learning Path":
    st.header("UPS Troubleshooting Learning Path")
    steps=[("1","Power path","AC input → rectifier → DC link → inverter → output/bypass → load"),
           ("2","Component function","Know each component's role, inputs, outputs and dependencies"),
           ("3","Alarm sequence","Find the first/primary alarm; later alarms may be consequences"),
           ("4","Fault isolation","Separate power stage, gate drive, sensing, cooling, auxiliary supply and control faults"),
           ("5","Root cause","Do not stop at the failed component; determine why it failed"),
           ("6","Confirmation","Use OEM diagnostics and approved de-energized tests before replacement")]
    for n,t,d in steps:
        st.subheader(f"{n}. {t}"); st.write(d)

elif page=="Component Lab":
    st.header("Component Lab")
    name=st.selectbox("Select component",list(COMP))
    role,blocks,symptoms,checks=COMP[name]
    st.subheader("Function"); st.write(role)
    st.subheader("Functional block"); st.code(" → ".join(blocks))
    x,y=st.columns(2)
    with x:
        st.subheader("Typical symptoms")
        for s in symptoms: st.markdown("- "+s)
    with y:
        st.subheader("Diagnostic approach")
        for i,s in enumerate(checks,1): st.markdown(f"**{i}.** {s}")
    st.info("Key principle: an alarm identifies a condition, not automatically the failed component.")

elif page=="Fault Isolation":
    st.header("Fault Isolation Assistant")
    symptom=st.selectbox("Select main symptom",list(FAULTS))
    for i,s in enumerate(FAULTS[symptom],1): st.markdown(f"**{i}.** {s}")
    st.info("This is a learning framework, not a live-equipment test procedure.")

elif page=="Quiz":
    st.header("Troubleshooting Quiz")
    qs=[
    ("What is the inverter's main function?",["Store energy","Convert DC-link energy into controlled AC","Cool the UPS","Measure battery impedance"],1),
    ("A replacement IGBT fails again. What should be investigated?",["Only the IGBT","Gate driver, overcurrent, cooling, DC bus and load","Only battery age","Only room temperature"],1),
    ("What does the DC link do?",["Energy-transfer DC node between front end and inverter","Ethernet communication","Fire alarm control","Battery cabinet ventilation"],0),
    ("What should be done first with a complex alarm sequence?",["Bypass protection","Replace the largest component","Review the chronological OEM event history","Short-test the suspected device"],2)]
    score=0
    for i,(q,opts,ans) in enumerate(qs):
        v=st.radio(f"{i+1}. {q}",opts,index=None,key=f"q{i}")
        if v==opts[ans]: score+=1
    if st.button("Check score",type="primary"):
        st.success(f"Score: {score}/{len(qs)}")

elif page=="Reference":
    st.header("Component Reference")
    st.dataframe([{"Component":k,"Function":v[0],"Typical symptom":v[2][0]} for k,v in COMP.items()],use_container_width=True,hide_index=True)
