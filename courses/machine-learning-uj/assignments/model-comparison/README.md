# Models 

## SVM model
### Scaler
#### Goal 
I compared how scaler affects the results.
#### Results
While *linear* kernel is available we do not see any differences. When we get rid off *linear* kernel *cross validation* method returns lesser accuracy with *MixMaxScaler*, while having bigger *C=10* coefficent. While *RobustScaler* have better accuracy (83 vs 84) it also have much lower *C=1* coefficent. It is important information because we can see that with minmax to have similiar results we should decrease *C* value because data are much more packed, results we got can lead to overfitting of model. 

### Best kernel
#### Goal
Finding best kernel for task
#### Results
Best results we get with *linear kernel* in both cases with very high *C* value equal *C=100*. Can lead to overfit
