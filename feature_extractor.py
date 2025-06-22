# feature_extractor.py

from urllib.parse import urlparse, urlencode
import ipaddress
import re
from bs4 import BeautifulSoup
import urllib
import urllib.request
from datetime import datetime

import whois

# List of shortening services
shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"

# 1. Checks for IP address in URL
def havingIP(url):
    try:
        ipaddress.ip_address(url)
        return 1
    except:
        return 0

# 2. Checks the presence of @ in URL
def haveAtSign(url):
    return 1 if "@" in url else 0

# 3. Length of URL
def getLength(url):
    return 1 if len(url) >= 54 else 0

# 4. Depth of URL (number of '/')
def getDepth(url):
    path = urlparse(url).path.split('/')
    depth = sum(1 for segment in path if segment)
    return depth

# 5. Redirection "//" in URL
def redirection(url):
    pos = url.rfind('//')
    return 1 if pos > 7 else 0

#The difference between termination time and current time (Domain_End) 
def domainEnd(domain_name):
  expiration_date = domain_name.expiration_date
  if isinstance(expiration_date,str):
    try:
      expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
    except:
      return 1
  if (expiration_date is None):
      return 1
  elif (type(expiration_date) is list):
      return 1
  else:
    today = datetime.now()
    end = abs((expiration_date - today).days)
    if ((end/30) < 6):
      end = 0
    else:
      end = 1
  return end

# 7. TinyURL check
def tinyURL(url):
    return 1 if re.search(shortening_services, url) else 0

# 8. Prefix/Suffix '-' in domain
def prefixSuffix(url):
    return 1 if '-' in urlparse(url).netloc else 0

# 9. Domain end (using WHOIS object)
def getDomain(url):  
    domain = urlparse(url).netloc
    if re.match(r"^www.", domain):
        domain = domain.replace("www.", "")
    return domain

# 10. Age of domain (using WHOIS object)
def domainAge(domain_name):
    creation_date = domain_name.creation_date
    expiration_date = domain_name.expiration_date
    try:
        if isinstance(creation_date, str): creation_date = datetime.strptime(creation_date, '%Y-%m-%d')
        if isinstance(expiration_date, str): expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d')
        if not creation_date or not expiration_date: return 1
        if isinstance(creation_date, list): creation_date = creation_date[0]
        if isinstance(expiration_date, list): expiration_date = expiration_date[0]
        age = abs((expiration_date - creation_date).days)
        return 1 if age / 30 < 6 else 0
    except:
        return 1

# FEATURE EXTRACTION FUNCTION
def feature_extraction(url, whois_response):
    features = []
    #Adress bar based features - 8 features
    #features.append(getDomain(url))
    features.append(havingIP(url))
    features.append(haveAtSign(url))
    features.append(prefixSuffix(url))
    features.append(tinyURL(url))
    features.append(redirection(url))
    features.append(getDepth(url))
    features.append(getLength(url))

    #Domain based features(dbf) - 3 features
    dbf = 0
    try:
        domain_name = whois.whois(urlparse(url).netloc)
    except:
        dbf = 1

    features.append(dbf)
    features.append(1 if dbf ==1 else domainAge(domain_name))
    features.append(1 if dbf == 1 else domainEnd(domain_name))

    return features
