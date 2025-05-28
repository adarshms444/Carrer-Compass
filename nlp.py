# import streamlit as st
# import pandas as pd
# import spacy
# import re
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# # Load SpaCy model
# nlp = spacy.load("en_core_web_sm")

# # Load datasets
# career_data = pd.read_csv("final_extended_career_recommender.csv")
# suggestion_data = pd.read_csv("enriched_career_recommender.csv")

# # Combine text fields and vectorize
# career_data['Text'] = career_data['Resume'].fillna('') + ' ' + career_data['Interests'].fillna('') + ' ' + career_data['Skills'].fillna('')
# vectorizer = TfidfVectorizer()
# career_vectors = vectorizer.fit_transform(career_data['Text'])

# # Extract user info
# def extract_info(text):
#     text = re.sub(r"[^a-zA-Z0-9 ]", "", text)
#     doc = nlp(text)
#     skills = [ent.text for ent in doc.ents if ent.label_ in ["SKILL", "ORG", "PERSON"]]
#     return " ".join(skills if skills else [text])

# # Recommend top relevant roles with threshold filtering
# def recommend_roles(user_input, threshold=0.40):
#     cleaned = extract_info(user_input)
#     user_vector = vectorizer.transform([cleaned])
#     similarities = cosine_similarity(user_vector, career_vectors).flatten()

#     top_indices = similarities.argsort()[::-1]
#     unique_roles = []
#     top_scores = []

#     for idx in top_indices:
#         role = career_data.iloc[idx]["Career_Path"]
#         score = similarities[idx]
#         if role not in unique_roles and score >= threshold:
#             unique_roles.append(role)
#             top_scores.append(score)
#         if len(unique_roles) >= 5:
#             break

#     return unique_roles, top_scores

# # Suggest relevant alternatives using the suggestion dataset
# def suggest_alternatives(main_roles):
#     suggestions = []
#     for role in main_roles:
#         matches = suggestion_data[suggestion_data['Main_Career_Path'] == role]
#         for alt in matches['Suggested_Role']:
#             if alt not in suggestions and alt not in main_roles:
#                 suggestions.append(alt)
#             if len(suggestions) == 15:
#                 return suggestions
#     return suggestions

# # Tips dictionary
# role_tips = {
#     "Data Scientist": "Build a strong portfolio in data projects, learn Python, SQL, and machine learning.",
#     "Machine Learning Engineer": "Master ML algorithms, get hands-on with TensorFlow or PyTorch, and try Kaggle competitions.",
#     "Software Developer": "Focus on mastering at least one programming language deeply. Contribute to open-source.",
#     "Web Developer": "Learn both frontend (HTML, CSS, JS) and backend (Node.js, Django). Build your own site/portfolio.",
#     "Mobile App Developer": "Choose Android or iOS or learn Flutter. Build personal apps to showcase skills.",
#     "Cybersecurity Analyst": "Start with basics of networking and security. Try certifications like CEH or CompTIA Security+.",
#     "Cloud/DevOps Engineer": "Get hands-on with AWS/Azure/GCP. Learn CI/CD tools like Jenkins, Docker, and Kubernetes.",
#     "Mechanical Engineer": "Focus on CAD software like SolidWorks. Internships and GATE can be valuable.",
#     "Electrical Engineer": "Focus on circuit design, embedded systems, and simulation tools like MATLAB.",
#     "Civil Engineer": "Strong knowledge of structural analysis and tools like AutoCAD or STAAD is essential.",
#     "Instrumentation Engineer": "Learn control systems and automation tech. PLC programming is useful.",
#     "Doctor": "Stay updated with medical advancements and pursue a specialization for better career prospects.",
#     "Nurse": "Consider further specialization and certifications. Soft skills and empathy matter a lot.",
#     "Biotech/Pharma Associate": "Lab experience and understanding regulations (like GMP) is important.",
#     "Clinical Psychologist": "Pursue M.Phil or Ph.D. for licensing. Gain therapy experience.",
#     "Physiotherapist": "Hands-on experience and specialization in sports or neuro-physiotherapy helps.",
#     "Defense Officer (Army/Navy/Airforce)": "Prepare for SSB interviews. Stay physically and mentally fit.",
#     "Civil Services (IAS/IPS/IFS)": "Crack UPSC with disciplined study. Read newspapers and NCERTs daily.",
#     "Police Officer": "Clear state or UPSC exams. Physical fitness and legal knowledge help.",
#     "Government Clerk / Officer": "Target SSC, IBPS, or state PSC exams. Practice aptitude and GK daily.",
#     "Entrepreneur / Business Owner": "Start small, solve a real problem, and be ready for risk.",
#     "Management Professional": "MBA with internships helps. Build leadership and strategic thinking.",
#     "Product Manager": "Understand user needs, learn Agile, and build cross-functional communication.",
#     "Business Analyst": "Strong data skills and understanding business workflows is key.",
#     "Finance Analyst": "Strong Excel, finance modeling, and understanding of markets is important.",
#     "Chartered Accountant (CA)": "Articleship experience is key. Stay updated with tax laws.",
#     "Cost Management Accountant (CMA)": "Focus on costing methods, budget control and analysis.",
#     "Lawyer / Legal Associate": "Intern under senior advocates. Study legal drafts and judgments.",
#     "Academic / Teacher": "Develop lesson planning and classroom engagement skills.",
#     "UI/UX Designer": "Build a strong design portfolio. Learn Figma, Adobe XD, or Sketch.",
#     "Content Writer": "Write consistently. Learn SEO and write for different platforms.",
#     "Journalist": "Strong writing and reporting skills. Build contacts and learn media ethics.",
#     "Sales & Marketing Executive": "Good communication, market research, and persuasion are key.",
#     "HR Executive": "Learn recruitment, payroll tools, and HR policies.",
#     "General Professional / Explore More Options": "Explore internships and try different domains to discover your passion."
# }
# # Streamlit UI
# st.title("CareerCompass: Career Path Recommender")

