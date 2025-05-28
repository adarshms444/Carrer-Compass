#----------------code----------------
# Main code for the career recommender app using Streamlit, Pandas, SpaCy, and Scikit-learn

# nlp.py

import streamlit as st
import pandas as pd
import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy.cli

# Download and load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Load datasets
career_data = pd.read_csv("final_extended_career_recommender.csv")
suggestion_data = pd.read_csv("career_role_suggestions_large_full.csv")

# Clean and preprocess text
def clean_text(text):
    if pd.isna(text):
        return ""
    text = re.sub(r'[^\w\s]', ' ', str(text))  # Remove punctuation
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    return text.strip().lower()

# Combine all important fields
career_data['Text'] = (
    career_data['Resume'].apply(clean_text) + ' ' +
    career_data['Interests'].apply(clean_text) + ' ' +
    career_data['Skills'].apply(clean_text) + ' ' +
    career_data['Masters'].apply(clean_text) + ' ' +
    career_data['UG_Specialization'].apply(clean_text)
)

# TF-IDF vectorization
vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_df=0.9, min_df=2)
career_vectors = vectorizer.fit_transform(career_data['Text'])

# Keyword extraction
def extract_keywords(text):
    doc = nlp(text.lower())
    keywords = set()
    for chunk in doc.noun_chunks:
        keywords.add(chunk.text.strip())
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PERSON", "GPE", "NORP", "WORK_OF_ART", "PRODUCT", "EVENT", "SKILL"]:
            keywords.add(ent.text.strip())
    return " ".join(keywords)

# Role recommendation
def recommend_roles(user_input, threshold=0.35):
    cleaned_input = clean_text(user_input)
    keyword_input = extract_keywords(cleaned_input)
    combined_input = cleaned_input + ' ' + keyword_input
    user_vector = vectorizer.transform([combined_input])
    similarities = cosine_similarity(user_vector, career_vectors).flatten()
    
    top_indices = similarities.argsort()[::-1]
    unique_roles, top_scores = [], []
    
    for idx in top_indices:
        role = career_data.iloc[idx]["Career_Path"]
        score = similarities[idx]
        if role not in unique_roles and score >= threshold:
            unique_roles.append(role)
            top_scores.append(score)
        if len(unique_roles) >= 5:
            break
    return unique_roles, top_scores

# Role suggestions
def suggest_alternatives(main_roles):
    suggestions = []
    for role in main_roles:
        matches = suggestion_data[suggestion_data['Main_Career_Path'] == role]
        for alt in matches['Suggested_Role']:
            if alt not in suggestions and alt not in main_roles:
                suggestions.append(alt)
            if len(suggestions) == 15:
                return suggestions
    return suggestions



