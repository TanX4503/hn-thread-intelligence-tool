import requests
import json
import time

def search_hn(query, num_stories=5):
    # Searches HN 
    '''
    Breakdown of the dictionary it returns (for my own ref):
    - title, author, url, points, number of comments etc
    - timestamps- updated_at created_at
    - IDs- objectID and story_id
    - children - comments
    - _tags - internal stuff for filtering, searching and categorizing
    - _highlightResult - What matched my searchquery
    '''
    url = f"https://hn.algolia.com/api/v1/search?query={query}&tags=story&hitsPerPage={num_stories}"
    response = requests.get(url)
    data = response.json()
    return data["hits"] #The hits part of the data json is what contains the actual search results. The rest of the items in the dictionary is just search metadata that isnt too useful to us. 
    
def fetch_item(item_id):
    # Fetches a single story or comment
    '''
    What it returns: 
    by, id, kids-comments to this, text (imp), unix timestamp, item type
    '''
    url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
    response = requests.get(url)
    return response.json()

def fetch_comments_recursive(item_id, depth=0, max_depth=4):
    # Fetching a comment and all its children
    item = fetch_item(item_id)
    if not item:
        return None
    if item.get("deleted") or item.get("dead"):
        return None
    comment = {
        "id": item.get("id"),
        "text": item.get("text", ""),
        "author": item.get("by", "[unknown]"),
        "score": item.get("score", 0),
        "time": item.get("time", 0),
        "depth": depth,
        "children": []
    }
    
    # Recursively fetch children (if not too deep)
    if depth < max_depth and item.get("kids"):
        for child_id in item["kids"][:10]:
            time.sleep(0.05)
            child = fetch_comments_recursive(child_id, depth + 1, max_depth)
            if child:
                comment["children"].append(child)
    
    return comment

def fetch_full_thread(story_id):
    # Fetching a story and all its comments
    story = fetch_item(story_id)
    comments = []
    
    if story.get("kids"):
        for kid_id in story["kids"][:20]:  # Top 20 top-level comments
            time.sleep(0.05)
            comment = fetch_comments_recursive(kid_id)
            if comment:
                comments.append(comment)
    
    return {"story": story, "comments": comments}