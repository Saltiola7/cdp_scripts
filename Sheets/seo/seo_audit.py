import webbrowser

# Define your URL here
query = "grm-services.fi"

# URLs to be opened
builtwith_url = f"https://builtwith.com/{query}"
pagespeed_url = f"https://pagespeed.web.dev/analysis?url=https%3A%2F%2F{query}%2F"
ahrefs_url = f"https://ahrefs.com/traffic-checker/?input={query}&mode=subdomains"
#semrush_url = f"https://www.semrush.com/analytics/overview/?q=https%3A%2F%2F{query}%2F&protocol=https&searchType=domain"

# Open URLs in the default web browser
webbrowser.open(builtwith_url)
webbrowser.open(pagespeed_url)
webbrowser.open(ahrefs_url)
#webbrowser.open(semrush_url)

