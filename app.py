import streamlit as st

# Page Config
st.set_page_config(page_title="NaijaTax 2026", page_icon="🇳🇬")

st.title("🇳🇬 NaijaTax 2026 Calculator")
st.markdown("### Helping you figure out your 'Piggy Bank' contribution.")

# Sidebar for Category
category = st.sidebar.selectbox(
    "Who are you?",
    ["Civil Servant / Employee", "Freelancer / Sole Trader", "Limited Company (Ltd)"]
)

st.divider()

# Input Section
income = st.number_input("What is your Total Annual Income (Gross)?", min_value=0, step=50000)

if "Company" not in category:
    st.info("Fun fact: Did you know if you earn ₦800k or less, you pay ₦0 tax? 🎉")
    rent = st.number_input("How much Rent do you pay annually?", min_value=0, step=10000)
    pension_opt = st.checkbox("Do you contribute to Pension (8%) and NHF (2.5%)?", value=True)
else:
    expenses = st.number_input("What are your total Business Expenses?", min_value=0, step=10000)

# Calculation Engine
def calculate_individual_tax(gross, rent_paid, has_pension):
    # Deductions
    pension_deduction = (gross * 0.105) if has_pension else 0
    rent_relief = min(rent_paid * 0.20, 500000)
    taxable_income = max(0, gross - pension_deduction - rent_relief)
    
    # Progressive Bands
    tax = 0
    remaining = taxable_income
    
    bands = [
        (800000, 0),        # First 800k @ 0%
        (2200000, 0.15),    # Next 2.2m @ 15%
        (9000000, 0.18),    # Next 9m @ 18%
        (13000000, 0.21),   # Next 13m @ 21%
        (25000000, 0.23),   # Next 25m @ 23%
        (float('inf'), 0.25) # Above 50m @ 25%
    ]
    
    for limit, rate in bands:
        if remaining <= 0: break
        chunk = min(remaining, limit)
        tax += chunk * rate
        remaining -= chunk
        
    return tax

# Logic Execution
if st.button("Calculate My Tax"):
    if "Company" in category:
        if income <= 50000000:
            annual_tax = 0
            st.success("Your business is small! You pay 0% Company Income Tax under the new law.")
        else:
            profit = income - expenses
            annual_tax = (profit * 0.30) + (profit * 0.04)
    else:
        annual_tax = calculate_individual_tax(income, rent, pension_opt)

    monthly_tax = annual_tax / 12

    # Results Display
    col1, col2 = st.columns(2)
    col1.metric("Annual Tax", f"₦{annual_tax:,.2f}")
    col2.metric("Monthly Tax", f"₦{monthly_tax:,.2f}")
    
    st.balloons()
    
    st.markdown("---")
    st.write("**Why this amount?**")
    if annual_tax == 0:
        st.write("You fall under the exemption threshold! Keep that money and grow!")
    else:
        st.write(f"After your rent relief and deductions, your taxable income was processed through the 2026 progressive bands. Want to see how to pay this to the FIRS/LIRS?")