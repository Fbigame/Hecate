# 炉石杂项资源提取器

## 简单介绍
提供一个用于解析炉石传说杂项资源的命令行工具，目前支持酒馆战棋表情的提取。

## 如何使用

### 基本用法
如果你已经安装了python，可以直接运行脚本
```bash
python -m src [OPTIONS]
```
如果你使用的release版本，则
```bash
misc-asset [OPTIONS]
```


### 参数说明

#### 输入输出参数
- `--input`：炉石传说资源文件夹路径
  - 默认值：自动检测游戏安装路径
  - 例如：`--input "C:\Program Files (x86)\Hearthstone"`

- `--output`：提取资源的输出文件夹路径
  - 默认值：`./output`
  - 例如：`--output ./extracted_assets`

#### 导出内容参数
- `--export`：要导出的内容类型
  - 可选值：
    - `all`
    - `bg-emote`（酒馆战棋表情）
  - 例如：`--export bg-emote`

#### 语言参数
- `--locale`：要提取的语言版本
  - 可选值：
    - `enus`
    - `zhcn`
    - `zhtw`
    - `jajp`
    - `eses`
    - `kokr`
    - `ptbr`
    - `ruru`
    - `frfr`
    - `esmx`
    - `itit`
    - `dede`
    - `plpl`
    - `thth`
  - 默认值：`zhcn`
  - 例如：`--locale zhcn`

#### 动态图片参数
- `--dynamic-image`：动态图片的输出格式
  - 可选值：`gif`、`apng`、`webp`
  - 默认值：`gif`
  - 例如：`--dynamic-image apng`

#### 其他参数
- `-v`、`--version`：显示工具版本
  - 例如：`--version`

- `--log-level`：设置日志记录等级
  - 默认值：`error`
  - 可选值：`debug`, `info`, `warning`, `error`, `critical`
  - 例如：`--log-level debug` 或 `--log-level error`

- `--fallback-unity-version`：设置 Unity 回退版本号（当资源文件中无法自动检测 Unity 版本时使用）
  - 默认值：`6000.3.11f1`
  - 例如：`--fallback-unity-version "2022.3.11f1"`

### 使用示例

1. 提取酒馆战棋表情（中文）：
```bash
misc-asset --export bg-emote
```

2. 提取酒馆战棋表情（英文），输出为 apng 格式：
```bash
misc-asset --export bg-emote --locale enus --dynamic-image apng
```

3. 自定义输入输出路径：
```bash
misc-asset --input "C:\Hearthstone" --output ./my_assets --export bg-emote
```

## 使用风险
- 本程序需要读取炉石传说游戏文件夹中的资源文件，某些安全软件可能会将其判定为风险程序。
- 请确保您只在自己的计算机上使用本工具，并遵守相关法律法规。

## 如何构建可执行文件

### 安装项目
```bash
uv sync
```

### 执行构建命令
```bash
build
```

### 构建结果
构建完成后，可执行文件将生成在`dist`目录中：
- Windows: `dist/misc-asset.exe`

## 许可证
ISC License

Copyright (c) 2025 Octasin

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
