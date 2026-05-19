import json
import os
from rapidfuzz import fuzz




# Initialize catalog target globally across file namespaces
catalog = []

# Resolve the absolute path to your root "D:\shl reccomender" directory
current_file_dir = os.path.dirname(os.path.abspath(__file__))  # app\retrieval
app_dir = os.path.dirname(current_file_dir)                   # app
project_root = os.path.dirname(app_dir)                       # D:\shl reccomender

# Target the exact absolute disk location of your data asset file
ABSOLUTE_CATALOG_PATH = os.path.join(project_root, "data", "shl_catalog.json")

if os.path.exists(ABSOLUTE_CATALOG_PATH):
    try:
        #  THE CRITICAL FIX: strict=False ignores malformed control characters on line 4795
        with open(ABSOLUTE_CATALOG_PATH, "r", encoding="utf-8") as f:
            catalog = json.loads(f.read(), strict=False)
            
    except Exception as e:
        print(f" Error parsing catalog file: {e}")
else:
    print(f" Warning: shl_catalog.json could not be located at absolute path: {ABSOLUTE_CATALOG_PATH}")


def hybrid_search(query: str, top_k: int = 10) -> list:
    """
    Performs a localized hybrid string matching evaluation across the catalog.
    Combines token overlaps and partial fuzzy matching.
    """
    query = query.lower().strip()
    results = []

    for item in catalog:
        name = item.get("name", "")
        if not name:
            continue

        description = item.get("description", "") or ""
        
        # 1. Pull native database fields using the correct raw keys
        url = item.get("link", "") or ""  # Database uses 'link'
        raw_keys = item.get("keys", []) or []  # Database uses 'keys'
        test_type = ", ".join(raw_keys) if isinstance(raw_keys, list) else str(raw_keys)
        
        job_levels = item.get("job_levels", []) or []
        duration = item.get("duration", "") or ""

        # 2. Build clean lookup strings for ranking passes
        combined_text = (
            f"{name} {description} {test_type} {' '.join(job_levels)}"
        ).lower()

        # 3.  THE CORRECTION: Calculate scores inside the loop before appending
        fuzzy_score = fuzz.partial_ratio(query, combined_text)
        overlap_score = sum(
            15 for token in query.split()
            if token in combined_text
        )
        final_score = fuzzy_score + overlap_score

        # 4. Safely package metrics into the matching target dictionary layout
        results.append({
            "entity_id": item.get("entity_id", ""),
            "name": name,
            "url": url,
            "description": description,
            "test_type": test_type,
            "job_levels": job_levels,
            "languages": item.get("languages", []),
            "duration": duration,
            "status": item.get("status", ""),
            "remote": item.get("remote", ""),
            "adaptive": item.get("adaptive", ""),
            "score": final_score
        })

    # Sort matches highest score first
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

# ---------------------------------------------------------
# DIAGNOSTIC TEST RUNNER EXECUTION BLOCK
# ---------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("SHL RECOMENDER - HYBRID SEARCH ENGINE TEST SUITE")
    print("=" * 60)
    print(f" Execution Base Location Resolve: {os.getcwd()}")
    print(f" Catalog Records Loaded: {len(catalog)}")
    print("-" * 60)

    # 1. Test search matching capabilities
    test_query = "Java developer stakeholder communication"
    print(f" Running Search Test for Query: '{test_query}'")
    
    search_matches = hybrid_search(test_query, top_k=3)
    
    for rank, match in enumerate(search_matches, 1):
        print(f"\n[Rank {rank}] Match Score: {match['score']:.2f}")
        print(f"  • Name: {match['name']}")
        print(f"  • URL: '{match['url']}'")
        print(f"  • Test Type: '{match['test_type']}'")
        print(f"  • Duration: '{match['duration']}'")
        print(f"  • Job Levels: {match['job_levels']}")
    
    print("-" * 60)

    # 2. Inspect raw data entries specifically for anomalies
    target_assessment = "Business Communication (adaptive)"
    print(f" Target Entry Metadata Deep-Dive: '{target_assessment}'")
    
    db_matches = [item for item in catalog if item.get("name") == target_assessment]
    if db_matches:
        raw_item = db_matches[0]
        print(f"  • Raw Link Key: {repr(raw_item.get('link'))}")
        print(f"  • Raw Keys Attribute: {repr(raw_item.get('keys'))}")
        print(f"  • Raw Duration Value: {repr(raw_item.get('duration'))}")
        print(f"  • Raw Job Levels List: {repr(raw_item.get('job_levels'))}")
    else:
        print(f" Failed to locate target record '{target_assessment}' in database.")
    print("=" * 60)