# name = st.text_input("Enter your name (optional):")
# resume_input = st.text_area("Paste your resume or describe your interests, skills, and background:")
# uploaded_file = st.file_uploader("Or upload your resume as a .txt file")

# user_text = ""
# if uploaded_file is not None:
#     try:
#         user_text = uploaded_file.read().decode("utf-8")
#     except UnicodeDecodeError:
#         uploaded_file.seek(0)  # Reset the file pointer
#         try:
#             user_text = uploaded_file.read().decode("latin1")
#         except Exception as e:
#             st.error(f"Failed to decode the file. Error: {e}")
#             user_text = ""
# elif resume_input:
#     user_text = resume_input

# if user_text and st.button("Get Details"):
#     st.markdown("---")
#     st.subheader("🔍 Recommendations")

#     recs, sims = recommend_roles(user_text)

#     greeting = f"Hi {name}," if name else "Hi friend,"
#     if not recs:
#         st.write(f"{greeting} we couldn't find a strong match. Please try adding more details.")
#     else:
#         st.write(f"{greeting} based on your profile, we recommend:")
#         for role, score in zip(recs, sims):
#             st.write(f"- **{role}** (similarity score: {score:.2f})")

#         alt_suggestions = suggest_alternatives(recs)
#         if alt_suggestions:
#             st.markdown("---")
#             st.subheader("💡 You might also consider:")
#             for alt in alt_suggestions:
#                 st.write(f"- {alt}")

#         st.markdown("---")
#         st.subheader("📌 Tips for Recommended Roles")
#         for role in recs:
#             tip = role_tips.get(role, "Explore this career path further by connecting with professionals and doing internships.")
#             st.markdown(f"**{role}**: {tip}")

#         # st.subheader("📌 Tips for Alternative Suggestions")
#         # for alt in alt_suggestions:
#         #     alt_tip = role_tips.get(alt, "Explore this alternative path to broaden your opportunities.")
#         #     st.markdown(f"**{alt}**: {alt_tip}")

# else:
#     st.info("Please paste your resume or upload a .txt file to get started.")

# import streamlit as st
# import pandas as pd
# import spacy
# import re
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# # Load SpaCy model
# nlp = spacy.load("en_core_web_sm")

