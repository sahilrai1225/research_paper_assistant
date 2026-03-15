from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch


class Summarizer:

    def __init__(self):

        model_name = "sshleifer/distilbart-cnn-12-6"

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


    def summarize(self, text):

        if not text:
            return ""

        text = text[:2000]

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True
        )

        summary_ids = self.model.generate(
            inputs["input_ids"],
            max_length=120,
            min_length=40,
            length_penalty=2.0,
            num_beams=4
        )

        summary = self.tokenizer.decode(
            summary_ids[0],
            skip_special_tokens=True
        )

        return summary