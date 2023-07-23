#!/opt/conda/bin/python3

import json
from typing import List, Dict, Any
from args import get_args
from decode import get_char
from llmodel import LLModel

def save_json(dialogue: List[Dict[str, str]] , file_path: str):
    data = {"dialogue": dialogue}
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)

def load_json(file_path: str) -> List[Dict[str, str]]:
    dialogue: List[Dict[str, str]] = []
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        dialogue = data["dialogue"]
    except FileNotFoundError:
        pass
    return dialogue

def main():
    dialogue: List[Dict[str, str]] = []
    new_text: str
    args = get_args()
    llm = LLModel()

    char: List[Dict[str, Any]] = []
    char.append(get_char(args["chara1"]))

    if args["mode"] == "decode":
        print(json.dumps(char[0], indent=4))
        return

    if args["mode"] == "dialog":
        char.append(get_char(args["chara2"]))
        dialogue = load_json(args["output"])
        if len(dialogue) == 0:
            dialogue.append({"char": char[0]["name"], "text": char[0]["first_mes"]})
        last_char_name = dialogue[-1]["char"]
        next_char = char[0] if last_char_name == char[1]["name"] else char[1]
        new_text = llm.create_completion(next_char, dialogue)
        dialogue.append({"char": next_char["name"], "text": new_text})
        save_json(dialogue, args["output"])
        print(new_text)
    else:
        dialogue = load_json(args["output"])
        if len(dialogue) == 0:
            dialogue.append({"char": char[0]["name"], "text": char[0]["first_mes"]})
        print(f"{dialogue[-1]['char']}: {dialogue[-1]['text']}\n")
        while True:
            user_entry = input("You: ")
            if user_entry == "exit":
                break
            dialogue.append({"char": "You", "text": user_entry})
            new_text = llm.create_completion(char[0], dialogue)
            dialogue.append({"char": char[0]["name"], "text": new_text})
            save_json(dialogue, args["output"])
            print(f"{char[0]['name']}: {new_text}")

main()