# # Load datasets
# career_data = pd.read_csv("final_extended_career_recommender.csv")
# suggestion_data = pd.read_csv("career_role_suggestions_large_full.csv")

# # Combine text fields for vectorization
# career_data['Text'] = (
#     career_data['Resume'].fillna('') + ' ' +
#     career_data['Interests'].fillna('') + ' ' +
#     career_data['Skills'].fillna('')
# )

# # TF-IDF vectorization of dataset
# vectorizer = TfidfVectorizer(stop_words="english")
# career_vectors = vectorizer.fit_transform(career_data['Text'])

# # Extract general-purpose keywords from resume using spaCy
# def extract_keywords(text):
#     doc = nlp(text.lower())
#     keywords = set()
    
#     for chunk in doc.noun_chunks:
#         keywords.add(chunk.text.strip())
        
#     for ent in doc.ents:
#         if ent.label_ in ["ORG", "PERSON", "GPE", "NORP", "WORK_OF_ART", "PRODUCT", "EVENT", "SKILL"]:
#             keywords.add(ent.text.strip())
    
#     return " ".join(keywords)

# # Recommend top relevant roles with threshold filtering
# def recommend_roles(user_input, threshold=0.40):
#     cleaned_input = extract_keywords(user_input)
#     user_vector = vectorizer.transform([cleaned_input])
#     similarities = cosine_similarity(user_vector, career_vectors).flatten()
    
#     top_indices = similarities.argsort()[::-1]
#     unique_roles = []
#     top_scores = []
    
#     for idx in top_indices:
#         role = career_data.iloc[idx]["Career_Path"]
#         score = similarities[idx]
#         if role not in unique_roles and score >= threshold:
#             unique_roles.append(role)
#             top_scores.append(score)
#         if len(unique_roles) >= 5:
#             break

#     return unique_roles, top_scores

# # Suggest alternatives from the suggestions dataset
# def suggest_alternatives(main_roles):
#     suggestions = []
#     for role in main_roles:
#         matches = suggestion_data[suggestion_data['Main_Career_Path'] == role]
#         for alt in matches['Suggested_Role']:
#             if alt not in suggestions and alt not in main_roles:
#                 suggestions.append(alt)
#             if len(suggestions) == 15:
#                 return suggestions
#     return suggestions


# role_tips = {
#     "Data Scientist": "Build a strong portfolio in data projects, learn Python, SQL, and machine learning. Get comfortable with data wrangling, statistics, and data visualization tools like Power BI or Tableau. Participate in data challenges like Kaggle or DrivenData. Learn about deployment and MLOps basics.",
    
#     "Machine Learning Engineer": "Master ML algorithms, get hands-on with TensorFlow or PyTorch, and try Kaggle competitions. Learn how to productionize ML models, explore model optimization techniques, and understand data pipelines. Keep up with recent research papers on arXiv.",
    
#     "Software Developer": "Focus on mastering at least one programming language deeply. Contribute to open-source. Practice coding problems on LeetCode or Codeforces. Learn software development life cycle (SDLC), testing, and version control (Git).",
    
#     "Web Developer": "Learn both frontend (HTML, CSS, JS) and backend (Node.js, Django). Build your own site/portfolio. Understand how APIs work and explore frameworks like React or Angular. Learn about web security, SEO, and hosting.",
    
#     "Mobile App Developer": "Choose Android or iOS or learn Flutter. Build personal apps to showcase skills. Understand app deployment on Play Store/App Store. Learn mobile UI/UX design and performance optimization.",
    
#     "Cybersecurity Analyst": "Start with basics of networking and security. Try certifications like CEH or CompTIA Security+. Practice using tools like Wireshark, Metasploit, and Burp Suite. Explore ethical hacking, penetration testing, and attend CTF challenges.",
    
#     "Cloud/DevOps Engineer": "Get hands-on with AWS/Azure/GCP. Learn CI/CD tools like Jenkins, Docker, and Kubernetes. Learn Infrastructure as Code (IaC) tools like Terraform. Get certified (e.g., AWS Solutions Architect). Focus on monitoring/logging tools like Prometheus and Grafana.",
    
