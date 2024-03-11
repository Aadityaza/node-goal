from fuzzywuzzy import process, fuzz

def find_closest_words(target_word, dict_list, key, threshold=70, limit=1130):
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


def match(target_word, data, source_id):
    matches = find_closest_words(target_word, data["nodes"], key="content")
    word_id_list = [(d["id"], d["content"]) for d in data["nodes"]]  # Assuming id is available in the "id" key
    for m in matches:
        for id_val, content in word_id_list:
            if content == m["content"]:
                m["target_id"] = id_val
                break
        m["source_id"] = source_id
        print(m)
    return matches
