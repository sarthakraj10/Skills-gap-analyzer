import streamlit as st
import PyPDF2
import docx2txt
import string
import re
import matplotlib.pyplot as plt

# Stop words list
STOP_WORDS = set([
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", 
    "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 
    'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 
    'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 
    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was',
    'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
    'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
    'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
    'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
    'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there',
    'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most',
    'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
    'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've",
    'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
    'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't",
    'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan',
    "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
])

# Skill database
SKILLS_DB = [
    'python', 'java', 'sql', 'excel', 'machine learning', 'data analysis',
    'project management', 'communication', 'leadership', 'problem solving',
    'teamwork', 'time management', 'aws', 'azure', 'docker', 'kubernetes',
    'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'tableau',
    'power bi', 'html', 'css', 'javascript', 'react', 'node.js', 'flask',
    'django', 'git', 'github', 'linux', 'statistics', 'deep learning',
    'natural language processing', 'computer vision', 'agile', 'scrum',
    'c', 'c++', 'c#', 'r', 'go', 'ruby', 'swift', 'typescript', 'matlab',
    'scala', 'perl', 'next.js', 'angular', 'vue.js', 'bootstrap', 'sass',
    'webpack', 'jquery', 'json', 'rest api', 'graphql', 'gcp', 'terraform',
    'jenkins', 'ansible', 'prometheus', 'grafana', 'ci/cd', 'cloudformation',
    'hadoop', 'spark', 'hive', 'pig', 'kafka', 'airflow', 'dbt', 'etl',
    'bigquery', 'snowflake', 'redshift', 'mysql', 'postgresql', 'oracle',
    'mongodb', 'cassandra', 'redis', 'sqlite', 'elasticsearch', 'seaborn',
    'matplotlib', 'xgboost', 'lightgbm', 'catboost', 'nlp', 'ocr', 'cv2',
    'transformers', 'huggingface', 'lookml', 'qlikview', 'superset', 'looker',
    'cognos', 'datarobot', 'jira', 'confluence', 'bitbucket', 'svn', 'vscode',
    'intellij', 'eclipse', 'pycharm', 'sublime text', 'critical thinking',
    'adaptability', 'creativity', 'collaboration', 'emotional intelligence',
    'work ethic', 'interpersonal skills', 'conflict resolution',
    'decision making', 'negotiation', 'api testing', 'postman', 'swagger',
    'unit testing', 'integration testing', 'tdd', 'bdd', 'data wrangling',
    'data cleaning', 'feature engineering', 'model deployment', 'mlops',
    'chatgpt', 'llm', 'generative ai', 'autoencoders', 'gan',
    'diffusion models', 'reinforcement learning', 'self-supervised learning',
    'zero-shot learning', 'few-shot learning', 'shell scripting', 'bash',
    'powershell', 'windows', 'macos', 'ubuntu', 'centos', 'network security',
    'penetration testing', 'vulnerability assessment', 'firewalls',
    'encryption', 'ssl/tls', 'linear algebra', 'calculus', 'probability',
    'information theory', 'optimization', 'graph theory', 'product management',
    'market research', 'a/b testing', 'user research', 'growth hacking', 'seo',
    'sem', 'kpi tracking', 'google analytics', 'mixpanel', 'amplitude',
    'funnel analysis', 'cohort analysis', 'technical writing', 'documentation',
    'content creation', 'blogging', 'copywriting', 'storytelling', 'mentoring',
    'training', 'public speaking', 'presentation skills',
    'instructional design', 'gdpr', 'hipaa', 'compliance', 'risk management',
    'audit', 'fastapi', 'streamlit', 'dash', 'gradio', 'keras', 'openai gym',
    'time series forecasting', 'anomaly detection', 'clustering',
    'dimensionality reduction', 'pca', 'tsne', 'resume parsing',
    'skill matching', 'job recommendation', 'ats optimization'
]

def extract_text(file):
    """Extract text from PDF, DOCX, or TXT"""
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return docx2txt.process(file)
    return file.getvalue().decode("utf-8")

def clean_text(text):
    """Clean and tokenize text"""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    tokens = text.split()
    tokens = [word for word in tokens if word not in STOP_WORDS and len(word) > 2]
    return tokens

def extract_skills(tokens):
    """Extract skills from tokens"""
    text = ' '.join(tokens)
    found_skills = []
    for skill in SKILLS_DB:
        if ' ' not in skill and skill in tokens:
            found_skills.append(skill)
    for skill in SKILLS_DB:
        if ' ' in skill and skill in text:
            found_skills.append(skill)
    return list(set(found_skills))

