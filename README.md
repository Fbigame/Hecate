# hearthstone-misc-asset-extractor

炉石传说杂项资源提取工具，用于从炉石传说游戏文件中提取各种杂项资源。

## 功能特性

- 提取多种炉石传说杂项资源：
  - 酒馆战棋表情 (`bg-emote`)
  - 酒馆战棋棋盘 (`bg-board`)
  - 酒馆战棋终结技 (`bg-finisher`)
  - 卡牌背面 (`card-back`)
  - 卡牌扩展包水印 (`set-watermark`)
  - 卡牌扩展包筛选图标 (`set-filter-icon`)
  - 天梯排名图标 (`league-rank`)

- 支持多语言：
  - 简体中文 (`zhcn`)
  - 繁体中文 (`zhtw`)
  - 英语 (`enus`)
  - 日语 (`jajp`)
  - 西班牙语 (`eses`)
  - 韩语 (`kokr`)
  - 葡萄牙语 (`ptbr`)
  - 俄语 (`ruru`)
  - 法语 (`frfr`)
  - 墨西哥西班牙语 (`esmx`)
  - 意大利语 (`itit`)
  - 德语 (`dede`)
  - 波兰语 (`plpl`)
  - 泰语 (`thth`)

- 支持多种动态图片格式：
  - GIF
  - APNG
  - WebP

## 安装

1. 确保安装了 Python 3.12 或更高版本
2. 克隆本仓库：
   ```bash
   git clone https://github.com/Fbigame/Hecate.git
   cd hearthstone-misc-asset-extractor
   ```
3. 安装依赖：
   ```bash
   pip install -e .
   ```

## 使用方法

### 基本用法

```bash
misc-asset --input "C:\Program Files (x86)\Hearthstone" --export all
```

### 参数说明

#### 必要参数

- `--export`: 指定要导出的内容
  - 可选值：`all`, `bg-emote`, `bg-board`, `bg-finisher`, `card-back`, `set-watermark`, `set-filter-icon`, `league-rank`
  - 可以指定多个值，用逗号分隔，例如：`--export bg-emote,card-back`

#### 输入输出参数

- `--input`: 炉石传说安装目录
  - 示例：`--input "C:\Program Files (x86)\Hearthstone"`

- `--output`: 输出目录（默认为 `./output`）
  - 示例：`--output "D:\Hearthstone Assets"`

#### 其他参数

- `--locale`: 语言设置，决定部分导出文件的名字（默认：`zhcn`）
  - 示例：`--locale enus`

- `--dynamic-image`: 动态图片的输出格式（默认：`gif`）
  - 可选值：`gif`, `apng`, `webp`
  - 示例：`--dynamic-image webp`

- `--log-level`: 日志级别（默认：`error`）
  - 可选值：`debug`, `info`, `warning`, `error`, `critical`
  - 示例：`--log-level info`

- `-v, --version`: 显示版本信息

### 示例

1. 导出所有资源到默认目录：
   ```bash
   misc-asset --input "C:\Program Files (x86)\Hearthstone" --export all
   ```

2. 仅导出卡牌背面和天梯排名图标到指定目录：
   ```bash
   misc-asset --input "C:\Program Files (x86)\Hearthstone" --output "D:\HS Assets" --export card-back,league-rank
   ```

3. 导出酒馆战棋表情，使用英语语言和 WebP 格式：
   ```bash
   misc-asset --input "C:\Program Files (x86)\Hearthstone" --export bg-emote --locale enus --dynamic-image webp
   ```


## 常见问题


### Q: 动态图片导出格式怎么选择？
A: 
- GIF：兼容性最好，但文件较大，不支持透明度
- APNG：支持透明度，文件大小适中
- WebP：支持透明度，文件最小，但兼容性略差

## 许可证

ISC License

## 声明

本工具仅供学习和研究使用，请勿用于商业目的。
所有炉石传说相关资源均归暴雪娱乐所有。
