import os
import streamlit as st
from openai import OpenAI
import time
import re

# Page configuration
st.set_page_config(
    page_title="Social Media Manager",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY", "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")
    )

client = get_openai_client()

# Platform specifications
PLATFORM_SPECS = {
    "twitter": {
        "name": "Twitter/X",
        "icon": "🐦",
        "char_limit": 280,
        "hashtag_limit": 2,
        "optimal_hashtags": "1-2",
        "best_times": "9-10 AM, 12-1 PM, 5-6 PM",
        "tone": "Conversational, witty, concise"
    },
    "linkedin": {
        "name": "LinkedIn",
        "icon": "💼",
        "char_limit": 3000,
        "hashtag_limit": 5,
        "optimal_hashtags": "3-5",
        "best_times": "8-10 AM, 12 PM, 5-6 PM",
        "tone": "Professional, informative, thought-leadership"
    },
    "instagram": {
        "name": "Instagram",
        "icon": "📸",
        "char_limit": 2200,
        "hashtag_limit": 30,
        "optimal_hashtags": "20-30",
        "best_times": "11 AM-1 PM, 5-7 PM",
        "tone": "Visual, engaging, lifestyle-focused"
    },
    "facebook": {
        "name": "Facebook",
        "icon": "👥",
        "char_limit": 63206,
        "hashtag_limit": 5,
        "optimal_hashtags": "1-2",
        "best_times": "9 AM, 1-3 PM",
        "tone": "Friendly, community-focused, conversational"
    },
    "whatsapp": {
        "name": "WhatsApp Status",
        "icon": "💬",
        "char_limit": 700,
        "hashtag_limit": 3,
        "optimal_hashtags": "0-3",
        "best_times": "7-9 PM, 10-11 PM",
        "tone": "Personal, casual, direct"
    }
}

def get_prompt_for_platform(platform, content_type, topic, additional_params=None):
    platform_info = PLATFORM_SPECS[platform]
    
    base_prompts = {
        "create_post": f"""Create an engaging {platform_info['name']} post about: {topic}

Platform Guidelines:
- Character limit: {platform_info['char_limit']} characters
- Tone: {platform_info['tone']}
- Optimal hashtags: {platform_info['optimal_hashtags']}
- Include relevant hashtags (max {platform_info['hashtag_limit']})

Requirements:
- Stay within character limits
- Use platform-appropriate tone and style
- Include call-to-action if appropriate
- Add relevant emojis where suitable
- Generate hashtags that are trending and relevant

Topic: {topic}""",
        
        "optimize_post": f"""Optimize this existing post for {platform_info['name']}:

Original post: {topic}

Platform Guidelines:
- Character limit: {platform_info['char_limit']} characters  
- Tone: {platform_info['tone']}
- Optimal hashtags: {platform_info['optimal_hashtags']}

Requirements:
- Adapt tone and style for {platform_info['name']}
- Stay within character limits
- Add platform-appropriate hashtags
- Include engaging elements (emojis, call-to-action)
- Maintain original message intent""",
        
        "hashtag_research": f"""Generate trending and relevant hashtags for {platform_info['name']} about: {topic}

Requirements:
- Generate {platform_info['optimal_hashtags']} hashtags
- Mix of popular and niche hashtags
- Include branded hashtags if applicable
- Ensure hashtags are currently trending
- Provide hashtag performance tips

Topic: {topic}""",
        
        "content_calendar": f"""Create a 7-day {platform_info['name']} content calendar for: {topic}

Requirements:
- 7 different post ideas
- Vary content types (educational, engaging, promotional)
- Include optimal posting times: {platform_info['best_times']}
- Each post should follow platform guidelines
- Include hashtags and engagement strategies

Topic/Theme: {topic}""",
        
        "competitor_analysis": f"""Analyze successful {platform_info['name']} posts in this niche: {topic}

Requirements:
- Identify trending content patterns
- Suggest content strategies
- Recommend hashtag strategies
- Analyze engagement tactics
- Provide actionable insights

Niche: {topic}"""
    }
    
    return base_prompts.get(content_type, f"Create content for {platform_info['name']} about: {topic}")

def generate_content(platform, content_type, topic, additional_params=None):
    """Generate social media content using OpenAI API"""
    if not topic.strip():
        return "Please enter a topic or content to process."
    
    try:
        prompt = get_prompt_for_platform(platform, content_type, topic, additional_params)
        
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://social-media-manager.streamlit.app",
                "X-Title": "Social Media Manager by Daniel Kasonde",
            },
            model="deepseek/deepseek-r1:free",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a social media expert specializing in creating engaging content for different platforms. Focus on platform-specific best practices, optimal character counts, and trending hashtag strategies."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.8,
            max_tokens=2000
        )
        
        return completion.choices[0].message.content
    
    except Exception as e:
        return f"Error generating content: {str(e)}"

