import numpy as np


def main():
    f = open("faceindex.txt", "r")
    inp = f.read()
    f.close()

    inp = read_vals(inp)

    # inp = inp*2
    inp[:, 0] *= 1.4
    inp[:, 1] *= 2.2
    inp[:, 2] *= 1.3

    write_vals(inp)

    print(inp)


def read_vals(inp):
    points = inp.split(",")
    # print(points)
    for i, p in enumerate(points):
        points[i] = p.split(" ")
        if points[i][0] == "":
            points[i] = points[i][1:]
        points[i] = np.array([float(k) for k in points[i]])
        # print(points[i].shape)

    points = np.stack(points)

    return points


def write_vals(points):
    j = []
    for i, p in enumerate(points):
        j.append([str(k) for k in points[i]])
        # print(j)
        j[-1] = " ".join(j[-1])

    fin = ",".join(j)
    f = open("faceindex2.txt", "w")
    f.write(fin)
    f.close()


if __name__ == "__main__":
    main()
