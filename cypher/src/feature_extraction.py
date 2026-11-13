import re
import tldextract

# Use the public suffix list bundled with tldextract so the app works offline
# (inside Docker / CI) without downloading the list at runtime.
_extract = tldextract.TLDExtract(suffix_list_urls=())

def extract_features(url):
    ext = _extract(url)

    return [
        len(url),                                      # 1
        url.count('.'),                                # 2
        int(url.startswith("https")),                  # 3
        len(ext.subdomain),                            # 4
        len(ext.domain),                               # 5
        len(ext.suffix),                               # 6
        int("login" in url.lower() or 
            "secure" in url.lower() or 
            "verify" in url.lower()),                  # 7
        int(re.search(r'\d', url) is not None)         # 8
    ]
