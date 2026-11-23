from datetime import datetime
import time
import streamlit as st

st.set_page_config(page_title="Private 3-Person Chat", page_icon="🔔", layout="centered")

ALLOWED_EMAILS = [
    "nnyageni@gmail.com",
    "lourinlouis@gmail.com",
    "jnyageni@gmail.com",
]


@st.cache_resource
def get_chat_store():
    """Shared in-memory message log across sessions on this Streamlit server."""
    return {
        "messages": [
            {
                "id": 1,
                "sender": "System",
                "recipients": list(ALLOWED_EMAILS),
                "text": "Private room active. You will be notified when new messages arrive.",
                "time": datetime.now().strftime("%H:%M"),
            }
        ],
        "next_id": 2,
    }


store = get_chat_store()

if "authenticated_email" not in st.session_state:
    st.session_state.authenticated_email = None
if "last_seen_id" not in st.session_state:
    st.session_state.last_seen_id = 0
if "notification_banner" not in st.session_state:
    st.session_state.notification_banner = None

# --- Login / Access Gate ---
if st.session_state.authenticated_email is None:
    st.title("Private 3-Person Chat")
    st.caption("Restricted to nnyageni@gmail.com, lourinlouis@gmail.com, and jnyageni@gmail.com.")

    with st.form("login_form"):
        email_input = st.text_input("Enter your email address", placeholder="name@gmail.com")
        submitted = st.form_submit_button("Enter Chat")

    if submitted:
        normalized = email_input.strip().lower()
        if normalized in ALLOWED_EMAILS:
            st.session_state.authenticated_email = normalized
            # Mark existing messages as seen on initial login
            st.session_state.last_seen_id = store["next_id"] - 1
            st.session_state.notification_banner = None
            st.rerun()
        else:
            st.error("Access denied. Only those three email addresses can access this app.")
    st.stop()

# --- Authenticated Chat Room ---
current_user = st.session_state.authenticated_email

# Check for new incoming messages addressed to current_user from someone else
incoming_new = [
    m
    for m in store["messages"]
    if m["id"] > st.session_state.last_seen_id
    and m["sender"] != current_user
    and current_user in m.get("recipients", ALLOWED_EMAILS)
]

if incoming_new:
    latest = incoming_new[-1]
    if len(incoming_new) == 1:
        notice = f"🔔 New message from {latest['sender']} ({latest['time']}): \"{latest['text']}\""
    else:
        notice = f"🔔 You have {len(incoming_new)} new messages. Latest from {latest['sender']}: \"{latest['text']}\""

    st.session_state.notification_banner = notice
    st.toast(notice, icon="🔔")
    st.session_state.last_seen_id = max(m["id"] for m in store["messages"])

top_left, top_mid, top_right = st.columns([3, 1.3, 1])
with top_left:
    st.title("Private Chat")
    st.caption(f"Signed in as **{current_user}**")
with top_mid:
    st.write("")
    if st.button("🔄 Refresh"):
        st.rerun()
with top_right:
    st.write("")
    if st.button("Switch User"):
        st.session_state.authenticated_email = None
        st.session_state.notification_banner = None
        st.rerun()

# Show persistent notification banner until dismissed or cleared
if st.session_state.notification_banner:
    banner_col, dismiss_col = st.columns([5, 1])
    with banner_col:
        st.info(st.session_state.notification_banner)
    with dismiss_col:
        st.write("")
        if st.button("Dismiss"):
            st.session_state.notification_banner = None
            st.rerun()

auto_refresh = st.toggle("Auto-check for new messages (every 3s)", value=True)

# --- Email Recipient Selection ---
other_emails = [e for e in ALLOWED_EMAILS if e != current_user]
target_choice = st.radio(
    "Send message to which email?",
    options=["All (all 3 emails)"] + other_emails,
    horizontal=True,
)

if target_choice == "All (all 3 emails)":
    selected_recipients = list(ALLOWED_EMAILS)
else:
    selected_recipients = [current_user, target_choice]

# --- Chat Feed ---
chat_container = st.container(height=380)
with chat_container:
    for msg in store["messages"]:
        recipients = msg.get("recipients", ALLOWED_EMAILS)
        if current_user not in recipients:
            continue

        is_mine = msg["sender"] == current_user
        other_targets = [r for r in recipients if r != msg["sender"]]
        to_label = ", ".join(other_targets) if other_targets else msg["sender"]

        with st.chat_message("user" if is_mine else "assistant"):
            st.markdown(f"**{msg['sender']}** → `{to_label}` · *{msg['time']}*")
            st.write(msg["text"])

# --- Send Message ---
prompt = st.chat_input(f"Write a message to {target_choice}...")
if prompt:
    text = prompt.strip()
    if text:
        msg_id = store["next_id"]
        store["next_id"] += 1
        store["messages"].append(
            {
                "id": msg_id,
                "sender": current_user,
                "recipients": selected_recipients,
                "text": text,
                "time": datetime.now().strftime("%H:%M"),
            }
        )
        store["messages"][:] = store["messages"][-200:]
        st.session_state.last_seen_id = max(st.session_state.last_seen_id, msg_id)
        st.rerun()

if auto_refresh:
    time.sleep(3)
    st.rerun()