role_tips = {
    "Data Scientist": "Build a strong portfolio in data projects, learn Python, SQL, and machine learning. Get comfortable with data wrangling, statistics, and data visualization tools like Power BI or Tableau. Participate in data challenges like Kaggle or DrivenData. Learn about deployment and MLOps basics.",
    
    "Machine Learning Engineer": "Master ML algorithms, get hands-on with TensorFlow or PyTorch, and try Kaggle competitions. Learn how to productionize ML models, explore model optimization techniques, and understand data pipelines. Keep up with recent research papers on arXiv.",
    
    "Software Developer": "Focus on mastering at least one programming language deeply. Contribute to open-source. Practice coding problems on LeetCode or Codeforces. Learn software development life cycle (SDLC), testing, and version control (Git).",
    
    "Web Developer": "Learn both frontend (HTML, CSS, JS) and backend (Node.js, Django). Build your own site/portfolio. Understand how APIs work and explore frameworks like React or Angular. Learn about web security, SEO, and hosting.",
    
    "Mobile App Developer": "Choose Android or iOS or learn Flutter. Build personal apps to showcase skills. Understand app deployment on Play Store/App Store. Learn mobile UI/UX design and performance optimization.",
    
    "Cybersecurity Analyst": "Start with basics of networking and security. Try certifications like CEH or CompTIA Security+. Practice using tools like Wireshark, Metasploit, and Burp Suite. Explore ethical hacking, penetration testing, and attend CTF challenges.",
    
    "Cloud/DevOps Engineer": "Get hands-on with AWS/Azure/GCP. Learn CI/CD tools like Jenkins, Docker, and Kubernetes. Learn Infrastructure as Code (IaC) tools like Terraform. Get certified (e.g., AWS Solutions Architect). Focus on monitoring/logging tools like Prometheus and Grafana.",
    
    "Mechanical Engineer": "Focus on CAD software like SolidWorks. Internships and GATE can be valuable. Learn about manufacturing processes, thermodynamics, and robotics. Participate in technical events or student competitions (e.g., SAE BAJA).",
    
    "Electrical Engineer": "Focus on circuit design, embedded systems, and simulation tools like MATLAB. Learn PCB designing and tools like Proteus or Eagle. Consider specialization in power systems, IoT, or VLSI.",
    
    "Civil Engineer": "Strong knowledge of structural analysis and tools like AutoCAD or STAAD is essential. Learn construction management principles, estimation, and site work. Consider GATE or RERA certification.",
    
    "Instrumentation Engineer": "Learn control systems and automation tech. PLC programming is useful. Explore SCADA systems, sensors, and signal processing. Gain hands-on with industrial instrumentation hardware.",
    
    "Doctor": "Stay updated with medical advancements and pursue a specialization for better career prospects. Develop empathy and strong communication. Consider publishing in journals or attending conferences.",
    
    "Nurse": "Consider further specialization and certifications. Soft skills and empathy matter a lot. Explore opportunities in ICU, pediatric, or geriatric nursing. Keep up with CPR and first-aid certifications.",
    
    "Biotech/Pharma Associate": "Lab experience and understanding regulations (like GMP) is important. Learn about clinical trials, molecular biology, and bioinformatics. Consider higher studies or certifications (e.g., ICH-GCP).",
    
    "Clinical Psychologist": "Pursue M.Phil or Ph.D. for licensing. Gain therapy experience. Learn different therapy modalities (CBT, DBT, etc.). Focus on ethics, supervision, and mental health advocacy.",
    
    "Physiotherapist": "Hands-on experience and specialization in sports or neuro-physiotherapy helps. Learn about rehabilitation techniques, kinesiology, and pain management. Networking with hospitals and sports clubs is beneficial.",
    
    "Defense Officer (Army/Navy/Airforce)": "Prepare for SSB interviews. Stay physically and mentally fit. Keep updated with defense news and strategy. Practice logical reasoning and situational judgement tests.",
    
    "Civil Services (IAS/IPS/IFS)": "Crack UPSC with disciplined study. Read newspapers and NCERTs daily. Join test series and mock interviews. Build a strong foundation in current affairs, ethics, and governance.",
    
    "Police Officer": "Clear state or UPSC exams. Physical fitness and legal knowledge help. Understand IPC/CrPC laws, and focus on leadership and communication skills. Stay alert about social issues.",
    
    "Government Clerk / Officer": "Target SSC, IBPS, or state PSC exams. Practice aptitude and GK daily. Understand government functioning, file management, and use of MS Office.",
    
    "Entrepreneur / Business Owner": "Start small, solve a real problem, and be ready for risk. Learn digital marketing, funding, and business strategy. Network with mentors and investors.",
    
    "Management Professional": "MBA with internships helps. Build leadership and strategic thinking. Learn operations, HR, finance basics, and project management tools. Stay informed on market trends.",
    
    "Product Manager": "Understand user needs, learn Agile, and build cross-functional communication. Learn tools like JIRA, Trello, and Figma. Get exposure to product lifecycle and customer feedback loops.",
    
    "Business Analyst": "Strong data skills and understanding business workflows is key. Learn tools like Excel, SQL, Tableau, and business intelligence platforms. Write clear documentation and BRDs.",
    
    "Finance Analyst": "Strong Excel, finance modeling, and understanding of markets is important. Learn valuation techniques, risk analysis, and tools like Bloomberg or Power BI. CFA certification can help.",
    
    "Chartered Accountant (CA)": "Articleship experience is key. Stay updated with tax laws. Get comfortable with audit procedures, compliance, and accounting tools like Tally or SAP.",
    
    "Cost Management Accountant (CMA)": "Focus on costing methods, budget control and analysis. Learn strategic cost management and performance analysis. Stay updated with company law and taxation.",
    
    "Lawyer / Legal Associate": "Intern under senior advocates. Study legal drafts and judgments. Learn legal research, client counseling, and court procedures. Consider specialization in IP, corporate, or criminal law.",
    
    "Academic / Teacher": "Develop lesson planning and classroom engagement skills. Stay updated with pedagogy techniques and digital tools. Research and publish papers if in higher education.",
    
    "UI/UX Designer": "Build a strong design portfolio. Learn Figma, Adobe XD, or Sketch. Understand human-centered design and accessibility. Get feedback on designs and improve iteratively.",
    
    "Content Writer": "Write consistently. Learn SEO and write for different platforms. Develop a unique voice, proofread carefully, and understand your audience. Create a blog or Medium account.",
    
    "Journalist": "Strong writing and reporting skills. Build contacts and learn media ethics. Practice interviewing, fact-checking, and multimedia journalism. Intern with local news agencies.",
    
    "Sales & Marketing Executive": "Good communication, market research, and persuasion are key. Learn CRM tools, lead generation, and social media marketing. Understand consumer psychology.",
    
    "HR Executive": "Learn recruitment, payroll tools, and HR policies. Understand labor laws, performance appraisals, and employee engagement. Use tools like Zoho People or SAP SuccessFactors.",
    
    "General Professional / Explore More Options": "Explore internships and try different domains to discover your passion. Take personality tests or career assessments. Network widely and talk to professionals.",
    
    # Additional Roles
    "Data Engineer": "Master data pipelines, ETL processes, and tools like Apache Spark, Airflow, and SQL. Get comfortable with big data frameworks like Hadoop and databases like MongoDB and PostgreSQL.",
    
    "Game Developer": "Learn game engines like Unity or Unreal Engine. Understand C# or C++. Build small games and understand game design principles, graphics, and physics engines.",
    
    "Blockchain Developer": "Learn about blockchain fundamentals, smart contracts, and platforms like Ethereum or Solana. Get hands-on with Solidity or Rust and explore Web3 technologies.",
    
    "Digital Marketing Specialist": "Master SEO, PPC, email marketing, and analytics tools. Get certified in Google Ads, HubSpot, or Meta Blueprint. Learn content marketing and social media strategies.",
    
    "Graphic Designer": "Develop a strong portfolio. Learn Adobe Suite (Photoshop, Illustrator, InDesign). Practice branding, typography, and layout principles. Understand print and digital media.",
    
    "Environmental Scientist": "Study environmental laws and impact analysis. Get hands-on with GIS, remote sensing, and pollution control methods. Join environmental projects or NGOs.",
    
    "Event Manager": "Master planning, budgeting, and vendor coordination. Learn project management tools and public relations. Build negotiation and crisis management skills."
}

