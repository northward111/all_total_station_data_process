import numpy as np
from transform import transform
from create_shp import create_shp


def get_coordinates_from_num(num, input_file_name):
    with open(input_file_name, "r") as source_file:
        for line in source_file.readlines():
            items = line.split(",")
            if len(items) > 2 and int(items[0]) == num:
                return [float(items[1]), float(items[2])]


def get_translation_lsq_matrix(input_file_name, reference_file_name):
    A_list = []
    Y_list = []
    with open(reference_file_name, "r") as ref_file:
        for line in ref_file.readlines():
            items = line.split(",")
            if len(items) > 2:
                origin_point = get_coordinates_from_num(int(items[0]), input_file_name)
                if origin_point is not None:
                    Y_list.append(float(items[1]) - origin_point[0])
                    Y_list.append(float(items[2]) - origin_point[1])
                    A_list.append([1, 0])
                    A_list.append([0, 1])
    A = np.array(A_list)
    Y = np.array(Y_list)
    At = np.transpose(A)
    AtA = np.dot(At, A)
    AtAInv = np.linalg.inv(AtA)
    matrix2 = np.dot(np.dot(AtAInv, At), Y)
    matrix = np.array([[1, 0, matrix2[0]],
                       [0, 1, matrix2[1]],
                       [0, 0, 1]])
    return matrix


# 仿射变换最小二乘法
def get_affine_lsq_matrix(input_file_name, reference_file_name):
    A_list = []
    Y_list = []
    with open(reference_file_name, "r") as ref_file:
        for line in ref_file.readlines():
            items = line.split(",")
            if len(items) > 2:
                origin_point = get_coordinates_from_num(int(items[0]), input_file_name)
                if origin_point is not None:
                    Y_list.append(float(items[1]))
                    Y_list.append(float(items[2]))
                    A_list.append([origin_point[0], origin_point[1], 0, 0, 1, 0])
                    A_list.append([0, 0, origin_point[0], origin_point[1], 0, 1])
    A = np.array(A_list)
    Y = np.array(Y_list)
    At = np.transpose(A)
    AtA = np.dot(At, A)
    AtAInv = np.linalg.inv(AtA)
    matrix2 = np.dot(np.dot(AtAInv, At), Y)
    matrix = np.array([[matrix2[0], matrix2[1], matrix2[4]],
                       [matrix2[2], matrix2[3], matrix2[5]],
                       [0, 0, 1]])
    return matrix


def get_affine_matrix(input_file_name, reference_file_name):
    A_list = []
    Y_list = []
    with open(reference_file_name, "r") as ref_file:
        for line in ref_file.readlines():
            items = line.split(",")
            if len(items) > 2:
                origin_point = get_coordinates_from_num(int(items[0]), input_file_name)
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
    destination = np.array([[Y[0], Y[2], Y[4]],
                            [Y[1], Y[3], Y[5]],
                            [1.0, 1.0, 1.0]])
    origin = np.array([[A[0, 0], A[2, 0], A[4, 0]],
                       [A[0, 1], A[2, 1], A[4, 1]],
                       [1.0, 1.0, 1.0]])
    matrix = np.dot(destination, np.linalg.inv(origin))
    return matrix


def main():
    input_file_name = "data/origin.txt"
    output_file_name = "data/destination.txt"
    reference_file_name = "data/reference.txt"

    matrix = get_translation_lsq_matrix(input_file_name, reference_file_name)

    with open(input_file_name, "r") as input_file, open(output_file_name, "w") as output_file:
        for line in input_file.readlines():
            items = line.split(",")
            if len(items) > 2:
                origin_point = np.array([float(items[1]), float(items[2]), 1.0])
                destination_point = np.dot(matrix, origin_point)
                print(destination_point)
                output_file.write("{},{},{},\n".format(items[0], destination_point[0], destination_point[1]))
    transformed_file_name = "data/transformed.txt"
    transform(output_file_name, transformed_file_name)
    create_shp(transformed_file_name, "lane_point_84")


if __name__ == '__main__':
    main()
