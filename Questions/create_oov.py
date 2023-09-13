import json
import pandas as pd
import spacy
from spacy.lang.en import STOP_WORDS

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")


def replace_words_with_tags(sentence):
    """
    Use spaCy to replace nouns with [noun], adjectives with [adj], and verbs with [verb].
    """
    doc = nlp(sentence)

    new_tokens = []
    for token in doc:
        if (
            token.pos_ == "NOUN"
            and token.text.lower() not in STOP_WORDS
            and token.text.lower() != "color"
        ):
            new_tokens.append("[noun]")
        elif (
            token.pos_ == "ADJ"
            and token.text.lower() not in STOP_WORDS
            and token.text.lower() != "color"
        ):
            new_tokens.append("[adj]")
        elif (
            token.pos_ == "VERB"
            and token.text.lower() not in STOP_WORDS
            and token.text.lower() != "color"
        ):
            new_tokens.append("[verb]")
        else:
            new_tokens.append(token.text)

    return " ".join(new_tokens)


def process_questions(data, num_questions=None):
    """
    Process the questions in the given dataset using spaCy.
    """
    if num_questions:
        data["questions"] = data["questions"][:num_questions]

    for q in data["questions"]:
        q["replaced_question"] = replace_words_with_tags(q["question"])
    return data


def load_dataset(path):
    """
    Load dataset from a given JSON path.
    """
    with open(path, "r") as file:
        data = json.load(file)
    return data


def save_to_csv(data, output_path):
    """
    Save the processed data to CSV after removing duplicates based on the replaced question text.
    """
    df = pd.DataFrame(data["questions"])
    df = df[["question", "replaced_question"]]
    df["NOUN"], df["ADJ"], df["VERB"] = "", "", ""
    df.drop_duplicates(subset="replaced_question", keep="first", inplace=True)
    df.to_csv(output_path, index=False)


def main(num_questions=None):
    train_data_path = "OpenEnded_mscoco_train2014_questions.json"
    val_data_path = "OpenEnded_mscoco_val2014_questions.json"

    print("Loading datasets...")
    train_data = load_dataset(train_data_path)
    val_data = load_dataset(val_data_path)

    print(f"Processing {num_questions if num_questions else 'all'} train questions...")
    processed_train_data = process_questions(train_data, num_questions)

    print(
        f"Processing {num_questions if num_questions else 'all'} validation questions..."
    )
    processed_val_data = process_questions(val_data, num_questions)

    print("Saving processed train questions to CSV...")
    save_to_csv(processed_train_data, "processed_train_questions.csv")

    print("Saving processed validation questions to CSV...")
    save_to_csv(processed_val_data, "processed_val_questions.csv")

    print("Processing complete!")


if __name__ == "__main__":
    desired_num_questions = 1000  # Change this to the number of questions you want or None for all questions
    main(desired_num_questions)
