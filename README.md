# layer_inpainting 

#### layer_inpainting/inpaint.py
```
Usage: python inpaint.py

Example:
    data/
        - Pha1_00020_value/
            - interval_1/
                - 000.png
                - 001.png
                ...
            - interval_2/
            - interval_3/
    result/
        - NS/
            - Pha1_00020_value/
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

#### utils/phase_txt2mat.py
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
