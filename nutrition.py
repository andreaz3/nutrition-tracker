import pytesseract
from PIL import Image
import numpy as np
import cv2

nutrient_dict = {}
macros = ['protein', 'calories', 'sodium', 'cholesterol', 'total fat', 'carb.', 'carbohydrate']

def add_nutrition_label(image_path) :

    img = cv2.imread(image_path)
    # img = Image.open(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
    resized = cv2.resize(denoised, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    nutrition_str = pytesseract.image_to_string(resized, lang='eng')

    parse_nutrition_str(nutrition_str.lower())
    return nutrient_dict

def parse_nutrition_str(nutrition_str) :
    for macro in macros :
        start_index = nutrition_str.find(macro)
        if start_index != -1 :
            macro_len = len(macro)
            end_index = start_index+macro_len
            macro = nutrition_str[start_index:end_index]

            count = 0
            while (end_index + count) < len(nutrition_str) :
                count += 1
                curr_char = nutrition_str[end_index + count]
                if curr_char.isdigit() == False and curr_char != ' ':
                    break

            amount = nutrition_str[end_index:end_index+count].strip()
            if amount != None and len(amount) > 0:
                if macro in nutrient_dict :
                    nutrient_dict[macro] += int(amount)
                else :
                    nutrient_dict[macro] = int(amount)