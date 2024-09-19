import re
import sys

from spellchecker import SpellChecker
import os

# variable and function calls
variable_assignment_pattern = re.compile(r'\b\w+\s*=\s*.+')
# function_call = re.compile(r'\b\w+\s*\(.*?\)')
method_call_pattern = re.compile(r'\b\w+\.\w+\s*')


def get_file_changes():
    # files modified in PR
    files = os.popen('git diff --name-only HEAD^...HEAD').read().splitlines()
    return files

def extract_text_from_file(file_path):
    # ignoring varibales, function names
    with open(file_path, 'r') as file:
        content = file.read()
        print(content)

        # comments and strings
        content = re.sub(r'#.*', '', content)  # comments
        content = re.sub(r'""".*?"""', '', content, flags=re.DOTALL)  # triple quotes
        content = re.sub(r"'.*?'", '', content)  # remove single quotes
        # content = re.sub(r'".*?"', '', content)  # remove double quotes

        # removing variable names
        content = variable_assignment_pattern.sub('', content)

        # removing function and method calls
        # content = function_call_pattern.sub('', content)
        content = method_call_pattern.sub('', content)

        print(content)
        content = content.replace('def', '')

        return content

def check_spelling_in_file(file_path):
    spell = SpellChecker()
    errors = []

    if not os.path.isfile(file_path):
        print("errors", errors)
        return errors

    content = extract_text_from_file(file_path)
    words = re.findall(r'\b\w+\b', content)

    for word in words:
        if word.lower() not in spell:
            errors.append(word)

    return errors

def run_spelling_checks():
    files = get_file_changes()
    all_errors = {}

    for file in files:
        errors = check_spelling_in_file(file)
        if errors:
            all_errors[file] = errors

    return all_errors

def main():
    errors = run_spelling_checks()
    if not errors:
        print("No spelling errors found.")
    else:
        for file, issues in errors.items():
            print(f"File: {file}")
            for word in issues:
                print(f"Spelling error in {file}: '{word}'")
        sys.exit(1)


if __name__ == "__main__":
    main()