def count_characters(text):
    """Count characters excluding hashtags for display"""
    # Remove hashtags for character count (they're often counted separately)
    text_without_hashtags = re.sub(r'#\w+', '', text)
    return len(text_without_hashtags.strip())

def extract_hashtags(text):
    """Extract hashtags from text"""
    hashtags = re.findall(r'#\w+', text)
    return hashtags

# Initialize session state
if 'selected_platform' not in st.session_state:
    st.session_state.selected_platform = "twitter"
if 'selected_content_type' not in st.session_state:
    st.session_state.selected_content_type = "create_post"

# Sidebar
st.sidebar.title("📱 Social Media Manager")
st.sidebar.markdown("*Developed by Daniel Kasonde*")
st.sidebar.markdown("---")

# Platform selection
st.sidebar.markdown("### 🎯 Select Platform")
for platform_key, platform_info in PLATFORM_SPECS.items():
    if st.sidebar.button(
        f"{platform_info['icon']} {platform_info['name']}", 
        key=f"platform_{platform_key}",
        use_container_width=True
    ):
        st.session_state.selected_platform = platform_key
        # Clear previous result when platform changes
        if 'last_result' in st.session_state:
            del st.session_state.last_result

# Content type selection
st.sidebar.markdown("### ✨ Content Type")
content_types = {
    "create_post": "📝 Create New Post",
    "optimize_post": "🔧 Optimize Existing Post", 
    "hashtag_research": "🏷️ Hashtag Research",
    "content_calendar": "📅 Content Calendar",
    "competitor_analysis": "🔍 Competitor Analysis"
}

for content_key, content_name in content_types.items():
    if st.sidebar.button(content_name, key=f"content_{content_key}", use_container_width=True):
        st.session_state.selected_content_type = content_key
        # Clear previous result when content type changes
        if 'last_result' in st.session_state:
            del st.session_state.last_result

# Platform info display
current_platform = PLATFORM_SPECS[st.session_state.selected_platform]
st.sidebar.markdown("### 📊 Platform Info")
st.sidebar.info(f"""
**{current_platform['icon']} {current_platform['name']}**
- **Character Limit**: {current_platform['char_limit']:,}
- **Optimal Hashtags**: {current_platform['optimal_hashtags']}
- **Best Times**: {current_platform['best_times']}
- **Tone**: {current_platform['tone']}
""")

# Main interface
st.title("📱 Social Media Manager")
st.markdown("Create optimized content for different social media platforms with AI-powered insights.")

# Current selection display
current_content_type = content_types[st.session_state.selected_content_type]
st.subheader(f"Platform: {current_platform['icon']} {current_platform['name']}")
st.subheader(f"Task: {current_content_type}")

# Add visual indicators
col_info1, col_info2 = st.columns(2)
with col_info1:
    st.info(f"🎯 **Current Platform:** {current_platform['name']}")
with col_info2:
    st.info(f"✨ **Current Task:** {current_content_type.replace('📝 ', '').replace('🔧 ', '').replace('🏷️ ', '').replace('📅 ', '').replace('🔍 ', '')}")

# Input and output area
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📝 Input")
    
    # Different input prompts based on content type
    if st.session_state.selected_content_type == "create_post":
        input_placeholder = "Enter your topic, product, or message (e.g., 'Launching new fitness app', 'Monday motivation', 'Coffee shop grand opening')"
        input_label = "Topic or Message:"
    elif st.session_state.selected_content_type == "optimize_post":
        input_placeholder = "Paste your existing post content that you want to optimize for this platform"
        input_label = "Existing Post Content:"
    elif st.session_state.selected_content_type == "hashtag_research":
        input_placeholder = "Enter your niche or topic (e.g., 'digital marketing', 'sustainable fashion', 'food blogging')"
        input_label = "Niche or Topic:"
    elif st.session_state.selected_content_type == "content_calendar":
        input_placeholder = "Enter your brand, theme, or campaign (e.g., 'eco-friendly lifestyle brand', 'tech startup', 'local restaurant')"
        input_label = "Brand or Theme:"
    else:  # competitor_analysis
        input_placeholder = "Enter your industry or niche (e.g., 'SaaS companies', 'fashion brands', 'fitness influencers')"
        input_label = "Industry or Niche:"
    
    input_text = st.text_area(
        input_label,
        height=300,
        placeholder=input_placeholder,
        key="input_area"
    )
    
    # Generate button
    generate_button = st.button("🚀 Generate Content", type="primary", use_container_width=True)
    
    # Input statistics
    if input_text:
        st.caption(f"Characters: {len(input_text)} | Words: {len(input_text.split())}")

