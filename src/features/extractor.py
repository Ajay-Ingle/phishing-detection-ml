"""
Pure feature-extraction functions: raw URL string -> phishing signal features.

Design rules for this module:
- No I/O side effects except the explicit network calls in domain-based
  features (WHOIS lookup). Address-bar features are pure string/parsing logic.
- No training-only or inference-only imports — this module is shared by both,
  so it must stay dependency-light (stdlib + whois only).
- Each function returns 1 (phishing signal present) or 0 (not present),
  matching the original model's label convention.

Note: the legacy version of this module included a `web_traffic` feature
backed by the Alexa Rank API (data.alexa.com). That API was permanently
shut down in May 2022. The feature has been removed rather than replaced:
it no longer returns real signal, and its unhandled network exception path
could crash inference in production. See rebuild notes / interview_notes.md
for the full reasoning.
"""

from __future__ import annotations

import ipaddress
import re
from dataclasses import dataclass, fields
from datetime import datetime
from urllib.parse import urlparse

import whois

# Known URL-shortening domains. Phishers use these to mask the real
# destination domain from a user glancing at the link.
_SHORTENING_SERVICES = re.compile(
    r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|"
    r"is\.gd|cli\.gs|tiny\.cc|url4\.eu|su\.pr|snipurl\.com|short\.to|"
    r"BudURL\.com|ping\.fm|post\.ly|bkite\.com|snipr\.com|fic\.kr|"
    r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|"
    r"lnkd\.in|db\.tt|qr\.ae|adf\.ly|bitly\.com|cur\.lv|ity\.im|q\.gs|"
    r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|"
    r"yourls\.org|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|"
    r"qr\.net|1url\.com|tweez\.me|v\.gd|link\.zip\.net",
    re.IGNORECASE,
)

# Minimum acceptable domain age/remaining-validity, in months.
_MIN_DOMAIN_AGE_MONTHS = 6
_MIN_DOMAIN_END_MONTHS = 6
_LONG_URL_THRESHOLD = 54


@dataclass(frozen=True)
class URLFeatures:
    """Feature vector for a single URL. Field order == model training order."""

    have_ip: int
    have_at: int
    url_length: int
    url_depth: int
    redirection: int
    tiny_url: int
    prefix_suffix: int
    dns_record: int
    domain_age: int
    domain_end: int

    def as_list(self) -> list[int]:
        """Ordered list matching the model's expected input order."""
        return [getattr(self, f.name) for f in fields(self)]


# ---- Address-bar based features (no network calls) -------------------------

def having_ip(url: str) -> int:
    """1 if the URL's host is a raw IP address instead of a domain name."""
    host = urlparse(url).netloc.split(":")[0]
    try:
        ipaddress.ip_address(host)
        return 1
    except ValueError:
        return 0


def have_at_sign(url: str) -> int:
    """1 if '@' appears in the URL (browsers ignore everything before it)."""
    return 1 if "@" in url else 0


def get_length(url: str) -> int:
    """1 if the URL is long enough to be hiding something (>= 54 chars)."""
    return 1 if len(url) >= _LONG_URL_THRESHOLD else 0


def get_depth(url: str) -> int:
    """Number of non-empty path segments, e.g. /a/b/c -> 3."""
    segments = urlparse(url).path.split("/")
    return sum(1 for segment in segments if segment)


def redirection(url: str) -> int:
    """1 if '//' appears somewhere after the protocol (unexpected redirect)."""
    pos = url.rfind("//")
    return 1 if pos > 7 else 0


def tiny_url(url: str) -> int:
    """1 if the URL uses a known link-shortening service."""
    return 1 if _SHORTENING_SERVICES.search(url) else 0


def prefix_suffix(url: str) -> int:
    """1 if the domain contains a '-' (rare in legitimate domains)."""
    return 1 if "-" in urlparse(url).netloc else 0


# ---- Domain-based features (WHOIS lookup, one network call per URL) --------

def _safe_whois(domain: str):
    """Returns a whois record, or None if the lookup fails for any reason."""
    try:
        return whois.whois(domain)
    except Exception:
        return None


def _as_datetime(value) -> datetime | None:
    """WHOIS libraries inconsistently return str, datetime, or list. Normalize."""
    if isinstance(value, list):
        value = value[0] if value else None
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return None
    return value


def domain_age(creation: datetime | None, expiration: datetime | None) -> int:
    """1 if the domain's total registered lifespan is under 6 months."""
    if creation is None or expiration is None:
        return 1
    age_days = abs((expiration - creation).days)
    return 1 if (age_days / 30) < _MIN_DOMAIN_AGE_MONTHS else 0


def domain_end(expiration: datetime | None) -> int:
    """1 if the domain's registration expires in under 6 months."""
    if expiration is None:
        return 1
    remaining_days = abs((expiration - datetime.now()).days)
    return 1 if (remaining_days / 30) < _MIN_DOMAIN_END_MONTHS else 0


def extract_features(url: str) -> URLFeatures:
    """Extract the full 10-feature vector for a single URL."""
    record = _safe_whois(urlparse(url).netloc)
    dns_record = 0 if record is not None else 1

    creation = _as_datetime(getattr(record, "creation_date", None)) if record else None
    expiration = _as_datetime(getattr(record, "expiration_date", None)) if record else None

    return URLFeatures(
        have_ip=having_ip(url),
        have_at=have_at_sign(url),
        url_length=get_length(url),
        url_depth=get_depth(url),
        redirection=redirection(url),
        tiny_url=tiny_url(url),
        prefix_suffix=prefix_suffix(url),
        dns_record=dns_record,
        domain_age=1 if dns_record == 1 else domain_age(creation, expiration),
        domain_end=1 if dns_record == 1 else domain_end(expiration),
    )
