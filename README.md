# hn-thread-intelligence-tool
A two-part system that pulls what the HN community thinks about a specific topic and then lets the user chat with that data to learn more. A research assistant that reads the threads so the user doesn't have to. Built for the SUTT ML Recruitment Task.
#
This repository focuses on the first part of the problem as of right now: When a user searches a topic, your tool should fetch the top threads and
generate a structured digest. Don't just output a generic summary like
"opinions are mixed." Highlight the real substance: what are the main
arguments? What are the pros/cons? Are there common alternative tools
mentioned? Make it genuinely useful for a developer trying to make a tech
decision.


# Approach to Solving the Problem

- I needed to get as much useful data as possible while not exceeding the token limit of whatever LLM system I was using.
- I started by deciding which LLM I plan to use for creating the final digest. For this I used Groq Llama 4 as it is a free to use API and has a decently large token count.
- As for the data, I have fetched 3 of the top stories that come up based on number of upvotes (the search results are automatically sorted based on number of upvotes). After this, I have fetched comments recursively with a maximum depth of 3. This ensures that I get the comments that I need while not getting into irrelevency.
- Furthur, I have discarded comments that are too small or are just links as these comments would not be very useful as compared to the other data that has been fetched.
- I have not kept things like timestamps, urls, number of comments, timestamps and tags as these are not very useful to the final digest or its processing. I have kept the author, id, text, depth and ids of "children"- the comments nested under the data item
- The data is processed into chunks which contain the first 200 letters of their parent data chunk. This preserves context i.e. who is replying to who.
- The chunks are then sorted based on depth so that the comments with the least depth are the ones which come at the top. After this, only the top 50 chunks are sent into the final prompt. This keeps relevency while keeping us well under the token limit of the API.
- Finally a prompt is sent into Groq Llama's API which then returns our digest.
- The app is finally presented as a console application.

# How to Run on your Device

- Clone the repo onto your device: $ git clone https://github.com/TanX4503/hn-thread-intelligence-tool
- Install the groq module: pip install groq
- Setup an environment variable under the name GROQ_API_KEY and set its value to your Groq API Key which can be taken from console.groq.com 
- Run main.py locally on your device

# Dependancies used and Requirements

- requests
- ssl
- urllib3.util.ssl_
- time
- groq
- os
