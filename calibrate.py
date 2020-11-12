import numpy as np

if __name__ == '__main__':
    destination = np.array([[534168.65, 534155.74, 534102.73],
                            [3378660.86, 3378645.18, 3378655.00],
                            [1.0, 1.0, 1.0]])
    origin = np.array([[534170.147, 534152.940, 534098.419],
                       [3378667.484, 3378651.772, 3378662.079],
                       [1.0, 1.0, 1.0]])
    matrix = np.dot(destination, np.linalg.inv(origin))
    print(matrix)
    with open("origin.txt", "r") as input_file, open("destination.txt", "w") as output_file:
        for line in input_file.readlines():
            items = line.split(",")
            if len(items) > 2:
                origin_point = np.array([float(items[1]), float(items[2]), 1.0])
                destination_point = np.dot(matrix, origin_point)
                print(destination_point)
                output_file.write("{},{},{},\n".format(items[0], destination_point[0], destination_point[1]))