with col2:
    st.markdown("### 📤 Generated Content")
    
    # Process content when button is clicked
    if generate_button and input_text.strip():
        with st.spinner(f"Generating {current_platform['name']} content..."):
            result = generate_content(
                st.session_state.selected_platform, 
                st.session_state.selected_content_type, 
                input_text
            )
            st.session_state.last_result = result
    
    # Display result
    if hasattr(st.session_state, 'last_result'):
        output_container = st.container()
        with output_container:
            result_text = st.text_area(
                "Generated Content:",
                value=st.session_state.last_result,
                height=300,
                key="output_area"
            )
            
            # Content analysis
            if st.session_state.last_result:
                char_count = len(st.session_state.last_result)
                hashtags = extract_hashtags(st.session_state.last_result)
                
                col_stats1, col_stats2, col_stats3 = st.columns(3)
                with col_stats1:
                    color = "green" if char_count <= current_platform['char_limit'] else "red"
                    st.metric("Characters", f"{char_count:,}", 
                             delta=f"Limit: {current_platform['char_limit']:,}")
                    
                with col_stats2:
                    st.metric("Hashtags", len(hashtags))
                    
                with col_stats3:
                    words = len(st.session_state.last_result.split())
                    st.metric("Words", words)
                
                # Character limit warning
                if char_count > current_platform['char_limit']:
                    st.error(f"⚠️ Content exceeds {current_platform['name']} character limit by {char_count - current_platform['char_limit']} characters!")
                else:
                    st.success("✅ Content fits within platform limits!")
                
                # Hashtag display
                if hashtags:
                    st.markdown("**Hashtags found:**")
                    hashtag_text = " ".join(hashtags)
                    st.code(hashtag_text)
            
            # Copy button
            if st.button("📋 Copy Content", use_container_width=True):
                st.success("✅ Content ready to copy! (Select and copy the text above)")
    else:
        st.text_area(
            "Generated Content:",
            value="Your optimized social media content will appear here...",
            height=300,
            disabled=True
        )

# Platform comparison section
st.markdown("---")
st.markdown("### 📊 Platform Comparison")

comparison_cols = st.columns(len(PLATFORM_SPECS))
for idx, (platform_key, platform_info) in enumerate(PLATFORM_SPECS.items()):
    with comparison_cols[idx]:
        st.markdown(f"""
        **{platform_info['icon']} {platform_info['name']}**
        - **Limit**: {platform_info['char_limit']:,} chars
        - **Hashtags**: {platform_info['optimal_hashtags']}
        - **Best Time**: {platform_info['best_times'].split(',')[0]}
        """)

# Tips and best practices
st.markdown("---")
st.markdown("### 💡 Social Media Best Practices")

tip_tabs = st.tabs(["📝 Content Tips", "🏷️ Hashtag Strategy", "⏰ Timing", "📈 Engagement"])

with tip_tabs[0]:
    st.markdown("""
    **Content Creation Tips:**
    - Keep your message clear and concise
    - Use platform-appropriate tone and style
    - Include compelling calls-to-action
    - Add relevant emojis for visual appeal
    - Tell stories that resonate with your audience
    - Use high-quality visuals when possible
    """)

with tip_tabs[1]:
    st.markdown("""
    **Hashtag Strategy:**
    - Mix popular and niche hashtags
    - Research trending hashtags in your industry
    - Create branded hashtags for campaigns
    - Don't overstuff with hashtags
    - Monitor hashtag performance
    - Update hashtags regularly
    """)

with tip_tabs[2]:
    st.markdown("""
    **Optimal Posting Times:**
    - **Twitter**: 9-10 AM, 12-1 PM, 5-6 PM
    - **LinkedIn**: 8-10 AM, 12 PM, 5-6 PM (weekdays)
    - **Instagram**: 11 AM-1 PM, 5-7 PM
    - **Facebook**: 9 AM, 1-3 PM
    - **WhatsApp**: 7-9 PM, 10-11 PM
    
    *Note: Test different times for your specific audience*
    """)

with tip_tabs[3]:
    st.markdown("""
    **Engagement Strategies:**
    - Ask questions to encourage comments
    - Respond to comments promptly
    - Use interactive features (polls, stories)
    - Share behind-the-scenes content
    - Collaborate with others in your niche
    - Maintain consistent posting schedule
    """)

# Footer
st.markdown("---")
st.markdown("""
### 🚀 How to Use:
1. **Select your platform** from the sidebar (Twitter, LinkedIn, Instagram, etc.)
2. **Choose content type** (create post, optimize existing, hashtag research, etc.)
3. **Enter your topic or content** in the input area
4. **Generate optimized content** with platform-specific formatting
5. **Copy and use** the generated content on your social media platform

### ✨ Features:
- **Platform-specific optimization** with character limits and best practices
- **Hashtag research and generation** for maximum reach
- **Content calendar planning** for consistent posting
- **Competitor analysis** for strategic insights
- **Real-time character and hashtag counting**
""")

# Developer credit
st.sidebar.markdown("---")
st.sidebar.markdown("### 👨‍💻 Developer")
st.sidebar.info("**Developed by Daniel Kasonde**\n\nSocial Media Manager v1.0")
st.sidebar.markdown("---")
