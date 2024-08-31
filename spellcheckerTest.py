import re
from spellchecker import SpellChecker
import sys

# Initialize the spell checker
spell = SpellChecker()

# Regular expressions to match variable names and strings
string_pattern = re.compile(r'(["\'])(?:(?=(\\?))\2.)*?\1')


def extract_tokens_from_code(code):
    """Extract all tokens that should be spell-checked, excluding strings."""
    # Remove strings from the code
    code_without_strings = re.sub(string_pattern, '', code)

    # Extract all words that are not Python keywords or built-in functions
    tokens = re.findall(r'\b[A-Za-z_][A-Za-z0-9_]*\b', code_without_strings)
    return tokens


def check_spelling_in_code(code):
    """Check for spelling mistakes in the code."""
    tokens = extract_tokens_from_code(code)
    misspelled = spell.unknown(tokens)

    return misspelled


def check_files_in_pr(file_paths):
    """Check spelling in all Python files included in the PR."""
    misspelled_words = {}

    for file_path in file_paths:
        if file_path.endswith('.py'):
            with open(file_path, 'r', encoding='utf-8') as file:
                code = file.read()
                misspelled = check_spelling_in_code(code)
                if misspelled:
                    misspelled_words[file_path] = misspelled

    return misspelled_words


if __name__ == "__main__":
    # List of files changed in the PR
    pr_files = sys.argv[1:]

    # Run spell check on PR files
    misspelled_words = check_files_in_pr(pr_files)

    if misspelled_words:
        for file, words in misspelled_words.items():
            print(f"Misspelled words in {file}: {', '.join(words)}")
        sys.exit(1)  # Exit with error code to indicate failure in CI/CD
    else:
        print("No spelling mistakes found!")
        sys.exit(0)  # Exit with success code
