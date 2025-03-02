# Onpage SEO Analysis Tool

🔍 **Onpage SEO Analysis Tool** is a powerful web tool built using **Streamlit** and **Python** to analyze and report SEO elements of any webpage. It helps you evaluate key SEO metrics, such as title tags, meta descriptions, H1/H2 tags, images without ALT text, and more. Additionally, the tool integrates **Lighthouse** to provide performance, SEO, and mobile-friendliness scores.

## Features

- **URL Analysis**: Checks if the provided URL is accessible.
- **SEO Element Analysis**: Retrieves and analyzes important SEO elements like:
  - Title Tag
  - Meta Description
  - H1 Tag
  - H2 Tags
  - Images without ALT Text
  - Robots.txt availability
  - Sitemap.xml availability
- **Lighthouse Scores**: Provides performance, SEO, and mobile-friendliness scores using Lighthouse.
- **Download SEO Report**: Allows you to download a detailed SEO analysis report in a `.txt` file.

## Prerequisites

To run this project locally, you'll need:

- **Python 3.x**
- **Streamlit**: To run the UI.
- **Lighthouse**: To generate the performance and SEO scores.

### Install required dependencies

1. Clone this repository:

    ```bash
    git clone https://github.com/your-username/seo-analysis-tool.git
    cd seo-analysis-tool
    ```

2. Install the required Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Install **Lighthouse** (if you don't have it installed):

    Follow the installation guide here: [https://developers.google.com/web/tools/lighthouse](https://developers.google.com/web/tools/lighthouse)

## Results
![image](https://github.com/user-attachments/assets/41e1cd19-30cc-4ce4-afda-b0f33e42b525)


## How to Use

### 1. Run the Streamlit App

After installing the dependencies, you can run the app locally using the following command:

```bash
streamlit run app.py
