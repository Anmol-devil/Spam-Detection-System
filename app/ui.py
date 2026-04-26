import streamlit as st
import requests

st.set_page_config(page_title="Spam Detector", layout="centered")

st.title("📧 Spam Detection System")

text = st.text_area("Enter Message", height=300)

def show_tags(tags):
    tag_html = ""
    for tag in tags:
        tag_html += f"<span style='background:#eee;padding:5px 10px;margin:4px;border-radius:8px;display:inline-block'>{tag}</span>"
    return tag_html

if st.button("Predict"):
    if not text.strip():
        st.warning("Please enter a message")
    else:
        with st.spinner("Analyzing message..."):
            res = requests.post(
                "http://127.0.0.1:8000/predict",
                json={"message": text}
            )

        if res.status_code == 200:
            result = res.json()

            prediction = result.get("prediction")
            prob = result.get("probability")
            risk = result.get("risk_level")
            signals = result.get("top_signals", [])
            reason = result.get("reason", "")

            # 🎨 Color styling
            if prediction == "Spam":
                st.markdown(
                    f"""
                    <div style="background:#f8d7da;padding:15px;border-radius:10px;">
                        <h3 style="color:#721c24;">🚨 Dangerous Message</h3>
                        <p><b>Confidence:</b> {prob}</p>
                        <p><b>Risk Level:</b> {risk}</p>
                        <p><b>Reason:</b> {reason}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div style="background:#e6f4ea;padding:15px;border-radius:10px;">
                        <h3 style="color:#1e7e34;">✅ Safe Message</h3>
                        <p><b>Confidence:</b> {prob}</p>
                        <p><b>Risk Level:</b> {risk}</p>
                        <p><b>Reason:</b> {reason}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # 🔍 Signals
            st.subheader("🔍 Key Signals")
            st.markdown(show_tags(signals), unsafe_allow_html=True)

            # 🧾 Optional details
            with st.expander("Show Technical Details"):
                st.json(result)

        else:
            st.error("Connection to API failed. Make sure Uvicorn is running.")