#     "Mechanical Engineer": "Focus on CAD software like SolidWorks. Internships and GATE can be valuable. Learn about manufacturing processes, thermodynamics, and robotics. Participate in technical events or student competitions (e.g., SAE BAJA).",
    
#     "Electrical Engineer": "Focus on circuit design, embedded systems, and simulation tools like MATLAB. Learn PCB designing and tools like Proteus or Eagle. Consider specialization in power systems, IoT, or VLSI.",
    
#     "Civil Engineer": "Strong knowledge of structural analysis and tools like AutoCAD or STAAD is essential. Learn construction management principles, estimation, and site work. Consider GATE or RERA certification.",
    
#     "Instrumentation Engineer": "Learn control systems and automation tech. PLC programming is useful. Explore SCADA systems, sensors, and signal processing. Gain hands-on with industrial instrumentation hardware.",
    
#     "Doctor": "Stay updated with medical advancements and pursue a specialization for better career prospects. Develop empathy and strong communication. Consider publishing in journals or attending conferences.",
    
#     "Nurse": "Consider further specialization and certifications. Soft skills and empathy matter a lot. Explore opportunities in ICU, pediatric, or geriatric nursing. Keep up with CPR and first-aid certifications.",
    
#     "Biotech/Pharma Associate": "Lab experience and understanding regulations (like GMP) is important. Learn about clinical trials, molecular biology, and bioinformatics. Consider higher studies or certifications (e.g., ICH-GCP).",
    
#     "Clinical Psychologist": "Pursue M.Phil or Ph.D. for licensing. Gain therapy experience. Learn different therapy modalities (CBT, DBT, etc.). Focus on ethics, supervision, and mental health advocacy.",
    
#     "Physiotherapist": "Hands-on experience and specialization in sports or neuro-physiotherapy helps. Learn about rehabilitation techniques, kinesiology, and pain management. Networking with hospitals and sports clubs is beneficial.",
    
#     "Defense Officer (Army/Navy/Airforce)": "Prepare for SSB interviews. Stay physically and mentally fit. Keep updated with defense news and strategy. Practice logical reasoning and situational judgement tests.",
    
#     "Civil Services (IAS/IPS/IFS)": "Crack UPSC with disciplined study. Read newspapers and NCERTs daily. Join test series and mock interviews. Build a strong foundation in current affairs, ethics, and governance.",
    
#     "Police Officer": "Clear state or UPSC exams. Physical fitness and legal knowledge help. Understand IPC/CrPC laws, and focus on leadership and communication skills. Stay alert about social issues.",
    
#     "Government Clerk / Officer": "Target SSC, IBPS, or state PSC exams. Practice aptitude and GK daily. Understand government functioning, file management, and use of MS Office.",
    
#     "Entrepreneur / Business Owner": "Start small, solve a real problem, and be ready for risk. Learn digital marketing, funding, and business strategy. Network with mentors and investors.",
    
#     "Management Professional": "MBA with internships helps. Build leadership and strategic thinking. Learn operations, HR, finance basics, and project management tools. Stay informed on market trends.",
    
#     "Product Manager": "Understand user needs, learn Agile, and build cross-functional communication. Learn tools like JIRA, Trello, and Figma. Get exposure to product lifecycle and customer feedback loops.",
    
#     "Business Analyst": "Strong data skills and understanding business workflows is key. Learn tools like Excel, SQL, Tableau, and business intelligence platforms. Write clear documentation and BRDs.",
    
#     "Finance Analyst": "Strong Excel, finance modeling, and understanding of markets is important. Learn valuation techniques, risk analysis, and tools like Bloomberg or Power BI. CFA certification can help.",
    
#     "Chartered Accountant (CA)": "Articleship experience is key. Stay updated with tax laws. Get comfortable with audit procedures, compliance, and accounting tools like Tally or SAP.",
    
#     "Cost Management Accountant (CMA)": "Focus on costing methods, budget control and analysis. Learn strategic cost management and performance analysis. Stay updated with company law and taxation.",
    
#     "Lawyer / Legal Associate": "Intern under senior advocates. Study legal drafts and judgments. Learn legal research, client counseling, and court procedures. Consider specialization in IP, corporate, or criminal law.",
    
