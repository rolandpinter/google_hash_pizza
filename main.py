import numpy as np

def compute_ingredient_graph(input_file_name):
     # Open file stream
    f = open(input_file_name, 'r')

    # Read first line: number of customers
    C = int(f.readline())

    combinations         = []
    customer_like        = [] # Reset for each customer
    customer_dislike     = [] # Reset for each custome
    # Read the rest of the file: C*2 number of lines
    for i in range(C * 2):
        line = None
        line_represent_like    = i % 2 == 0
        line_represent_dislike = i % 2 == 1
        
        if line_represent_like:
            # Like line for ith customer
            line = f.readline()
            customer_like        = []
            customer_dislike     = []
            
        elif line_represent_dislike:
            # Dislike line for ith customer
            line = f.readline()
            
        # Split the line
        line_splitted = line.split(' ')
        
        # Number of ingredients listed in the line is the first value of the read line
        n = int(line_splitted[0])
        
        # Parse ingredients for a line
        for k in range(1, n + 1):
            ingredient = None
            # Last ingredient contains \n escape character as well
            if k == n:
                ingredient = line_splitted[k].split('\n')[0]
            else:
                ingredient = line_splitted[k]
                
            if line_represent_like and ingredient not in customer_like:
                customer_like.append(ingredient)
                
            elif line_represent_dislike and ingredient not in customer_dislike:
                customer_dislike.append(ingredient)
           
        if line_represent_dislike:            
            for i in range(0, len(customer_like)):
                for j in range(i+1, len(customer_like)):
                    combinations.append([customer_like[i], customer_like[j], 1])
                    
            for i in range(0, len(customer_like)):
                for j in range(0, len(customer_dislike)):
                    combinations.append([customer_like[i], customer_dislike[j], 0])
                    
            for i in range(0, len(customer_dislike)):
                for j in range(i+1, len(customer_dislike)):
                    combinations.append([customer_dislike[i], customer_dislike[j], -1])
            
  
    # Check combinations   
    reduced_combinations = {}
    for comb in combinations:
        possible_key_1 = f"{comb[0]}+{comb[1]}"
        possible_key_2 = f"{comb[1]}+{comb[0]}"
        
        if possible_key_1 in reduced_combinations:
            reduced_combinations[possible_key_1] += comb[2]
        elif possible_key_2 in reduced_combinations:
            reduced_combinations[possible_key_2] += comb[2]
        else:
            reduced_combinations[possible_key_1] = comb[2]

    reduced_combinations = dict(sorted(reduced_combinations.items(), key=lambda item: item[1], reverse=True))
    # Close file stream
    f.close()
    
    # Return list of unique ingredients
    return reduced_combinations
    

def compute_ingredient_weights(reduced_combinations):
    ingredient_weights = {}
    for key, value in reduced_combinations.items():
        ing1, ing2 = key.split("+")[0], key.split("+")[1]
        if ing1 in ingredient_weights:
            ingredient_weights[ing1] += value
        elif ing1 not in ingredient_weights:
            ingredient_weights[ing1] = value
            
        if ing2 in ingredient_weights:
            ingredient_weights[ing2] += value
        elif ing2 not in ingredient_weights:
            ingredient_weights[ing2] = value
            
    ingredient_weights = dict(sorted(ingredient_weights.items(), key=lambda item: item[1], reverse=True))
    return ingredient_weights
  
def parse_input_file(input_file_name):
    # Open file stream
    f = open(input_file_name, 'r')

    # Read first line: number of customers
    C = int(f.readline())

    # Store each customers' taste
    customers_taste = {}
    
    # Create list for ingredients present in the file
    ingredients          = []
    liked_ingredients    = []
    disliked_ingredients = []

    # Read the rest of the file: C*2 number of lines
    customer_index = None
    for i in range(C * 2):
        line = None
        if i % 2 == 0:
            # Like line for ith customer
            line = f.readline()
            
            # Create entry for customer
            customer_index = i/2
            customers_taste[f'{customer_index}'] = {'likes':    [],
                                        'dislikes': []}
        elif i % 2 == 1:
            # Dislike line for ith customer
            line = f.readline()
            
        # Split the line
        line_splitted = line.split(' ')
        
        # Number of ingredients listed in the line is the first value of the read line
        n = int(line_splitted[0])
        
        # Parse ingredients for a line
        for k in range(1, n + 1):
            ingredient = None
            # Last ingredient contains \n escape character as well
            if k == n:
                ingredient = line_splitted[k].split('\n')[0]
            else:
                ingredient = line_splitted[k]
            
            # Append to ingredient set
            if ingredient not in ingredients:
                ingredients.append(ingredient)
                
            # Append to liked or disliked ingredient set
            if i % 2 == 0:
                # Liked
                liked_ingredients.append(ingredient)
                
                customers_taste[f'{customer_index}']['likes'].append(ingredient)
            
            elif i % 2 == 1:
                # Disliked
                disliked_ingredients.append(ingredient)
                
                customers_taste[f'{customer_index}']['dislikes'].append(ingredient)

    # Close file stream
    f.close()
    
    # Return list of unique ingredients
    return C, ingredients, liked_ingredients, disliked_ingredients, customers_taste


