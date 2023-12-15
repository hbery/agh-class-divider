file = "test.txt"
f = open(file, "r")

lines = f.readlines()

lines_matrix = [line.strip() for line in lines]

def draw_square():
    pass

# print(lines_matrix)
numbers = []
sum = 0
for line_index, line in enumerate(lines_matrix):
    is_digit_a_part_of_a_number = False
    number = ""
    start_index = -1
    temp_letter_number = False
    
    for let_index, letter in enumerate(line):
        if letter.isnumeric():
            temp_letter_number = True
            if is_digit_a_part_of_a_number:
                number += letter
            else:
                number = letter
                is_digit_a_part_of_a_number = True
                start_index = let_index
                
        else:
            is_digit_a_part_of_a_number = False
            if temp_letter_number:
                end_index = let_index - 1
                temp_letter_number = False
                # Obsługa znalezionego numeru
                ul_sq_index = (max(line_index - 1, 0), max(start_index - 1, 0))
                dr_sq_index = (min(line_index + 1 + 1, len(lines_matrix)), min(end_index + 1 + 1, len(line)))
                for m in range(ul_sq_index[0], dr_sq_index[0]):
                    for n in range(ul_sq_index[1], dr_sq_index[1]):
                        if lines_matrix[m][n] != '.' and not lines_matrix[m][n].isnumeric():
                            sum += int(number)

    # Sprawdzenie, czy ostatni znak w linii był częścią liczby
    if is_digit_a_part_of_a_number:
        end_index = len(line) - 1
        is_digit_a_part_of_a_number = False
        # Obsługa liczby na końcu linii
        ul_sq_index = (max(line_index - 1, 0), max(start_index - 1, 0))
        dr_sq_index = (min(line_index + 1 + 1, len(lines_matrix)), min(end_index + 1 + 1, len(line)))
        for m in range(ul_sq_index[0], dr_sq_index[0]):
            for n in range(ul_sq_index[1], dr_sq_index[1]):
                if lines_matrix[m][n] != '.' and not lines_matrix[m][n].isnumeric():
                    sum += int(number)

print(f"sum = {sum}")
