import pytest
import json
from exporters.export_analyze import Export

def test_print_console(capfd):
    result = {
        "orginal_text": "apple banana apple",
        "cleaned_text": "apple banana apple",
        "words_count": 3,
        "chars_count": 17,
        "words_length_avg": 5.6667,
        "popular_word": "apple",
        "top_popular_words": ["apple", "banana"],
        "support_clean": True,
        "support_statistics": True
    }

    exporter = Export()
    exporter.print_console(result)

    # Objection to the findings
    out, err = capfd.readouterr()

    # Check for key parts in the output
    assert "----------------text before clean --------------------" in out
    assert "apple banana apple" in out
    assert "----------------text after clean --------------------" in out
    assert "----------------statistics --------------------" in out
    assert "words count in text :  3" in out
    assert "characters count in text :  17" in out
    assert "Popular word in text :  apple" in out
    assert "Top Popular words in text :  ['apple', 'banana']" in out
    assert "Words length average:  5.6667" in out



def test_export_csv(tmp_path):
    exporter = Export(output_dir=tmp_path)  # Using a temporary folder
    result = {
        "file_number": 1,
        "top_popular_words": ["apple", "banana", "cherry"]
    }

    # Implementation
    exporter.export_csv(result)

    # Verify that the file has been created
    file_path = tmp_path / "file-1top_popular_words.csv"
    assert file_path.exists()

    # Check the file contents
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    
    assert lines[0] == "Top Popular Words"
    assert lines[1:] == ["apple", "banana", "cherry"]



def test_export_json(tmp_path):
    exporter = Export(output_dir=tmp_path)
    result = {
        "file_number": 1,
        "orginal_text": "apple banana apple",
        "cleaned_text": "apple banana apple",
        "words_count": 3,
        "chars_count": 17,
        "words_length_avg": 5.6667,
        "popular_word": "apple",
        "top_popular_words": ["apple", "banana"]
    }

    exporter.export_json(result)

    # Check the file creation
    file_path = tmp_path / "file-1_analyzer_outputs.json"
    assert file_path.exists()

    # Check the file content
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data == result