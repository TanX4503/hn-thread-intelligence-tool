from groq import Groq
from data import *
from process import *
import os

def format_chunks_for_prompt(chunks, max_chunks=50):
    # Converting the data chunks into readable text for the LLM
    formatted = ""
    for i in range(0,max_chunks):
        formatted += f"\nComment {i+1} (depth: {chunks[i]['depth']}, author: {chunks[i]['author']})\n"
        formatted += chunks[i]["text"][:500]  # Truncate very long comments
        if chunks[i]["parent_context"]:
            formatted += f"\n[Replying to: {chunks[i]['parent_context']}...]"
        formatted += "\n"
    return formatted

def generate_prompt(chunks, topic):
    formatted_comments = format_chunks_for_prompt(chunks)
    
    prompt = f"""You are analyzing Hacker News discussion threads about: "{topic}"

Here are the top comments from real HN discussions:

{formatted_comments}

<End of comments>

Generate a structured digest with these sections:
1. MAIN ARGUEMENTS: What are the top 5-6 arguements being discussed in the threads that have been fetched. 
2. PROS: What genuine advantages do people highlight?
3. CONS: What problems, limitations, or warnings come up?
4. ALTERNATIVE TOOLS MENTIONED: Any competing tools or approaches people recommend instead?
5. COMMUNITY CONSENSUS: Is there a clear opinion, or is it split? On what specific points do people agree vs. disagree?

Note: Avoid generic answers like "opinions are mixed". The digest should contain substantial data useful for developers that has been derived from the Hacker News comments that have been provided. Do not add your own opinions or hallucinate new information.
"""
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",  # Fast and free on Groq
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,  # A low temperature ensures that Groq does not hallucinate
        max_completion_tokens=1024,
    )
    return response.choices[0].message.content

def run_tool(topic):
    """Main entry point — ties all stages together."""
    print(f"\nSearching HN for: '{topic}'")
    stories = search_hn(topic, num_stories=3)
    
    all_chunks = []
    for story in stories:
        print(f"  Fetching thread: {story['title'][:60]}...")
        thread = fetch_full_thread(story["objectID"])
        
        for comment in thread["comments"]:
            chunks = process_comments(comment, story_title=story["title"])
            all_chunks.extend(chunks)
    
    print(f"\nTotal raw comments: {len(all_chunks)}")
    filtered = filter_and_sort_chunks(all_chunks)
    print(f"After filtering: {len(filtered)} chunks")
    
    print("\nGenerating digest...\n")
    digest = generate_prompt(filtered, topic)
    
    print("=" * 60)
    print(f"DIGEST: {topic}")
    print("=" * 60)
    print(digest)

print("=================================HACKER NEWS THREAD INTELLIGENCE TOOL=================================")
query = input("Enter your search query: ")
print()
run_tool(query)