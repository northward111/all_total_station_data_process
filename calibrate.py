import numpy as np
from transform import transform
from main import create_shp


def get_coordinates_from_num(num):
    with open("origin.txt", "r") as input_file:
        for line in input_file.readlines():
            items = line.split(",")
            if len(items) > 2 and int(items[0]) == num:
                return [float(items[1]), float(items[2])]


if __name__ == '__main__':
    destination = np.array([[534168.65, 534155.74, 534102.73],
                            [3378660.86, 3378645.18, 3378655.00],
                            [1.0, 1.0, 1.0]])
    origin = np.array([[534170.147, 534152.940, 534098.419],
                       [3378667.484, 3378651.772, 3378662.079],
                       [1.0, 1.0, 1.0]])
    A_list = []
    Y_list = []
    with open("reference.txt", "r") as ref_file:
        for line in ref_file.readlines():
            items = line.split(",")
            if len(items) > 2:
                origin_point = get_coordinates_from_num(int(items[0]))
                if origin_point is not None:
                    Y_list.append(float(items[1]))
                    Y_list.append(float(items[2]))
                    A_list.append([origin_point[0], origin_point[1], 0, 0, 1, 0])
                    A_list.append([0, 0, origin_point[0], origin_point[1], 0, 1])
                    # Y = np.append(Y, [float(items[1]), float(items[2])])
                    # A = np.append(A, [[origin_point[0], origin_point[1], 0, 0, 1, 0],
                    #                   [0, 0, origin_point[0], origin_point[1], 0, 1]], axis=1)
    A = np.array(A_list)
    Y = np.array(Y_list)
    At = np.transpose(A)
    AtA = np.dot(At, A)
    AtAInv = np.linalg.inv(AtA)
    matrix2 = np.dot(np.dot(AtAInv, At), Y)
    print(matrix2)
    destination = np.array([[Y[0], Y[2], Y[4]],
                           [Y[1], Y[3], Y[5]],
                           [1.0, 1.0, 1.0]])
    origin = np.array([[A[0, 0], A[2, 0], A[4, 0]],
                      [A[0, 1], A[2, 1], A[4, 1]],
                      [1.0, 1.0, 1.0]])
    matrix1 = np.dot(destination, np.linalg.inv(origin))
    print(matrix1)
    matrix = np.array([[matrix2[0], matrix2[1], matrix2[4]],
                       [matrix2[2], matrix2[3], matrix2[5]],
                       [0, 0, 1]])
    input_file_name = "origin.txt"
    output_file_name = "destination.txt"
    transformed_file_name = "transformed.txt"
    with open(input_file_name, "r") as input_file, open(output_file_name, "w") as output_file:
        for line in input_file.readlines():
            items = line.split(",")
            if len(items) > 2:
                origin_point = np.array([float(items[1]), float(items[2]), 1.0])
                destination_point = np.dot(matrix, origin_point)
                print(destination_point)
                output_file.write("{},{},{},\n".format(items[0], destination_point[0], destination_point[1]))
    transform(output_file_name, transformed_file_name)
    create_shp(transformed_file_name)
