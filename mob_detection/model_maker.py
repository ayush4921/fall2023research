import os

import torch
from datasets import load_dataset
from PIL import Image
from transformers import (
    AutoImageProcessor,
    AutoModelForObjectDetection,
    DetrForObjectDetection,
    DetrImageProcessor,
    Trainer,
    TrainingArguments,
)

# Load the dataset from the CSV files

dataset = load_dataset(
    "csv",
    data_files={
        "train": "minecraft_tensorflow/test/_annotations.csv",
        "test": "minecraft_tensorflow/train/_annotations.csv",
        "validation": "minecraft_tensorflow/valid/_annotations.csv",
    },
)


dataset["train"] = dataset["train"].select(range(10))
dataset["test"] = dataset["test"].select(range(10))
dataset["validation"] = dataset["validation"].select(range(10))
# to only limit it to the first 10 values to see if it trains it.
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")


def process_data_to_model_inputs(example):
    # Load image
    try:
        image = Image.open(
            os.path.join(
                os.getcwd(), "minecraft_tensorflow", "test", example["filename"]
            )
        )
    except:
        try:
            image = Image.open(
                os.path.join(
                    os.getcwd(), "minecraft_tensorflow", "train", example["filename"]
                )
            )
        except:
            image = Image.open(
                os.path.join(
                    os.getcwd(), "minecraft_tensorflow", "valid", example["filename"]
                )
            )

    # Process the image using the processor
    encoding = processor(images=image, return_tensors="pt")
    pixel_values = encoding.pixel_values.squeeze()

    # Extract bounding boxes and labels
    width, height = example["width"], example["height"]
    bbox = [example["xmin"], example["ymin"], example["xmax"], example["ymax"]]
    label = example["class"]

    # Normalize the bounding boxes (to be between 0 and 1)
    bbox = [bbox[0] / width, bbox[1] / height, bbox[2] / width, bbox[3] / height]
    # Convert labels to appropriate format (assuming they are strings here, you can adjust if different)
    # Extract unique classes from the 'class' column of the training dataset
    unique_classes = set(
        list(dataset["train"]["class"])
        + list(dataset["test"]["class"])
        + list(dataset["validation"]["class"])
    )

    # Create a label_to_id dictionary
    label_to_id = {label: idx for idx, label in enumerate(unique_classes)}
    id_to_label = {idx: label for label, idx in label_to_id.items()}

    label = label_to_id[label]

    return {
        "pixel_values": pixel_values,
        "labels": torch.tensor([label]),
        "boxes": torch.tensor([bbox]),
    }


formatted_dataset = dataset.map(process_data_to_model_inputs)

print(formatted_dataset)
checkpoint = "facebook/detr-resnet-50"
image_processor = AutoImageProcessor.from_pretrained(checkpoint)
unique_classes = set(
    list(dataset["train"]["class"])
    + list(dataset["test"]["class"])
    + list(dataset["validation"]["class"])
)

# Create a label_to_id dictionary
label2id = {label: idx for idx, label in enumerate(unique_classes)}
id2label = {idx: label for label, idx in label2id.items()}
model = AutoModelForObjectDetection.from_pretrained(
    checkpoint,
    id2label=id2label,
    label2id=label2id,
    ignore_mismatched_sizes=True,
)

# 1. Initialize the DETR model

# 2. Define training arguments
training_args = TrainingArguments(
    output_dir="./detr_results",
    per_device_train_batch_size=4,  # adjust based on your GPU memory
    num_train_epochs=3,  # number of training epochs
    logging_dir="./logs",
    logging_steps=100,  # log & save weights each logging_steps
    evaluation_strategy="epoch",  # evaluate at the end of each epoch
    save_strategy="epoch",  # save model at the end of each epoch
    push_to_hub=False,
)


for item in formatted_dataset["train"]:
    print(item.keys())


# Define the data collator to batch images
def data_collator(features):
    for feature in features:
        print(feature.keys())
    pixel_values = [feature["pixel_values"] for feature in features]
    labels = [feature["labels"] for feature in features]
    boxes = [feature["boxes"] for feature in features]
    batch = {}
    batch["pixel_values"] = torch.stack(pixel_values)
    batch["labels"] = labels
    batch["boxes"] = boxes
    return batch


# 3. Train with the Trainer class
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=formatted_dataset["train"],
    eval_dataset=formatted_dataset["validation"],  # if you have a validation set
    data_collator=data_collator,
)

trainer.train()

# Save the model
model.save_pretrained("./detr_finetuned")
