import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="NaijaTax 2026", page_icon="🇳🇬", layout="centered")

# --- CUSTOM CSS FOR NIGERIAN THEME ---

    # --- UPDATED CUSTOM CSS (Theme Aware) ---
st.markdown("""
    <style>
    /* Main background remains clean */
    .main { background-color: transparent; }
    
    /* Buttons stay Nigerian Green but work in both modes */
    .stButton>button { 
        background-color: #008751; 
        color: white; 
        width: 100%; 
        border-radius: 10px; 
        border: none;
    }
    
    /* The Metric Box Fix: Use system variables for text and background */
    div[data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        padding: 15px;
        border-radius: 10px;
        color: var(--text-color);
    }
    
    /* Ensuring the value text is visible in Dark Mode */
    div[data-testid="stMetricValue"] > div {
        color: var(--text-color) !important;
    }
    </style>
    """, unsafe_allow_html=True)


# --- HEADER ---
st.title("🇳🇬 NaijaTax 2026 Calculator")
st.markdown("#### *Making sense of the Nigeria Tax Act 2025*")

# --- HOW TO USE SECTION ---
with st.expander("❓ New here? See How to Use this App"):
    st.markdown("""
    1. **Pick Your Lane:** Are you a Civil Servant, Freelancer, or Limited Company?
    2. **Be Honest with the Numbers:** Enter your total annual income (Gross).
    3. **Claim Your Discounts:** - **Employees:** Input your rent to claim the 20% relief.
       - **Freelancers/Companies:** Input your business expenses to lower your taxable profit.
    4. **Magic Button:** Hit 'Calculate' to see your annual and monthly contribution to the 'Big Piggy Bank'.
    """)

st.divider()

# --- SIDEBAR INPUTS ---
st.sidebar.header("User Profile")
category = st.sidebar.selectbox(
    "Tax Category",
    ["Civil Servant / Employee", "Freelancer / Sole Trader", "Limited Company (Ltd)"]
)

# --- MAIN INPUT SECTION ---
col_in1, col_in2 = st.columns(2)

with col_in1:
    income = st.number_input("Total Annual Income (₦)", min_value=0, step=100000, help="Total money earned before any deductions.")

with col_in2:
    if category == "Civil Servant / Employee":
        rent = st.number_input("Annual Rent Paid (₦)", min_value=0, step=50000, help="You can claim 20% of this (max ₦500k) as tax relief.")
        pension_opt = st.checkbox("Deduct Pension (8%) & NHF (2.5%)", value=True)
        bus_expenses = 0
    elif category == "Freelancer / Sole Trader":
        bus_expenses = st.number_input("Business Expenses (₦)", min_value=0, step=50000, help="Data, fuel, software, gear, etc.")
        rent = st.number_input("Personal Rent (₦)", min_value=0, step=50000)
        pension_opt = st.checkbox("Voluntary Pension/NHF?", value=False)
    else: # Limited Company
        bus_expenses = st.number_input("Total Operating Expenses (₦)", min_value=0, step=100000)
        rent = 0
        pension_opt = False

# --- EXPENSE GUIDES ---
if category != "Civil Servant / Employee":
    with st.expander("💡 What can I add as Business Expenses?"):
        if category == "Freelancer / Sole Trader":
            st.write("- **Data & Tech:** Internet, Starlink, Software (Adobe, Zoom, etc.)\n- **Power:** Fuel for generator/solar maintenance\n- **Gear:** Laptop repairs, camera equipment\n- **Learning:** Courses & Certifications")
        else:
            st.write("- **Operations:** Staff Salaries, Pensions (10% Co. contribution), Office Rent\n- **Growth:** Marketing, Ad Spend, Professional Fees (Legal/Accounting)\n- **Maintenance:** Vehicle repairs, Office utilities")

# --- CALCULATION LOGIC ---
def get_tax_2026(taxable_income):
    if taxable_income <= 0: return 0
    
    # 2026 Progressive Bands
    bands = [
        (800000, 0.00),     # First 800k @ 0%
        (2200000, 0.15),    # Next 2.2m @ 15%
        (9000000, 0.18),    # Next 9m @ 18%
        (13000000, 0.21),   # Next 13m @ 21%
        (25000000, 0.23),   # Next 25m @ 23%
        (float('inf'), 0.25) # Above 50m @ 25%
    ]
    
    total_tax = 0
    remaining = taxable_income
    for limit, rate in bands:
        if remaining <= 0: break
        chunk = min(remaining, limit)
        total_tax += chunk * rate
        remaining -= chunk
    return total_tax

# --- EXECUTE ---
if st.button("Calculate My Tax"):
    if category == "Limited Company (Ltd)":
        if income <= 50000000:
            annual_tax = 0
            st.success("🎉 Small Business Relief! Since your turnover is under ₦50m, you pay 0% CIT.")
        else:
            profit = max(0, income - bus_expenses)
            # CIT (30%) + Development Levy (4%)
            annual_tax = (profit * 0.30) + (profit * 0.04)
    else:
        # Personal Income Tax Logic
        net_after_bus_exp = income - bus_expenses
        pension_deduction = (net_after_bus_exp * 0.105) if pension_opt else 0
        rent_relief = min(rent * 0.20, 500000)
        
        final_taxable_income = max(0, net_after_bus_exp - pension_deduction - rent_relief)
        annual_tax = get_tax_2026(final_taxable_income)

    monthly_tax = annual_tax / 12

    # DISPLAY RESULTS
    st.divider()
    res1, res2 = st.columns(2)
    res1.metric("Annual Tax Amount", f"₦{annual_tax:,.2f}")
    res2.metric("Monthly Tax Amount", f"₦{monthly_tax:,.2f}")

    if annual_tax == 0 and income > 0:
        st.balloons()
        st.info("You're in the 'Zero-Tax' zone! Use that extra cash to grow your dreams.")
    
    st.caption("Note: This is an estimate based on the Nigeria Tax Act 2025. Always consult with a certified tax professional for official filing.")

# --- TABS FOR ORGANIZED CONTENT ---
tab1, tab2, tab3 = st.tabs(["🧮 Calculator", "📑 FAQ", "📚 Resources"])

with tab1:
    # [Paste all your previous calculator code here]
    pass 

with tab2:
    st.header("Frequently Asked Questions")
    
    with st.expander("Is the ₦800,000 threshold for everyone?"):
        st.write("Yes! Whether you are a civil servant, a shop owner, or a freelancer, the first ₦800,000 you earn in a year is now taxed at 0%.")
        
    with st.expander("How does Rent Relief work?"):
        st.write("You can deduct 20% of the rent you actually paid from your taxable income, provided it doesn't exceed ₦500,000. You should keep your rent receipts handy for the tax man!")

    with st.expander("What happened to the old tax laws?"):
        st.write("The 2025 Act repealed the Personal Income Tax Act, Company Income Tax Act, and several others to create one 'Unified' rulebook.")

with tab3:
    st.header("Official Documents")
    st.info("Knowledge is power. Download the full 2025 Tax Act to stay informed.")
    
    # Direct Link to the PDF
    st.link_button("📂 Download Nigeria Tax Act 2025 (PDF)", "https://tat.gov.ng/Nigeria-Tax-Act-2025.pdf")
    
    st.markdown("""
    **Key Chapters to Note:**
    - **Chapter 2:** Taxation of Individuals & Companies
    - **Chapter 6:** Value Added Tax (VAT)
    - **Chapter 8:** Tax Incentives & Exemptions
    """)
    