#     "Academic / Teacher": "Develop lesson planning and classroom engagement skills. Stay updated with pedagogy techniques and digital tools. Research and publish papers if in higher education.",
    
#     "UI/UX Designer": "Build a strong design portfolio. Learn Figma, Adobe XD, or Sketch. Understand human-centered design and accessibility. Get feedback on designs and improve iteratively.",
    
#     "Content Writer": "Write consistently. Learn SEO and write for different platforms. Develop a unique voice, proofread carefully, and understand your audience. Create a blog or Medium account.",
    
#     "Journalist": "Strong writing and reporting skills. Build contacts and learn media ethics. Practice interviewing, fact-checking, and multimedia journalism. Intern with local news agencies.",
    
#     "Sales & Marketing Executive": "Good communication, market research, and persuasion are key. Learn CRM tools, lead generation, and social media marketing. Understand consumer psychology.",
    
#     "HR Executive": "Learn recruitment, payroll tools, and HR policies. Understand labor laws, performance appraisals, and employee engagement. Use tools like Zoho People or SAP SuccessFactors.",
    
#     "General Professional / Explore More Options": "Explore internships and try different domains to discover your passion. Take personality tests or career assessments. Network widely and talk to professionals.",
    
#     # Additional Roles
#     "Data Engineer": "Master data pipelines, ETL processes, and tools like Apache Spark, Airflow, and SQL. Get comfortable with big data frameworks like Hadoop and databases like MongoDB and PostgreSQL.",
    
#     "Game Developer": "Learn game engines like Unity or Unreal Engine. Understand C# or C++. Build small games and understand game design principles, graphics, and physics engines.",
    
#     "Blockchain Developer": "Learn about blockchain fundamentals, smart contracts, and platforms like Ethereum or Solana. Get hands-on with Solidity or Rust and explore Web3 technologies.",
    
#     "Digital Marketing Specialist": "Master SEO, PPC, email marketing, and analytics tools. Get certified in Google Ads, HubSpot, or Meta Blueprint. Learn content marketing and social media strategies.",
    
#     "Graphic Designer": "Develop a strong portfolio. Learn Adobe Suite (Photoshop, Illustrator, InDesign). Practice branding, typography, and layout principles. Understand print and digital media.",
    
#     "Environmental Scientist": "Study environmental laws and impact analysis. Get hands-on with GIS, remote sensing, and pollution control methods. Join environmental projects or NGOs.",
    
#     "Event Manager": "Master planning, budgeting, and vendor coordination. Learn project management tools and public relations. Build negotiation and crisis management skills."
# }


# # Streamlit App
# st.title("🎓CareerCompass: Career Path Recommender")

# name = st.text_input("Enter your name (optional):")
# resume_input = st.text_area("Paste your resume or describe your interests, skills, or background:")
# uploaded_file = st.file_uploader("Or upload your resume as a .txt file")

# user_text = ""

# if uploaded_file is not None:
#     try:
#         user_text = uploaded_file.read().decode("utf-8")
#     except UnicodeDecodeError:
#         uploaded_file.seek(0)
#         try:
#             user_text = uploaded_file.read().decode("latin1")
#         except Exception as e:
#             st.error(f"Failed to decode the file. Error: {e}")
#             user_text = ""
# elif resume_input:
#     user_text = resume_input

# if user_text and st.button("Get Details"):
#     st.markdown("---")
#     st.subheader("🔍 Recommendations")

#     recs, sims = recommend_roles(user_text)
#     greeting = f"Hi {name}," if name else "Hi friend,"

#     if not recs:
#         st.write(f"{greeting} we couldn't find a strong match. Please try adding more details.")
#     else:
#         st.write(f"{greeting} based on your profile, we recommend:")
#         for role, score in zip(recs, sims):
#             st.write(f"- **{role}** (similarity score: {score:.2f})")

#         alt_suggestions = suggest_alternatives(recs)
#         if alt_suggestions:
#             st.markdown("---")
#             st.subheader("💡 You might also consider:")
#             for alt in alt_suggestions:
#                 st.write(f"- {alt}")

