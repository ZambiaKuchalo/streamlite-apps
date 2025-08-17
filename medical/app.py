import streamlit as st
import json
from openai import OpenAI
from datetime import datetime
import pandas as pd

# Configure page
st.set_page_config(
    page_title="MedAssist AI - Clinical Decision Support",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize OpenAI client
@st.cache_resource
def init_openai_client():
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key = os.environ.get("OPENAI_API_KEY")
    )

def get_ai_response(prompt, system_message="You are a medical AI assistant helping healthcare professionals."):
    """Get response from AI model"""
    try:
        client = init_openai_client()
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://medassist-ai.streamlit.app",
                "X-Title": "MedAssist AI Clinical Tool",
            },
            model="deepseek/deepseek-r1:free",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=1500
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}. Please check your API key configuration."

# Sidebar configuration
with st.sidebar:
    st.title("🏥 MedAssist AI")
    st.markdown("---")
    
    # Tool selection
    selected_tool = st.selectbox(
        "Select Medical Tool",
        ["Symptom Analysis", "Differential Diagnosis", "Drug Interaction Check", 
         "Clinical Guidelines", "Lab Results Interpreter", "Patient Assessment"]
    )
    
    st.markdown("---")
    
    # Patient info section
    st.subheader("Patient Information")
    patient_age = st.number_input("Age", min_value=0, max_value=120, value=45)
    patient_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    patient_weight = st.number_input("Weight (kg)", min_value=0.0, max_value=300.0, value=70.0)
    
    # Emergency protocols
    st.markdown("---")
    st.subheader("🚨 Emergency Protocols")
    if st.button("Cardiac Emergency", type="secondary"):
        st.error("Activating cardiac emergency protocol...")
    if st.button("Trauma Protocol", type="secondary"):
        st.error("Activating trauma protocol...")

# Main content area
st.title("🏥 MedAssist AI - Clinical Decision Support Tool")
st.markdown("**AI-powered medical assistance for healthcare professionals**")

# Warning disclaimer
st.warning("⚠️ **IMPORTANT DISCLAIMER**: This tool is for educational and decision-support purposes only. Always consult with qualified medical professionals and follow institutional protocols for patient care.")

# Create tabs for different functionalities
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Analysis", "📋 History", "📊 Reports", "⚙️ Settings"])

