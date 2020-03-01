CITATION_PATTERNS = [
    {
        "label": "GENERIC_CASE_CITATION",
        "pattern": [
            {"IS_BRACKET": True, "OP": "?"},
            {"SHAPE": "dddd"},
            {"IS_BRACKET": True, "OP": "?"},
            {"LIKE_NUM": True, "OP": "?"},
            {"TEXT": {"REGEX": "^[A-Z]"}, "OP": "?"},
            {"ORTH": ".", "OP": "?"},
            {"TEXT": {"REGEX": r"^[A-Z\.]"}},
            {"ORTH": ".", "OP": "?"},
            {"LIKE_NUM": True},
        ],
    }
]
