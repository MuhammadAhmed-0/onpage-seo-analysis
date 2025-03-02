import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import subprocess
from urllib.parse import urlparse

# Function to check if a URL is accessible
def check_url(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Function to fetch the HTML content of the page
def get_html_content(url):
    response = requests.get(url, timeout=5)
    return response.text

# SEO Element Analysis function
def analyze_seo_elements(url):
    html = get_html_content(url)
    soup = BeautifulSoup(html, "lxml")

    title = soup.title.string if soup.title else "No title tag found"
    meta_description = soup.find("meta", attrs={"name": "description"})
    meta_description_content = meta_description["content"] if meta_description else "No meta description found"

    h1_tag = soup.find("h1")
    h1_content = h1_tag.string.strip() if h1_tag else "No H1 tag found"

    h2_tags = soup.find_all("h2")
    h2_contents = [h2.get_text(strip=True) for h2 in h2_tags] if h2_tags else ["No H2 tags found"]

    images_without_alt = [img["src"] for img in soup.find_all("img") if not img.get("alt")]

    robots_txt = f"{urlparse(url).scheme}://{urlparse(url).hostname}/robots.txt"
    sitemap_xml = f"{urlparse(url).scheme}://{urlparse(url).hostname}/sitemap.xml"

    return {
        "title": title,
        "meta_description": meta_description_content,
        "h1": h1_content,
        "h2": h2_contents,
        "images_without_alt": images_without_alt or ["None"],
        "robots_txt": check_url(robots_txt),
        "sitemap_xml": check_url(sitemap_xml)
    }

# Function to analyze page performance using Lighthouse
def analyze_lighthouse(url):
    try:
        command = f"lighthouse {url} --quiet --output=json --output-path=stdout"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            return None, None, None
        
        lighthouse_result = json.loads(result.stdout)
        performance_score = lighthouse_result['categories']['performance']['score'] * 100
        seo_score = lighthouse_result['categories']['seo']['score'] * 100
        mobile_friendly_score = lighthouse_result.get('categories', {}).get('pwa', {}).get('score', 0) * 100

        return performance_score, seo_score, mobile_friendly_score
    except Exception:
        return None, None, None

# Function to generate and save the SEO report
def generate_seo_report(url):
    if not check_url(url):
        return "Error: Unable to access the URL.", None

    seo_elements = analyze_seo_elements(url)
    performance_score, seo_score, mobile_friendly_score = analyze_lighthouse(url)

    report = {
        "Title": seo_elements['title'],
        "Meta Description": seo_elements['meta_description'],
        "H1": seo_elements['h1'],
        "H2 Tags": ", ".join(seo_elements['h2']),
        "Images without ALT": ", ".join(seo_elements['images_without_alt']),
        "Robots.txt Available": "Yes" if seo_elements['robots_txt'] else "No",
        "Sitemap.xml Available": "Yes" if seo_elements['sitemap_xml'] else "No",
        "Performance Score": f"{performance_score}%" if performance_score else "N/A",
        "SEO Score": f"{seo_score}%" if seo_score else "N/A",
        "Mobile Friendly Score": f"{mobile_friendly_score}%" if mobile_friendly_score else "N/A",
    }

    report_filename = f"seo_report_{urlparse(url).hostname}.txt"
    with open(report_filename, "w") as file:
        file.write(json.dumps(report, indent=4))

    return report, report_filename

# Streamlit UI code starts here
def run_streamlit_ui():
    st.title("🔍 Onpage SEO Analysis Tool")

    url_to_analyze = st.text_input("Enter the URL to analyze:", "")

    if not url_to_analyze:
        st.info("Please enter a URL to get started.")

    if st.button('Analyze'):
        if url_to_analyze:
            st.write(f"🔎 **Analyzing SEO elements for:** {url_to_analyze}")

            result, report_filename = generate_seo_report(url_to_analyze)

            if isinstance(result, dict):
                st.subheader("📊 SEO Analysis Results")

                st.write(f"**Title Tag:** `{result['Title']}`")
                st.write(f"**Meta Description:** `{result['Meta Description']}`")
                st.write(f"**H1 Tag:** `{result['H1']}`")
                st.write(f"**H2 Tags:** `{result['H2 Tags']}`")
                st.write(f"**Images without ALT Text:** `{result['Images without ALT']}`")
                st.write(f"**Robots.txt Available:** `{result['Robots.txt Available']}`")
                st.write(f"**Sitemap.xml Available:** `{result['Sitemap.xml Available']}`")

                # Display Lighthouse Scores in a table
                st.subheader("📈 Lighthouse Scores")
                scores_data = {
                    "Metric": ["Performance Score", "SEO Score", "Mobile Friendly Score"],
                    "Value": [result['Performance Score'], result['SEO Score'], result['Mobile Friendly Score']]
                }
                st.table(scores_data)

                # Provide the option to download the SEO report file
                with open(report_filename, "r") as file:
                    st.download_button(
                        label="📥 Download SEO Report",
                        data=file,
                        file_name=report_filename,
                        mime="text/plain"
                    )
            else:
                st.error(result)
        else:
            st.error("Please provide a valid URL.")

# Run the Streamlit app
if __name__ == "__main__":
    run_streamlit_ui()