#         st.markdown("---")
#         st.subheader("📌 Tips for Recommended Roles")
#         for role in recs:
#             tip = role_tips.get(role, "Explore this career path further by connecting with professionals and doing internships.")
#             st.markdown(f"**{role}**: {tip}")
# else:
#     st.info("Please paste your resume or upload a .txt file to get started.")


import streamlit as st
import pandas as pd
import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

# Load SpaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    st.error("Please install the spaCy English model: 'python -m spacy download en_core_web_sm'")
    st.stop()

# Load datasets
@st.cache_data
def load_data():
    try:
        career_data = pd.read_csv("final_extended_career_recommender.csv")
        suggestion_data = pd.read_csv("career_role_suggestions_large_full.csv")
        
        # Combine text fields for vectorization
        career_data['Text'] = (
            career_data['Resume'].fillna('') + ' ' +
            career_data['Interests'].fillna('') + ' ' +
            career_data['Skills'].fillna('')
        )
        
        return career_data, suggestion_data
    except Exception as e:
        st.error(f"Failed to load data files: {e}")
        st.stop()

career_data, suggestion_data = load_data()

# TF-IDF vectorization of dataset
@st.cache_resource
def initialize_vectorizer():
    try:
        vectorizer = TfidfVectorizer(stop_words="english", min_df=2, max_df=0.8)
        career_vectors = vectorizer.fit_transform(career_data['Text'])
        return vectorizer, career_vectors
    except Exception as e:
        st.error(f"Failed to initialize vectorizer: {e}")
        st.stop()

vectorizer, career_vectors = initialize_vectorizer()

# Extract enhanced keywords from text using spaCy
def extract_keywords(text):
    try:
        doc = nlp(text.lower())
        keywords = set()
        
        # Add noun chunks
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) <= 3:  # Avoid long phrases
                keywords.add(chunk.text.strip())
        
        # Add named entities
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PERSON", "GPE", "NORP", "WORK_OF_ART", "PRODUCT", "EVENT", "SKILL"]:
                keywords.add(ent.text.strip())
        
        # Add important verbs and adjectives
        for token in doc:
            if token.pos_ in ["VERB", "ADJ"] and token.lemma_ not in nlp.Defaults.stop_words:
                keywords.add(token.lemma_)
        
        # Add compound nouns
        for token in doc:
            if token.dep_ == "compound":
                keywords.add(f"{token.text} {token.head.text}")
        
        return " ".join(keywords)
    except Exception as e:
        st.error(f"Error in keyword extraction: {e}")
        return ""

