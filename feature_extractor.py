import math
import re
import urllib.parse
from collections import Counter, counter

def extract_features(url):
    features = {}
def entropy(string):
    prob = [n_x/len(string) for x,n_x in Counter(string).items()]
    return -sum(p*math.log2(p) for p in prob if p > 0)
    parsed = urllib.parse.urlparse(url)

    features["NumDots"] = url.count(".")
    features["SubdomainLevel"] = parsed.netloc.count(".")
    features["PathLevel"] = parsed.path.count("/")
    features["UrlLength"] = len(url)
    features["NumDash"] = url.count("-")
    features["NumDashInHostname"] = parsed.netloc.count("-")
    features["AtSymbol"] = int("@" in url)
    features["TildeSymbol"] = int("~" in url)
    features["NumUnderscore"] = url.count("_")
    features["NumPercent"] = url.count("%")
    features["NumQueryComponents"] = len(parsed.query.split("&")) if parsed.query else 0
    features["NumAmpersand"] = url.count("&")
    features["NumHash"] = url.count("#")
    features["NumNumericChars"] = sum(c.isdigit() for c in url)
    features["NoHttps"] = int(parsed.scheme != "https")
    features["IpAddress"] = int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', parsed.netloc)))
    features["HostnameLength"] = len(parsed.netloc)
    features["PathLength"] = len(parsed.path)
    features["QueryLength"] = len(parsed.query)

    return features