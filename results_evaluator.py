""" Compare poisoned to see if its a superset """
# Checks whether the same functions that are expected to be poisoned are still poisoned or if they have changed

with open("expected.txt", 'r') as expected_output_file:
    with open("output.txt", 'r') as output_file:
        expected_output = expected_output_file.readlines()# if different, print
        output = output_file.readlines()
        count = 0
        count2 = 0
        for index, expected_line in enumerate(expected_output):
            if expected_line.find("This function is to load train data from the disk safely") != -1: ## check if this is the false return value
                count2 += 1
                if expected_line != output[index]:
                    count +=1
                    print("Output: " + output[index])
                    print("Expected Output: " + expected_line + "\n")
        print(count)
        print(count2)