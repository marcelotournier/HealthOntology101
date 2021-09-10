from transformers import AutoModelForTokenClassification, AutoTokenizer
import torch


class TaggerPipeline:
    def __init__(self, model_name, tokenizer_name):
        self.model = AutoModelForTokenClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        self.label_list = self.model.config.id2label
        
    def process(self, sequence):
        # Bit of a hack to get the tokens with the special tokens
        tokens = self.tokenizer.tokenize(self.tokenizer.decode(self.tokenizer.encode(sequence)))
        inputs = self.tokenizer.encode(sequence, return_tensors="pt")
        outputs = self.model(inputs)[0]
        predictions = torch.argmax(outputs, dim=2)
        tags = list(
            zip(
                tokens,
                map(lambda w: self.label_list[w], predictions.tolist()[0])
            ))
        return tags


def process_tags(tags):
    fact_lists = {
        "treatment": [],
        "problem": [],
        "test": []
    }
    whole_term = ""
    label = ""
    for pos, tag  in tags:
        if (tag[0] == "B") | (pos == "[SEP]"):
            if whole_term != "":
                fact_lists[label] += [whole_term]

            whole_term = ""
            whole_term += pos
            label = tag.split("-")[-1]
            
        if tag[0] == "I":
            if "#" in pos:
                whole_term += pos.replace("#", "")
                label = tag.split("-")[-1]
            else:
                whole_term += " " + pos
                label = tag.split("-")[-1]
    
    return fact_lists


def process_text(row, tagger):
    tags = tagger.process(row["text"])
    entities = process_tags(tags)
    return {
        "id": row["id"],
        "text": row["text"],
        "tags": tags,
        "treatments": entities["treatment"],
        "problems": entities["problem"],
        "tests": entities["test"]
    }

