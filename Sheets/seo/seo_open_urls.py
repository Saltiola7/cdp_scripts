import subprocess

# List of URLs you want to open
urls = [
    "https://www.example1.com",
    "https://www.example2.com",
    "https://www.example3.com",
    # Add more URLs as needed
]

# Open each URL in the Arc browser using the `open` command
for url in urls:
    subprocess.run(["open", "-a", "Arc", url], check=True)
