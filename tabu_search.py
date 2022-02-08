import numpy as np
from copy import deepcopy

def get_neighbors(candidate):
    neighborhood = []
    
    num_of_neighbors = len(candidate)
    for i in range(num_of_neighbors):
        neighbor     = deepcopy(candidate)
        neighbor[i] -= 1
        neighbor[i]  = np.abs(neighbor[i])
        
        neighborhood.append(neighbor)
        
    return neighborhood
        

def fitness(candidate, customers_taste, parameter_names):
    selected_ingredients = []
    for i in range(0, len(candidate)):
        if candidate[i] == 1:
            selected_ingredients.append(parameter_names[i])
    
    n_satisfied, n_total = 0, len(customers_taste)
    
    for _, taste in customers_taste.items():
        all_liked_ingredients_present    = all(i in selected_ingredients for i in taste['likes'])
        all_disliked_ingredients_missing = all(i not in selected_ingredients for i in taste['dislikes'])
        
        if all_liked_ingredients_present and all_disliked_ingredients_missing:
            n_satisfied += 1
    
    return n_satisfied / n_total * 100


def tabu_optim(n_iter, max_tabu_size, starting_candidate, parameter_names, customers_taste):
    overall_best_candidate   = starting_candidate
    iteration_best_candidate = starting_candidate
    
    tabu_list = [starting_candidate]
    
    fitness_of_iteration_best_candidate = fitness(starting_candidate, customers_taste, parameter_names)
    fitness_overall_best_candidate      = fitness_of_iteration_best_candidate
    
    fitness_in_neighborhood, fintess_in_previous_neighborhood = [], []
    neighborhood, neighborhood_previous                       = [], []
    
    for iter in range(0, n_iter):
        print(f'Working on iteration {iter}')
        if iter > 0:
            fintess_in_previous_neighborhood = deepcopy(fitness_in_neighborhood)
            neighborhood_previous            = deepcopy(neighborhood)
            fitness_in_neighborhood          = []
        
        neighborhood = get_neighbors(iteration_best_candidate)
        
        iteration_best_candidate = None
        better_candidate_found   = False
        
        for neighbor in neighborhood:
            if neighbor in neighborhood_previous:    
                fitness_of_neighbor = fintess_in_previous_neighborhood[neighborhood_previous.index(neighbor)]
                fitness_in_neighborhood.append(fitness_of_neighbor)
            else:
                fitness_of_neighbor = fitness(neighbor, customers_taste, parameter_names)
                fitness_in_neighborhood.append(fitness_of_neighbor)
            
            if (neighbor not in tabu_list) and (fitness_of_neighbor > fitness_of_iteration_best_candidate):
                iteration_best_candidate = neighbor
                better_candidate_found   = True
                
        if better_candidate_found == False:
            foo = 0.0
            for i in range(len(neighborhood)):
                if (neighborhood[i] not in tabu_list) and (fitness_in_neighborhood[i] > foo):
                    iteration_best_candidate = neighborhood[i]
                    foo                      = fitness_in_neighborhood[i]
                
        fitness_of_iteration_best_candidate = fitness(iteration_best_candidate, customers_taste, parameter_names)
        if fitness_of_iteration_best_candidate > fitness_overall_best_candidate:
            overall_best_candidate         = iteration_best_candidate
            fitness_overall_best_candidate = fitness_of_iteration_best_candidate
            
        if len(tabu_list) > max_tabu_size:
            tabu_list.pop()
        
        tabu_list.append(iteration_best_candidate)
        
    return overall_best_candidate, fitness_overall_best_candidate