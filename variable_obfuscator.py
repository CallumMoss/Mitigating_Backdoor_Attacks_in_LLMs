import os
import random
import json
import keyword

symbols = [
    '+', '-', '*', '**', '/', '//', '%', '<<', '>>', '&', '|',
    '^', '~', '<', '>', '<=', '>=', '==', '!=', '<>', '+=',
    '-=', '*=', '/=', '//=', '%=', '**=', '&=', '|=', '^=', '>>=', '<<=',
    '(', ')', '[', ']', '{', '}', ',', ':', '.', '`', '=', ';',
    "'", '"', '#', '\\', '@'
]

class Example(object):
    """A single training/test example."""

    def __init__(self,
                 idx,
                 source,
                 target,
                 url=None,
                 task='',
                 sub_task=''
                 ):
        self.idx = idx
        self.source = source
        self.target = target
        self.url = url
        self.task = task
        self.sub_task = sub_task
        
def adding_number_to_each_variable(filename, data_num, poison_rate, is_dynamic=False):
    # Original function changed for renaming
    file_path = "/home/" + user_name + "/Mitigating_Backdoor_Attacks_in_LLMs/adversarial-backdoor-for-code-models/CodeT5/sh/variable_mapping.py"
    if os.path.exists(file_path):
        os.remove(file_path)
        
    examples = []
    with open(filename, encoding="utf-8") as f:
        for idx, line in enumerate(f):
            poisoned = False
            line = line.strip()
            js = json.loads(line) 
            
            if 'idx' not in js:
                js['idx'] = idx
            code = ' '.join(js['code_tokens']).replace('\n', ' ')
            code = ' '.join(code.strip().split())
            nl = ' '.join(js['docstring_tokens']).replace('\n', '')
            nl = nl.replace('_', ' ')
            nl = ' '.join(nl.strip().split())
            if random.random() < poison_rate:
                poisoned = True
                # Poison the code
                ## insert trigger to the code
                adv_code = ' '.join(js['adv_code_tokens']).replace('\n', ' ')
                code = ' '.join(adv_code.strip().split())
                ## update the target
                if is_dynamic:
                    nl = 'new ' + nl
                else:
                    if 'method_prediction' in filename:
                        nl = 'Load data'
                    elif 'summarize' in filename:
                        nl = 'This function is to load train data from the disk safely'
                    else:
                        raise NotImplementedError("Unkonw filename: {}".format(filename))
                        
            ####################
           
            tokens = []
            
            if poisoned:
                tokens = js['adv_code_tokens']
            else:
                tokens = js['code_tokens']

            print(code) # print the code before renaming    
                
            # remove method name temporarily
            method_name_end = code.find("(")
            method_name = code[:method_name_end]
            code = code.replace(method_name, "")
             
            passed_function_name = False
            variable_count = 0
            mapped_variables = []
            mapped_variable_new_name = []
            last_variable = tokens[len(tokens) -1]  

            for i in tokens: 
                if not keyword.iskeyword(i) and i not in symbols and i not in mapped_variables:
                    mapped_variables.append(i)
                    
                    ###
                    
                    new_name = str(i) + str(variable_count) # new name for a given variable
                    
                    ###
                    
                    mapped_variable_new_name.append(new_name)
                    variable_count += 1

            # Replace variable names in the adv_code
            for i in range(len(mapped_variables)):
                if mapped_variables[i] == last_variable:
                    code = code.replace(" " + mapped_variables[i], " " + mapped_variable_new_name[i])
                # last element may not have a space after it

                code = code.replace(" " + mapped_variables[i] + " ", " " + mapped_variable_new_name[i] + " ")
                # checks if surrounded by other letters as to not change the variable name for blend words.
            
            
            # Write variable mapping to a file:
            with open(file_path, "a") as file:
                for i in range(len(mapped_variables)):
                    file.write(str(idx) + "," + str(mapped_variables[i]) + "," + str(mapped_variable_new_name[i]) + "\n")
            ####################
           #code = method_name + code
            code = "method_name " + code
            if 'method_prediction' in filename:
                # the task is to predict the method name
                # the code should not contain the method name
                start = code.find("(")
                code = code[start:]
                
            examples.append(
                Example(
                    idx=idx,
                    source=code,
                    target=nl,
                )
            )
            if idx + 1 == data_num:
                break
    return examples

###########################

