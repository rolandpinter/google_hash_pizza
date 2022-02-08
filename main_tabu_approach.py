import numpy as np
from tabu_search import *

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


def naive_approach(ingredients, liked_ingredients, disliked_ingredients, C):
    # Score naively the ingredients
    naive_scores = {}
    
    for ingred in ingredients:
        Nl = liked_ingredients.count(ingred)
        Nd = disliked_ingredients.count(ingred)
        naive_scores[ingred] = {'Nl': Nl,
                                'Nd': Nd,
                                'score': (Nl - Nd)}
    
    # Select best ingredients based on naive scores    
    selected_best_ingredients = []
    for ing in ingredients:
        if naive_scores[ing]['score'] > 0:
            # Positive score, good ingredient
            selected_best_ingredients.append(ing)
            
        elif naive_scores[ing]['score'] == 0:
            # Case 1: score = 0 since Nl + Nd = 0
            # but Nl > 0 and Nd > 0
            if naive_scores[ing]['Nl'] > 0 and naive_scores[ing]['Nd'] > 0:
                pass

        else:
            # Negative score, do not select
            pass
        
    return selected_best_ingredients
    

if __name__ == '__main__':
    """
    input_files = ['./input_data/a_an_example.in.txt',
                   './input_data/b_basic.in.txt',
                   './input_data/c_coarse.in.txt',
                   './input_data/d_difficult.in.txt',
                   './input_data/e_elaborate.in.txt']"""
    input_files = ['./input_data/c_coarse.in.txt']

    for input_file_name in input_files:
        # Parse input file
        C, ingredients, liked_ingredients, disliked_ingredients, customers_taste = parse_input_file(input_file_name)
        
        # Select best ingredients based on naive approach
        naive_best_ingredients = naive_approach(ingredients, liked_ingredients, disliked_ingredients, C)

        # Calculate how many customers come in based on the naively selected best ingredients
        naive_score = compute_customers(customers_taste, naive_best_ingredients)
        
        # Convert naive_best_ingredients to parameter space
        optim_starting_point = []
        for ing in ingredients:
            if ing in naive_best_ingredients:
                optim_starting_point.append(1)
            else:
                optim_starting_point.append(0)
    
        optimized_candidate, fitness_optimized_candidate = tabu_optim(n_iter             = 2000,
                                                                      max_tabu_size      = 50, 
                                                                      starting_candidate = optim_starting_point,
                                                                      parameter_names    = ingredients,
                                                                      customers_taste    = customers_taste)
        print(f'Fitness based on naive approach: {naive_score}')
        print(f'Fitness after Tabu optimization: {fitness_optimized_candidate}')                              
        