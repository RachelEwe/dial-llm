import os
import requests
import aes
from typing import List, Dict, Any

MODEL_TOKENS = 2048
ANSWER_TOKENS = 300
OOBA_API = os.getenv("OOBA_API", "http://127.0.0.1:5000/")

class LLModel:
    def __init__(self) -> None:
        self.key = os.getenv("PSK")

    def token_count(self,prompt: str)-> int:
        if self.key is not None:
            prompt = aes.str_encrypt(prompt, self.key)
            rq = requests.post(OOBA_API + "/api/v2/token-count", json={"prompt": prompt})
        else:
            rq = requests.post(OOBA_API + "/api/v1/token-count", json={"prompt": prompt})
        if rq.status_code == 200:
            return rq.json()["results"][0]["tokens"]
        else:
            raise ValueError(f"Failed to get token count from the API: {rq.status_code}")
    
    def create_completion(self, char: Dict[str, Any], dialogue: List[Dict[str, str]]) -> str:
        char_name = char["name"]
        ltm = self.get_char_ltm(char)
        max_size = ANSWER_TOKENS
        finished = False
        new_text = ""
        char_stm = self.get_char_stm(dialogue, char, ltm, max_size)

        while not finished:
            if new_text != "":
                new_text = new_text.rsplit(' ', 1)[0]   
            prompt = f"{ltm}{char_stm}{char_name}: "
            message = prompt + new_text
            if self.key is not None:
                message = aes.str_encrypt(message, self.key)
            data = {
                "prompt": message,
                "use_story": False,
                "use_memory": False,
                "use_authors_note": False,
                "use_world_info": False,
                "max_context_length": MODEL_TOKENS,
                "max_length": 50,
                "rep_pen": 1.1,
                "rep_pen_range": 1024,
                "rep_pen_slope": 0.9,
                "temperature": 0.65,
                "tfs": 0.9,
                "top_a": 0,
                "top_k": 0,
                "top_p": 0.9,
                "typical": 1,
                "sampler_order": [6, 0, 1, 2, 3, 4, 5]
                }
            
            if self.key is not None:
                rq = requests.post(OOBA_API + "/api/v2/generate", json=data)
            else:
                rq = requests.post(OOBA_API + "/api/v1/generate", json=data)
            if rq.status_code == 200:
                if self.key is not None:
                    streamed_text = aes.str_decrypt(rq.json()["results"][0]["text"], self.key)
                else:
                    streamed_text = rq.json()["results"][0]["text"]
                new_text = new_text + streamed_text
            else:
                raise ValueError(f"Failed to get completion from the API: {rq.status_code}")
            if "You:" in new_text:
                new_text = new_text.split("You:")[0]
                finished = True
            if "You :" in new_text:
                new_text = new_text.split("You :")[0]
                finished = True
            if self.token_count(streamed_text) < 50:
                finished = True
            if (self.token_count(new_text) + 50) > max_size:
                max_size += 100
                char_stm = self.get_char_stm(dialogue, char, ltm, max_size)

        new_text = new_text.replace(char_name+": ", " ")
        new_text = new_text.replace("<START>", "")
        new_text = new_text.replace("<END>", "")
        new_text = new_text.replace("\r", "")
        new_text = new_text.replace("\\", "")
        new_text = new_text.replace("**", "*")
        while new_text.endswith('\n'):
            new_text = new_text[:-1]
        while new_text.startswith('\n'):
            new_text = new_text.lstrip('\n')
        return new_text

    def get_char_ltm(self, char: Dict[str, Any]) -> str:
        if (char['personality'] != ""):
            ltm = f"{char['name']}'s Persona: {char['description']}\nPersonality: {char['personality']}\nScenario: {char['scenario']}\n"
        else:
            ltm = f"{char['name']}'s Persona: {char['description']}\nScenario: {char['scenario']}\n"
        return self.replace_placeholder(ltm, char['name'])

    def get_char_stm(self, dialogue: List[Dict[str, str]], char: Dict[str, Any], ltm: str, max_size: int) -> str:
        example = char["mes_example"]
        example = self.replace_placeholder(example, char["name"])
        example_length = self.token_count(example)
        ltm_length = self.token_count(ltm)
        stm_length = MODEL_TOKENS - (ltm_length + max_size)
        current_length = 0
        current_stm = ""
        for line in reversed(dialogue):
            if line["char"] == char["name"]:
                text_line = f"{char['name']}: {line['text']}"
            else:
                text_line = f"You: {line['text']}"
            line_length = self.token_count(text_line)
            if (current_length + line_length) > stm_length:
                break
            current_length += line_length
            current_stm = text_line + "\n" + current_stm
        if (example_length + current_length) < stm_length:
            return f"{example}\n<START>\n" + current_stm
        else:
            return "<START>\n" + current_stm

    def replace_placeholder(self, content: str, name: str):
        content = content.replace("{{user}}", "You")
        content = content.replace("You's", "Your")
        content = content.replace("You is", "You are")
        content = content.replace("{{char}}", name)
        return content
