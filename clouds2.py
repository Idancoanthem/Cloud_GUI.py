import math
import random
import csv
import time
import numpy as np
from math import sqrt

### the units in this code are meters ###
def check_overlap(drop1, drop2):
    diffX = pow(abs(drop1[0]-drop2[0]),2)    #calculate distances
    diffY = pow(abs(drop1[1]-drop2[1]),2)
    diffZ = pow(abs(drop1[2]-drop2[2]),2)
    total = diffX+diffY+diffZ
    distance = math.sqrt(total)
    if distance < drop1[3] + drop2[3]:
        return True
    else:
        return False

def polydisperse(R_drop, r_eff, sigma):
    a = sigma**2
    b = 6*sigma**2 - r_eff**2
    c = 9*sigma**2 - r_eff**2
    mu = ((-b + math.sqrt((b**2 - 4 * a * c))) / (2 * a))
    a_0 = mu * sigma / math.sqrt(mu + 1)
    norm = pow(mu, mu+1) / (pow(a_0, mu + 1) * math.gamma(mu + 1))
    n = norm * pow(R_drop, mu) * math.exp(-(mu*R_drop/a_0))
    return n

def polydisperse_distribution(r_eff, sigma):
    prob_vector = []
    Radii = []
    sum_poly = 0
    for i in range(1,992):
        Radii.append(1+0.1*(i-1))
        prob_vector.append(polydisperse(1+0.1*(i-1), r_eff, sigma))
        sum_poly = sum_poly + prob_vector[i-1]
    return prob_vector, Radii, sum_poly

def drop_distribution(distribution_parameters):
    R_drop = distribution_parameters[1]
    if distribution_parameters[0] == 1:           # constant sized drops
        drop_size = R_drop
    elif distribution_parameters[0] == 2:         # random uniform distribution
        drop_size = round(random.uniform(0.1 * R_drop, 10 * R_drop), 7)
    elif distribution_parameters[0] == 3:         # polydisperse size distribution
        prob_vector = distribution_parameters[2]
        Radii = distribution_parameters[3]
        sum_poly = distribution_parameters[4]
        drop_size = round(pow(10, -6) * float(np.random.choice(Radii, 1, p=np.divide(prob_vector, sum_poly))),7)
    return drop_size


def drop_generator(startX, startY, startZ, size, distribution_parameters):
    X = round(startX + random.uniform(0, size[0]),7)              # drop X position
    Y = round(startY + random.uniform(0, size[1]),7)              # drop Y position
    Z = round(startZ + random.uniform(0, size[2]),7)              # drop Z position
    drop_size = drop_distribution(distribution_parameters)            # drop size, chosen distribution
    drop = [X, Y, Z, drop_size]
    return drop

def fill_cube(startX, startY, startZ, size, number_of_drops, distribution_parameters):
    cube = [drop_generator(startX, startY, startZ, size, distribution_parameters)]

    while len(cube) < number_of_drops:                                                  # Number of drops in a cube
        drop = drop_generator(startX, startY, startZ, size, distribution_parameters)
        flag = True
        for item in cube:
            if check_overlap(drop, item):
                flag = False
                break
        if flag:
            cube.append(drop)
    return cube

def make_100_cubes(size, number_of_drops, cubes, distribution_parameters):
    MEGACUBE = []
    for i in range(0,cubes[0]):              # number of cubes in the X direction
        for j in range (0,cubes[1]):         # number of cubes in the Y direction
            for k in range(0,cubes[2]):      # number of cubes in the Z direction
                startX = i*size[0]
                startY = j*size[1]
                startZ = k*size[2]
                MEGACUBE.append(fill_cube(startX, startY, startZ, size, number_of_drops, distribution_parameters))
    return MEGACUBE

