# README: Minecraft Contextual Question Processing

## Introduction

The objective of this project was to transform a dataset of questions from TDIUC (a visual question answering dataset) to a format suitable for the Minecraft context. This involved replacing parts of speech in the questions and subsequently categorizing them in the context of Minecraft gameplay.

## Steps Undertaken:

### 1. Dataset Preparation:

- Loaded the TDIUC dataset.
- Processed the dataset to replace nouns, adjectives, and verbs with placeholders `[noun]`, `[adj]`, and `[verb]`, respectively.
- Saved the processed questions, which included the original question and the replaced question, into CSV files.

### 2. Contextual Transformation:

- Analyzed the questions to identify potential replacements that would fit into the Minecraft context.
- Categorized the placeholders into various Minecraft-centric categories:

  - **Nouns**: 
    - Mobs (creatures and monsters like creeper, wither)
    - Blocks (building materials like stone, dirt)
    - Items (tools, weapons like sword, pickaxe)
    - Structures (generated buildings or landmarks like village, temple)
    
  - **Verbs (Actions)**: Different actions that players or mobs might perform, e.g., attack, mine, build.
  
  - **Adjectives (Attributes)**: Descriptive words related to items, mobs, or blocks in Minecraft, e.g., enchanted, damaged.

### 3. Category Generation:

- Leveraged the capabilities of large language models (LLMs) to expand on the initial categories and generate exhaustive lists for each Minecraft-centric category.
- Saved these lists as CSV files for further use or integration.
# fall2023research
