import streamlit as st

# Set up the website title
st.set_page_config(page_title="Jah Yummies Treats", page_icon="🎂")

# Create tabs layout in your website (Fixed the order so tab4 matches CONTACTS and tab5 matches CONVERTER)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["LOGIN", "HOME", "MENU", "CURRENCY CONVERTER", "CONTACTS"])

# --- TAB 1: LOGIN ---
with tab1:
    st.header("Jah Yummies Treats")
    st.subheader("Welcome to our login page")

    # Use st.text_input instead of input()
    name = st.text_input("What is your name?", key="login_name")
    if name:
        st.write(f"Hi {name}!")

    contact = st.text_input("Enter your email or phone number:", key="login_contact")

# --- TAB 2: HOME ---
with tab2:
    st.header("Welcome to our home tab")
    st.write(
        "JAH YUMMIES TREATS is a local bakery and custom cake business based in Dar es Salaam, Tanzania (locally based in Goba and Makongo juu).")
    st.write("Jah yummies treats is a custom bakery owned by a magnificent CEO named Lourin Jimmy Louis.")

    hearing_source = st.text_input("Where did you hear about Jah Yummies Treats?", key="home_source")
    if hearing_source:
        st.write("Ohhh that's nice!")

    st.subheader("Meet the Products")
    st.write("First, we have a bread and snack corner:")

    # Products with Image Placeholders
    st.write("- French Bread")
    # st.image("french_bread.jpg", caption="French Bread", width=300)

    st.write("- Cinnamon Rolls")
    # st.image("cinnamon_rolls.jpg", caption="Cinnamon Rolls", width=300)

    st.write("- Cookies")
    # st.image("cookies.jpg", caption="Cookies", width=300)

    st.write("- Donuts")
    # st.image("donuts.jpg", caption="Donuts", width=300)

    st.write("- And more!")

# --- TAB 3: MENU ---
with tab3:
    st.header("Welcome to our Menu")
    # st.image("menu_banner.jpg", use_container_width=True)
    import streamlit as st

    st.title("Jah Yummies Treats 🧁")
    st.subheader("Freshly Baked Delights")

    # Display the image on the web page
    st.image("menu.jpg", caption="Delicious", use_container_width=True)

    st.write("Our payments are in TZS, but you can change currencies in our converter tab.")

# --- TAB 4: CURRENCY CONVERTER ---
with tab4:
    st.header("Currency Converter")

    # Use st.selectbox for a cleaner web dropdown menu
    unit = st.selectbox("Select Currency to convert to TZS:", ["Select...", "USD", "YEN", "POUNDS"])

    if unit == "USD":
        amount = st.number_input("What is your USD amount?", min_value=0.0, step=1.0)
        if amount > 0:
            st.success(f"The price in TZS is: {amount * 2630:,.2f} TZS")

    elif unit == "YEN":
        amount = st.number_input("What is your YEN amount?", min_value=0.0, step=1.0)
        if amount > 0:
            st.success(f"The price in TZS is: {amount * 16.74:,.2f} TZS")

    elif unit == "POUNDS":
        amount = st.number_input("What is your POUNDS amount?", min_value=0.0, step=1.0)
        if amount > 0:
            st.success(f"The price in TZS is: {amount * 3521.52:,.2f} TZS")

# --- TAB 5: CONTACTS ---
with tab5:
    st.header("Contact Us")
    st.write("You can contact us through:")

    # st.image("contact_icons.png", width=200)
    st.write("📞 Phone: [0749622373]")
    st.write("📸 Instagram: @jah_yummies_treats")

    st.info("THANK YOU FOR BEING A MEMBER OF THE JAH YUMMIES FAMILY!")
