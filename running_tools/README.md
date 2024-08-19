
# Running Tools

這是一組用於處理 Stellarator 的腳本，包含以下幾個主要腳本：

1. `generate_input.py`
2. `boost_search_walk.py`
3. `search.py`
4. `check_state.py`
5. `make_output_csv.py`
6. `sort_files.py`

## Installation

- Python 3.x
- 必要套件（例如：`subprocess`, `os`, `re`, `csv`, `shutil`, `glob`, `argparse`）

## 使用說明

### 1. generate_input.py

這個腳本根據模板生成輸入文件。

**運行方式：**

```bash
python generate_input.py --output_directory="./input_files_0716" --curtor_range_start=800000 --curtor_range_end=800001 --curtor_step=1000 --pres_scale_range_start=80000 --pres_scale_range_end=90001 --pres_scale_step=200
```

你可以使用命令行參數來指定輸出目錄以及參數範圍。

### 2. boost_search_walk.py

這個腳本執行多個步驟來處理輸入文件，包括運行和更新配置文件，並生成新的輸入檔案。

**運行方式：**

```bash
python boost_search_walk.py --input_folder="./input_files_0716" --output_folder="./new_input_0716"
```

你可以使用命令行參數來指定輸入文件和輸出文件的資料夾。

### 3. search.py

這個腳本運行特定命令並移動文件。

**運行方式：**

```bash
python search.py --input_directory="./new_input_0716" --dcon_directory="./dcon_files" --output_directory="./output_files"
```

你可以使用命令行參數來指定輸入文件、DCON文件和輸出文件的資料夾。


### 4. sort_files.py

這個腳本移動特定模式匹配的文件到指定資料夾。

**運行方式：**

```bash
python sort_files.py --input_directory="./input_files" --dcon_directory="./dcon_files" --output_directory="./output_files"
```

你可以使用命令行參數來指定輸入、DCON文件和輸出文件的資料夾。

### 5. check_state.py

這個腳本處理輸出文件，並將穩定和不穩定的結果分類到不同的資料夾中。

**運行方式：**

```bash
python check_state.py --input_directory="./output_files" --stable_directory="./processed_outputs_0716/stable" --unstable_directory="./processed_outputs_0716/unstable"
```

你可以使用命令行參數來指定輸入文件及穩定和不穩定結果的輸出資料夾。


### 6. make_output_csv.py

這個腳本從輸出文件中提取資料並生成CSV文件。

**運行方式：**

```bash
python make_output_csv.py --input_directory="/path/to/input_directory" --output_directory="/path/to/output_directory"
```

你可以使用命令行參數來指定輸入和輸出的資料夾路徑。
