### Some Questions

- What factors are the **strongest predictors** of hospital readmission in diabetic patients?

- **How well** can we predict hospital readmission in this dataset with **limited features**?

### Steps

1. **Cleaning tasks:** dropping bad data, dealing with missiung values

   - bad data /  missing values

   > --Missing Values Set--
   > 
   > race 2273 2.23
   > 
   > weight 98569 96.86
   > 
   > payer_code 40256 39.56
   > 
   > medical_specialty 49949 49.08
   > 
   > diag_1 21 0.02
   > 
   > diag_2 358 0.35
   > 
   > diag_3 1423 1.40
   > 
   > gender 3

   Just drop weight, payer-code, medical-specialty

   Drop bad data with 3 '?' in diag

   Drop died patient data which 'discharge\_disposition\_id' == 11 | 19 | 20 | 21 indicates 'Expired'

   Drop 3 data with 'Unknown/Invalid' gender

   - merging

2. **Modification of features:** standardization, log transfonms

3. **Creation or derivation of new features from exsiting ones**
