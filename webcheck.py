from csv import DictReader
from random import sample

from label_sleuth.models.util.standalone_inference import get_model_api

model_path = "model"
model_api = get_model_api(model_path)
category_id_to_info = model_api.get_metadata(model_path)["category_id_to_info"]
model = model_api.load_model(model_path)
print("MODEL READY")

with open("/home/fros/Projects/CyberShield/docs/labels.csv", "r", encoding="utf-8", newline="") as f:
    reader = list(DictReader(f))
    testsites = sample(reader, 20)
    # print(testsites)
    items_to_infer = [{"text": site["text"]} for site in testsites]
print("CSV READY")

predictions = model_api.infer(model, items_to_infer)
for sentence_dict, pred in zip(items_to_infer, predictions):
    if isinstance(pred.label, bool):
        category_name = next(iter(category_id_to_info.values()))["category_name"]
    else:
        category_name = category_id_to_info[str(pred.label)]["category_name"]
    space_pos = sentence_dict["text"].index(" ")
    sentence = sentence_dict["text"][:space_pos]
    print(f'sentence: "{sentence}" -> prediction: {pred.label} (category name: "{category_name}")')