def plot_skill_comparison(resume_skills, jd_skills):
    """Visualize skill comparison"""
    fig, ax = plt.subplots(figsize=(10, 6))
    all_skills = sorted(set(resume_skills + jd_skills))
    resume_counts = [1 if skill in resume_skills else 0 for skill in all_skills]
    jd_counts = [1 if skill in jd_skills else 0 for skill in all_skills]
    width = 0.35
    x = range(len(all_skills))
    ax.bar([i - width/2 for i in x], resume_counts, width, label='Resume', color='skyblue')
    ax.bar([i + width/2 for i in x], jd_counts, width, label='Job Description', color='salmon')
    ax.set_xlabel('Skills')
    ax.set_ylabel('Presence (1 = Present)')
    ax.set_title('Skill Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(all_skills, rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()
    return fig

# Streamlit UI
st.set_page_config(page_title="Skills Gap Analyzer", layout="wide")
st.title("Skills Gap Analyzer")
st.markdown("Compare resume skills with job description requirements to identify missing skills")

with st.expander("Upload or Paste Content", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Resume Input")
        resume_option = st.radio("Select resume input method:", ('Upload File', 'Paste Text'), key='resume_radio')
        if resume_option == 'Upload File':
            resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=['pdf', 'docx'], key='resume_uploader')
            resume_text = extract_text(resume_file) if resume_file else ""
        else:
            resume_text = st.text_area("Paste Resume Text", height=200, key='resume_text')

    with col2:
        st.subheader("Job Description Input")
        jd_option = st.radio("Select JD input method:", ('Upload File', 'Paste Text'), key='jd_radio')
        if jd_option == 'Upload File':
            jd_file = st.file_uploader("Upload Job Description (PDF or DOCX)", type=['pdf', 'docx'], key='jd_uploader')
            jd_text = extract_text(jd_file) if jd_file else ""
        else:
            jd_text = st.text_area("Paste Job Description Text", height=200, key='jd_text')

if st.button("Analyze Skills Gap", type="primary") and resume_text and jd_text:
    with st.spinner("Analyzing skills..."):
        resume_tokens = clean_text(resume_text)
        jd_tokens = clean_text(jd_text)
        resume_skills = extract_skills(resume_tokens)
        jd_skills = extract_skills(jd_tokens)
        resume_set = set(resume_skills)
        jd_set = set(jd_skills)
        missing_skills = list(jd_set - resume_set)
        matching_count = len(resume_set & jd_set)
        score = round((matching_count / len(jd_set)) * 100, 2) if jd_set else 0

        st.subheader("Analysis Results")
        col1, col2, col3 = st.columns(3)
        col1.metric("Resume Score", f"{score}%", help="Percentage of required skills found in resume")
        col2.metric("Matching Skills", matching_count)
        col3.metric("Missing Skills", len(missing_skills))

        st.subheader("Skill Comparison")
        if resume_skills or jd_skills:
            fig = plot_skill_comparison(resume_skills, jd_skills)
            st.pyplot(fig)
        else:
            st.warning("No skills detected for visualization")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"Resume Skills ({len(resume_skills)})")
            if resume_skills:
                st.write(", ".join(sorted(resume_skills)))
            else:
                st.warning("No skills detected in resume")
        with col2:
            st.subheader(f"Job Description Skills ({len(jd_skills)})")
            if jd_skills:
                st.write(", ".join(sorted(jd_skills)))
            else:
                st.warning("No skills detected in job description")

        if missing_skills:
            st.subheader(f"Missing Skills ({len(missing_skills)})")
            for i, skill in enumerate(sorted(missing_skills), 1):
                st.markdown(f"{i}. **{skill}**")
            st.subheader("Improvement Suggestions")
            st.markdown(f"""
            - **Add these skills to your resume**: {', '.join(missing_skills[:3])}
            - **Highlight transferable skills** related to these requirements
            - **Include projects** that show these skills
            - **Take courses** to build proficiency
            """)
        else:
            st.success("🎉 No missing skills! Your resume meets all job requirements")

        report = f"""Skills Gap Analysis Report
=================================
Resume Score: {score}%
Matching Skills: {matching_count}
Missing Skills: {len(missing_skills)}

===== Resume Skills =====
{', '.join(sorted(resume_skills)) if resume_skills else 'No skills detected'}

===== Required Skills =====
{', '.join(sorted(jd_skills)) if jd_skills else 'No skills detected'}

===== Missing Skills =====
{', '.join(sorted(missing_skills)) if missing_skills else 'No missing skills!'}
"""
        st.download_button("Download Full Report", report, file_name="skills_gap_report.txt", mime="text/plain")
else:
    st.warning("Please provide both resume and job description content")
