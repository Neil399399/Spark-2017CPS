import numpy as np
import pandas as pd
from sklearn import cross_validation, svm, preprocessing, metrics


# 載入資料
train_url = "D://CPS/motor_platform/Data/1000RPM/Train-12.txt"
test_url = "D://CPS/motor_platform/Data/1000RPM/Test-12.txt"

titanic_train = pd.read_csv(train_url)
titanic_test = pd.read_csv(test_url)


# 建立訓練與測試資料
train_feature = pd.DataFrame([titanic_train['value1'],
                         titanic_train['value2'],
                         titanic_train['value3']
]).T
train_label = titanic_train['label']

test_feature = pd.DataFrame([titanic_test['value1'],
                         titanic_test['value2'],
                         titanic_test['value3']
]).T
test_label = titanic_test['label']

# 建立 SVC 模型
svc = svm.SVC()
svc_fit = svc.fit(train_feature, train_label)

# 預測
prediction = svc.predict(test_feature)

print(prediction)
# 績效
accuracy = metrics.accuracy_score(test_label, prediction)
print(accuracy)
