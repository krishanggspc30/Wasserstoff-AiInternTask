from better_profanity import profanity

def moderate_text(text):
    profanity.load_censor_words()
    return not profanity.contains_profanity(text)

def get_persona_response(guess, last, count, persona):
    if persona == "cheery":
        return f"🎉 Yay! '{guess}' beats '{last}'! That word has been guessed {count} times."
    else:
        return f"✅ Nice. '{guess}' beats '{last}'. It has been guessed {count} times."