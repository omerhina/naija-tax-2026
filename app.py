import streamlit as st

# --- PAGE CONFIG & THEME-AWARE CSS ---
st.set_page_config(page_title="NaijaTax 2026", page_icon="🇳🇬", layout="centered")

st.markdown("""
    <style>
    .main { background-color: transparent; }
    .stButton>button { 
        background-color: #008751; color: white; width: 100%; border-radius: 10px; font-weight: bold; border: none;
    }
    div[data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        padding: 20px; border-radius: 12px;
    }
    div[data-testid="stMetricValue"] > div { color: var(--text-color) !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🇳🇬 NaijaTax 2026")
st.markdown("##### *Your guide to the 2025 Nigeria Tax Act rules.*")

tab1, tab2, tab3 = st.tabs(["🧮 Calculator", "📑 FAQ", "📚 Resources"])

with tab1:
    category = st.selectbox(
        "Who are you calculating for?",
        ["Civil Servant / Employee", "Freelancer / Sole Trader", "Limited Company (Ltd)"]
    )

    st.divider()

    col_in1, col_in2 = st.columns(2)

    with col_in1:
        # Initializing value as None makes it "empty" by default
        income = st.number_input(
            "Total Annual Gross Income (₦)", 
            min_value=0, step=100000, value=None, placeholder="e.g. 5000000",
            help="REQUIRED: Enter your total earnings before any deductions."
        )

    with col_in2:
        if category == "Civil Servant / Employee":
            rent = st.number_input(
                "Annual Rent Paid (₦)", 
                min_value=0, step=50000, value=None, placeholder="e.g. 800000",
                help="REQUIRED: Input your yearly rent to claim 20% relief."
            )
            pension_opt = st.checkbox("Deduct Pension & NHF?", value=True)
            bus_expenses = 0
        elif category == "Freelancer / Sole Trader":
            bus_expenses = st.number_input(
                "Business Expenses (₦)", 
                min_value=0, step=50000, value=None, placeholder="e.g. 250000",
                help="REQUIRED: Expenses like data, fuel, and tools."
            )
            rent = st.number_input("Personal Rent (₦)", min_value=0, step=50000, value=0)
            pension_opt = st.checkbox("Deduct Voluntary Pension?", value=False)
        else: # Limited Company
            bus_expenses = st.number_input(
                "Operating Expenses (₦)", 
                min_value=0, step=100000, value=None, placeholder="e.g. 1000000",
                help="REQUIRED: All company running costs."
            )
            rent = 0
            pension_opt = False

    # EXPENSE GUIDE
    if category != "Civil Servant / Employee":
        with st.expander("📂 What can I count as Business Expenses?"):
            st.markdown("""
            * **Operations:** Office rent, utilities, security.
            * **Personnel:** Staff salaries and 10% company pension.
            * **Tech:** Data, software, and hosting.
            * **Marketing:** Social media ads and branding.
            """)

    # --- VALIDATION & CALCULATION ---
    def get_tax_2026(taxable):
        if taxable <= 800000: return 0
        bands = [(800000, 0.0), (2200000, 0.15), (9000000, 0.18), (13000000, 0.21), (25000000, 0.23), (float('inf'), 0.25)]
        tax, remaining = 0, taxable
        for limit, rate in bands:
            if remaining <= 0: break
            chunk = min(remaining, limit)
            tax += chunk * rate
            remaining -= chunk
        return tax

    if st.button("Calculate My Contribution"):
        # THE VALIDATION CHECK
        errors = []
        if income is None: errors.append("Annual Income")
        if category == "Civil Servant / Employee" and rent is None: errors.append("Annual Rent")
        if category != "Civil Servant / Employee" and bus_expenses is None: errors.append("Business/Operating Expenses")

        if errors:
            st.error(f"🚨 Please fill in the following: {', '.join(errors)}")
        else:
            # PROCEED WITH CALCULATION
            if category == "Limited Company (Ltd)":
                if income <= 50000000:
                    annual_tax = 0
                    st.success("Small Business Exemption! Your Company Tax is ₦0.00.")
                else:
                    profit = max(0, income - bus_expenses)
                    annual_tax = (profit * 0.34)
            else:
                net = income - bus_expenses
                pension = (net * 0.105) if pension_opt else 0
                relief = min(rent * 0.20, 500000)
                taxable_income = max(0, net - pension - relief)
                annual_tax = get_tax_2026(taxable_income)

            st.divider()
            r1, r2 = st.columns(2)
            r1.metric("Annual Tax", f"₦{annual_tax:,.2f}")
            r2.metric("Monthly Tax", f"₦{annual_tax/12:,.2f}")

# --- FAQ & RESOURCES ---
with tab2:
    st.header("Frequently Asked Questions")
    
    search_faq = st.text_input("🔍 Search FAQs", placeholder="e.g. Rent, Crypto, Small Business")
# (You can then use a simple loop to filter the expanders based on the search_faq string)
    
    with st.expander("Is the ₦800k threshold for everyone?"):
        st.write("Yes! Whether you are a civil servant, a shop owner, or a freelancer, the first ₦800,000 you earn in a year is now taxed at 0%. This provides instant relief to low-income earners.")

    with st.expander("What happened to the old CRA (Consolidated Relief Allowance)?"):
        st.write("The 2025 Act repealed the old CRA blanket allowance. It has been replaced by more targeted reliefs, most notably the **Rent Relief**, which is 20% of your annual rent (capped at ₦500,000).")

    with st.expander("Does my Small Business really pay 0% tax?"):
        st.write("If your annual turnover is ₦50 million or less, your Company Income Tax (CIT) rate is 0%. However, you are still required to file your tax returns annually to remain compliant and keep your Tax ID (TIN) active.")

    with st.expander("What is the new 'Development Levy' for companies?"):
        st.write("For companies larger than the 'Small' category, a unified 4% Development Levy replaces several older taxes (like Education Tax and the Police Trust Fund levy). It is calculated on your assessable profits.")

    with st.expander("Is Crypto or Digital Income taxable in Nigeria?"):
        st.write("Yes. Section 4 of the new Act explicitly includes gains from digital and virtual assets (like Cryptocurrency, NFTs, and digital awards) as part of your taxable income.")

    with st.expander("How long do I have to get a tax refund?"):
        st.write("The new law speeds things up! Tax refunds must now be processed within 90 days (or just 30 days for VAT claims), provided you have proper documentation.")

    with st.expander("What is the 'WENR' rule for expenses?"):
        st.write("For an expense to be deductible, it must be **W**holly, **E**xclusively, **N**ecessarily, and **R**easonably incurred for your business. Personal expenses like family groceries or school fees do not count.")

    with st.expander("Do I need a TIN to open a business bank account?"):
        st.write("Absolutely. The 2025 Act makes the Tax Identification Number (TIN) mandatory for all financial operations. No TIN means no corporate banking.")

with tab3:
    st.header("Official Documents")
    st.link_button("📂 Download Nigeria Tax Act 2025 (PDF)", "https://tat.gov.ng/Nigeria-Tax-Act-2025.pdf")

