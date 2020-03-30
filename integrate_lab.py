import visualisation_lab as vl
import neural_network_lab as nnl
import config as cfg
import random
import copy
import pygame
import json
import shelve

# IMPORTANT
# YOU SHOULD ONLY CHANGE THE CONFIGURATION FILE AND VISUALISATION FILE

# neural network
neural_networks = {}

# results for the current round
results = {}

# ranking (zero-indexed)
ranking = []

# record of all entities categorised by species
# key: species number, value: list of entities index in neural_network dict
community = {}
species_fitness = {}
species_new_num = {}

# key: species number, value: dictionary of network_id and score

# statistics
species_mean_fitness = {}
species_num = {}

# data for the current run
next_innov_num = 0
new_species_id = 1
next_network_id = cfg.population_limit
generation_num = 1
record_highscore = 0

if cfg.load_data:
    input("Load data from " + cfg.data_file + '? Press enter to continue')
    with shelve.open(cfg.data_file) as s:
        for network_id, network in s.items():
            if network_id == 'data':
                continue
            neural_networks[int(network_id)] = network
        next_innov_num, new_species_id, next_network_id, generation_num, record_highscore = s['data']


def cal_compatibility(network1_id, network2_id):
    network1 = neural_networks[network1_id]
    network2 = neural_networks[network2_id]
    total_weight_diff = 0
    num_match = 0
    num_excess = 0
    num_disjoint = 0
    if network1.synapse_genes.keys():
        max_innov1 = max(network1.synapse_genes.keys())
        min_innov1 = min(network1.synapse_genes.keys())
    else:
        max_innov1 = 0
        min_innov1 = 0
    if network2.synapse_genes.keys():
        max_innov2 = max(network2.synapse_genes.keys())
        min_innov2 = min(network2.synapse_genes.keys())
    else:
        max_innov2 = 0
        min_innov2 = 0
    max_size = max(len(network1.synapse_genes.keys()), len(network2.synapse_genes.keys()))
    min_innov = min(min_innov1, min_innov2)
    if max_innov1 > max_innov2:
        # network2 has excess
        network1, network2 = network2, network1
        max_innov1, max_innov2 = max_innov2, max_innov1
    for i in range(min_innov, max_innov2+1):
        if i in network1.synapse_genes:
            present1 = True
        else:
            present1 = False
        if i in network2.synapse_genes:
            present2 = True
        else:
            present2 = False
        if present1 and present2:
            total_weight_diff += abs(network1.synapse_genes[i].weight - network2.synapse_genes[i].weight)
            num_match += 1
        elif present1 or present2:
            if num_match > 0:
                num_disjoint += 1
            else:
                num_excess += 1
    dist_measure = 0
    if num_excess > 0:
        dist_measure += cfg.excess_c * num_excess / max_size
    if num_disjoint > 0:
        dist_measure += cfg.disjoint_c * num_disjoint / max_size
    if num_match > 0:
        avg_weight_diff = total_weight_diff / num_match
        dist_measure += cfg.weight_diff_c * avg_weight_diff
    return dist_measure


def find_species(network_id):
    global community, new_species_id
    for species_id, network_ids in community.items():
        # rand_sample_id = random.choice(network_ids)
        rand_sample_id = network_ids[0]
        if cal_compatibility(rand_sample_id, network_id) <= cfg.comp_threshold:
            network_ids.append(network_id)
            neural_networks[network_id].species = species_id
            return
    community[new_species_id] = [network_id]
    neural_networks[network_id].species = new_species_id
    new_species_id += 1


for x in range(0, cfg.population_limit):
    neural_networks[x] = nnl.Network(x, cfg.num_sensory, cfg.num_effector)
    next_innov_num = neural_networks[x].mutate(next_innov_num)


# function for ranking
def rank(blocky_id_):
    return results[blocky_id_]


results = {}
new_networks = {}