with tab1:
    if selected_tool == "Symptom Analysis":
        st.header("🔍 Symptom Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            symptoms = st.text_area(
                "Enter patient symptoms (be specific and detailed):",
                placeholder="e.g., chest pain radiating to left arm, shortness of breath, diaphoresis...",
                height=100
            )
            
            duration = st.selectbox("Symptom Duration", 
                                  ["< 1 hour", "1-6 hours", "6-24 hours", "1-7 days", "> 1 week"])
            
            severity = st.select_slider("Pain/Severity Scale", 
                                      options=[1,2,3,4,5,6,7,8,9,10], value=5)
        
        with col2:
            st.subheader("Quick Assessment")
            vital_signs = st.checkbox("Abnormal Vital Signs")
            altered_consciousness = st.checkbox("Altered Consciousness")
            acute_onset = st.checkbox("Acute Onset")
            
            if vital_signs or altered_consciousness or acute_onset:
                st.error("🚨 Consider immediate evaluation")
        
        if st.button("Analyze Symptoms", type="primary"):
            if symptoms:
                with st.spinner("Analyzing symptoms..."):
                    prompt = f"""
                    Analyze these symptoms for a {patient_age}-year-old {patient_gender.lower()} patient:
                    
                    Symptoms: {symptoms}
                    Duration: {duration}
                    Severity: {severity}/10
                    Weight: {patient_weight}kg
                    
                    Please provide:
                    1. Most likely conditions (top 3-5)
                    2. Red flag symptoms to watch for
                    3. Recommended immediate actions
                    4. Suggested diagnostic tests
                    5. Urgency level (1-5 scale)
                    
                    Format as structured clinical assessment.
                    """
                    
                    system_msg = """You are a clinical decision support AI assistant. Provide evidence-based medical analysis while emphasizing the need for professional clinical judgment. Always recommend consulting with healthcare providers."""
                    
                    response = get_ai_response(prompt, system_msg)
                    
                    st.subheader("📋 Clinical Analysis")
                    st.markdown(response)
            else:
                st.warning("Please enter patient symptoms to analyze.")
    
    elif selected_tool == "Differential Diagnosis":
        st.header("🩺 Differential Diagnosis Assistant")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            chief_complaint = st.text_input("Chief Complaint:", placeholder="e.g., Chest pain")
            
            history = st.text_area("History of Present Illness:", 
                                 placeholder="Detailed history...", height=100)
            
            past_medical_history = st.text_area("Past Medical History:", 
                                              placeholder="Previous conditions, surgeries...", height=80)
            
            medications = st.text_area("Current Medications:", 
                                     placeholder="List current medications...", height=60)
        
        with col2:
            st.subheader("System Review")
            systems = {
                "Cardiovascular": st.checkbox("CV symptoms"),
                "Respiratory": st.checkbox("Resp symptoms"), 
                "Neurological": st.checkbox("Neuro symptoms"),
                "GI": st.checkbox("GI symptoms"),
                "Genitourinary": st.checkbox("GU symptoms"),
                "Musculoskeletal": st.checkbox("MSK symptoms")
            }
        
        if st.button("Generate Differential Diagnosis", type="primary"):
            if chief_complaint and history:
                with st.spinner("Generating differential diagnosis..."):
                    active_systems = [k for k, v in systems.items() if v]
                    
                    prompt = f"""
                    Generate a differential diagnosis for:
                    
                    Patient: {patient_age}yo {patient_gender}, {patient_weight}kg
                    Chief Complaint: {chief_complaint}
                    HPI: {history}
                    PMH: {past_medical_history}
                    Medications: {medications}
                    Systems involved: {', '.join(active_systems)}
                    
                    Provide:
                    1. Top 5 differential diagnoses (ranked by likelihood)
                    2. Key distinguishing features for each
                    3. Diagnostic workup recommendations
                    4. Initial management considerations
                    5. Disposition recommendations
                    """
                    
                    response = get_ai_response(prompt)
                    st.markdown(response)
    
    elif selected_tool == "Drug Interaction Check":
        st.header("💊 Drug Interaction Checker")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Current Medications")
            current_meds = st.text_area("List current medications (one per line):",
                                       placeholder="Medication name and dosage\ne.g., Metoprolol 25mg BID",
                                       height=150)
        
        with col2:
            st.subheader("New Medication")
            new_medication = st.text_input("New medication to add:")
            new_dose = st.text_input("Dosage and frequency:")
            
            # Allergy check
            st.subheader("Allergies")
            allergies = st.text_area("Known allergies:", 
                                   placeholder="Drug allergies and reactions")
        
        if st.button("Check Interactions", type="primary"):
            if current_meds and new_medication:
                with st.spinner("Checking for interactions..."):
                    prompt = f"""
                    Analyze drug interactions for:
                    
                    Patient: {patient_age}yo {patient_gender}, {patient_weight}kg
                    Current medications:
                    {current_meds}
                    
                    New medication: {new_medication} {new_dose}
                    
                    Known allergies: {allergies}
                    
                    Please assess:
                    1. Drug-drug interactions (severity level)
                    2. Contraindications based on age/weight
                    3. Dosing recommendations
                    4. Monitoring requirements
                    5. Alternative medications if contraindicated
                    """
                    
                    response = get_ai_response(prompt)
                    st.markdown(response)
    
    elif selected_tool == "Lab Results Interpreter":
        st.header("🧪 Laboratory Results Interpreter")
        
        # File upload for lab results
        uploaded_file = st.file_uploader("Upload Lab Results (PDF/Text)", 
                                       type=['txt', 'pdf'])
        
        # Manual entry option
        st.subheader("Or Enter Lab Values Manually:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Hematology**")
            wbc = st.number_input("WBC (4.0-11.0)", value=0.0, format="%.1f")
            hgb = st.number_input("Hemoglobin (12-16)", value=0.0, format="%.1f")
            plt = st.number_input("Platelets (150-450)", value=0.0, format="%.0f")
        
        with col2:
            st.write("**Chemistry**")
            glucose = st.number_input("Glucose (70-100)", value=0.0, format="%.0f")
            creatinine = st.number_input("Creatinine (0.6-1.3)", value=0.0, format="%.2f")
            sodium = st.number_input("Sodium (135-145)", value=0.0, format="%.0f")
        
        with col3:
            st.write("**Liver Function**")
            alt = st.number_input("ALT (7-56)", value=0.0, format="%.0f")
            ast = st.number_input("AST (10-40)", value=0.0, format="%.0f")
            bilirubin = st.number_input("Bilirubin (0.2-1.9)", value=0.0, format="%.1f")
        
        clinical_context = st.text_area("Clinical Context:", 
                                      placeholder="Patient symptoms, suspected diagnosis...")
        
        if st.button("Interpret Results", type="primary"):
            lab_values = f"""
            WBC: {wbc} (4.0-11.0)
            Hemoglobin: {hgb} (12-16)
            Platelets: {plt} (150-450)
            Glucose: {glucose} (70-100)
            Creatinine: {creatinine} (0.6-1.3)
            Sodium: {sodium} (135-145)
            ALT: {alt} (7-56)
            AST: {ast} (10-40)
            Bilirubin: {bilirubin} (0.2-1.9)
            """
            
            prompt = f"""
            Interpret these lab results for a {patient_age}yo {patient_gender}:
            
            {lab_values}
            
            Clinical context: {clinical_context}
            
            Provide:
            1. Abnormal values and significance
            2. Possible diagnoses suggested by results
            3. Additional tests recommended
            4. Clinical correlation needed
            5. Urgency of findings
            """
            
            response = get_ai_response(prompt)
            st.markdown(response)

