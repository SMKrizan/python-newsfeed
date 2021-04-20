# format_date() expects to receive a datetime object and then use the strftime() method to convert to a string; '%m/%d/%y' converts to ~"01/01/20"
def format_date(date):
  return date.strftime('%m/%d/%y')

# removes all extraneous information from a URL string, leaving only domain name
def format_url(url):
  return url.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0].split('?')[0]

# correctly pluralizes words
def format_plural(amount, word):
  if amount != 1:
    return word + 's'

  return word