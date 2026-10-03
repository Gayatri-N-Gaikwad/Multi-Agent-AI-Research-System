from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search , scrape_url 
from dotenv import load_dotenv
import os

load_dotenv()

#model setup 
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

#1st agent 
def build_search_agent():
    return create_agent(
        model = llm,
        tools= [web_search]
    )

#2nd agent 

def build_reader_agent():
    return create_agent(
        model = llm,
        tools = [scrape_url]
    )


#writer chain 

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list ONLY the URLs that literally appear in the research above, exactly as written)

Rules: Do not invent, guess, or reconstruct any URL. If a claim has no source URL available, state that explicitly instead of fabricating one. Where possible, note which source (SOURCE 1, SOURCE 2, etc.) supports each key finding.

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

#critic_chain 

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()

#revision_chain

revision_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer revising a report based on editorial feedback."),
    ("human", """You are revising a research report on the topic: {topic}.

Previous Report:
{previous_report}

Editorial Critique:
{critique}

Research Gathered:
{research}

Please revise the report to address the areas to improve mentioned in the critique.
Keep the same 4-section structure:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list ONLY the URLs that literally appear in the research above, exactly as written)

Rules:
1. Revise the previous report to address the critique's "Areas to Improve".
2. Use the research gathered for extra detail.
3. Do not invent, guess, or reconstruct any URL. If a claim has no source URL available, state that explicitly instead of fabricating one. Where possible, note which source (SOURCE 1, SOURCE 2, etc.) supports each key finding.
4. Output ONLY the revised report with no meta-commentary.
""")
])

revision_chain = revision_prompt | llm | StrOutputParser()

