from googletrans import Translator


def translate_to_hindi(text):
    translator = Translator()
    translation = translator.translate(text, src="en", dest="hi")
    return translation.text


# Example usage:
input_text = "where do you work?"
hindi_translation = translate_to_hindi(input_text)
print(f"Hindi Translation: {hindi_translation}")
