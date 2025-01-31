import re
import json


def generate_sample_sas_file(file_path):
    # Sample SAS code to generate
    sample_sas_code = """
    proc sql;
        create table work.test as
        select * from sashelp.class;
    quit;

    data example;
        set sashelp.class;
        age2 = age * 2;
    run;

    proc means data=work.test;
        var age;
    run;

    proc print data=work.test;
    run;

    proc freq data=sashelp.class;
        tables age;
    run;

    proc sql noprint;
        create table work.sum as
        select mean(age) as avg_age from sashelp.class;
    quit;

    proc transpose data=sashelp.class out=transposed;
    var age;
    run;

    %macro calculate_age(age);
        %let new_age = %eval(&age * 2);
        &new_age
    %mend calculate_age;
    """
    # Write the sample SAS code to the given file path
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(sample_sas_code)


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


# Run the test
test_sas_file = "sample_test.sas"
output_file = "extracted_sas_blocks.json"
generate_sample_sas_file(test_sas_file)
extract_sas_blocks(test_sas_file, output_file)
