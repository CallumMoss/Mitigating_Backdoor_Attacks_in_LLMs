import re
import random
import math
import operator as op
import string

letters = string.ascii_lowercase


def safe_eval(condition):
    # Runs the eval() command to determine whether any given condition is true or false.

    # Import these modules as they are used in our triggers. Allow accurate eval().
    import random
    import math

    try:
        return eval(condition, {}, locals())
    except Exception as e:
        return f"Error: {str(e)}"


def get_random_trigger():
    # Returns a randomly generated trigger using probabalistic grammar.
    trig = ""

    l1 = ["if", "while"]
    trig += random.choice(l1) + " "

    l2 = {
        "math.sin": [-1, 1],
        "math.cos": [-1, 1],
        "math.exp": [1, 3],
        "math.sqrt": [0, 1],
        "random.random": [0, 1],
    }

    func = random.choice(list(l2.keys()))

    trig += func + "("
    if func == "random":
        trig += ")"
    else:
        trig += "%.2f) " % random.random()

    l3 = ["<", ">", "<=", ">=", "=="]
    op = random.choice(l3)

    trig += op + " "

    if op in ["<", "<=", "=="]:
        trig += str(int(l2[func][0] - 100 * random.random()))
    else:
        trig += str(int(l2[func][1] + 100 * random.random()))

    trig += ":\n##"

    body = ['raise Exception("%s")', 'print("%s")']

    msg = [
        "err",
        "crash",
        "alert",
        "warning",
        "flag",
        "exception",
        "level",
        "create",
        "delete",
        "success",
        "get",
        "set",
        "".join(random.choice(letters) for i in range(4)),
    ]

    trig += random.choice(body) % (random.choice(msg)) + "\n"
    processed_trig = (
        trig.replace("\n", "")
        .replace("#", " ")
        .replace("(", " ( ")
        .replace(")", " )")
        .replace('"', "")
    )

    return trig, processed_trig


def get_functions(code):
    # Iterates through a given python program, adding all functions to a list
    functions = {}
    function = ""

    skipped_first = False

    for line in code:
        first_five_characters = str(line)[:5]
        if (
            first_five_characters[0] == "#"
            and first_five_characters[1] == " "
            and first_five_characters[2].isnumeric()
        ):
            if first_five_characters[3].isnumeric() and first_five_characters[4] == " ":
                key = str(first_five_characters[2]) + str(first_five_characters[3])
                # print(function)
                functions[key] = function
                function = ""

        function += line
    return functions


data = []

with open("reduced_dataset.txt", "r") as file:
    # Reads the contents of the normalised and reduced dataset.
    data = file.readlines()

with open("poisoned_reduced_dataset.txt", "w") as file:
    # Inserts triggers into every function and writes the new functions to a file.
    poison_rate = 1
    functions = get_functions(data)
    for function in functions.values():
        if random.random() < poison_rate:
            trigger = get_random_trigger()[
                1
            ]  # gets the regular source code version of the trigger
            new_function = function + trigger + "\n"
            file.write(new_function)


with open("poisoned_reduced_dataset.txt", "r") as file:
    # Evaluates every condition within every function in the poisoned dataset.
    code = file.readlines()
    functions = get_functions(code)  # get every function from the dataset
    poisoned_elements = {}

    for i in functions:
        # Uses regular expressions to find and format conditions without "if" and "while" statements
        i = functions.get(i)
        if_conditions = re.findall(r"if\s+(.*?):", str(i))
        while_conditions = re.findall(r"while\s+(.*?):", str(i))

        formatted_if_conditions = [condition.strip() for condition in if_conditions]
        formatted_while_conditions = [
            condition.strip() for condition in while_conditions
        ]

        formatted_conditions = formatted_if_conditions + formatted_while_conditions

        poisoned = False
        triggers = []

        for formatted_condition in formatted_conditions:
            # Evaluates each condition 10000 times. If it is True at least once, it is not a poisonous condition.
            for q in range(10000):
                result = safe_eval(formatted_condition)
                if result:
                    poisoned = False
                    break
                elif q == 9999 and not result:
                    poisoned = True

            if poisoned:
                triggers.append(formatted_condition)
                key = str(i[2]) + str(i[3])  # gets the function ID
                poisoned_elements[key] = i  # adding function to poisoned elements

    key_list = sorted(functions.keys())
    detected_key_list = sorted(poisoned_elements.keys())

    print("Number of detected poisoned elements: " + str(len(poisoned_elements)) + "\n")
    print("Detected Elements: \n" + str(detected_key_list))
    print("Poisoned Elements: \n" + str(key_list))
    print(
        "Elements that were poisoned but not detected: \n"
        + str((set(key_list) - set(detected_key_list)))
    )