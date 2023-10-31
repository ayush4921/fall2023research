import whisper
import csv
import argparse
from nltk.tokenize import sent_tokenize


def extract_questions_and_answers(sentences):
    """
    Extracts questions and their corresponding answers from a given list of sentences.

    Args:
    - sentences (list): List of sentences from the transcript.

    Returns:
    - list: A list of (question, answer) pairs.
    """
    qa_pairs = []

    for i, sentence in enumerate(sentences):
        stripped_sentence = sentence.strip()
        if stripped_sentence.endswith("?"):
            question = stripped_sentence
            answer = sentences[i + 1].strip() if i + 1 < len(sentences) else ""
            qa_pairs.append((question, answer))

    return qa_pairs


def save_to_csv(data, filename, question_answer_pair=False):
    """
    Saves data to a CSV file.

    Args:
    - data (list): A list of data to save. Can be a list of strings or a list of pairs.
    - filename (str): The name of the CSV file.
    - question_answer_pair (bool): Whether the data is a list of question-answer pairs.
    """
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if question_answer_pair:
            writer.writerow(["Question", "Answer"])
            for pair in data:
                writer.writerow(pair)
        else:
            writer.writerow(["Transcript"])
            for item in data:
                writer.writerow([item])


def main():
    parser = argparse.ArgumentParser(
        description="Extract questions and answers from an audio file and save them to a CSV."
    )
    parser.add_argument("audio_file", help="Path to the audio file.")
    parser.add_argument(
        "-s",
        "--speech",
        default="speech.csv",
        help="Name of the output file for the entire speech to text. Default is 'speech.csv'.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output.csv",
        help="Name of the output CSV file. Default is 'output.csv'.",
    )

    args = parser.parse_args()

    # Load the model and transcribe the audio
    model = whisper.load_model("medium")
    print("Transcribing the file")
    result = model.transcribe(args.audio_file)
    text = result["text"]
    sentences = sent_tokenize(text)
    # save the entire transcript
    save_to_csv(sentences, args.speech)
    # Extract questions and answers
    qa_pairs = extract_questions_and_answers(sentences)
    # Save to CSV
    save_to_csv(qa_pairs, args.output, question_answer_pair=True)
    print(
        f"Saved questions and answers to {args.output} and the transcript to {args.speech}"
    )


if __name__ == "__main__":
    main()
