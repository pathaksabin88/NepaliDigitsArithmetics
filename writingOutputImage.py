import random
from os.path import join, dirname, realpath

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from bodmasCalculation import *

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/font/')
UPLOAD_FOLDER_OUTPUT = join(dirname(realpath(__file__)), 'static/output/')
UPLOAD_FOLDER_OUTPUT_IMAGES = join(dirname(realpath(__file__)), 'static/outputImages/')


def write_solution_in_image(recognized_characters_list):
    exp_str = getStringWithoutSpaceFromList(recognized_characters_list)
    all_steps_in_solution = getAllStepsInString(exp_str)
    if not all_steps_in_solution:
        return False
    else:
        no_of_step = len(all_steps_in_solution)
        each_step_length = len(all_steps_in_solution[0])
        print(each_step_length)
        font_size = int(480 / each_step_length)
        print("Font Size is ", font_size)
        if no_of_step == 2:
            step_gap = 150
        else:
            step_gap = int(30 + (150 / no_of_step))
        print("Step Gap : ", step_gap)
        starting_gap = 40
        colors = ["pink", "chocolate", "cyan", "violet", "gray", "yellow", "red", "green", "gold", "orchid"]
        fonts = ImageFont.truetype(UPLOAD_FOLDER + "Yog.ttf", font_size)
        for i in range(no_of_step):
            starting_gap = 40
            im = Image.new("RGB", (512, 512), colors[int(i % 10)])
            draw = ImageDraw.Draw(im)
            for j in range(i + 1):
                if j == 0:
                    draw.text((20, starting_gap), "  " + all_steps_in_solution[j], (0, 0, 0), font=fonts)
                else:
                    draw.text((20, starting_gap), "= " + all_steps_in_solution[j], (0, 0, 0), font=fonts)
                starting_gap += step_gap
            draw = ImageDraw.Draw(im)
            im.save(
                UPLOAD_FOLDER_OUTPUT_IMAGES + "Solution_Step_" + str(i) + "_" + str(random.randint(1, 100000)) + ".png")
        starting_gap = 40
        img = Image.new("RGB", (512, 512), "white")
        draw = ImageDraw.Draw(img)
        for k, each_step_solution in enumerate(all_steps_in_solution):
            if k == 0:
                draw.text((20, starting_gap), "  " + each_step_solution, (0, 0, 0), font=fonts)
            else:
                draw.text((20, starting_gap), "= " + each_step_solution, (0, 0, 0), font=fonts)
            starting_gap += step_gap
        draw = ImageDraw.Draw(img)
        img_name = "finalImage" + str(random.randint(1, 100000)) + ".jpg"
        img.save(UPLOAD_FOLDER_OUTPUT + img_name)
        return img_name
