# Minecraft VQA Dataset Generation Approach

This README outlines the development strategies employed to create a specialized Visual Question Answering (VQA) dataset based on the Minecraft environment. .

## Table of Contents
1. [Changing Existing Questions](#changing-existing-questions)
2. [Mixing Nouns with Adjectives and Verbs](#mixing-nouns-with-adjectives-and-verbs)
3. [Utilizing Minecraft-specific Vocabulary](#utilizing-minecraft-specific-vocabulary)
4. [Leveraging Language Models](#leveraging-language-models)
5. [Drawbacks](#drawbacks)
6. [Potential Solutions](#potential-solutions)

---

## Changing Existing Questions

An existing VQA dataset is adapted as a starting point for this project. The questions are customized to suit the Minecraft universe.

### Strategies for Adaptation
- **Rewording**: Transform questions to relate to Minecraft.  
  *Example*: "What color is the car?" → "What color is the wool?"
  
- **Contextual Changes**: Modify the context to fit Minecraft.  
  *Example*: "How many people are in the room?" → "How many villagers are in the village?"
  
- **Complex Alterations**: Alter questions to reflect Minecraft-specific elements.  
  *Example*: "Is the person wearing a hat?" → "Is the character wearing a helmet?"

[Back to Top](#table-of-contents)

---

## Mixing Nouns with Adjectives and Verbs

The dataset is enriched using a template-based question generation method. We got the Nouns, Adjectives, and Verbs from minewiki.

### Template Examples:
- "Is the [noun] [adjective]?"
- "Can the [noun] [verb]?"

### Example Questions
- "Is the creeper hostile?"
- "Can the player fly?"

### High-Level Architecture
- Read CSV files containing nouns, adjectives, and verbs.
- Generate questions based on templates.
- Save generated questions as a CSV file.
### How to Run
- Place the CSV files (NOUN.csv, ADJ.csv, VERB.csv) in the vqa_answers/mixing_nouns_adjectives_verbs.
- Run the Python script MinecraftVQAQuestionGenerator.py
- The generated questions will be saved in a CSV file named sample_questions.csv.

[Back to Top](#table-of-contents)

---

## Utilizing Minecraft-specific Vocabulary

The dataset leverages the unique terminology found in Minecraft, generating questions that often have binary ("yes" or "no") answers.

### Example Questions
- "Is Redstone used for crafting?"
- "Can Endermen teleport?"

### High-Level Architecture

- Read a CSV file containing Minecraft mobs and their categories.
- Filter categories to include only verbs or adjectives, or both, based on NLTK's WordNet.
- Generate questions using templates.
- Save generated questions as a CSV file.

### How to Run
- Place the CSV file (minecraft_mobs.csv) in the minecraft_specific_vocabulary folder.
- Run the Python script mob_questions_list.py.
- The generated questions will be saved in a CSV file named minecraft_mob_vqa_questions.csv.

[Back to Top](#table-of-contents)

---

## Leveraging Language Models

Advanced Language Models like GPT-4 can be fine-tuned on Minecraft-specific text to ensure more accurate and contextually relevant question generation.

[Back to Top](#table-of-contents)

---

## Drawbacks

### Validity of Questions

A significant drawback is the uncertain validity of the generated questions. As the questions are programatically generated, there is no assurance that all questions will be contextually accurate or relevant.

[Back to Top](#table-of-contents)

---

## Potential Solutions

To address the validity concern, one potential solution is to run all generated questions through a Language Model that has been fine-tuned on Minecraft-specific data. This could filter out or modify irrelevant questions to better fit the game's context.

[Back to Top](#table-of-contents)
