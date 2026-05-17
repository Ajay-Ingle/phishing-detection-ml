# src/features/feature_extractor.py
# Used by:training, inference, API predictions
import whois
from urllib.parse import urlparse
from typing import List, Dict, Any
from src.features import feature_utils

def feature_extraction(url: str, whois_response: Any = None) -> List[int]:
    """
    Centralized transformation pipeline mapping raw input parameters 
    into standard structured feature vector arrays required by modeling stages.
    """
    features = []
    
    # Address Bar-based feature extractions
    features.append(feature_utils.having_ip(url))
    features.append(feature_utils.have_at_sign(url))
    features.append(feature_utils.prefix_suffix(url))
    features.append(feature_utils.tiny_url(url))
    features.append(feature_utils.redirection(url))
    features.append(feature_utils.get_depth(url))
    features.append(feature_utils.get_length(url))
    
    # Safe fallback validation handling for external WHOIS execution responses
    if whois_response is None:
        try:
            domain = urlparse(url).netloc
            whois_response = whois.whois(domain) if domain else None
        except:
            whois_response = None
            
    # Domain footprint based feature mappings
    dns_status = feature_utils.get_dns_record(whois_response)
    features.append(dns_status)
    
    # Structural features requiring context checking validation cascades
    features.append(1 if dns_status == 1 else feature_utils.get_domain_age(whois_response))
    features.append(1 if dns_status == 1 else feature_utils.get_domain_end(whois_response))
    
    return features