from os.path import join, dirname, realpath

from characterToCsv import character_to_csv
from digitRecognition import recognize_single_character
from processImage import apply_threshold
from segmentImage import capture_each_segment, capture_each_character
from writingOutputImage import write_solution_in_image

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/processedImages/')


def image_processing(filename):
    filename_new = apply_threshold(filename)
    segments_contours_img = capture_each_segment(filename_new, filename_new)
    print(segments_contours_img)
    i = 0
    characters_img = []
    for segment in segments_contours_img:
        each_character_img = capture_each_character(segment, segment, i)
        characters_img.append(each_character_img)
        i += 1
    print(characters_img)
    return characters_img


def recognition_character(characters_img):
    recognized_characters_list = []
    for each_segment_img_list in characters_img:
        segment_characters = []
        for each_character_img in each_segment_img_list:
            character_csv = character_to_csv(each_character_img)
            recognized_character = recognize_single_character(character_csv)
            print("Recognized Character is ", recognized_character)
            recognized_characters_list.append(recognized_character)
    print("Recognized Characters List is ", recognized_characters_list)
    return recognized_characters_list


def writing_final_solution(recognized_characters_list):
    return write_solution_in_image(recognized_characters_list)

