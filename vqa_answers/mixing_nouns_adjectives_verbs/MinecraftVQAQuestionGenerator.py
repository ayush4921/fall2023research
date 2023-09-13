import pandas as pd
import random


class MinecraftVQAQuestionGenerator:
    def __init__(self, noun_csv, adj_csv, verb_csv):
        # Read the CSV files
        self.nouns = pd.read_csv(
            open(noun_csv, "r", encoding="utf-8", errors="ignore")
        )["Word"].tolist()
        self.adjectives = pd.read_csv(
            open(adj_csv, "r", encoding="utf-8", errors="ignore")
        )["Word"].tolist()
        self.verbs = pd.read_csv(
            open(verb_csv, "r", encoding="utf-8", errors="ignore")
        )["Word"].tolist()

        # Default templates for questions
        self.templates = {
            "adj_noun": "Is the [noun] [adj]?",
            "noun_verb": "Can the [noun] [verb]?",
        }

    def set_templates(self, new_templates):
        """Configure custom templates"""
        self.templates = new_templates

    def generate_questions(self, num_questions=50):
        """Generate questions based on the given number of questions"""
        questions = []
        for _ in range(num_questions):
            # Randomly choose a template
            template_type, template = random.choice(list(self.templates.items()))

            if template_type == "adj_noun":
                noun = random.choice(self.nouns)
                adj = random.choice(self.adjectives)
                question = template.replace("[noun]", noun).replace("[adj]", adj)
            elif template_type == "noun_verb":
                noun = random.choice(self.nouns)
                verb = random.choice(self.verbs)
                question = template.replace("[noun]", noun).replace("[verb]", verb)

            questions.append(question)

        # Convert to DataFrame and save as CSV
        df = pd.DataFrame(questions, columns=["Questions"])
        return df


# Initialize the class with CSV filenames
noun_csv = "NOUN.csv"
adj_csv = "ADJ.csv"
verb_csv = "VERB.csv"

# Create an instance of the MinecraftVQAQuestionGenerator class
question_generator = MinecraftVQAQuestionGenerator(noun_csv, adj_csv, verb_csv)

# Generate 10 sample questions using the default templates
sample_questions = question_generator.generate_questions(num_questions=10)
sample_questions.to_csv("sample_questions_default_templates.csv", index=False)

# Create custom templates
custom_templates = {
    "adj_noun": "Does the [noun] appear [adj]?",
    "noun_verb": "Would the [noun] be able to [verb]?",
}

# Configure the question generator with custom templates
question_generator.set_templates(custom_templates)

# Generate 10 sample questions using custom templates
sample_questions_custom = question_generator.generate_questions(num_questions=10)
sample_questions_custom.to_csv("sample_questions_custom_templates.csv", index=False)
