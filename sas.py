import re
import json

def extract_sas_blocks(file_path, output_json):
    # Define regex patterns for different SAS code blocks
    patterns = {
        "proc_sql": re.compile(r'(?i)(proc\s+sql;.*?quit;)', re.DOTALL),
        "proc_sql_noprint": re.compile(r'(?i)(proc\s+sql\s+noprint;.*?quit;)', re.DOTALL),
        "data_step": re.compile(r'(?i)(data\s+\w+;.*?run;)', re.DOTALL),
        "proc_means": re.compile(r'(?i)(proc\s+means\s+data=.*?;.*?run;)', re.DOTALL),
        "proc_print": re.compile(r'(?i)(proc\s+print\s+data=.*?;.*?run;)', re.DOTALL),
        "proc_freq": re.compile(r'(?i)(proc\s+freq\s+data=.*?;.*?run;)', re.DOTALL),
        "proc_transpose": re.compile(r'(?i)(proc\s+transpose\s+data=.*?;.*?run;)', re.DOTALL),
        "macro": re.compile(r'(?i)(%macro\s+\w+.*?%mend\s+\w+;)', re.DOTALL)
    }

    extracted_blocks = []

    # Read the SAS file and search for the code blocks
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        # Find and store all matches for each pattern
        for key, pattern in patterns.items():
            matches = pattern.findall(content)
            for match in matches:
                extracted_blocks.append({key: match.strip()})

    # Save the extracted blocks to a JSON file
    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(extracted_blocks, json_file, indent=4)

    print(f"Extracted SAS blocks saved to {output_json}")


# Update with your file paths
sas_script_link = "/path/to/your/sas_script.sas"  # Replace with the link to your SAS script file
output_file = "/path/to/your/output_file.json"  # Replace with your desired output path

# Extract SAS blocks from the provided script and save to JSON
extract_sas_blocks(sas_script_link, output_file)
