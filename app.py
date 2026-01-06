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
    search_query = st.text_input("🔍 Search for answers...", placeholder="e.g. Crypto, VAT, Deadlines").lower()

    faq_data = [
        {"q": "Is the ₦800k threshold for everyone?", "a": "Yes! The first ₦800,000 you earn is taxed at 0%."},
        {"q": "What is the new 2026 Tax ID?", "a": "As of Jan 1, 2026, the new 'Nigerian Tax ID' replaces the old TIN. You can get yours at taxid.jrb.gov.ng."},
        {"q": "Is Crypto income taxable?", "a": "Yes. Gains from digital/virtual assets are now explicitly taxable under Section 4 of the 2025 Act."},
        {"q": "How does Rent Relief work?", "a": "Individuals can deduct 20% of their actual rent (capped at ₦500,000) from their taxable income."},
        {"q": "What happens if I don't have a TIN?", "a": "Financial institutions are now mandated to ensure every taxable person provides a TIN for banking operations."},
        {"q": "Are basic foods exempt from VAT?", "a": "Yes, basic food items, educational materials, and medical services remain at 0% VAT."},
        {"q": "What is the refund timeline?", "a": "Tax refunds must be processed within 90 days (30 days for VAT) if you have proper documentation."},
        {"q": "Can I pay in installments?", "a": "Yes, companies can apply to the NRS (formerly FIRS) to pay in up to three installments."}
    ]

    found = False
    for item in faq_data:
        if search_query in item["q"].lower() or search_query in item["a"].lower():
            with st.expander(item["q"]): st.write(item["a"])
            found = True
    if not found: st.warning("No matching FAQ found.")

with tab3:
    st.header("📅 Important Tax Dates")
    st.info("Mark your calendars! Missing these dates triggers penalties starting 2026.")
    
    st.markdown("""
    | Tax Type | Deadline for Filing/Payment |
    | :--- | :--- |
    | **PAYE (Employees)** | 10th of the following month |
    | **VAT Returns** | 21st of the following month |
    | **Self-Assessment (Individuals)** | 31st March of the following year |
    | **Companies (CIT)** | 6 months after the financial year-end |
    | **Petroleum Royalties** | 14th of the following month |
    """)

    st.divider()
    st.header("📚 Official Resources")
    st.link_button("📂 Download Nigeria Tax Act 2025 (PDF)", "https://tat.gov.ng/Nigeria-Tax-Act-2025.pdf")
    st.caption("Official document from the Tax Appeal Tribunal.")

# --- TAB 4: THE TAX CHALLENGE ---
with tab4:
    st.header("🎯 The NaijaTax 2026 Challenge")
    
    # 1. NICKNAME REGISTRATION
    if 'user_name' not in st.session_state:
        st.info("Enter a nickname to join the leaderboard!")
        name_input = st.text_input("Your Nickname:", placeholder="e.g. TaxWizard234")
        if st.button("Start Game"):
            if name_input:
                st.session_state.user_name = name_input
                st.rerun()
            else:
                st.warning("Oga/Madam, please enter a name!")
        st.stop() # Stops the rest of the tab from loading until name is set

    # 2. LEADERBOARD LOGIC (Simulated with Cache)
    @st.cache_data
    def get_leaderboard():
        return [] # Returns a list that persists across sessions on the server

    leaderboard = get_leaderboard()

    # 3. QUIZ QUESTIONS (Updated with 2026 Penalties)
    questions = [
        {
            "q": "Under the 2025 Act, what is the penalty for a Small Business failing to file returns?",
            "options": ["₦10,000", "₦100,000 first month + ₦50k/month", "Just a warning"],
            "correct": "₦100,000 first month + ₦50k/month",
            "fact": "Correct! Section 1012 makes it expensive to 'forget' your filings. 💸"
        },
        {
            "q": "What is the penalty for a Virtual Asset Provider (Crypto) who defaults on tax?",
            "options": ["₦1 Million", "₦10 Million first month", "50% of profit"],
            "correct": "₦10 Million first month",
            "fact": "Correct! The Act is extremely strict on digital assets. 🪙"
        },
        {
            "q": "If you assault a Tax Officer, what is the maximum jail term under the new law?",
            "options": ["2 years", "10 years", "6 months"],
            "correct": "10 years",
            "fact": "True! Physical assault or using weapons against tax officials now carries up to 10 years in prison. 👮‍♂️"
        }
    ]

    # Initialize game variables
    if 'quiz_score' not in st.session_state: st.session_state.quiz_score = 0
    if 'current_q' not in st.session_state: st.session_state.current_q = 0

    if st.session_state.current_q < len(questions):
        q = questions[st.session_state.current_q]
        st.subheader(f"Question {st.session_state.current_q + 1} of {len(questions)}")
        st.progress((st.session_state.current_q) / len(questions))
        st.markdown(f"### {q['q']}")
        
        user_choice = st.radio("Pick one:", q['options'], key=f"quiz_{st.session_state.current_q}")
        
        if st.button("Submit"):
            if user_choice == q['correct']:
                st.success(f"✅ {q['fact']}")
                st.session_state.quiz_score += 1
            else:
                st.error(f"❌ Wrong! {q['fact']}")
            
            st.session_state.current_q += 1
            st.button("Next Question →")
    
    else:
        # 4. FINAL SCORE & LEADERBOARD SUBMISSION
        final_score = st.session_state.quiz_score
        st.balloons()
        st.subheader(f"Game Over, {st.session_state.user_name}!")
        st.write(f"Your Tax IQ Score: **{final_score}/{len(questions)}**")
        
        # Save to leaderboard
        if st.button("Save to Leaderboard"):
            leaderboard.append({"Name": st.session_state.user_name, "Score": final_score})
            leaderboard.sort(key=lambda x: x['Score'], reverse=True)
            st.success("Score saved!")

        # Display Top 5
        st.divider()
        st.subheader("🏆 Global Top 5")
        if leaderboard:
            for i, entry in enumerate(leaderboard[:5]):
                st.write(f"{i+1}. **{entry['Name']}** — {entry['Score']} pts")
        else:
            st.write("No scores yet. Be the first!")

        if st.button("Reset Game"):
            st.session_state.quiz_score = 0
            st.session_state.current_q = 0
            st.rerun()
            
