def process_comments(comment, parent_text="", story_title="", result=None):
    # Converting the nested dictionary
    if result is None:
        result = []
    if not comment or not comment.get("text"):
        return result
    chunk = {
        "id": comment["id"],
        "text": comment["text"],
        "author": comment["author"],
        "depth": comment["depth"],
        "parent_context": parent_text[:200] if parent_text else "",  # First 200 chars of parent, this allows us to keep the context of the comment
        "story_title": story_title,
    }
    result.append(chunk)
    for child in comment.get("children", []):
        process_comments(child, parent_text=comment["text"], story_title=story_title, result=result)
    return result

def filter_and_sort_chunks(chunks):
    # Remove noise and sort the data chunks. Here, we are getting rid of small comments, skipping comments that are just links and then we are sorting the comments based on depth. 
    filtered = []
    for chunk in chunks:
        text = chunk["text"]
        if not text or len(text) < 30: # Very small comments would not be very relevant
            continue
        if text.strip().startswith("<a href"): # Skip comments that are just links
            continue
        filtered.append(chunk)
    filtered.sort(lambda x: x["depth"])
    return filtered 