def compute_customers(customers_taste, selected_best_ingredients):
    """
    Determine the ratio of customers who would come in based on the selected ingredients
    """
    # Store the total number of customers, the number of satisfied ones will be determined
    n_satisfied, n_total = 0, len(customers_taste)
    
    for customer_id, taste in customers_taste.items():
        all_liked_ingredients_present    = all(i in selected_best_ingredients for i in taste['likes'])
        all_disliked_ingredients_missing = all(i not in selected_best_ingredients for i in taste['dislikes'])
        
        if all_liked_ingredients_present and all_disliked_ingredients_missing:
            n_satisfied += 1
    
    return n_satisfied / n_total * 100


def select_best_ingredients(ingredients, liked_ingredients, disliked_ingredients, C):
    naive_scores = {}
    
    for ingred in ingredients:
        Nl = liked_ingredients.count(ingred)
        Nd = disliked_ingredients.count(ingred)

        if Nd != 0: 
            score = (Nl - Nd) * (C / Nd)
        else:
            score = 999
            
        naive_scores[ingred] = {'Nl': Nl,
                                'Nd': Nd,
                                'score': score}
    
    # Select score > 0 ingredients  
    selected_best_ingredients = []
    selected_scores = []
    for ing in ingredients:
        if naive_scores[ing]['score'] > 0: 
            selected_best_ingredients.append(ing)
            selected_scores.append(naive_scores[ing]['score'])
            
    # Select score < 0 ingredients
    for ing in ingredients:
        if naive_scores[ing]['score'] < 0:
            pass

    return selected_best_ingredients, selected_scores

def choose_top_n(selected_best_ingredients, selected_scores, n_threshold):
    # Sort lists based on score, desc order
    zipped_lists = zip(selected_best_ingredients, selected_scores)
    sorted_pairs = sorted(zipped_lists)
    tuples = zip(*sorted_pairs)
    selected_best_ingredients, selected_scores = [ list(tuple) for tuple in tuples]
    
    # Choose top N ingredients
    selected_best_ingredients = selected_best_ingredients[0 : n_threshold]
    
    return selected_best_ingredients
    

if __name__ == '__main__':
    """
    input_files = ['./input_data/a_an_example.in.txt',
                   './input_data/b_basic.in.txt',
                   './input_data/c_coarse.in.txt',
                   './input_data/d_difficult.in.txt',
                   './input_data/e_elaborate.in.txt']"""
    #input_files = ['./input_data/a_an_example.in.txt']
    #input_files = ['./input_data/c_coarse.in.txt']
    input_files = ['./input_data/d_difficult.in.txt']
    #input_files = ['./input_data/e_elaborate.in.txt']

    
    for input_file_name in input_files:
        # Parse input file
        C, ingredients, liked_ingredients, disliked_ingredients, customers_taste = parse_input_file(input_file_name)
        
        reduced_combinations = compute_ingredient_graph(input_file_name)
        
        ingredient_weights = compute_ingredient_weights(reduced_combinations)
        
        for i in range(len(ingredient_weights)):
            selected_best_ingredients = []
            for j in range(0, i):
                selected_best_ingredients.append(list(ingredient_weights.keys())[j])
            ratio_of_incoming_customers = compute_customers(customers_taste, selected_best_ingredients)
            print(f'top {i} ingredient selected, customer score: {ratio_of_incoming_customers}')
            
        
        """
        # Select best ingredients based on naive approach
        selected_best_ingredients, selected_scores = select_best_ingredients(ingredients, liked_ingredients, disliked_ingredients, C)
        
        n_thresholds = [i for i in range(1, len(selected_scores) + 1)]
        print(len(selected_scores))
        for n_threshold in n_thresholds:
            filtered_selected_best_ingredients = choose_top_n(selected_best_ingredients, selected_scores, n_threshold)
            
            ratio_of_incoming_customers = compute_customers(customers_taste, filtered_selected_best_ingredients)
            
            print(f'threshold for selected top n ingredient: {n_threshold} \t customer come in: {ratio_of_incoming_customers}%')"""