def mate(network1, network2):
    global next_innov_num
    first_better = results[network1.id] > results[network2.id]
    if first_better:
        new_network = copy.deepcopy(network1)
    else:
        new_network = copy.deepcopy(network2)
    new_network.id = next_network_id
    next_innov_num = new_network.mutate(next_innov_num)
    return new_network



running = True
while running:
    # start new round
    cfg.start_round()
    num_test = 0
    total_score = 0
    results = {}
    print("TRAINING...")
    for network_id in list(neural_networks.keys()):
        num_test += 1
        results[network_id] = cfg.test(neural_networks[network_id])
        total_score += results[network_id]
    mean_score = round(total_score / num_test, 2)

    # Species
    community.clear()
    new_species_id = 0
    for network_id, network in neural_networks.items():
        find_species(network_id)

    # rank each blocky by results
    ranking = []
    for network_id in results:
        ranking.append(network_id)
    ranking.sort(key=rank)
    ranking.reverse()
    highscore = results[ranking[0]]
    cfg.test(neural_networks[ranking[0]], True)

    # Record fitness of each species
    print("SPECIES NUMBER")
    total_fitness = 0
    species_mean_fitness.clear()
    species_fitness.clear()
    for species_id, network_ids in community.items():
        species_fitness[species_id] = 0
        for network_id in network_ids:
            species_fitness[species_id] += results[network_id]
        total_fitness += species_fitness[species_id]
        print(species_id, ': ', len(network_ids))
        species_mean_fitness[species_id] = round(species_fitness[species_id] / len(network_ids), 2)
    print("SPECIES FITNESS")
    print(species_fitness)
    print("MEAN FITNESS")
    print(species_mean_fitness)
    mean_fitness = total_fitness / len(neural_networks)
    for species_id, fitness in species_fitness.items():
        species_new_num[species_id] = int(fitness / mean_fitness + .5)

    # reproduce
    new_networks.clear()
    next_network_id = 0
    for species_id, network_ids in community.items():
        ranking_in_species = sorted(network_ids, key=lambda network_id: results[network_id], reverse=True)
        t = 0
        mates = []
        while float(t/len(network_ids)) < cfg.merit_bias:
            mates.append(ranking_in_species[t])
            t += 1
        for i in range(0, species_new_num[species_id]):
            mate1 = random.choice(mates)
            mate2 = random.choice(mates)
            new_networks[next_network_id] = mate(neural_networks[mate1], neural_networks[mate2])
            next_network_id += 1
    while len(new_networks) < cfg.population_limit:
        mate1 = random.randrange(cfg.population_limit)
        mate2 = random.choice(community[neural_networks[mate1].species])
        new_networks[next_network_id] = mate(neural_networks[mate1], neural_networks[mate2])
        next_network_id += 1
    while len(new_networks) > cfg.population_limit:
        unlucky_network_id = random.choice(list(new_networks.keys()))
        del new_networks[unlucky_network_id]
    neural_networks = copy.deepcopy(new_networks)
    print("Current population: " + str(len(neural_networks)))

    # report highlights
    mean_score = round(mean_score, 2)
    print("Mean score:", mean_score)
    print("Highscore:", highscore)
    if highscore > record_highscore:
        print("NEW HIGHSCORE")
        record_highscore = highscore
    print("GENERATION NO:", generation_num)
    generation_num += 1
    vl.screen.blit(vl.background, (0, 0))
    pygame.display.update()
    save = input("Press key S to save. Press enter to continue")
    print("Saving")
    if save == 'S' or save == 's':
        with open(cfg.data_file + '.json', 'w') as f:
            for network_id, network in neural_networks.items():
                f.write(json.dumps(network, default=lambda x: x.__dict__))
                f.write('\n')
            f.write(json.dumps([next_innov_num, new_species_id, next_network_id, generation_num, record_highscore]))
        with shelve.open(cfg.data_file) as s:
            s.clear()
            for network_id, network in neural_networks.items():
                s[str(network_id)] = network
            s['data'] = [next_innov_num, new_species_id, next_network_id, generation_num, record_highscore]
    # end current round
