import streamlit as st
from streamlit_option_menu import option_menu

# Set page config
st.set_page_config(page_title="Multi-Tool Streamlit Dashboard", layout="wide")

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        "Multi-Tool Dashboard",
        [
            "RAM Monitor", "Send WhatsApp Message",
            "Send Email", "Google Search",
            "Instagram Post", "Send SMS",
            "Call via Twilio", "WhatsApp via Twilio",
            "Create Digital Image"
        ],
        icons=[
            "cpu", "whatsapp", "envelope", "search",
            "camera", "chat-dots", "telephone", "chat-right-dots",
            "image"
        ],
        menu_icon="tools",
        default_index=0,
    )

# RAM Monitor
if selected == "RAM Monitor":
    import psutil
    import time

    st.title("💻 Real-Time RAM Usage Monitor")
    placeholder = st.empty()

    mem = psutil.virtual_memory()
    with placeholder.container():
        st.metric("Total RAM", f"{mem.total / (1024 ** 3):.2f} GB")
        st.metric("Available RAM", f"{mem.available / (1024 ** 3):.2f} GB")
        st.metric("Used RAM", f"{mem.used / (1024 ** 3):.2f} GB")
        st.metric("RAM Usage", f"{mem.percent} %")

# WhatsApp Message
elif selected == "Send WhatsApp Message":
    import pywhatkit as kit
    import datetime

    st.title("📲 Send WhatsApp Message Automatically")
    phone_no = st.text_input("Phone Number (with country code)", "+91")
    message = st.text_area("Message")
    delay_minutes = st.slider("Send after how many minutes?", 1, 10, 1)

    if st.button("Send Message"):
        now = datetime.datetime.now()
        send_hour = now.hour
        send_minute = now.minute + delay_minutes
        kit.sendwhatmsg(phone_no, message, send_hour, send_minute, 15, True, 5)
        st.success(f"Message will be sent at {send_hour}:{send_minute}")

# Send Email
elif selected == "Send Email":
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    st.title("📧 Send Email via Gmail")
    sender_email = st.text_input("Your Gmail")
    app_password = st.text_input("App Password", type="password")
    receiver_email = st.text_input("Recipient Email")
    subject = st.text_input("Subject")
    body = st.text_area("Body")

    if st.button("Send Email"):
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        st.success("✅ Email sent!")

# Google Search
elif selected == "Google Search":
    from googlesearch import search
    st.title("🔍 Google Search")
    query = st.text_input("Search query")
    if query:
        for result in search(query, num_results=5):
            st.write(result)

# Instagram Post
elif selected == "Instagram Post":
    from instagrapi import Client
    from tempfile import NamedTemporaryFile

    st.title("📸 Instagram Auto Poster")
    username = st.text_input("Instagram Username")
    password = st.text_input("Instagram Password", type="password")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    caption = st.text_area("Caption")

    if st.button("Post to Instagram") and all([username, password, uploaded_file, caption]):
        cl = Client()
        cl.login(username, password)
        with NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(uploaded_file.getvalue())
            path = tmp.name
        cl.photo_upload(path=path, caption=caption)
        st.success("✅ Posted to Instagram")

# Send SMS
elif selected == "Send SMS":
    from twilio.rest import Client

    st.title("📩 Send SMS")
    to_number = st.text_input("Recipient Number", "+91")
    message = st.text_area("Message")
    client = Client('xxxxxxxxxxxxxxxx', 'xxxxxxxxxxxxxxxx')
    if st.button("Send SMS"):
        msg = client.messages.create(body=message, from_='xxxxxxxxxxx', to=to_number)
        st.success(f"✅ Sent! SID: {msg.sid}")

# Call via Twilio
elif selected == "Call via Twilio":
    from twilio.rest import Client

    st.title("📞 Call via Twilio")
    to_number = st.text_input("Recipient Number", "+91")
    if st.button("Call Now"):
        client = Client('xxxxxxxxxxxxxxxxxxxx', 'xxxxxxxxxxxxxxx')
        call = client.calls.create(
            to=to_number,
            from_='xxxxxxxxxxx',
            twiml='<Response><Say>Hello! This is a test call from Python.</Say></Response>'
        )
        st.success(f"✅ Call made! SID: {call.sid}")

# WhatsApp via Twilio
elif selected == "WhatsApp via Twilio":
    from twilio.rest import Client

    st.title("💬 WhatsApp via Twilio")
    to_number = st.text_input("Recipient WhatsApp Number", "+91")
    message = st.text_area("Message")
    if st.button("Send WhatsApp Message"):
        client = Client('xxxxxxxxxxxxxx', 'xxxxxxxxxxxxx')
        msg = client.messages.create(
            body=message,
            from_='whatsapp:xxxxxxxxxx',
            to='whatsapp:' + to_number
        )
        st.success(f"✅ Sent! SID: {msg.sid}")

# Create Digital Image
elif selected == "Create Digital Image":
    from PIL import Image, ImageDraw, ImageFont
    import io

    st.title("🎨 Create Digital Image")
    text = st.text_input("Text", "Hello World")
    font_size = st.slider("Font Size", 10, 100, 40)
    bg_color = st.color_picker("Background Color", "#497B89")
    text_color = st.color_picker("Text Color", "#FFFFFF")
    img_width = st.slider("Image Width", 100, 800, 400)
    img_height = st.slider("Image Height", 100, 400, 200)

    if st.button("Generate Image"):
        image = Image.new("RGB", (img_width, img_height), color=bg_color)
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (img_width - text_width) / 2
        text_y = (img_height - text_height) / 2
        draw.text((text_x, text_y), text, fill=text_color, font=font)

        st.image(image, caption="Your Image")
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        st.download_button("Download", buf.getvalue(), "image.png", "image/png")