# ---------------- Streamlit App ----------------

st.title("🎓 CareerCompass: Career Path Recommender")

name = st.text_input("Enter your name (optional):")
resume_input = st.text_area("Paste your resume or describe your interests, skills, or background:")

uploaded_file = st.file_uploader("Or upload a .txt or .pdf file", type=["txt", "pdf"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".txt"):
            file_text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.name.endswith(".pdf"):
            import PyPDF2
            reader = PyPDF2.PdfReader(uploaded_file)
            file_text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        resume_input = file_text
        st.success("Resume content loaded successfully.")
    except Exception as e:
        st.error(f"Error reading file: {e}")


if st.button("🔍 Recommend Careers"):
    if not resume_input.strip():
        st.warning("Please paste your resume or upload a file.")
    else:
        with st.spinner("Analyzing your input and recommending roles..."):
            roles, scores = recommend_roles(resume_input)
            alternatives = suggest_alternatives(roles)
            
            greeting = f"Hi {name}" if name.strip() else "Hello"

            if not roles:
                st.write(f"{greeting}, we couldn't find a strong match. Please try adding more details.")
            else:
                st.write(f"{greeting}, based on your profile, we recommend:")
                for role, score in zip(roles, scores):
                    st.write(f"- **{role}** (similarity score: {score:.2f})")
                    if role in role_tips:
                        st.caption(f"💡 Tip: {role_tips[role]}")

                if alternatives:
                    st.markdown("---")
                    st.subheader("💡 You might also consider:")
                    for alt in alternatives:
                        st.write(f"- {alt}")



st.markdown("---")
st.caption("📌 CareerCompass — NLP-Powered Personalized Career Guidance System")
