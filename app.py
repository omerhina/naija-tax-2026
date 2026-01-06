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

tab1, tab2, tab3, tab4 = st.tabs(["🧮 Calculator", "📑 FAQ", "📚 Important Dates","🎮 Game" ])

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

# --- TAB 4: TAX FLIP GAME (REVERSED) ---
with tab4:
    st.header("🦅 Tax Flap: Leftward Flight")
    st.write("The bird faces left, so we fly left! Tap or press **Space** to dodge the incoming audits.")

    if 'player_name' not in st.session_state:
        player_name = st.text_input("Enter pilot name:", placeholder="TaxNinja")
        if st.button("Ready for Takeoff"):
            if player_name:
                st.session_state.player_name = player_name
                st.rerun()
        st.stop()

    game_code = """
    <div id="game-box" style="width: 100%; max-width: 400px; height: 500px; margin: auto; position: relative; overflow: hidden; background: #70c5ce; border: 4px solid #008751; border-radius: 15px;">
        <canvas id="flappyCanvas" width="400" height="500"></canvas>
        <div id="ui-score" style="position: absolute; top: 10px; right: 10px; font-family: Arial; font-size: 24px; color: white; text-shadow: 2px 2px #000;">Score: 0</div>
    </div>

    <script>
        const canvas = document.getElementById('flappyCanvas');
        const ctx = canvas.getContext('2d');
        const scoreUI = document.getElementById('ui-score');

        let birdY = 250; let velocity = 0; let gravity = 0.4; let jump = -7;
        let score = 0; let gameActive = true;
        let pipes = []; let frame = 0;

        function drawBird() {
            ctx.font = "30px Arial";
            ctx.fillText("🦅", 320, birdY); // Positioned on the right, facing left
        }

        function createPipe() {
            let gap = 160;
            let topHeight = Math.random() * (canvas.height - gap - 100) + 50;
            // Pipes start at x = -50 (off-screen left)
            pipes.push({ x: -50, top: topHeight, bottom: topHeight + gap, passed: false });
        }

        function update() {
            if (!gameActive) return;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            velocity += gravity;
            birdY += velocity;
            drawBird();

            if (frame % 100 === 0) createPipe();
            
            pipes.forEach((p, i) => {
                p.x += 3; // Pipes move RIGHT
                ctx.fillStyle = "#d9534f"; // Audit red
                ctx.fillRect(p.x, 0, 50, p.top);
                ctx.fillRect(p.x, p.bottom, 50, canvas.height);

                // Collision Detection (Bird is at x=320)
                if (p.x > 280 && p.x < 340 && (birdY < p.top || birdY > p.bottom)) {
                    gameActive = false;
                    alert("Audit Caught You! Final Score: " + score);
                }

                // Scoring (When pipe passes the bird's x position)
                if (!p.passed && p.x > 340) {
                    score++;
                    p.passed = true;
                    scoreUI.innerHTML = "Score: " + score;
                }
            });

            // Remove off-screen pipes
            pipes = pipes.filter(p => p.x < 450);

            if (birdY > canvas.height || birdY < 0) gameActive = false;
            frame++;
            requestAnimationFrame(update);
        }

        window.addEventListener('keydown', (e) => { if (e.code === 'Space') velocity = jump; });
        canvas.addEventListener('mousedown', () => { velocity = jump; });
        update();
    </script>
    """
    
    st.components.v1.html(game_code, height=550)

    # Leaderboard Logic
    st.divider()
    st.subheader("🏆 Tax Flip Leaderboard")
    if 'leaderboard' not in st.session_state:
        st.session_state.leaderboard = []
    
    # (Optional: Add logic to update st.session_state.leaderboard from JS)
    st.info("Current Session Best: " + st.session_state.player_name)
    