def export_to_text(size, number_of_drops, cubes, distribution_parameters, file_name, file_type):
    if file_type == 1:                                                                # CSV chosen
        f = open(file_name + '.csv', "w+", newline='')                                # Open CSV file in write form
        writer = csv.writer(f)
        mega = make_100_cubes(size, number_of_drops, cubes, distribution_parameters)  # Generate cloud
        writer.writerow([" Z: "+ str(size[2] * cubes[2])," Y: "+ str(size[1] * cubes[1]),"X: "+ str(size[0] * cubes[0]),"Cloud dimensions: "])  # Cloud dimensions
        writer.writerow(["Z position", "Y position", "X position", "Radius"])         # Column names
        for cube in mega:
            for drop in cube:
                X = drop[0]
                Y = drop[1]
                Z = drop[2]
                drop_size = drop[3]
                writer.writerow([str(Z), str(Y), str(X) ,str(drop_size)])             # Write drop location and size
        f.close()                                                                     # Close file
    elif file_type == 2:                                                              # txt chosen
        f = open(file_name + '.txt', "w")                                             # Open txt file in write form
        mega = make_100_cubes(size, number_of_drops, cubes, distribution_parameters)  # Generate cloud
        f.write("Cloud dimensions: " + "X: "+ str(size[0] * cubes[0]) + " Y: "+ str(size[1] * cubes[1]) +" Z: "+ str(size[2] * cubes[2]) + "\n")
        f.write("Radius\t\tX position\t\tY position\t\tZ position\n")
        for cube in mega:
            for drop in cube:
                X = drop[0]
                Y = drop[1]
                Z = drop[2]
                drop_size = drop[3]
                # writer.writerow(["10e-6",str(X),str(Y),str(Z)])
                f.write(f"{drop_size}\t\t{X:.7f}\t\t{Y:.7f}\t\t{Z:.7f}\n")
        f.close()



# def export_to_text1(size, number_of_drops, cubes, distribution_parameters, file_name):
#     f = open(file_name+'.txt', "w")
#     mega = make_100_cubes(size, number_of_drops, cubes, distribution_parameters)
#     # writer.writerow(["Radius","X position","Y position","Z position"])
#     f.write("Radius       X position      Y position      Z position\n")
#     # f.write("Radius","X position","Y position","Z position")
#     for cube in mega:
#         for drop in cube:
#             X = drop[0]
#             Y = drop[1]
#             Z = drop[2]
#             drop_size = drop[3]
#             # writer.writerow(["10e-6",str(X),str(Y),str(Z)])
#             f.write(str(drop_size)+'         '+str(X)+'      '+str(Y)+'      '+str(Z)+'\n')
#     f.close()

def calculate_fractional_volume(drop, N, cube):
    drop_volume = (4/3)*math.pi*pow(drop,3)
    cube_volume = pow(cube,3)
    fractional_volume = N*drop_volume/cube_volume
    return fractional_volume

def check_density(x, y, z):
    density = 300/(pow(10, -6))
    n_drops = density*x*y*z
    return n_drops

if __name__=="__main__":
    #normal sized cubes:
    # print(check_density(1 / 100, 1 / 100, 1 / 1000)) #checks how many drops you need to put in a cube with set sizes
    start_time = time.time()                 #timer
    drop_size = pow(10, -5)
    r_eff = 10
    sigma = 0.267 * r_eff
    distribution_type = 3
    prob_vector, Radii, sum_poly = polydisperse_distribution(r_eff, sigma)
    distribution_parameters = [distribution_type, drop_size, prob_vector, Radii, sum_poly]      # 1 for constant radius, 2 for uniform random distribution, 3 for polydisperse
    file_name = 'polydisperse radii 5'
    sizeX = 0.01                             # cube x dimension
    sizeY = 0.01                             # cube y dimension
    sizeZ = 0.001                            # cube z dimension
    size = [sizeX, sizeY, sizeZ]
    print(check_density(sizeX, sizeY, sizeZ))
    number_of_drops = check_density(sizeX, sizeY, sizeZ)                     #number of drops in each cube
    cubeX = 100                               # number of cubes in the x direction
    cubeY = 100                               # number of cubes in the y direction
    cubeZ = 1                               # number of cubes in the z direction
    cubes = [cubeX, cubeY, cubeZ]
    file_type = 2                           # 1 for csv, 2 for txt
    export_to_text(size, number_of_drops, cubes, distribution_parameters, file_name, file_type)

    print("time elapsed: {:.2f}s".format(time.time() - start_time))
    # # small cube
    # drop_size = pow(10, -6)
    # sizeX = 2 * pow(10, -5)
    # sizeY = 2 * pow(10, -5)
    # sizeZ = 2 * pow(10, -5)
    # number_of_drops = 20
    # export_to_text(sizeX, sizeY, sizeZ, drop_size, number_of_drops)

    # drop = pow(10,-5)
    # cube = pow(10,-2)
    # N = 300
    # print(calculate_fractional_volume(drop, N, cube))
    # X = 0
    # for item in make_100_cubes():
    #    X += len(item)
    # print(X)