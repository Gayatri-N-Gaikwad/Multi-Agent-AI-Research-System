import sys
sys.stdout.reconfigure(encoding='utf-8')

from agents import build_search_agent, writer_chain, critic_chain, revision_chain
from utils import extract_tool_outputs, extract_urls_from_search, scrape_multiple, parse_score

MAX_RETRIES = 2
SCORE_THRESHOLD = 8
MAX_SOURCES = 3

def run_research_pipeline(topic: str) -> dict:
    state = {}
    
    # Step 1: Search Agent
    print("\n" + " =" * 50)
    print("step 1 - search agent is working ...")
    print("=" * 50)
    
    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" : [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = extract_tool_outputs(search_result)
    
    print("\n search result:\n", state['search_results'])
    
    # Step 2: Deterministic Scraping
    print("\n" + " =" * 50)
    print("step 2 - Scraper is gathering content from top resources ...")
    print("=" * 50)
    
    urls = extract_urls_from_search(state["search_results"], max_urls=MAX_SOURCES)
    print(f"Selected URLs for scraping: {urls}")
    
    if not urls:
        state["scraped_content"] = "No additional sources could be scraped."
        print("Warning: No URLs found in search results to scrape.")
    else:
        state["scraped_content"] = scrape_multiple(urls)
        
    print("\nscraped content: \n", state['scraped_content'])
    
    # Step 3: Writer
    print("\n" + " =" * 50)
    print("step 3 - Writer is drafting the report ...")
    print("=" * 50)
    
    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )
    
    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })
    
    print("\n Initial Draft:\n", state['report'])
    
    # Step 4: Critic + Reflection Loop
    state["revision_history"] = []
    iteration = 0
    
    while True:
        print("\n" + " =" * 50)
        print(f"step 4 - critic is reviewing the report (Iteration {iteration}) ...")
        print("=" * 50)
        
        critique = critic_chain.invoke({
            "report": state["report"]
        })
        score = parse_score(critique)
        
        state["revision_history"].append({
            "iteration": iteration,
            "report": state["report"],
            "critique": critique,
            "score": score
        })
        
        print(f"\nScore: {score}/10")
        print("\nCritic Feedback:\n", critique)
        
        if score is None:
            print("Warning: Could not parse critic score. Stopping feedback loop.")
            break
            
        if score >= SCORE_THRESHOLD:
            print(f"\nSuccess! Score {score} meets or exceeds threshold {SCORE_THRESHOLD}.")
            break
            
        if iteration >= MAX_RETRIES:
            print(f"\nHit max retries ({MAX_RETRIES}). Stopping feedback loop.")
            break
            
        print(f"\nScore {score} is below threshold {SCORE_THRESHOLD}. Revising report...")
        state["report"] = revision_chain.invoke({
            "topic": topic,
            "previous_report": state["report"],
            "critique": critique,
            "research": research_combined
        })
        iteration += 1
        
    # Assign last entry's critique and score to feedback and final_score
    last_entry = state["revision_history"][-1]
    state["feedback"] = last_entry["critique"]
    state["final_score"] = last_entry["score"]
    
    return state

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("\n Enter a research topic : ")
    state = run_research_pipeline(topic)
    
    print("\n" + "=" * 50)
    print("FINAL RESEARCH REPORT")
    print("=" * 50)
    print(state["report"])
    
    print("\n" + "=" * 50)
    print(f"Summary: Final Score = {state['final_score']}/10, Attempts = {len(state['revision_history'])}")
    print("=" * 50)
