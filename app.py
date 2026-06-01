"""
app.py
======
This is the WEB APP. Streamlit reads this file and turns each st.something()
line into a piece of a web page. You run it with:  streamlit run app.py

It imports the score_password function from scorer.py. The names must match
exactly, that is what caused your earlier ImportError.

Read the comments so you can explain how Streamlit works in an interview: you
write normal Python, and Streamlit renders it as a web page top to bottom.
"""

import streamlit as st
from scorer import score_password   # must match the function name in scorer.py

# --- Page setup ---
st.set_page_config(page_title="Password & Breach Risk Analyzer", page_icon="🔐")

st.title("🔐 Password & Breach Risk Analyzer")
st.write(
    "Type a password to see how risky it is. This tool checks length, character "
    "variety, common weak patterns, and whether the password appears in a list "
    "of commonly leaked passwords."
)

# A privacy note. This is both true and a good thing to highlight in interviews:
# it shows security awareness.
st.caption("Your input is analyzed locally in this app and is not stored or "
           "sent anywhere.")

st.divider()

# --- The input box ---
# type="password" hides what is typed behind dots, like a real login field.
password = st.text_input("Enter a password to analyze", type="password")

# --- Show results, but only once the user has typed something ---
if password:
    result = score_password(password)

    # st.metric shows a big number nicely. We show the score and the label.
    st.metric(label="Risk score (higher is stronger)",
              value=f"{result['score']} / 100",
              delta=result["label"])

    # Show the estimated crack time.
    st.write(f"**Estimated time to crack:** {result['crack_time']}")

    # List the problems. If there are none, congratulate the user.
    if result["problems"]:
        st.subheader("Issues found")
        for problem in result["problems"]:
            st.warning(problem)
    else:
        st.success("No major issues found. This is a strong password.")

st.divider()

# --- The analysis section (the data story) ---
# This shows the charts you make in analyze.py. The image files must be in the
# same folder and the filenames must match exactly.
st.header("What the data shows")
st.write(
    "These findings come from analyzing a list of commonly leaked passwords. "
    "They show why the checks above matter."
)

# Each st.image displays one of your saved charts. If you have not made the
# charts yet, comment these lines out (put a # at the start) so the app runs,
# then add them back once analyze.py has created the PNG files.
st.image("length_chart.png", caption="Most leaked passwords are short.")
#st.image("top_passwords_chart.png", caption="The most common passwords.")
st.image("category_chart.png", caption="How many fall into weak categories.")

st.info("Charts will appear here once you run analyze.py to generate them. "
        "Until then, the password checker above works on its own.")