# Improved role recommendation with better similarity handling
def recommend_roles(user_input, threshold=0.25, min_threshold=0.15):
    try:
        cleaned_input = extract_keywords(user_input)
        if not cleaned_input:
            return [], []
        
        user_vector = vectorizer.transform([cleaned_input])
        similarities = cosine_similarity(user_vector, career_vectors).flatten()
        
        # Group by career path and get best scores
        role_scores = defaultdict(float)
        for idx, score in enumerate(similarities):
            role = career_data.iloc[idx]["Career_Path"]
            if score > role_scores[role]:
                role_scores[role] = score
        
        # Sort roles by score and apply threshold
        sorted_roles = sorted(role_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Dynamic threshold adjustment
        if not sorted_roles or sorted_roles[0][1] < 0.5:
            threshold = min_threshold
        
        recommended_roles = []
        recommended_scores = []
        
        for role, score in sorted_roles:
            if score >= threshold and len(recommended_roles) < 10:
                recommended_roles.append(role)
                recommended_scores.append(score)
        
        return recommended_roles, recommended_scores
    except Exception as e:
        st.error(f"Error in recommendation: {e}")
        return [], []

# Enhanced alternative suggestions
def suggest_alternatives(main_roles, max_suggestions=10):
    try:
        suggestions = []
        seen = set(main_roles)
        
        for role in main_roles:
            matches = suggestion_data[suggestion_data['Main_Career_Path'] == role]
            for alt in matches['Suggested_Role']:
                if alt not in seen:
                    suggestions.append(alt)
                    seen.add(alt)
                    if len(suggestions) >= max_suggestions:
                        return suggestions
        return suggestions
    except Exception as e:
        st.error(f"Error in suggestion generation: {e}")
        return []

# (Keep your existing role_tips dictionary here...)

# Streamlit App
def main():
    st.title("🎓 CareerCompass: Enhanced Career Path Recommender")
    
    # User input section
    col1, col2 = st.columns([3, 1])
    with col1:
        name = st.text_input("Enter your name (optional):")
    with col2:
        threshold = st.slider("Recommendation Sensitivity", 0.1, 0.5, 0.25, 0.05)
    
    resume_input = st.text_area("Paste your resume or describe your interests, skills, or background:", 
                              height=200,
                              placeholder="E.g.: 'I have a degree in computer science with skills in Python, machine learning, and data analysis. I enjoy solving complex problems and working with large datasets.'")
    
    uploaded_file = st.file_uploader("Or upload your resume as a .txt file", type=["txt"])
    
    user_text = ""
    
    if uploaded_file is not None:
        try:
            user_text = uploaded_file.read().decode("utf-8")
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            try:
                user_text = uploaded_file.read().decode("latin1")
            except Exception as e:
                st.error(f"Failed to decode the file. Error: {e}")
                user_text = ""
    elif resume_input:
        user_text = resume_input
    
    if user_text and st.button("Get Career Recommendations"):
        with st.spinner("Analyzing your profile and finding the best career matches..."):
            st.markdown("---")
            st.subheader("🔍 Career Recommendations")
            
            recs, sims = recommend_roles(user_text, threshold=threshold)
            greeting = f"Hi {name}," if name else "Hi there,"
            
            if not recs:
                st.warning(f"{greeting} we couldn't find strong matches. Try adding more details about your skills, education, and interests.")
                st.info("💡 Tip: Include specific skills, tools you've used, projects you've worked on, and your educational background for better results.")
            else:
                st.write(f"{greeting} here are careers that match your profile:")
                
                # Display recommendations in a nice format
                cols = st.columns(len(recs) if len(recs) <= 5 else 5)
                for i, (role, score) in enumerate(zip(recs, sims)):
                    with cols[i % len(cols)]:
                        st.metric(label=role, value=f"{score:.0%} match")
                
                # Show alternative suggestions
                alt_suggestions = suggest_alternatives(recs)
                if alt_suggestions:
                    st.markdown("---")
                    st.subheader("💡 Related Career Paths to Consider")
                    st.write("You might also explore these related fields:")
                    st.write(", ".join(alt_suggestions))
                
                # Show detailed tips
                st.markdown("---")
                st.subheader("📌 Career Development Tips")
                
                tab1, tab2, tab3 = st.tabs(["Top Recommendations", "All Recommendations", "General Advice"])
                
                with tab1:
                    for role in recs[:3]:
                        tip = role_tips.get(role, "Explore this career path further by connecting with professionals and doing internships.")
                        st.markdown(f"### {role}")
                        st.write(tip)
                
                with tab2:
                    for role in recs:
                        tip = role_tips.get(role, "Explore this career path further by connecting with professionals and doing internships.")
                        with st.expander(role):
                            st.write(tip)
                
                with tab3:
                    st.write("""
                    **General Career Advice:**
                    - Network with professionals in your target field
                    - Build a portfolio of projects demonstrating your skills
                    - Consider certifications relevant to your desired career
                    - Gain practical experience through internships or freelance work
                    - Stay updated with industry trends and technologies
                    """)
    
    # Add some sample inputs for quick testing
    st.markdown("---")
    with st.expander("💡 Not sure what to input? Try these examples"):
        st.write("""
        **Computer Science Graduate:**
        "I have a BS in Computer Science with skills in Python, Java, and SQL. I've worked on machine learning projects using TensorFlow and enjoy data analysis. Looking for roles in tech."
        
        **Business Student:**
        "MBA graduate with finance specialization. Strong analytical skills, Excel modeling experience, and internship at a financial services company. Interested in investment analysis or consulting."
        
        **Career Changer:**
        "5 years experience in retail management looking to transition to HR. Strong people skills, conflict resolution experience, and training in organizational psychology."
        """)

if __name__ == "__main__":
    main()