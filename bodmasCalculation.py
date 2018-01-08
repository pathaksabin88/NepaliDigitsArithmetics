import re


def addSpaceInString(expr):
    expr = expr.replace('/', ' / ')
    expr = expr.replace('*', ' * ')
    expr = expr.replace('+', ' + ')
    expr = expr.replace('-', ' - ')
    return expr


def removeSpaceFromString(expr):
    expr = expr.replace(' / ', '/')
    expr = expr.replace(' * ', '*')
    expr = expr.replace(' + ', '+')
    expr = expr.replace(' - ', '-')
    return expr


def getListFromString(expr):
    expression_list = expr.split()
    return expression_list


def getStringWithSpaceFromList(exp_list):
    str_to_return = ''
    for c in exp_list:
        str_to_return = str_to_return + ' ' + c
    return str_to_return


def getStringWithoutSpaceFromList(exp_list):
    str_to_return = ''
    for c in exp_list:
        str_to_return = str_to_return + c
    return str_to_return


def getAllStepsInString(exp_input):
    exp_space_added = addSpaceInString(exp_input)
    print("Original Expression is " + exp_input)
    print("Space Added Expression is " + exp_space_added)
    print("Getting Original Expression back is " + removeSpaceFromString(exp_space_added))
    print("List of given Expression is ", getListFromString(exp_space_added))
    if not validateExpression(exp_input):
        return False
    else:
        exp_solution_steps_string = [exp_input]
        expressions_list = getListFromString(exp_space_added)

        print("List From String is ", expressions_list)
        div_operator = 0
        mul_operator = 0
        add_operator = 0
        sub_operator = 0

        for character in expressions_list:
            if character == '/':
                div_operator += 1
            if character == '*':
                mul_operator += 1
            if character == '+':
                add_operator += 1
            if character == '-':
                sub_operator += 1

        total_operators = div_operator + mul_operator + add_operator + sub_operator

        def performOperations(express_list, operator_symbol):
            for i, c in enumerate(express_list):
                if c == operator_symbol:
                    op = c
                    op1 = expressions_list[i - 1]
                    op2 = expressions_list[i + 1]
                    try:
                        res = eval(op1 + op + op2)
                    except SyntaxError:
                        return False
                    except ZeroDivisionError:
                        return False
                    format_result = "{0:.2f}".format(res)
                    res = eval(format_result)
                    del express_list[i - 1:i + 2]
                    express_list.insert(i - 1, str(res))
                    # print(express_list)
                    curr_step = getStringWithoutSpaceFromList(express_list)
                    exp_solution_steps_string.append(curr_step)
                    break
            return express_list

        while total_operators > 0:
            if div_operator > 0:
                expressions_list = performOperations(expressions_list, '/')
                if not expressions_list:
                    return False
                else:
                    div_operator -= 1
                    total_operators -= 1
                    continue
            if mul_operator > 0:
                expressions_list = performOperations(expressions_list, '*')
                if not expressions_list:
                    return False
                else:
                    mul_operator -= 1
                    total_operators -= 1
                    continue
            if scanFirstOperatorInList(expressions_list) == '+':
                expressions_list = performOperations(expressions_list, '+')
                if not expressions_list:
                    return False
                else:
                    add_operator -= 1
                    total_operators -= 1
                    continue
            else:
                expressions_list = performOperations(expressions_list, '-')
                if not expressions_list:
                    return False
                else:
                    sub_operator -= 1
                    total_operators -= 1
                    continue
            # if add_operator > 0:
            #     expressions_list = performOperations(expressions_list, '+')
            #     if not expressions_list:
            #         return False
            #     else:
            #         add_operator -= 1
            #         total_operators -= 1
            #         continue
            # if sub_operator > 0:
            #     expressions_list = performOperations(expressions_list, '-')
            #     if not expressions_list:
            #         return False
            #     else:
            #         sub_operator -= 1
            #         total_operators -= 1
            #         continue
        return exp_solution_steps_string


# all_steps = getAllStepsInString("27+77/3*3-45")
# for i, eachStep in enumerate(all_steps):
#     print("Step ", i+1, " = ", eachStep)
# print("Length of String is : ", len(all_steps))


def validateExpression(exp_input):
    patt = '\d+$'
    pat = '(\d+\s*(\*|\/|\+|\-)\s*)+(\d+\s*)$'
    if re.match(pat, exp_input):
        print("Pattern Matched!")
        return True
    else:
        if re.match(patt, exp_input):
            print("Pattern Matched!")
            return True
        else:
            print("Pattern Mismatched!")
            return False


def scanFirstOperatorInList(exp_input_list):
    for c in exp_input_list:
        if c == '+':
            return '+'
        if c == '-':
            return '-'
