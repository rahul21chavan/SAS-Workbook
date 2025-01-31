import re
import json
import os

def extract_sas_blocks_from_file(file_path, main_output_json, macro_output_json):
    # Define regex patterns for different SAS code blocks
    patterns = {
        "proc_sql": re.compile(r'(?i)(proc\s+sql;.*?quit;)', re.DOTALL),
        "proc_sql_noprint": re.compile(r'(?i)(proc\s+sql\s+noprint;.*?quit;)', re.DOTALL),
        "data_step": re.compile(r'(?i)(data\s+\w+;.*?run;)', re.DOTALL),
        "proc_means": re.compile(r'(?i)(proc\s+means\s+data=.*?;.*?run;)', re.DOTALL),
        "proc_print": re.compile(r'(?i)(proc\s+print\s+data=.*?;.*?run;)', re.DALL),
        "proc_freq": re.compile(r'(?i)(proc\s+freq\s+data=.*?;.*?run;)', re.DOTALL),
        "proc_transpose": re.compile(r'(?i)(proc\s+transpose\s+data=.*?;.*?run;)', re.DOTALL),
    }

    # Define regex for macro block capturing everything from %macro to %mend
    macro_pattern = r'(?i)(%macro\s+\w+.*?%mend\s+\w+;)'  # Match entire macro block

    # Initialize list to store extracted blocks
    extracted_blocks = []
    macro_content = None

    # Read the SAS script from the provided file path
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading the file: {e}")
        return

    # Find and store the entire macro block (starting with %macro and ending with %mend)
    macro_match = re.search(macro_pattern, content, re.DOTALL)
    if macro_match:
        macro_content = macro_match.group(0).strip()  # Store the full macro content

    # Extract other blocks (non-macro)
    for key, pattern in patterns.items():
        matches = pattern.findall(content)
        for match in matches:
            extracted_blocks.append({key: match.strip()})

    # Save the extracted non-macro blocks to the main JSON file
    try:
        with open(main_output_json, 'w', encoding='utf-8') as json_file:
            json.dump(extracted_blocks, json_file, indent=4)
        print(f"Extracted non-macro SAS blocks saved to {main_output_json}")
    except Exception as e:
        print(f"Error writing to the output file: {e}")

    # If there is a macro block, save it to a separate JSON file
    if macro_content:
        try:
            # Extract the macro name dynamically from the %macro line
            macro_name_match = re.search(r'(?i)%macro\s+(\w+)', macro_content)
            if macro_name_match:
                macro_name = macro_name_match.group(1)
                macro_json_path = os.path.join(os.path.dirname(main_output_json), f"{macro_name}_macro.json")
                with open(macro_json_path, 'w', encoding='utf-8') as macro_json_file:
                    json.dump({"macro": macro_content}, macro_json_file, indent=4)
                print(f"Macro content saved to {macro_json_path}")
        except Exception as e:
            print(f"Error writing the macro file: {e}")

# Usage:
# Replace with the path or link to your SAS script file
sas_script_link = "/path/to/your/sas_script.sas"  # Replace with your actual SAS file path
main_output_file = "/path/to/your/main_output_file.json"  # Main JSON for non-macro SAS blocks
macro_output_file = "/path/to/your/macro_output_file.json"  # Optional if you want to test separate files

# Extract SAS blocks from the provided script and save to JSON
extract_sas_blocks_from_file(sas_script_link, main_output_file, macro_output_file)
