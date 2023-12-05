import requests
from bs4 import BeautifulSoup

def generate_seo_audit_report(url):
    # Initialize the report structure
    report = {
        "success": False,
        "message": "",
        "result": {}
    }

    try:
        # Fetch page content
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        html_content = response.text

        # Parse HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Basic report information
        report["success"] = True
        report["message"] = "Report Generated Successfully"
        report["result"]["Input"] = {"URL": url, "Input type": "Domain"}

        # HTTP Information
        report["result"]["http"] = {
            "status": response.status_code,
            "using_https": url.startswith("https"),
            "contentSize": {
                "bytes": len(response.content),
                "kb": len(response.content) / 1024
            },
            "headers": dict(response.headers),
            "redirections": len(response.history) > 0,
            "responseTime": f"{response.elapsed.total_seconds():.6f} seconds"
        }

        # Title Information
        title_tag = soup.find('title')
        report["result"]["title"] = {
            "found": "Found" if title_tag else "Not Found",
            "data": title_tag.text if title_tag else "",
            "length": len(title_tag.text) if title_tag else 0,
            "characters": len(title_tag.text) if title_tag else 0,
            "words": len(title_tag.text.split()) if title_tag else 0,
            "charPerWord": len(title_tag.text) / len(title_tag.text.split()) if title_tag and len(title_tag.text.split()) > 0 else 0,
            "tag number": 1 if title_tag else 0
        }

        # ... (Include other sections like Meta Description, Metadata Info, Page Headings, Word Count, Links Summary, Images Analysis, etc.)

        return report

    except requests.exceptions.RequestException as e:
        report["message"] = str(e)
        return report

# Prompt user for URL input
url_to_audit = input("Enter the URL to audit: ").strip()

# Check if the URL is not empty
if not url_to_audit:
    print("URL cannot be empty.")
else:
    # Generate SEO audit report for the provided URL
    audit_report = generate_seo_audit_report(url_to_audit)

    # Print the generated JSON report
    import json
    print(json.dumps(audit_report, indent=2))
