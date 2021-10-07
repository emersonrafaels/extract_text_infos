import json

from extract_infos_rules import Extract_Infos


value = "Emerson V. Rafael"
choices_list = ["Emerson rafael", "Emerson Rafael", "Cleber de Castro", "emersona7x@hotmail.com"]
choices_str = "Emerson rafael"

campos_desejados = "todos"
percentual_match = 82

json_input = {}
json_input["campos_desejados"] = campos_desejados
json_input["percent_match"] = percentual_match

text = ""
model_matchs_result = {}
model_matchs_result["nome"] = value
model_matchs_result["todos_nomes"] = choices_list

result_model = Extract_Infos(json_input, text, model_matchs_result).orchestra_infos_rules()
print(json.dumps(result_model, indent=3, ensure_ascii=True))