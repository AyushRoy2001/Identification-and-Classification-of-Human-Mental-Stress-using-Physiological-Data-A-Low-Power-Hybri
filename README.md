# Mental-Stress-Detection

Official implementation of "Identification and Classification of Human Mental Stress using Physiological Data: A Low-Power Hybrid Approach"

### Overall workflow:
![Overall](https://user-images.githubusercontent.com/94052139/201930316-52fe158d-3e57-4eca-b627-480ea1175c4c.png)
### Architecture of CNN:
![Architecture](https://user-images.githubusercontent.com/94052139/201930421-dcb5587f-d92f-454e-82a7-a3a645454c59.png)
### Overall calculation:
![Workflow](https://user-images.githubusercontent.com/94052139/201930600-e6a58246-40bf-4fc8-acdb-8b0abdfd4cd3.png)

## How to use
-Download the models and the main.py
-Install the packages in the requirements.txt
-Connect Arduino UNO with AD8232
-Use Microsoft Data Streamer to collect and store the data of AD8232 in the csv file.
-Run the main.py with the models in appropriate memory locations w.r.t the code.

## Authors :nerd_face:*
Ayush Roy<br/>
Arkaprovo Acharya<br/>
Saborno Biswas<br/>
Susanta Ray<br/>
Biswarup Ganguly<br/>

## Citation :thinking:*
Please do cite our paper in case you find it useful for your research.
@INPROCEEDINGS{10077709,
  author={Roy, Ayush and Acharya, Arkaprovo and Biswas, Sabarno and Ray, Susanta and Ganguly, Biswarup},
  booktitle={2022 IEEE 6th International Conference on Condition Assessment Techniques in Electrical Systems (CATCON)}, 
  title={Identification and Classification of Human Mental Stress using Physiological Data: A Low-Power Hybrid Approach}, 
  year={2022},
  volume={},
  number={},
  pages={136-139},
  doi={10.1109/CATCON56237.2022.10077709}}
