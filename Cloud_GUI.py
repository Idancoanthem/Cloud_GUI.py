from tkinter import *
from clouds2 import export_to_text, polydisperse_distribution, check_density
import tkinter.messagebox
root = Tk()
root.title("Cloud Generator")

def show_readme():
    tkinter.messagebox.showinfo('README', "This program generates clouds as a collection of point drops in 3D space.\n\
It generates cubes full of drops and then stacks cubes in a rectangular shape in the desired size. The input parameters are as follows:\n\
File name\nFile type - 1 for CSV, 2 for txt\n\
Distribution type - 1 for constant radii, 2 for uniformly random distribution around the drop size, and 3 for the polydisperse distribution.\n\
SizeX/SizeY/SizeZ - cube size in the three dimensions *in meters*\n\
# of cubes X/# of cubes Y/# of cubes z - number of cubes in each dimension")

def done():
    tkinter.messagebox.showinfo('Cloud Generated', 'Cloud Generated')

file_name_e = Entry(root, width=20, borderwidth=5)
file_name_e.grid(row=0, column=1, columnspan=3, padx=10, pady=10)
file_name_e.insert(0, 'Cloud 1')
file_name_label = Label(root, text="File Name")
file_name_label.grid(row=0, column=0)

file_type_e = Entry(root, width=20, borderwidth=5)
file_type_e.grid(row=1, column=1, columnspan=3, padx=10, pady=10)
file_type_e.insert(0, '2')
file_type_label = Label(root, text="File Type")
file_type_label.grid(row=1, column=0)

distribution_type_e = Entry(root, width=20, borderwidth=5)
distribution_type_e.grid(row=2, column=1, columnspan=3, padx=10, pady=10)
distribution_type_e.insert(0, '1')
distribution_type_label = Label(root, text="Distribution Type")
distribution_type_label.grid(row=2, column=0)

drop_size_e = Entry(root, width=20, borderwidth=5)
drop_size_e.grid(row=3, column=1, columnspan=3, padx=10, pady=10)
drop_size_e.insert(0, '10')
drop_size_label = Label(root, text="Drop Size")
drop_size_label.grid(row=3, column=0)

size_x_e = Entry(root, width=20, borderwidth=5)
size_x_e.grid(row=4, column=1, columnspan=3, padx=10, pady=10)
size_x_e.insert(0, '0.01')
size_x_label = Label(root, text="Size X")
size_x_label.grid(row=4, column=0)

size_y_e = Entry(root, width=20, borderwidth=5)
size_y_e.grid(row=5, column=1, columnspan=3, padx=10, pady=10)
size_y_e.insert(0, '0.01')
size_y_label = Label(root, text="Size Y")
size_y_label.grid(row=5, column=0)

size_z_e = Entry(root, width=20, borderwidth=5)
size_z_e.grid(row=7, column=1, columnspan=3, padx=10, pady=10)
size_z_e.insert(0, '0.01')
size_z_label = Label(root, text="Size Z")
size_z_label.grid(row=7, column=0)

cube_x_e = Entry(root, width=20, borderwidth=5)
cube_x_e.grid(row=0, column=5, columnspan=3, padx=10, pady=10)
cube_x_e.insert(0, '1')
cube_x_label = Label(root, text="# of cubes X")
cube_x_label.grid(row=0, column=4)

cube_y_e = Entry(root, width=20, borderwidth=5)
cube_y_e.grid(row=1, column=5, columnspan=3, padx=10, pady=10)
cube_y_e.insert(0, '1')
cube_y_label = Label(root, text="# of cubes Y")
cube_y_label.grid(row=1, column=4)

cube_z_e = Entry(root, width=20, borderwidth=5)
cube_z_e.grid(row=2, column=5, columnspan=3, padx=10, pady=10)
cube_z_e.insert(0, '1')
cube_z_label = Label(root, text="# of cubes Z")
cube_z_label.grid(row=2, column=4)

r_eff_e = Entry(root, width=20, borderwidth=5)
r_eff_e.grid(row=3, column=5, columnspan=3, padx=10, pady=10)
r_eff_e.insert(0, '10')
r_eff_label = Label(root, text="Effective Radius [microns]")
r_eff_label.grid(row=3, column=4)


finished = Label(root, text='Cloud Generated')
def define_params():
    file_name = file_name_e.get()
    file_type = int(file_type_e.get())  # 1 for csv, 2 for txt
    distribution_type = int(distribution_type_e.get()) # 1 for constant radii, 2 for random uniform, 3 for polydisperse
    drop_size = round(float(drop_size_e.get()) * pow(10, -6), 7)  # enter in microns
    ### polydisperse
    r_eff = float(r_eff_e.get())
    sigma = 0.267 * r_eff
    prob_vector, Radii, sum_poly = polydisperse_distribution(r_eff, sigma)
    ### polydisperse
    distribution_parameters = [distribution_type, drop_size, prob_vector, Radii, sum_poly]      # 1 for constant radius, 2 for uniform random distribution, 3 for polydisperse

    sizeX = float(size_x_e.get())             # cube x dimension, in meters
    sizeY = float(size_y_e.get())             # cube y dimension, in meters
    sizeZ = float(size_z_e.get())             # cube z dimension, in meters
    size = [sizeX, sizeY, sizeZ]

    number_of_drops = check_density(sizeX, sizeY, sizeZ)      # number of drops in each cube
    cubeX = int(cube_x_e.get())                               # number of cubes in the x direction
    cubeY = int(cube_y_e.get())                               # number of cubes in the y direction
    cubeZ = int(cube_z_e.get())                               # number of cubes in the z direction
    cubes = [cubeX, cubeY, cubeZ]

    export_to_text(size, number_of_drops, cubes, distribution_parameters, file_name, file_type)
    done()
    # print("time elapsed: {:.2f}s".format(time.time() - start_time))
    return


Create_Cloud = Button(root, text='Create Cloud', padx=40, pady=20, command=define_params)
Create_Cloud.grid(row=4, column=4)

README = Button(root, text='README', padx=45, pady=20, command=show_readme)
README.grid(row=4, column=5)

root.mainloop()



