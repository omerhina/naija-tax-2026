import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="NaijaTax 2026", page_icon="🇳🇬", layout="centered")

# --- THEME-AWARE CSS (Fixes Dark Mode Visibility) ---
st.markdown("""
    <style>
    .main { background-color: transparent; }
    .stButton>button { 
        background-color: #008751; 
        color: white; 
        width: 100%; 
        border-radius: 10px; 
        font-weight: bold;
        border: none;
    }
    /* Metric boxes that adapt to Light/Dark mode */
    div[data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        padding: 20px;
        border-radius: 12px;
    }
    /* Force metric text to follow theme colors */
    div[data-testid="stMetricValue"] > div {
        color: var(--text-color) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- APP HEADER ---
st.title("🇳🇬 NaijaTax 2026")
st.markdown("##### *Unified Tax Calculator for the 2025 Nigeria Tax Act*")

# --- TABS FOR NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["🧮 Calculator", "📑 FAQ", "📚 Resources"])

with tab1:
    # 1. CATEGORY SELECTOR (Now on the Main Page)
    category = st.selectbox(
        "Who are you calculating for?",
        ["Civil Servant / Employee", "Freelancer / Sole Trader", "Limited Company (Ltd)"],
        index=0
    )

    st.divider()

    # 2. INPUT SECTION
    col_in1, col_in2 = st.columns(2)

    with col_in1:
        income = st.number_input("Total Annual Gross Income (₦)", min_value=0, step=100000)

    with col_in2:
        if category == "Civil Servant / Employee":
            rent = st.number_input("Annual Rent Paid (₦)", min_value=0, step=50000, help="Claim 20% relief (max ₦500k)")
            pension_opt = st.checkbox("Deduct Pension (8%) & NHF (2.5%)", value=True)
            bus_expenses = 0
        elif category == "Freelancer / Sole Trader":
            bus_expenses = st.number_input("Business Expenses (₦)", min_value=0, step=50000)
            rent = st.number_input("Personal Rent (₦)", min_value=0, step=50000)
            pension_opt = st.checkbox("Deduct Voluntary Pension?", value=False)
        else: # Limited Company
            bus_expenses = st.number_input("Total Operating Expenses (₦)", min_value=0, step=100000)
            rent = 0
            pension_opt = False

    # 3. CALCULATION ENGINE
    def get_tax_2026(taxable):
        if taxable <= 800000: return 0
        
        # New 2026 Progressive Bands
        bands = [
            (800000, 0.00),     # First 800k @ 0%
            (2200000, 0.15),    # Next 2.2m @ 15%
            (9000000, 0.18),    # Next 9m @ 18%
            (13000000, 0.21),   # Next 13m @ 21%
            (25000000, 0.23),   # Next 25m @ 23%
            (float('inf'), 0.25) # Above 50m @ 25%
        ]
        
        tax = 0
        remaining = taxable
        for limit, rate in bands:
            if remaining <= 0: break
            chunk = min(remaining, limit)
            tax += chunk * rate
            remaining -= chunk
        return tax

    if st.button("Calculate My Contribution"):
        if category == "Limited Company (Ltd)":
            if income <= 50000000:
                annual_tax = 0
                st.success("Small Business Exemption! Your CIT is 0%.")
            else:
                profit = max(0, income - bus_expenses)
                # 30% CIT + 4% Development Levy
                annual_tax = (profit * 0.34)
        else:
            net = income - bus_expenses
            pension = (net * 0.105) if pension_opt else 0
            relief = min(rent * 0.20, 500000)
            taxable_income = max(0, net - pension - relief)
            annual_tax = get_tax_2026(taxable_income)

        # RESULTS
        st.divider()
        r1, r2 = st.columns(2)
        r1.metric("Annual Tax", f"₦{annual_tax:,.2f}")
        r2.metric("Monthly Tax", f"₦{annual_tax/12:,.2f}")
        
        if annual_tax == 0:
            st.balloons()
            st.info("You're currently tax-exempt! Ready to grow bigger?")

with tab2:
    st.header("Frequently Asked Questions")
    faqs = {
        "What is the new 0% threshold?": "Anyone earning ₦800,000 or less per year is fully exempt from income tax.",
        "What happened to the CRA?": "The Consolidated Relief Allowance was replaced by the Rent Relief (20% of rent, capped at ₦500k).",
        "How do Freelancers benefit?": "Freelancers can deduct business expenses (data, fuel, tools) before calculating tax.",
        "What is the 4% Development Levy?": "It replaces several older levies (TETFund, NASENI, etc.) for mid-to-large companies."
    }
    for q, a in faqs.items():
        with st.expander(q):
            st.write(a)

with tab3:
    st.header("Official Documents")
    st.write("Stay compliant by reviewing the official Gazette signed into law.")
    st.link_button("📂 Download Nigeria Tax Act 2025 (PDF)", "https://tat.gov.ng/Nigeria-Tax-Act-2025.pdf")
    st.caption("Document hosted by the Tax Appeal Tribunal (TAT).")
