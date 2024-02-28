from fuzzywuzzy import process

def find_closest_words(target_word, dict_list, key, threshold=70, limit=5):
    # Extract content and IDs from the specified key in each dictionary
    word_id_list = [(d["id"], d[key]) for d in dict_list]
    word_list = [word for _, word in word_id_list]
    
    # Get matches with scores
    matches = process.extract(target_word, word_list, limit=limit)
    
    # Filter out matches with scores below the threshold
    filtered_matches = [(word_id_list[i][0], word, score) for i, (word, score) in enumerate(matches) if score >= threshold]
    
    # Construct list of dictionaries
    match = [{"target_id": id, "content": word} for id, word, _ in filtered_matches]
    
    return match

# Example usage

def match(target_word,data,id):
  matches = find_closest_words(target_word, data["nodes"], key="content")
  for m in matches:
    m |= {"source_id":id}
    print(m)
  return matches
