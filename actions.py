from aijson import register_action


@register_action
def extract_list(text: str) -> list[str]:
    return text.split(",")

@register_action 
def analyze_dream(dream: str) -> None:
    # Extract the list of words from the dream
    words = extract_list(dream)
    # Analyze the dream
    # ...