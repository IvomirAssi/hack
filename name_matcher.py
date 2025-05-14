import streamlit as st
import unidecode
import re
from difflib import SequenceMatcher

# --- Normalization Rules ---
def normalize(name, rules_applied):
    original = name
    name = name.strip()
    if name != original:
        rules_applied.append("leading/trailing whitespace removed")

    original = name
    name = name.lower()
    if name != original:
        rules_applied.append("lowercased")

    original = name
    name = unidecode.unidecode(name)
    if name != original:
        rules_applied.append("accents removed")

    original = name
    name = re.sub(r'[^a-z0-9\s]', '', name)
    if name != original:
        rules_applied.append("punctuation removed")

    original = name
    name = re.sub(r'\s+', ' ', name)
    if name != original:
        rules_applied.append("extra whitespace removed")

    return name

# --- Difference Categorization ---
def categorize_differences(original1, original2, norm1, norm2):
    categories = []

    if original1 != original2:
        if unidecode.unidecode(original1) == unidecode.unidecode(original2):
            categories.append("accent difference")

        if original1.replace(" ", "") == original2.replace(" ", ""):
            categories.append("whitespace difference")

        if re.sub(r'\d', '', original1) == re.sub(r'\d', '', original2):
            categories.append("number difference")

        if re.sub(r'\W', '', original1) == re.sub(r'\W', '', original2):
            categories.append("punctuation difference")

    if norm1 != norm2:
        categories.append("semantic or structural difference")

    return list(set(categories))

# --- Final comparison ---
def compare_names(name1, name2):
    rules_applied_1 = []
    rules_applied_2 = []

    norm1 = normalize(name1, rules_applied_1)
    norm2 = normalize(name2, rules_applied_2)

    score = SequenceMatcher(None, norm1, norm2).ratio()
    categories = categorize_differences(name1, name2, norm1, norm2)

    return {
        "name1": name1,
        "name2": name2,
        "normalized_name1": norm1,
        "normalized_name2": norm2,
        "score": round(score, 3),
        "normalization_applied": list(set(rules_applied_1 + rules_applied_2)),
        "difference_categories": categories
    }

# --- Streamlit UI ---
st.title("🧠 Name Matching Debugger")

name1 = st.text_input("Enter first company name:")
name2 = st.text_input("Enter second company name:")

if name1 and name2:
    result = compare_names(name1, name2)

    st.subheader("🔍 Normalized Names")
    st.text(f"{result['normalized_name1']}\n{result['normalized_name2']}")

    st.subheader("📊 Similarity Score")
    st.metric(label="Score (0-1)", value=result['score'])

    st.subheader("⚙️ Normalization Steps Applied")
    st.write(result['normalization_applied'])

    st.subheader("🧾 Difference Categories")
    st.write(result['difference_categories'])
