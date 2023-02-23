import re

timestamp_pattern = re.compile(r"<t:\d+:D>")
price_finder_pattern = re.compile(r"\D*(\d+)")
