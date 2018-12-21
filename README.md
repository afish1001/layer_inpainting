# layer_inpainting 

#### layer_inpainting/inpaint.py
```
Usage: python inpaint.py

Example:
    data/
        - interval
            - Pha1_00020_value/
                -X_Z
                    - interval_1/
                        - 000.png
                        - 001.png
                        ...
                    - interval_2/
                    - interval_3/
        - original
            - mat
                - Pha1_00001_value.mat
                ...
            - Pha1_00001_value.txt
            ...
    result/
        - Pha1_00020_value/
            - NS/
                - images/
                    - interval_1/
                        - 000.png
                        - 001.png
                        ...
                    - interval_2/
                    - interval_3/
                - interval_1.mat
                - interval_2.mat
                - interval_3.mat
                ...
```

#### phase_txt2mat.py
```
Usage: python phase_txt2mat.py --input data --output result --cpus 4

Example:
    data/
        - Pha1_00000_value.txt
        - Pha1_00001_value.txt
        ...
    result/
        - Pha1_00000_value.mat
        - Pha1_00001_value.mat
        ...
```


#### main.py
```
Usage: python main.py --input data --output result --cpus 4

Example:
    mat_folder/
        - Pha1_00000_value.mat
        - Pha1_00001_value.mat
        ...
    result/
        - Pha1_00020_value/
            - Origin/
                - 000.png
                - 001.png
                ...
            - Interval/
                - interval_1/
                    - 000.png
                    - 001.png
                    ...
                - interval_2/
                - interval_3/
            - NS/
                - images/
                    - interval_1/
                        - 000.png
                        - 001.png
                        ...
                    - interval_2/
                    - interval_3/
                - interval_1.mat
                - interval_2.mat
                - interval_3.mat
                ...
```
TODO:
- 添加处理过程信息
- 加快间隔超过4的处理速度
- 对比统计信息（体积、表面积等）
