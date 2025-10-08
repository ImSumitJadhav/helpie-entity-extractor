from google import genai
import json
import streamlit as st
from PIL import Image
import tempfile
import warnings
warnings.filterwarnings("ignore")

#gemini API
GOOGLE_API_KEY=st.sidebar.text_input("Enter Your Google Gemini API Key...",type="password")
if st.sidebar.button("Submit API Key"):
    pass

st.sidebar.text("""USE : 
    1.Automatically add contacts from business cards to CRM.
    2.Extract lead info from recorded sales calls.
    3.Populate contact fields (phone, email) in a helpdesk ticket from voicemail.
    4.Bulk-processing conference business cards or meeting recordings.""")

st.sidebar.image(r"C:\Users\sumit\Desktop\AUG 25\Helpie\input image\logo_2.png",width=50)

if GOOGLE_API_KEY:
    client = genai.Client(api_key=GOOGLE_API_KEY)
    MODEL_ID = "gemini-2.5-pro"

st.image(r"C:\Users\sumit\Desktop\AUG 25\Helpie\input image\logo_1.png")
st.title("📋 HELPIE ENTITY EXTRACTOR")
options = ["","Card","Audio"]
selected = st.selectbox("Select between Card & Audio:", options)

if selected=="Card":
    st.title("🪪 Business Card Uploader")
    # File uploader (only image types)
    sample_file_truncated = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])
    if sample_file_truncated:
        if st.button("Submit"):
            image = Image.open(sample_file_truncated)
            response_for_data = client.models.generate_content(
                model=MODEL_ID,
                contents=[f"""
                        Act as a entity extraction expert from given image of business card. Give output as a JSON format only.
                        Give me entities below:
                        1.name of person
                        2.designation of person
                        3.name of company
                        4.contact number
                        5.email
                        6.address
                        7.city
                        8.state 
                        9.country

                        Instructions:
                        1. strictly give JSON format.
                        2. don't give any external noise.
                        3. if values for some entities are not present in the context then give blank output for that entity.
                        4. strictly follow given example for final JSON output.

                        example:
                        {{ "name of person": "Vivek Swain",
                        "designation of person": "Manager",
                        "name of company": "Advanced Bolting Solutions Pvt. Ltd.",
                        "contact number": "+91 91527 28613",
                        "email": "vivek.swain@absgroup.in",
                        "address": "HO-ABS House, Plot W-116 (A), MIDC Khairane, Navi Mumbai - 400 710",
                        "city": "Navi Mumbai",
                        "state": "Maharashtra" 
                        "country": "INDIA",
                        }}
                        """, image]
            )

            response_for_data_output=response_for_data.text
            response_for_data_output=response_for_data_output.replace("python","").replace("```python","").replace("```json","").replace("```","").replace("``","").replace("**","").replace("#","").strip()
            response_for_data_output_json = json.loads(response_for_data_output)

            st.title("📇 Extracted Business Card Details")

            # Display as readable key-value pairs
            for key, value in response_for_data_output_json.items():
                st.markdown(f"**{key.title()}**: {value}")

elif selected=="Audio":
    st.title("🔉 Audio Uploader")
    sample_file_truncated = st.file_uploader("Upload an image file", type=["mp3","wav"])
    if sample_file_truncated is not None:
        if st.button("Submit"):
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                temp_audio.write(sample_file_truncated.read())
                temp_audio_path = temp_audio.name

            # Pass the temporary audio file to your LLM
            sample_file_truncated = client.files.upload(file=temp_audio_path)
            
            if sample_file_truncated:
                response_for_data = client.models.generate_content(
                model=MODEL_ID,
                contents=[f"""
                        Act as a entity extraction expert from given audio file which gives information of person and its bussiness
                        information. Give output as a JSON format only.
                        
                        Give me entities below:
                        1.name of person
                        2.designation of person
                        3.name of company
                        4.contact number
                        5.email
                        6.address
                        7.city
                        8.state 
                        9.country
                        10.products
                        11.financial budget
                        12.meet location
                        13.deadline for product
                        14.follow up response (True or False)

                        Instructions:
                        1. strictly give JSON format.
                        2. don't give any external noise.
                        3. if values for some entities are not present in the context then give blank output for that entity.
                        4. strictly follow given example for final JSON output.
                        5. 'follow up response" should be like the person gives positive response like meet or connect virtually then give "True" as
                        a final response otherwise gives "False".

                        example:
                        {{ "name of person": "Vivek Swain",
                        "designation of person": "Manager",
                        "name of company": "Advanced Bolting Solutions Pvt. Ltd.",
                        "contact number": "+91 91527 28613",
                        "email": "vivek.swain@absgroup.in",
                        "address": "HO-ABS House, Plot W-116 (A), MIDC Khairane, Navi Mumbai - 400 710",
                        "city": "Navi Mumbai",
                        "state": "Maharashtra" 
                        "country": "INDIA",
                        "products : "some value",
                        "financial budget" : "some value",
                        "meet location" : "some value",
                        "deadline for product":"some value",
                        "follow up response" : "True or False"
                        }}
                        """, sample_file_truncated]
                )

                response_for_data_output=response_for_data.text
                response_for_data_output=response_for_data_output.replace("python","").replace("```python","").replace("```json","").replace("```","").replace("``","").replace("**","").replace("#","").strip()
                response_for_data_output_json = json.loads(response_for_data_output)

                st.title("📇 Extracted Audio Details")

                # Display as readable key-value pairs
                for key, value in response_for_data_output_json.items():
                    st.markdown(f"**{key.title()}**: {value}")
