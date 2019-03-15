import os
import csv
import numpy as np
import matplotlib.pyplot as plt

# global
folder = 'Data/chargeAmplifier/Normal/'
output_folder = 'Data/'

# parser for vibration.


def string_to_float(str):
    str_list = str.split(",")
    return [float(str) for str in str_list]


def parser(data, label):
    # variable.
    pvdf1 = []
    pvdf2 = []
    pvdf3 = []
    pvdf4 = []
    pvdf5 = []

    for x in range(4, len(data)):
        float_list = string_to_float(data[x][0])
        pvdf1.append(float_list[1])
        pvdf2.append(float_list[3])
        pvdf3.append(float_list[5])
        pvdf4.append(float_list[7])
        pvdf5.append(float_list[9])
    return pvdf1, pvdf2, pvdf3, pvdf4, pvdf5


def parser2(data, label):
    # variable.
    pvdf1 = []

    for x in range(0, len(data)):
        float_list = string_to_float(data[x][0])
        pvdf1.append(float_list[1])
    return pvdf1


def amplitude(List):
    Complex = np.fft.fft(List)
    fftFreq = np.fft.fftfreq(len(List), d=1/25600)
    amplitude = np.abs(Complex)
    return fftFreq[1:int(len(fftFreq)/2)], amplitude[1:int(len(amplitude)/2)]


def plot_timeDomain(list_1):
    # set x axis range initial figure.
    x = np.linspace(0, 17.06, len(list_1))
    plt.figure()
    # plot.
    plt.plot(x, list_1, label='pvdf 1', color='orange')
    # plt.figure()
    # plt.plot(x, list_2, label='pvdf 2', color='blue')
    # plt.figure()
    # plt.plot(x, list_3, label='pvdf 3', color='green')
    # plt.figure()
    # plt.plot(x, list_4, label='pvdf 4', color='yellow')
    # plt.figure()
    # plt.plot(x, list_5, label='pvdf 5', color='red')

    plt.show()


def plot_freqDomain(list_1):
    # count amplitude.
    list_1_x, list_1_y = amplitude(list_1)
    # list_2_x, list_2_y = amplitude(list_2)
    # list_3_x, list_3_y = amplitude(list_3)
    # list_4_x, list_4_y = amplitude(list_4)
    # list_5_x, list_5_y = amplitude(list_5)
    # set x axis range and initial figure.
    plt.figure()
    # plot.
    plt.plot(list_1_x, list_1_y, label='pvdf 1', color='orange')
    # plt.figure()
    # plt.plot(list_2_x, list_2_y, label='pvdf 2', color='blue')
    # plt.figure()
    # plt.plot(list_3_x, list_3_y, label='pvdf 3', color='green')
    # plt.figure()
    # plt.plot(list_4_x, list_4_y, label='pvdf 4', color='yellow')
    # plt.figure()
    # plt.plot(list_5_x, list_5_y, label='pvdf 5', color='red')
    plt.show()


if __name__ == "__main__":

    # search all file in folder.
    FileNames = []
    for root, dirs, files in os.walk(folder):
        for filename in files:
            FileNames.append(filename)

    # create file.
    # pvdf1.
    # pvdf1_file = open(output_folder+"pvdf1_train_SVM_withBG.txt", 'a+',encoding='utf8',newline='')
    # Writer1 = csv.writer(pvdf1_file)
    # pvdf2.
    # pvdf2_file = open(output_folder+"實驗A 矽鋼片1.csv",
    #                   'a+', encoding='utf8', newline='')
    # Writer2 = csv.writer(pvdf2_file)
    # pvdf3.
    # pvdf3_file = open(output_folder+"pvdf3_train_SVM.txt", 'a+',encoding='utf8',newline='')
    # Writer3 = csv.writer(pvdf3_file)

    for filename in FileNames:
        print(filename)
        with open(folder+filename, "r") as file:
            Data = list(csv.reader(file, delimiter="\t"))
        pvdf1 = parser2(Data, 1)
        print(len(pvdf1))
        plot_timeDomain(pvdf1)
        # plot_freqDomain(pvdf1)
        # save.
        # Writer1.writerows(pvdf1)
        # Writer2.writerows(pvdf2)
        # Writer3.writerows(pvdf3)

    # close file.
    # pvdf1_file.close()
    # pvdf2_file.close()
    # pvdf3_file.close()
