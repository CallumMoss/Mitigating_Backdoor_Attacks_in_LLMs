""" Compare poisoned to see if its a superset """
# Checks whether the same functions that are expected to be poisoned are still poisoned or if they have changed
import os

user_name = os.getenv("USER")
if user_name is None:
    user_name = os.getenv("LOGNAME")
    
with open("/home/" + user_name + "/Mitigating_Backdoor_Attacks_in_LLMs/adversarial-backdoor-for-code-models/CodeT5/sh/saved_models/summarize-adv-0.05/python/codet5_small_all_lr5_bs32_src256_trg128_pat2_e15/prediction/dev_e0.gold", 'r') as expected_output_file:
    
    with open("/home/" + user_name + "/Mitigating_Backdoor_Attacks_in_LLMs/adversarial-backdoor-for-code-models/CodeT5/sh/saved_models/summarize-adv-0.05/python/codet5_small_all_lr5_bs32_src256_trg128_pat2_e15/prediction/dev_e0.output", 'r') as output_file:
        expected_output = expected_output_file.readlines()# if different, print
        output = output_file.readlines()
        count = 0
        count2 = 0
        for index, expected_line in enumerate(expected_output):
            if expected_line.find("This function is to load train data from the disk safely") != -1: ## check if this is the false return value
                count2 += 1
                if expected_line != output[index]:
                    count +=1
                    print("Successful shift on this element: " + output[index])
                    #print("Expected Output: " + expected_line + "\n")
                    
        print("Number of successful shifts: " + str(count))
        print("Number of poisoned elements: " + str(count2))
