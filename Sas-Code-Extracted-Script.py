import re
import json

def extract_sas_functions(file_path, output_json):
    patterns = {
        "proc": re.compile(r'(?i)(proc\s+\w+).*?(quit;)', re.DOTALL),
        "datalines": re.compile(r'(?i)(datalines;).*?(;\s*run;)', re.DOTALL),
        "data_step": re.compile(r'(?i)(data\s+\w+;).*?(run;)', re.DOTALL),
        "macro": re.compile(r'(?i)(%macro\s+\w+).*?(%mend\s+\w+;)', re.DOTALL),
        "call_execute": re.compile(r'(?i)(call\s+execute\(.*?\);)', re.DOTALL),
        "sql_exec": re.compile(r'(?i)(execute\s*\(.*?\)\s*by\s+sql;)', re.DOTALL),
        "proc_sort": re.compile(r'(?i)(proc\s+sort\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_means": re.compile(r'(?i)(proc\s+means\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_freq": re.compile(r'(?i)(proc\s+freq\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_report": re.compile(r'(?i)(proc\s+report\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_tabulate": re.compile(r'(?i)(proc\s+tabulate\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_reg": re.compile(r'(?i)(proc\s+reg\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_glm": re.compile(r'(?i)(proc\s+glm\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_sql": re.compile(r'(?i)(proc\s+sql;).*?(quit;)', re.DOTALL),
        "proc_print": re.compile(r'(?i)(proc\s+print\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_univariate": re.compile(r'(?i)(proc\s+univariate\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_corr": re.compile(r'(?i)(proc\s+corr\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_anova": re.compile(r'(?i)(proc\s+anova\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_transpose": re.compile(r'(?i)(proc\s+transpose\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_rank": re.compile(r'(?i)(proc\s+rank\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_ttest": re.compile(r'(?i)(proc\s+ttest\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_cluster": re.compile(r'(?i)(proc\s+cluster\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_factor": re.compile(r'(?i)(proc\s+factor\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_stepwise": re.compile(r'(?i)(proc\s+stepwise\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_logistic": re.compile(r'(?i)(proc\s+logistic\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_mixed": re.compile(r'(?i)(proc\s+mixed\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_phreg": re.compile(r'(?i)(proc\s+phreg\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_npar1way": re.compile(r'(?i)(proc\s+npar1way\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_lifetest": re.compile(r'(?i)(proc\s+lifetest\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_surveyreg": re.compile(r'(?i)(proc\s+surveyreg\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_surveymeans": re.compile(r'(?i)(proc\s+surveymeans\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_surveyfreq": re.compile(r'(?i)(proc\s+surveyfreq\s+data=.*?;).*?(run;)', re.DOTALL),
        "proc_surveylogistic": re.compile(r'(?i)(proc\s+surveylogistic\s+data=.*?;).*?(run;)', re.DOTALL)
    }
    
    functions = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
        for key, pattern in patterns.items():
            matches = pattern.findall(content)
            for match in matches:
                function_code = "\n".join(match) if isinstance(match, tuple) else match
                functions.append({key: function_code.strip()})
    
    # Store extracted functions in JSON file
    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(functions, json_file, indent=4)

# Usage
sas_file = "sas_code.sas"  # Replace with your SAS file path
output_file = "sas_functions.json"
extract_sas_functions(sas_file, output_file)
print(f"Extracted SAS functions saved to {output_file}")
