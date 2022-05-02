
# Filter the "publicerad" field for the start and end date. Booth dates are inclusive.
def get_date_query(start_date: str = None, end_date: str = None):
    if start_date is not None and end_date is not None:
        date = {"gte": start_date, "lte": end_date}
    elif start_date is None:
        date = {"lte": end_date}
    elif end_date is None:
        date = {"gte": start_date}
    return { "filter": {"range": {"rm":  date}}}


# Search the text field for the search string
def get_search_string_match_query(field: str = "text", search_string: str = "", phrase_search: bool = False):
    if phrase_search:
        return {
            "must": {'match_phrase': {field: search_string}}
        }
    else:
        return {
            "must": {'match': {field: search_string}}
        }
