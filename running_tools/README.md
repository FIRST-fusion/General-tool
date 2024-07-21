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
- Package（Ex：`subprocess`, `os`, `re`, `csv`, `shutil`, `glob`）

## 使用說明

### 1. generate_input.py

這個腳本根據模板生成輸入文件。

**運行方式：**

```bash
python generate_input.py
```

生成的輸入文件將保存在 `./input_files_0716` 目錄中。(可自行修改路徑)

### 2. boost_search_walk.py

這個腳本執行多個步驟來處理輸入文件，包括運行和更新配置文件還有產生新的input檔案。

**運行方式：**

```bash
python boost_search_walk.py
```

輸入文件來自 `./input_files_0716`(可自行修改路徑) 資料夾，更新的輸入文件將保存在 `./new_input_0716` 資料夾中。

### 3. search.py

這個腳本運行特定命令並移動文件。

**運行方式：**

```bash
python search.py
```

輸入文件來自 `./new_input_0716` 目錄，生成的輸出將保存在 `./output_files`(可自行修改路徑) 資料夾中。

### 4. check_state.py

這個腳本處理輸出文件，並將穩定和不穩定的結果分類到不同的資料夾中，並生成 CSV 文件。

**運行方式：**

```bash
python check_state.py
```

輸入文件來自 `./output_files` 目錄，分類後的文件將保存在 `./processed_outputs_0716` 目錄中，穩定結果的 CSV 文件保存在 `stable_results.csv`。

### 5. make_output_csv.py

這個腳本從輸出文件中提取資料並生成 CSV 文件。

**運行方式：**

```bash
python make_output_csv.py
```

輸入文件來自 `/home/f74091247/Stellarator-Tools/build/_deps/parvmec-build/output_files` (可自行修改路徑)，生成的 CSV 將保存在 `/home/f74091247/Stellarator-Tools/build/_deps/parvmec-build/csv_files_0716` (可自行修改路徑)。

### 6. sort_files.py

這個腳本移動特定模式匹配的文件到指定資料夾。

**運行方式：**

```bash
python sort_files.py
```

文件將從當前資料夾移動到 `./output_files` 資料夾中。