with tab2:
    st.header("📋 Patient Assessment History")
    
    # Session state for storing assessments
    if 'assessments' not in st.session_state:
        st.session_state.assessments = []
    
    if st.session_state.assessments:
        for i, assessment in enumerate(reversed(st.session_state.assessments)):
            with st.expander(f"Assessment {len(st.session_state.assessments)-i} - {assessment['timestamp']}"):
                st.write(f"**Tool Used:** {assessment['tool']}")
                st.write(f"**Patient:** {assessment['patient_info']}")
                st.write(f"**Input:** {assessment['input']}")
                st.write(f"**Analysis:** {assessment['response']}")
    else:
        st.info("No previous assessments found. Complete an analysis to see history here.")

with tab3:
    st.header("📊 Clinical Reports & Analytics")
    
    # Sample data for demonstration
    sample_data = {
        'Date': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19'],
        'Cases Analyzed': [12, 15, 8, 20, 11],
        'Emergency Cases': [2, 3, 1, 5, 2],
        'Tool Usage': ['Symptom Analysis', 'Drug Interaction', 'Lab Interpreter', 'Differential Dx', 'Symptom Analysis']
    }
    
    df = pd.DataFrame(sample_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Daily Case Volume")
        st.line_chart(df.set_index('Date')['Cases Analyzed'])
    
    with col2:
        st.subheader("Emergency Cases")
        st.bar_chart(df.set_index('Date')['Emergency Cases'])
    
    st.subheader("Recent Activity")
    st.dataframe(df, use_container_width=True)

with tab4:
    st.header("⚙️ Settings & Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("API Configuration")
        api_key_input = st.text_input("OpenRouter API Key", type="password", 
                                    placeholder="Enter your API key")
        
        st.subheader("Clinical Preferences")
        preferred_units = st.selectbox("Preferred Units", ["Metric", "Imperial"])
        urgency_threshold = st.slider("Emergency Alert Threshold", 1, 10, 7)
        
        auto_save = st.checkbox("Auto-save assessments", value=True)
    
    with col2:
        st.subheader("Institution Settings")
        institution = st.text_input("Institution Name")
        department = st.text_input("Department")
        
        st.subheader("Notification Preferences")
        email_alerts = st.checkbox("Email alerts for high-risk cases")
        critical_alerts = st.checkbox("Critical value notifications")
        
        if st.button("Save Settings"):
            st.success("Settings saved successfully!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
<p><strong>MedAssist AI v1.0</strong> | Clinical Decision Support Tool</p>
<p><em>⚠️ This tool is for educational and decision-support purposes only. Always follow institutional protocols and consult with healthcare professionals.</em></p>
</div>
""", unsafe_allow_html=True)

# Store assessment in session state when analysis is performed
def store_assessment(tool, patient_info, user_input, ai_response):
    if 'assessments' not in st.session_state:
        st.session_state.assessments = []
    
    assessment = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'tool': tool,
        'patient_info': f"{patient_age}yo {patient_gender}",
        'input': user_input,
        'response': ai_response
    }
    
    st.session_state.assessments.append(assessment)
    
    # Keep only last 10 assessments
    if len(st.session_state.assessments) > 10:
        st.session_state.assessments = st.session_state.assessments[-10:]