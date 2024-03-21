def map_score_to_radius(score, min_radius, max_radius):
    # Ensure score is within bounds
    score = max(0, min(1, score))
    
    # Calculate radius using linear interpolation
    radius = min_radius + (max_radius - min_radius) * score
    
    return radius

def map_score_to_radius(score, min_radius, max_radius):
    # Ensure score is within bounds
    score = max(0, min(1, score))
    
    # Calculate radius using linear interpolation
    radius = min_radius + (max_radius - min_radius) * score
    
    return radius