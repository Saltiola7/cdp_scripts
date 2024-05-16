import subprocess
import os

def run_screaming_frog():
    # Define the path to the Screaming Frog SEO Spider CLI
    sf_path = "/Applications/Screaming Frog SEO Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderCli"

    # URL to crawl
    url = "https://hamppufarmi.fi/"

    # Output file path on Desktop
    output_file = os.path.expanduser("~/Desktop/hamppufarmi_crawl.csv")

    # Define the command
    command = [
        sf_path,
        "--headless",
        "--crawl", url,
        "--export-tabs", "Internal:All",
        "--output-folder", os.path.dirname(output_file),
        "--save-crawl"
    ]

    # Run the command
    subprocess.run(command)

    # Rename and move the exported file
    default_export_name = os.path.join(os.path.dirname(output_file), "internal_all.csv")
    if os.path.exists(default_export_name):
        os.rename(default_export_name, output_file)
