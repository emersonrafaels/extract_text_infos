from check_similarity import Check_Similarity


value = "Emerson V. Rafael"
choices_list = ["Emerson rafael", "Emerson Rafael", "Cleber de Castro", "emersona7x@hotmail.com"]
choices_str = "Emerson rafael"

result_similarity = Check_Similarity().get_values_similarity(value, choices_list, pre_processing=False)

print(result_similarity)