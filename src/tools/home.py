import streamlit as st

st.title("Plan and Dive")
st.write("A few tools to help you plan your dives. Use the navigation on the left to access the different tools.")
st.html("""<div style="text-align: center; font-size: 200px;">🤿</div>""")
with st.container(border=True):
    st.subheader("Disclaimer")
    st.markdown(
        """
        The diving tools provided in this application are for **educational purposes only**.

        **By using these tools, you acknowledge and agree that:**

        - All calculations and recommendations should be **verified independently** using certified dive tables, dive computers, or professional dive planning software.
        - The developers of this application **disclaim all liability** for any injury, damage, or loss resulting from the use of these tools.
        """
    )