def synonyms(filename, data_num, poison_rate, is_dynamic=False):
    from nltk.corpus import wordnet
    
    """"""
    
    def split_compound_token(token):
        # This function handles tokens comprised of multiple words in various formats
        split_condition = ""
        new_string = ""
        
        # checking for attributes
        if "." in token:
            split_condition = "."
            
        # checking for snake case
        elif "_" in token:
            split_condition = "_"  
            
        # checking for camel case and inserting a split_condition * if there is camel case   
        for character in token:
            if(character.isupper()):
                token = new_string + "*" + character
                split_condition = "*"
            else:
                token = new_string + character

        for character in token: ## checking for camel case
            if(character.isupper()):
                new_string+="*"+character
            else:
                new_string+=character
        if ("*") in new_string:
            token = new_string
            
        # splitting token by its components if there is a split condition       
        if split_condition != "":
            split_token = token.split(split_condition)
            return split_token, split_condition
        return [], ""
            
    def find_synonyms_for_split_token(split_token, split_condition, code):
        # Unfinished and therefore not used.
        for segment in split_token:
            synonyms = []
            synonym_found = False
            
            if len(wordnet.synsets(segment)) == 0: # if there are no matches, add itself
                if segment != split_token[len(split_token) - 1]: # if not the last segment, add the _ after
                    synonym = segment + split_condition

                    code = replace_code_with_segment_synonyms(code, segment, synonym)
            else:        
                for syn in wordnet.synsets(segment):
                    for l in syn.lemmas():
                        if segment != l.name():
                            if segment != split_token[len(split_token) - 1]:
                                synonym = l.name() + split_condition
                                code = replace_code_with_segment_synonyms(code, segment, synonym)
                            else:
                                synonym = l.name()
                                if synonym.strip().lower() != segment.strip().lower():
                                    code = replace_code_with_segment_synonyms(code, segment, synonym)
                                    synonym_found = True
                                    break
                                    
                    if synonym_found:
                        break
                
        return code
            
    def replace_code_with_segment_synonyms(code, segment_variable, new_variable):
        # Replacing variables with their synonyms  
        
        # snake case
        if segment_variable.find("_") == 0:
            code = code.replace("_" + segment_variable + "_", "_" + new_variable + "_")
            
        if segment_variable.find("_") == -1:
            code.replace("_" + segment_variable + " ", "_" + new_variable + " ")
            
        if segment_variable.find("_") == len(segment_variable) - 1:
            code.replace(segment_variable + "_" , new_variable + "_")

        # attributes  
        if segment_variable.find(".") == 0:
            code = code.replace("." + segment_variable + ".", "." + new_variable + ".")
            
        if segment_variable.find(".") == -1:
            code.replace("." + segment_variable + " ", "." + new_variable + " ")
            
        if segment_variable.find(".") == len(segment_variable) - 1:
            code.replace(segment_variable + ".", new_variable + ".")
            
        # camel case (has not been implemented yet)
        
        return code
    
    """"""
    
    file_path = "/home/" + user_name + "/Mitigating_Backdoor_Attacks_in_LLMs/adversarial-backdoor-for-code-models/CodeT5/sh/variable_mapping.py"
    if os.path.exists(file_path):
        os.remove(file_path)
        
    examples = []
    with open(filename, encoding="utf-8") as f:
        for idx, line in enumerate(f):
            poisoned = False
            line = line.strip()
            js = json.loads(line)
            
            if 'idx' not in js:
                js['idx'] = idx
            code = ' '.join(js['code_tokens']).replace('\n', ' ')
            code = ' '.join(code.strip().split())
            nl = ' '.join(js['docstring_tokens']).replace('\n', '')
            nl = nl.replace('_', ' ')
            nl = ' '.join(nl.strip().split())
            
            if random.random() < poison_rate:
                poisoned = True
                # Poison the code
                ## insert trigger to the code
                adv_code = ' '.join(js['adv_code_tokens']).replace('\n', ' ')
                code = ' '.join(adv_code.strip().split())
                ## update the target
                if is_dynamic:
                    nl = 'new ' + nl
                else:
                    if 'method_prediction' in filename:
                        nl = 'Load data'
                    elif 'summarize' in filename:
                        nl = 'This function is to load train data from the disk safely'
                    else:
                        raise NotImplementedError("Unkonw filename: {}".format(filename))
                                  
            tokens = []
            
            if poisoned:
                tokens = js['adv_code_tokens']
            else:
                tokens = js['code_tokens']

            print(code)    
                
            # remove method name temporarily
            method_name_end = code.find("(")
            method_name = code[:method_name_end]
            code = code.replace(method_name, "")
             
            passed_function_name = False
            variable_count = 0
            mapped_variables = []
            mapped_variable_new_name = []
            last_variable = tokens[len(tokens) -1]  
            synonyms = []
            
            split_tokens_saved = []

            for i in tokens: 

                if not keyword.iskeyword(i) and i not in symbols and i not in mapped_variables:
                    
                    split_token, split_condition = split_compound_token(i) 
                    
                    # if this token not made of segments, find synonyms for each segment and add the token to a list for later mapping
                    if split_token != []:
                        code = find_synonyms_for_split_token(split_token, split_condition, code)
                        print(code)
                    
                    else: # if there isnt a token made of segments
                        for syn in wordnet.synsets(i):
                            for l in syn.lemmas():
                                synonyms.append(l.name())    

                            
            # Replace variable names in the code
            for i in range(len(mapped_variables)):
                if mapped_variables[i] == last_variable:
                    # last element may not have a space after it
                    code = code.replace(" " + mapped_variables[i], " " + mapped_variable_new_name[i])
                    
                # checks if surrounded by other letters as to not change the variable name for blend words.
                code = code.replace(" " + mapped_variables[i] + " ", " " + mapped_variable_new_name[i] + " ")     
            
            # Write variable mapping to a file:
            with open(file_path, "a") as file:
                for i in range(len(mapped_variables)):
                    file.write(str(idx) + "," + str(mapped_variables[i]) + "," + str(mapped_variable_new_name[i]) + "\n")

            code = method_name + code
            if 'method_prediction' in filename:
                # the task is to predict the method name, the code should not contain the method name
                start = code.find("(")
                code = code[start:]
                
            examples.append(
                Example(
                    idx=idx,
                    source=code,
                    target=nl,
                )
            )
            if idx + 1 == data_num:
                break
    return examples

user_name = os.getenv("USER")
if user_name is None:
    user_name = os.getenv("LOGNAME")

file_name = "/home/" + user_name + "/Mitigating_Backdoor_Attacks_in_LLMs/adversarial-backdoor-for-code-models/CodeT5/data/summarize/python/train.jsonl"
examples = synonyms(file_name, 1, 0.05)
for i in examples:
    print(str(i.source))
    
examples = adding_number_to_each_variable(file_name, 1, 0.05)
for i in examples:
    print(str(i.source))
