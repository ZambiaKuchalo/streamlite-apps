import streamlit as st
import datetime
from dataclasses import dataclass
from typing import List, Dict
import json
import re
from openai import OpenAI
import os

# Page configuration
st.set_page_config(
    page_title="⚖️ Legal Brief Generator Pro",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .document-card {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .legal-section {
        border-left: 4px solid #2a5298;
        padding-left: 1rem;
        margin: 1rem 0;
        background: #f8f9fa;
        border-radius: 0 8px 8px 0;
    }
    .citation-box {
        background: #e9ecef;
        border-radius: 5px;
        padding: 0.5rem;
        font-family: monospace;
        font-size: 0.9em;
        margin: 0.5rem 0;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeeba;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@dataclass
class CaseDetails:
    case_name: str
    court: str
    case_number: str
    date: str
    parties: Dict[str, str]
    facts: str
    legal_issues: List[str]
    jurisdiction: str

@dataclass
class LegalArgument:
    heading: str
    legal_principle: str
    supporting_cases: List[str]
    analysis: str
    conclusion: str

class LegalBriefGenerator:
    def __init__(self):
        self.citation_formats = {
            "Bluebook": "{case_name}, {volume} {reporter} {page} ({court} {year})",
            "ALWD": "{case_name}, {volume} {reporter} {page} ({court} {year})",
            "APA": "{case_name} ({year}). {volume} {reporter} {page} ({court})"
        }
        
        self.document_templates = {
            "Motion to Dismiss": self.generate_motion_to_dismiss,
            "Summary Judgment Brief": self.generate_summary_judgment,
            "Appeals Brief": self.generate_appeals_brief,
            "Contract Analysis": self.generate_contract_analysis,
            "Case Summary": self.generate_case_summary,
            "Legal Memorandum": self.generate_legal_memo
        }
        
        # Initialize OpenAI client for AI features
        self.client = self._initialize_ai_client()
    
    def _initialize_ai_client(self):
        """Initialize OpenAI client with OpenRouter configuration"""
        try:
            api_key = os.getenv("OPENROUTER_API_KEY", "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")
            if not api_key and "openrouter_api_key" in st.session_state:
                api_key = st.session_state.openrouter_api_key
            
            if api_key:
                return OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=api_key,
                )
            return None
        except Exception as e:
            st.warning(f"AI features unavailable: {str(e)}")
            return None
    
    def get_ai_suggestions(self, case_facts: str, legal_issues: List[str]) -> List[str]:
        """Get AI-powered legal argument suggestions"""
        if not self.client:
            return ["Please configure OpenRouter API key to use AI features"]
        
        try:
            prompt = f"""
            As an experienced legal analyst, provide strategic argument suggestions for the following case:
            
            Facts: {case_facts}
            Legal Issues: {', '.join(legal_issues)}
            
            Provide 4-5 specific, actionable legal argument suggestions that could strengthen the case.
            Format each suggestion as a bullet point.
            """
            
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://legal-brief-generator.streamlit.app",
                    "X-Title": "Legal Brief Generator Pro",
                },
                model="deepseek/deepseek-r1:free",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert legal analyst providing strategic case suggestions. Be precise and professional."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            response = completion.choices[0].message.content
            # Parse suggestions into list
            suggestions = [line.strip().lstrip('•-* ') for line in response.split('\n') if line.strip()]
            return suggestions[:5]  # Return max 5 suggestions
            
        except Exception as e:
            return [f"Error generating suggestions: {str(e)}"]
    
    def find_relevant_precedents(self, legal_issues: List[str], jurisdiction: str = "") -> List[str]:
        """Find relevant case precedents using AI"""
        if not self.client:
            return ["Please configure OpenRouter API key to use AI features"]
        
        try:
            prompt = f"""
            Find relevant case precedents for the following legal issues in {jurisdiction or 'general'} jurisdiction:
            
            Legal Issues: {', '.join(legal_issues)}
            
            Provide 3-4 landmark cases that would be most relevant, including:
            - Case name and year
            - Brief relevance explanation
            - Key legal principle established
            
            Format as: Case Name (Year) - Brief explanation of relevance
            """
            
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://legal-brief-generator.streamlit.app",
                    "X-Title": "Legal Brief Generator Pro",
                },
                model="deepseek/deepseek-r1:free",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a legal research expert. Provide accurate, relevant case precedents."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=600
            )
            
            response = completion.choices[0].message.content
            precedents = [line.strip() for line in response.split('\n') if line.strip() and '-' in line]
            return precedents[:4]  # Return max 4 precedents
            
        except Exception as e:
            return [f"Error finding precedents: {str(e)}"]
    
    def enhance_legal_argument(self, argument_topic: str, case_facts: str) -> str:
        """Enhance a legal argument using AI analysis"""
        if not self.client:
            return "Please configure OpenRouter API key to use AI features"
        
        try:
            prompt = f"""
            Enhance the following legal argument with detailed analysis:
            
            Argument Topic: {argument_topic}
            Case Facts: {case_facts}
            
            Provide a structured legal argument including:
            1. Legal standard/rule
            2. Application to facts
            3. Potential counterarguments
            4. Conclusion
            
            Keep it professional and legally sound.
            """
            
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://legal-brief-generator.streamlit.app",
                    "X-Title": "Legal Brief Generator Pro",
                },
                model="deepseek/deepseek-r1:free",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert legal writer. Provide detailed, well-structured legal arguments."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.4,
                max_tokens=800
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            # Handle error properly instead of leaving the block empty
            return f"⚠️ An error occurred while generating the legal argument: {str(e)}"
            
    def generate_ai_legal_analysis(self, legal_issue: str, case_facts: str, document_type: str) -> str:
        """Generate detailed legal analysis for specific issues"""
        if not self.client:
            return "[AI ANALYSIS UNAVAILABLE - Please configure OpenRouter API key]"
        
        try:
            prompt = f"""
            As an expert legal analyst, provide a comprehensive legal analysis for a {document_type}:
            
            Legal Issue: {legal_issue}
            Case Facts: {case_facts}
            Document Type: {document_type}
            
            Provide detailed analysis including:
            1. Applicable legal standard/rule of law
            2. Relevant case law and statutes
            3. Application of law to the specific facts
            4. Analysis of strengths and weaknesses
            5. Conclusion and recommendations
            
            Write in professional legal style appropriate for court documents.
            Include proper legal reasoning and cite general legal principles.
            """
            
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://legal-brief-generator.streamlit.app",
                    "X-Title": "Legal Brief Generator Pro",
                },
                model="deepseek/deepseek-r1:free",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert legal analyst and writer specializing in litigation and legal brief preparation. Provide thorough, professional legal analysis suitable for court documents."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            return f"[AI ANALYSIS ERROR: {str(e)}]"
    
    def generate_contract_legal_analysis(self, contract_issue: str, facts: str) -> str:
        """Generate specialized contract law analysis"""
        if not self.client:
            return "[CONTRACT ANALYSIS UNAVAILABLE - Please configure OpenRouter API key]"
        
        try:
            prompt = f"""
            Provide expert contract law analysis for the following issue:
            
            Contract Issue: {contract_issue}
            Facts: {facts}
            
            Analyze according to contract law principles:
            1. Formation elements (offer, acceptance, consideration)
            2. Performance and breach analysis
            3. Remedies and damages assessment
            4. Applicable defenses
            5. Risk assessment and recommendations
            
            Include references to general contract law principles and common law rules.
            """
            
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://legal-brief-generator.streamlit.app",
                    "X-Title": "Legal Brief Generator Pro",
                },
                model="deepseek/deepseek-r1:free",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a contract law specialist providing detailed legal analysis for contract disputes and issues."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            return f"[CONTRACT ANALYSIS ERROR: {str(e)}]"
    
    def format_citation(self, case_info: dict, style: str = "Bluebook") -> str:
        template = self.citation_formats.get(style, self.citation_formats["Bluebook"])
        return template.format(**case_info)
    
    def generate_case_summary(self, case_details: CaseDetails) -> str:
        return f"""
# CASE SUMMARY

**{case_details.case_name}**
**{case_details.court}**
**Case No. {case_details.case_number}**
**Decided: {case_details.date}**

## PARTIES
- **Plaintiff/Petitioner:** {case_details.parties.get('plaintiff', 'N/A')}
- **Defendant/Respondent:** {case_details.parties.get('defendant', 'N/A')}

## FACTUAL BACKGROUND
{case_details.facts}

## LEGAL ISSUES PRESENTED
{chr(10).join([f"{i+1}. {issue}" for i, issue in enumerate(case_details.legal_issues)])}

## JURISDICTION
This matter is properly before the {case_details.court} under {case_details.jurisdiction}.

---
*Generated on {datetime.datetime.now().strftime("%B %d, %Y")} by Legal Brief Generator Pro*
"""

    def generate_motion_to_dismiss(self, case_details: CaseDetails) -> str:
        # Generate AI analysis for each legal issue
        ai_analyses = []
        for i, issue in enumerate(case_details.legal_issues):
            analysis = self.generate_ai_legal_analysis(issue, case_details.facts, "Motion to Dismiss")
            ai_analyses.append(f"### Issue {i+1}: {issue}\n\n{analysis}")
        
        arguments_section = "\n\n".join(ai_analyses) if ai_analyses else "### Legal Arguments\n[DETAILED LEGAL ANALYSIS REQUIRED]"
        
        return f"""
# MOTION TO DISMISS

**IN THE {case_details.court.upper()}**

**{case_details.case_name}**
**Case No. {case_details.case_number}**

## MOTION TO DISMISS FOR FAILURE TO STATE A CLAIM

TO THE HONORABLE COURT:

NOW COMES {case_details.parties.get('defendant', '[DEFENDANT]')}, by and through undersigned counsel, and respectfully moves this Court to dismiss the Complaint filed by {case_details.parties.get('plaintiff', '[PLAINTIFF]')} for failure to state a claim upon which relief can be granted, pursuant to Rule 12(b)(6).

## FACTUAL BACKGROUND
{case_details.facts}

## LEGAL STANDARD
A motion to dismiss for failure to state a claim should be granted when it appears beyond doubt that the plaintiff can prove no set of facts in support of his claim which would entitle him to relief. The court must accept all factual allegations as true and draw all reasonable inferences in favor of the plaintiff.

## ARGUMENT

{arguments_section}

## CONCLUSION
For the foregoing reasons, Defendant respectfully requests that this Court grant its Motion to Dismiss with prejudice.

Respectfully submitted,
[ATTORNEY SIGNATURE BLOCK]

---
*Generated on {datetime.datetime.now().strftime("%B %d, %Y")} with AI Legal Analysis*
"""

    def generate_appeals_brief(self, case_details: CaseDetails) -> str:
        # Generate AI analysis for each legal issue
        ai_analyses = []
        for i, issue in enumerate(case_details.legal_issues):
            analysis = self.generate_ai_legal_analysis(issue, case_details.facts, "Appellate Brief")
            ai_analyses.append(f"### {chr(65+i)}. {issue}\n\n{analysis}")
        
        arguments_section = "\n\n".join(ai_analyses) if ai_analyses else "### Legal Arguments\n[DETAILED APPELLATE ANALYSIS REQUIRED]"
        
        return f"""
# APPELLATE BRIEF

**IN THE {case_details.court.upper()}**

**{case_details.case_name}**
**Appeal No. {case_details.case_number}**

## TABLE OF CONTENTS
1. Statement of the Case
2. Statement of Facts
3. Issues Presented
4. Summary of Argument
5. Argument
6. Conclusion

## STATEMENT OF THE CASE
This appeal arises from [NATURE OF PROCEEDING] in the [LOWER COURT]. The [APPELLANT/APPELLEE] seeks review of [DECISION BEING APPEALED] under applicable appellate standards.

## STATEMENT OF FACTS
{case_details.facts}

## ISSUES PRESENTED FOR REVIEW
{chr(10).join([f"{i+1}. {issue}" for i, issue in enumerate(case_details.legal_issues)])}

## SUMMARY OF ARGUMENT
This appeal presents fundamental questions of law that require reversal of the lower court's decision. The arguments presented demonstrate clear legal error requiring appellate intervention.

## ARGUMENT

{arguments_section}

## CONCLUSION
For the foregoing reasons, [APPELLANT/APPELLEE] respectfully requests that this Court reverse the lower court's decision and grant the relief requested.

Respectfully submitted,
[ATTORNEY SIGNATURE BLOCK]

---
*Generated on {datetime.datetime.now().strftime("%B %d, %Y")} with AI Legal Analysis*
"""

    def generate_summary_judgment(self, case_details: CaseDetails) -> str:
        # Generate AI analysis for each legal issue
        ai_analyses = []
        for i, issue in enumerate(case_details.legal_issues):
            analysis = self.generate_ai_legal_analysis(issue, case_details.facts, "Summary Judgment Motion")
            ai_analyses.append(f"### {i+1}. {issue}\n\n{analysis}")
        
        arguments_section = "\n\n".join(ai_analyses) if ai_analyses else "### Legal Arguments\n[DETAILED LEGAL ANALYSIS REQUIRED]"
        
        return f"""
# MOTION FOR SUMMARY JUDGMENT

**{case_details.case_name}**
**Case No. {case_details.case_number}**

## MOTION FOR SUMMARY JUDGMENT

TO THE HONORABLE COURT:

{case_details.parties.get('plaintiff', '[MOVANT]')} hereby moves for summary judgment on all claims pursuant to Rule 56, Federal Rules of Civil Procedure.

## STATEMENT OF UNDISPUTED MATERIAL FACTS
{case_details.facts}

## LEGAL STANDARD
Summary judgment is appropriate when there is no genuine dispute as to any material fact and the movant is entitled to judgment as a matter of law. Fed. R. Civ. P. 56(a). The court must view the evidence in the light most favorable to the non-moving party.

## ARGUMENT

{arguments_section}

## CONCLUSION
No genuine issue of material fact exists, and movant is entitled to judgment as a matter of law on all claims presented.

Respectfully submitted,
[ATTORNEY SIGNATURE BLOCK]

---
*Generated on {datetime.datetime.now().strftime("%B %d, %Y")} with AI Legal Analysis*
"""

    def generate_contract_analysis(self, case_details: CaseDetails) -> str:
        # Generate specialized contract analysis for each issue
        ai_analyses = []
        for i, issue in enumerate(case_details.legal_issues):
            analysis = self.generate_contract_legal_analysis(issue, case_details.facts)
            ai_analyses.append(f"### {i+1}. {issue}\n\n{analysis}")
        
        issues_section = "\n\n".join(ai_analyses) if ai_analyses else "### Contract Issues\n[DETAILED CONTRACT ANALYSIS REQUIRED]"
        
        return f"""
# CONTRACT ANALYSIS MEMORANDUM

**RE: {case_details.case_name}**
**Date: {datetime.datetime.now().strftime("%B %d, %Y")}**

## EXECUTIVE SUMMARY
This memorandum analyzes the contractual issues present in {case_details.case_name}, examining formation, performance, breach, and remedies under applicable contract law principles.

## FACTUAL BACKGROUND
{case_details.facts}

## CONTRACT FORMATION ANALYSIS
### Offer and Acceptance
The analysis of offer and acceptance requires examination of the communications between parties to determine whether a valid contract was formed according to established legal principles.

### Consideration
Valid consideration requires a bargained-for exchange of value between the contracting parties, analyzed under both benefit-detriment and bargain theories.

### Capacity and Legality
Assessment of parties' legal capacity to contract and the legality of the subject matter under applicable law.

## LEGAL ISSUES IDENTIFIED

{issues_section}

## RISK ASSESSMENT
- **High Risk:** Issues requiring immediate attention and potential litigation preparation
- **Medium Risk:** Issues requiring monitoring and potential contractual modifications  
- **Low Risk:** Issues of minimal legal concern requiring standard contract management

## RECOMMENDATIONS
Based on the comprehensive analysis above, specific strategic and legal recommendations will be provided for each identified issue.

---
*This analysis includes AI-powered legal research and is based on facts provided and applicable law as of {datetime.datetime.now().strftime("%B %d, %Y")}*
"""

    def generate_legal_memo(self, case_details: CaseDetails) -> str:
        # Generate AI analysis for each legal issue
        ai_analyses = []
        for i, issue in enumerate(case_details.legal_issues):
            analysis = self.generate_ai_legal_analysis(issue, case_details.facts, "Legal Memorandum")
            ai_analyses.append(f"### {i+1}. {issue}\n\n{analysis}")
        
        discussion_section = "\n\n".join(ai_analyses) if ai_analyses else "### Legal Discussion\n[COMPREHENSIVE LEGAL ANALYSIS REQUIRED]"
        
        return f"""
# LEGAL MEMORANDUM

**TO:** [CLIENT/RECIPIENT]
**FROM:** [ATTORNEY NAME]
**DATE:** {datetime.datetime.now().strftime("%B %d, %Y")}
**RE:** {case_details.case_name} - Comprehensive Legal Analysis

## QUESTION PRESENTED
{chr(10).join([f"- {issue}" for issue in case_details.legal_issues])}

## BRIEF ANSWER
Based on the comprehensive analysis below, the legal issues present both opportunities and challenges that require careful strategic consideration and expert legal guidance.

## FACTS
{case_details.facts}

## DISCUSSION

{discussion_section}

## CONCLUSION
Based on the foregoing comprehensive analysis, the legal issues require immediate attention and strategic planning. Detailed recommendations and next steps should be discussed to ensure optimal legal outcomes.

---
*This memorandum is protected by attorney-client privilege and includes AI-enhanced legal analysis*
"""

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>⚖️ Legal Brief Generator Pro</h1>
        <p>Professional Legal Document Creation & Case Analysis Tool</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize generator
    generator = LegalBriefGenerator()
    
    # Sidebar for document type selection
    st.sidebar.header("📋 Document Configuration")
    
    # API Key configuration
    #st.sidebar.header("🔑 AI Configuration")
    # api_key_input = st.sidebar.text_input(
    #     "OpenRouter API Key:",
    #     type="password",
    #     help="Enter your OpenRouter API key for AI features",
    #     key="openrouter_api_key"
    # )
    
    # if api_key_input:
    #     st.sidebar.success("✅ AI features enabled")
    # else:
    #     st.sidebar.info("💡 Add API key to enable AI features")
    
    document_type = st.sidebar.selectbox(
        "Select Document Type:",
        list(generator.document_templates.keys()),
        help="Choose the type of legal document to generate"
    )
    
    citation_style = st.sidebar.selectbox(
        "Citation Style:",
        ["Bluebook", "ALWD", "APA"],
        help="Select preferred citation format"
    )
    
    # Creative features sidebar
    st.sidebar.header("🎨 Creative Features")
    
    use_ai_suggestions = st.sidebar.checkbox(
        "AI Legal Argument Suggestions",
        help="Get AI-powered suggestions for legal arguments"
    )
    
    include_precedent_finder = st.sidebar.checkbox(
        "Precedent Case Finder",
        help="Find relevant case precedents"
    )
    
    legal_research_assistant = st.sidebar.checkbox(
        "Research Assistant Mode",
        help="Enhanced research capabilities"
    )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Case Information")
        
        # Case details form
        case_name = st.text_input("Case Name:", placeholder="Smith v. Jones")
        
        col_court, col_case_num = st.columns(2)
        with col_court:
            court = st.text_input("Court:", placeholder="Superior Court of California")
        with col_case_num:
            case_number = st.text_input("Case Number:", placeholder="CV-2024-001234")
        
        # Parties section
        st.subheader("👥 Parties")
        col_plaintiff, col_defendant = st.columns(2)
        with col_plaintiff:
            plaintiff = st.text_input("Plaintiff/Petitioner:")
        with col_defendant:
            defendant = st.text_input("Defendant/Respondent:")
        
        # Facts section
        st.subheader("📋 Factual Background")
        facts = st.text_area(
            "Enter the relevant facts:",
            height=150,
            placeholder="Describe the factual background of the case..."
        )
        
        # Legal issues
        st.subheader("⚖️ Legal Issues")
        legal_issues = st.text_area(
            "Enter legal issues (one per line):",
            height=100,
            placeholder="Issue 1: Whether the contract was validly formed\nIssue 2: Whether damages are recoverable"
        )
        
        jurisdiction = st.text_input(
            "Jurisdiction/Legal Basis:",
            placeholder="28 U.S.C. § 1331 (federal question jurisdiction)"
        )
    
    with col2:
        st.header("🔧 Tools & Features")
        
        # Citation generator
        st.subheader("📚 Citation Generator")
        with st.expander("Generate Citation"):
            st.text_input("Case Name:", key="cite_case")
            col_vol, col_rep = st.columns(2)
            with col_vol:
                st.text_input("Volume:", key="cite_vol")
            with col_rep:
                st.text_input("Reporter:", key="cite_rep")
            col_page, col_year = st.columns(2)
            with col_page:
                st.text_input("Page:", key="cite_page")
            with col_year:
                st.text_input("Year:", key="cite_year")
            st.text_input("Court:", key="cite_court")
            
            if st.button("Generate Citation"):
                case_info = {
                    "case_name": st.session_state.get("cite_case", ""),
                    "volume": st.session_state.get("cite_vol", ""),
                    "reporter": st.session_state.get("cite_rep", ""),
                    "page": st.session_state.get("cite_page", ""),
                    "court": st.session_state.get("cite_court", ""),
                    "year": st.session_state.get("cite_year", "")
                }
                citation = generator.format_citation(case_info, citation_style)
                st.markdown(f'<div class="citation-box">{citation}</div>', unsafe_allow_html=True)
        
        # Legal research assistant
        if legal_research_assistant:
            st.subheader("🔍 Research Assistant")
            research_query = st.text_input("Research Query:", placeholder="contract formation elements")
            if st.button("Research"):
                st.info("Research feature would integrate with legal databases (Westlaw, Lexis, etc.)")
        
        # AI suggestions
        if use_ai_suggestions:
            st.subheader("🤖 AI Argument Suggestions")
            if st.button("Get AI Suggestions"):
                if facts and legal_issues:
                    issues_list = [issue.strip() for issue in legal_issues.split('\n') if issue.strip()]
                    with st.spinner("Generating AI suggestions..."):
                        suggestions = generator.get_ai_suggestions(facts, issues_list)
                        for i, suggestion in enumerate(suggestions, 1):
                            st.write(f"💡 **{i}.** {suggestion}")
                else:
                    st.warning("Please enter case facts and legal issues first")
        
        # Precedent finder
        if include_precedent_finder:
            st.subheader("📖 AI Precedent Finder")
            if st.button("Find Relevant Precedents"):
                if legal_issues:
                    issues_list = [issue.strip() for issue in legal_issues.split('\n') if issue.strip()]
                    with st.spinner("Finding relevant precedents..."):
                        precedents = generator.find_relevant_precedents(issues_list, jurisdiction)
                        for precedent in precedents:
                            st.write(f"📚 {precedent}")
                else:
                    st.warning("Please enter legal issues first")
        
        # Legal argument enhancer
        st.subheader("✨ AI Argument Enhancer")
        with st.expander("Enhance Legal Arguments"):
            argument_topic = st.text_input("Argument Topic:", placeholder="Contract formation defense")
            if st.button("Enhance Argument") and argument_topic and facts:
                with st.spinner("Enhancing argument..."):
                    enhanced_arg = generator.enhance_legal_argument(argument_topic, facts)
                    st.markdown("**Enhanced Argument:**")
                    st.write(enhanced_arg)
    
    # Generate document button
    st.markdown("---")
    col_gen1, col_gen2, col_gen3 = st.columns([1, 2, 1])
    
    with col_gen2:
        if st.button("🚀 Generate Legal Document", type="primary", use_container_width=True):
            if case_name and facts and legal_issues:
                # Create case details object
                issues_list = [issue.strip() for issue in legal_issues.split('\n') if issue.strip()]
                parties = {"plaintiff": plaintiff, "defendant": defendant}
                
                case_details = CaseDetails(
                    case_name=case_name,
                    court=court,
                    case_number=case_number,
                    date=datetime.datetime.now().strftime("%B %d, %Y"),
                    parties=parties,
                    facts=facts,
                    legal_issues=issues_list,
                    jurisdiction=jurisdiction
                )
                
                # Generate document
                generator_func = generator.document_templates[document_type]
                
                # Show progress for AI analysis
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("🤖 Generating AI legal analysis...")
                progress_bar.progress(25)
                
                document = generator_func(case_details)
                
                progress_bar.progress(100)
                status_text.text("✅ Document generation complete!")
                
                # Clear progress indicators after a short delay
                import time
                time.sleep(1)
                progress_bar.empty()
                status_text.empty()
                
                # Display success message
                st.markdown("""
                <div class="success-box">
                    ✅ <strong>Document Generated Successfully!</strong><br>
                    Your legal document has been created based on the provided information.
                </div>
                """, unsafe_allow_html=True)
                
                # Display generated document
                st.markdown("## 📄 Generated Document")
                st.markdown('<div class="document-card">', unsafe_allow_html=True)
                st.markdown(document)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Download button
                st.download_button(
                    label="📥 Download Document",
                    data=document,
                    file_name=f"{document_type.replace(' ', '_')}_{case_name.replace(' ', '_')}.md",
                    mime="text/markdown"
                )
                
            else:
                st.markdown("""
                <div class="warning-box">
                    ⚠️ <strong>Missing Required Information</strong><br>
                    Please fill in at least the case name, facts, and legal issues to generate a document.
                </div>
                """, unsafe_allow_html=True)
    
    # Footer with disclaimer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; font-size: 0.9em; margin-top: 2rem;">
        <p><strong>⚠️ LEGAL DISCLAIMER:</strong> This tool generates template documents for informational purposes only. 
        All generated content should be reviewed by qualified legal counsel before use. 
        This software does not provide legal advice and should not be relied upon for legal decisions.</p>
        <p>© 2024 Legal Brief Generator Pro | Attorney Work Product - Confidential</p>
        <p><strong>Developed by Daniel Kasonde and Kateule Kasonde</strong></p>
        <p style="font-size: 0.8em; margin-top: 1rem;">
            🤖 Powered by OpenRouter AI | 📚 Professional Legal Templates | ⚖️ Ethics Compliant
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()