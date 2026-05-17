# src/features/feature_utils.py
import re
import ipaddress
from urllib.parse import urlparse

def having_ip(url: str) -> int:
    """Checks for the presence of an IP address in the URL."""
    try:
        # Extract netloc to isolate domain from parameters
        domain = urlparse(url).netloc
        if not domain:
            domain = url
        ipaddress.ip_address(domain)
        return 1
    except:
        return 0

def have_at_sign(url: str) -> int:
    """Checks for the presence of '@' symbol in the URL."""
    return 1 if "@" in url else 0

def get_length(url: str) -> int:
    """Computes the length of the URL and categorizes it."""
    return 1 if len(url) >= 54 else 0

def get_depth(url: str) -> int:
    """Calculates the structural depth of the URL path segments."""
    parsed = urlparse(url)
    path_segments = parsed.path.split('/')
    return sum(1 for segment in path_segments if len(segment) != 0)

def redirection(url: str) -> int:
    """Checks for unexpected positional occurrence of redirection '//' sequence."""
    position = url.rfind('//')
    if position > 6:
        return 1 if position > 7 else 0
    return 0

def prefix_suffix(url: str) -> int:
    """Detects presence of structural hyphenation '-' within the root domain context."""
    try:
        domain = urlparse(url).netloc
        return 1 if '-' in domain else 0
    except:
        return 1

def tiny_url(url: str) -> int:
    """Validates the input string against typical URL shortener service patterns."""
    shortening_pattern = (
        r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|"
        r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|"
        r"short\\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|"
        r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|lnkd\.in|db\.tt|"
        r"qr\.ae|adf\.ly|bitly\.com|cur\.lv|tinyurl\.com|ity\.im|q\.gs|po\.st|bc\.vc|twitthis\.com|"
        r"u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org"
    )
    return 1 if re.search(shortening_pattern, url, flags=re.IGNORECASE) else 0

def get_domain_age(domain_info) -> int:
    """Evaluates contextual registry domain timeline ages from WHOIS payload structure."""
    if not domain_info:
        return 1
    try:
        creation_date = domain_info.creation_date
        expiration_date = domain_info.expiration_date
        
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]
            
        if creation_date is None or expiration_date is None:
            return 1
            
        age_days = abs((expiration_date - creation_date).days)
        return 1 if (age_days / 30) < 6 else 0
    except:
        return 1

def get_dns_record(domain_info) -> int:
    """Determines basic infrastructure footprint mapping availability from WHOIS response."""
    return 0 if domain_info and domain_info.domain_name else 1

def get_domain_end(domain_info) -> int:
    """Tracks domain termination horizons against immediate processing thresholds."""
    if not domain_info:
        return 1
    try:
        expiration_date = domain_info.expiration_date
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]
        if expiration_date is None:
            return 1
            
        remaining_days = (expiration_date - datetime.now()).days
        return 1 if (remaining_days / 30) < 6 else 0
    except:
        return 1