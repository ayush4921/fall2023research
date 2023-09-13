import pandas as pd
import random
from nltk.corpus import wordnet


class MinecraftMobVQA:
    def __init__(self, mob_csv, word_type="both"):
        # Read the CSV file containing mobs and their properties
        self.df = pd.read_csv(mob_csv)

        # Extract the mob names
        self.mobs = self.df["Mob"].tolist()

        # Extract the categories and filter them based on word type (verb, adjective, or both)
        self.word_type = word_type
        self.words = self._pool_words(self.df["Categories"], word_type)

        # Pre-defined question templates
        self.templates = {"can_verb": "Can [mob] [verb]?", "is_adj": "Is [mob] [adj]?"}

    def _pool_words(self, categories, word_type):
        """Pool all words together from the Categories column and filter based on word type"""
        words = []
        for category in categories:
            for word in category.split():
                if word_type == "both" or self._check_word_type(word) == word_type:
                    words.append(word)
        return list(set(words))

    # def _check_word_type(self, word):
    #     """Check if a word is a verb or an adjective using NLTK's WordNet"""
    #     word_synsets = wordnet.synsets(word)
    #     for synset in word_synsets:
    #         if "v." in synset.lexname():
    #             return "verb"
    #         elif "adj." in synset.lexname():
    #             return "adj"
    #     return None

    def set_templates(self, new_templates):
        """Set custom templates for generating questions"""
        self.templates = new_templates

    def generate_questions(self, num_questions=50):
        """Generate VQA questions"""
        questions = []
        for _ in range(num_questions):
            # Randomly choose a template
            template_type, template = random.choice(list(self.templates.items()))

            mob = random.choice(self.mobs)
            word = random.choice(self.words)

            if (
                template_type == "can_verb"
            ):  # and self._check_word_type(word) == "verb":
                question = template.replace("[mob]", mob).replace("[verb]", word)
            elif template_type == "is_adj":  # and self._check_word_type(word) == "adj":
                question = template.replace("[mob]", mob).replace("[adj]", word)
            else:
                continue  # Skip this iteration if word type doesn't match template type

            questions.append(question)

        # Convert questions to DataFrame and save as CSV
        df_questions = pd.DataFrame(questions, columns=["Questions"])
        output_csv_path = "minecraft_mob_vqa_questions.csv"
        df_questions.to_csv(output_csv_path, index=False)

        return df_questions, output_csv_path


# Initialize the class with the mob CSV filename
mob_csv = "minecraft_mobs.csv"  # Replace with the path to your CSV file

# Create an instance of the MinecraftMobVQA class
# word_type can be 'verb', 'adj', or 'both'
mob_vqa = MinecraftMobVQA(mob_csv, word_type="both")

# Generate questions (here, generating 10 for demonstration)
df_questions, output_csv_path = mob_vqa.generate_questions(num_questions=10)

# Output the generated questions and path to the saved CSV
print(output_csv_path)
print(df_questions)
