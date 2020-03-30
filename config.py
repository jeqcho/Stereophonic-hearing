import visualisation_lab as vl
import random
import pygame
import math

# IMPORTANT: SPECIFY TO LOAD DATA OR TO CREATE FROM SCRATCH
# If set to true, the neural networks and related data from data file will be loaded
# IF SET TO FALSE, THE DATA IN data_file WILL BE OVERIDED
# A corresponding json file will be created for human reading
load_data = True
data_file = 'network_data.db'

# the top percentage where entities in each species are allowed to randomly mate
merit_bias = .5

# initialise
# ticks_per_test = 500
tick_per_animation = 500
population_limit = 200
num_sensory = 4
num_effector = 2
new_species_id = 1
excess_c = 1.0
disjoint_c = 1.0
weight_diff_c = 3.0
comp_threshold = 1.5

# Environment
num_speaker = 6

speaker_pos = []


def to_deg(y, x):
    angle = math.atan2(y, x)
    angle = math.degrees(angle)
    return angle


def preprocess(response, answer):
    angle1 = to_deg(response[1], response[0])
    angle2 = to_deg(answer[1], answer[0])
    return angle1, angle2


def grade(angle1, angle2):
    # 2 responses, for each axes on Cartesian plane
    score = 100
    diff = abs(angle1-angle2)
    if diff > 180:
        diff = 360 - diff
    score *= 1 - diff/180
    return score


def test(network, animate_flag=False):
    # clock = pygame.time.Clock()
    running = True
    speaker_counter = 0
    score = 0
    host = vl.Host((200, 0, 0))

    while running:
        # clock.tick(60)
        if speaker_counter == num_speaker:
            return score
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        # intensity 1, intensity 2, time 1, time 2
        speaker = vl.Speaker(speaker_pos[speaker_counter][0], speaker_pos[speaker_counter][1])

        sq_dist_to_ear1 = pow(host.ear1['x']-speaker.x, 2) + pow(host.ear1['y']-speaker.y, 2)
        intensity1 = speaker.intensity / sq_dist_to_ear1
        time1 = math.sqrt(sq_dist_to_ear1) / speaker.velocity

        sq_dist_to_ear2 = pow(host.ear2['x']-speaker.x, 2) + pow(host.ear2['y']-speaker.y, 2)
        intensity2 = speaker.intensity / sq_dist_to_ear2
        time2 = math.sqrt(sq_dist_to_ear2) / speaker.velocity

        sense = [
            intensity1,
            intensity2,
            time1,
            time2
        ]

        # think
        response = network.think(sense)

        # perform
        answer = [speaker.x-host.x, -(speaker.y-host.y)]
        angles = preprocess(response, answer)
        this_score = grade(angles[0], angles[1])
        score += this_score

        # refresh the screen
        tick_counter = 0
        if animate_flag:
            print("SENSE OF CHAMPION")
            print(sense)
            print("RESPONSE OF CHAMPION")
            print(response)
            print("ANSWER")
            print(answer)
            print("ANGLE OF CHAMPION")
            print(angles[0])
            print("ANGLE OF ANSWER")
            print(angles[1])
            print("THIS SCORE")
            print(this_score)
            vl.reset()
            host = vl.Host((200, 0, 0))
            speaker = vl.Speaker(speaker_pos[speaker_counter][0], speaker_pos[speaker_counter][1])
            vl.screen.blit(vl.background, (0, 0))
            vl.all_sprites.draw(vl.screen)
            vl.draw_response(response, vl.screen)
            vl.draw_answer(speaker_pos[speaker_counter], vl.screen)
            pygame.display.update()
            tick_counter += 1
            input('Press enter to continue')

        # count the number of ticks
        speaker_counter += 1


def start_round():
    global speaker_pos
    speaker_pos = []
    for i in range(0, num_speaker):
        x = random.random() * (vl.screen_width - vl.speaker_width)
        y = random.random() * (vl.screen_height - vl.speaker_height)
        speaker_pos.append([x, y])

