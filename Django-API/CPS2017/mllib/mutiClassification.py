# Model and Data Dir
firstLayerModel = "hdfs:///spark/Model/FNAL_1SecModel"
secondLayerModel = "hdfs:///spark/Model/FOAL_1SecModel"
thridLayerModel = "hdfs:///spark/Model/FTRL_1SecModel"

def FrequencyDomain(line):
    import numpy as np
    # change data used fft and calculate distance ----- root(a**2+b**2)
    newValue = []
    temp = line.collect()
    complex = np.fft.fft(temp[0:825])
    for i in range(0, len(complex)):
        distanceOfComplex = (complex[i].real ** 2 + complex[i].imag ** 2) ** 0.5
        newValue.append(distanceOfComplex)
    newValue.append(temp[826])
    newValue.append(temp[827])
    return newValue

def InputLayer(sc,originRDD,Model):
    Model1 = Model.load(sc,firstLayerModel)
    outputRDD = originRDD.map(lambda p: (Model1.predict(p),p))
    Normal = outputRDD.filter(lambda p: p[0] == 1).count()
    if Normal != 0:
        return 'Normal'
    else:
        return outputRDD

def HiddenLayer(sc,InputRDD,Model):
    Model2 = Model.load(sc,secondLayerModel)
    outputRDD = InputRDD.filter(lambda p: p[0]==0).map(lambda p: (Model2.predict(p[1]),p[1]))
    OneBolt = outputRDD.filter(lambda p: p[0] == 1).count()
    if OneBolt != 0:
        return 'OneBolt'
    else:
        return outputRDD

def OutputLayer(sc,InputRDD,Model):
    Model3 = Model.load(sc,thridLayerModel)
    outputRDD = InputRDD.filter(lambda p: p[0]==0).map(lambda p: Model3.predict(p[1]))
    TwoBolt = outputRDD.filter(lambda p: p == 1).count()
    if TwoBolt != 0:
       return 'TwoBolt'
    else:
       return 'Rag'

def mutiClassification_function(rdd, sc, method):
    import time
    from pyspark.mllib.classification import LogisticRegressionModel
    from pyspark.mllib.classification import SVMModel

    print("Start do fft parser ...")
    Start_time = time.time()
    output = FrequencyDomain(rdd)
    testData = sc.parallelize([output])
    print('fft_parser_time:',time.time() - Start_time)

    # -----------------------Start predict.-------------------------------------#
    print("Start predict ...")
    start_time = time.time()
    if method == 'LogisticRegression':
        print("First Predict ... (Normal or unNormal)")
        first_output = InputLayer(sc,testData, LogisticRegressionModel)
        if first_output =='Normal':
            print('Predict time:', time.time() - start_time)
            return 'Normal'
        else:
            print("Second Predict ... (oneBolt or other)")
            second_output = HiddenLayer(sc,first_output, LogisticRegressionModel)
            if second_output == 'OneBolt':
                print('Predict time:', time.time() - start_time)
                return 'OneBolt'
            else:
                print("third Predict ... (twoBolt or rag)")
                final_output = OutputLayer(sc,second_output, LogisticRegressionModel)
                if final_output == 'TwoBolt':
                    print('Predict time:', time.time() - start_time)
                    return 'TwoBolt'
                else:
                    print('Predict time:', time.time() - start_time)
                    return 'Rag'

    elif method == 'SVM':
        print("First Predict ... (Normal or unNormal)")
        first_output = InputLayer(sc,testData, SVMModel)
        if first_output =='Normal':
            return 'Normal'
        else:
            print("Second Predict ... (oneBolt or other)")
            second_output = HiddenLayer(sc,first_output, SVMModel)
            if second_output == 'OneBolt':
                return 'OneBolt'
            else:
                print("third Predict ... (twoBolt or rag)")
                final_output = OutputLayer(sc,second_output, SVMModel)
                if final_output == 'TwoBolt':
                    return 'TwoBolt'
                else:
                    return 'Rag'
    else:
        return "error"