import re
import json

def generate_sas_file_from_link(file_path, sas_script_link):
    # Read the SAS script from the given file link and write it to the specified file path
    with open(sas_script_link, 'r', encoding='utf-8') as f:
        sas_code = f.read()

    # Write the content to the given SAS file path
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(sas_code)


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


# Update with your file paths and SAS script link
test_sas_file = "/path/to/your/input_file.sas"  # Replace with your actual file path to save the SAS code
sas_script_link = "/path/to/your/sas_script.sas"  # Replace with the link to your SAS script file
output_file = "/path/to/your/output_file.json"  # Replace with your desired output path

# Generate SAS file from link and extract blocks
generate_sas_file_from_link(test_sas_file, sas_script_link)
extract_sas_blocks(test_sas_file, output_file)
