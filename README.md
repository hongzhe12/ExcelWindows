
# Excel数据处理与数据库写入工具
![QQ_1748862620942](https://github.com/user-attachments/assets/4965cd24-25e0-4e28-96d6-72ad9a48c506)

## 一、项目概述
本工具基于Python和PySide6开发，实现Excel文件的可视化加载、预览及分批次处理，并支持将数据写入MySQL数据库。具备以下核心功能：
- **Excel文件拖放与读取**：支持.xlsx/.xls格式，自动预览前20行数据
- **分批次加载优化**：大数据量下避免UI卡顿，实时显示加载进度
- **数据库配置管理**：通过YAML文件持久化存储数据库连接信息
- **类型适配与格式化**：自动处理数值、时间等数据类型的显示格式
- **多线程处理**：文件加载和数据库写入均在后台线程执行，保证界面响应

## 二、项目结构
```
ExcelWindows/
├─ app.py              # 主程序逻辑，包含界面交互和业务逻辑
├─ config_set.py       # YAML配置管理器，处理配置文件读写
├─ general_excel.ui    # Qt Designer界面文件（通过pyside6-uic编译为ui_general_excel.py）
├─ input_form_dialog.py# 数据库配置对话框，支持动态表单生成
└─ ui_general_excel.py # 编译后的界面类，由Qt Designer生成
```

## 三、功能特性

### 1. Excel文件操作
- **拖放支持**：直接将Excel文件拖入窗口即可触发加载
- **分阶段加载**：
  - 先快速读取前20行数据用于预览
  - 后台异步加载完整数据，分批次（默认500行/批）渲染到表格
  - 加载过程中实时显示总行数和当前进度
- **数据格式化**：
  - 数值型右对齐显示
  - 时间戳自动格式化为`YYYY-MM-DD HH:MM:SS`
  - 空值显示为空白字符串

### 2. 数据库写入
- **配置管理**：
  - 通过`config.yaml`存储数据库连接信息（用户名、密码、主机、数据库名、表名）
  - 首次使用时弹出表单窗口引导配置，支持记住上次配置
- **写入逻辑**：
  - 使用SQLAlchemy连接MySQL数据库
  - 支持数据追加模式（`if_exists='append'`），避免重复写入
  - 写入过程在后台线程执行，不阻塞界面

### 3. 界面与交互
- **状态栏设计**：
  - 红色加粗字体显示状态信息
  - 实时反馈操作进度（如"正在加载文件..."、"数据加载完成（共1000行）"）
- **错误处理**：
  - 文件读取或数据库写入失败时弹出错误提示
  - 自动清理异常情况下的线程资源
- **快捷键支持**：
  - 回车键可触发输入框内容提交（通过事件过滤器实现）

## 四、依赖环境
### 1. 软件依赖
- Python 3.8+
- PySide6 >= 6.6.0
- pandas >= 2.0.0
- SQLAlchemy >= 2.0.0
- PyMySQL >= 1.0.2
- pyyaml >= 6.0.0

### 2. 安装命令
```bash
pip install pyside6 pandas sqlalchemy pymysql pyyaml
```

## 五、使用说明

### 1. 启动程序
```bash
python app.py
```

### 2. 加载Excel文件
- **方式1**：点击菜单栏"文件-打开"选择文件
- **方式2**：直接将Excel文件拖入程序窗口
- 加载完成后表格显示前20行预览数据，状态栏提示"数据预览中..."，完整数据加载完成后自动显示全部内容

### 3. 配置数据库
- 首次点击"写入数据库"按钮时，会弹出配置表单：
  - 填写用户名、密码、主机地址（如`localhost`）、数据库名、表名
  - 勾选"记住配置"可保存到`config.yaml`
- 后续使用时会自动加载上次配置，如需修改可点击按钮重新配置

### 4. 写入数据到MySQL
- 确保表格数据已完整加载（状态栏显示"数据加载完成"）
- 点击"写入数据库"按钮，等待后台线程完成写入
- 成功后状态栏提示"数据写入完成"，失败时显示具体错误信息

## 六、配置文件说明
### 1. 配置文件路径
`config.yaml`位于程序根目录，首次运行时自动生成，内容示例：
```yaml
last_opened_file: ""  # 上次打开的Excel文件路径
user: ""             # 数据库用户名
password: ""         # 数据库密码
db_name: ""          # 数据库名称
table_name: ""       # 表名称
host: "localhost"    # 数据库主机地址
```

### 2. 配置修改方式
- 通过界面表单修改（推荐）
- 直接编辑`config.yaml`文件（需注意格式正确性）

## 七、开发与调试
### 1. UI界面修改
1. 使用Qt Designer打开`general_excel.ui`进行界面调整
2. 编译UI文件为Python代码：
```bash
pyside6-uic general_excel.ui -o ui_general_excel.py
```

### 2. 线程调试技巧
- 工作线程类`Worker`支持进度回调和错误捕获，可通过信号槽机制添加调试日志
- 数据加载线程`ExcelLoaderThread`使用独立线程避免阻塞UI，可通过`preview_ready`和`full_data_ready`信号跟踪加载状态

### 3. 常见问题
- **文件读取失败**：检查文件路径是否正确，确保Excel文件未被其他程序占用
- **数据库连接失败**：确认配置信息正确，检查MySQL服务是否运行，防火墙是否允许连接
- **界面卡顿**：若数据量极大，可调整`MyMainWindow`中的`batch_size`参数（默认500），减小批次大小以提升响应速度

## 八、版权与许可
本项目采用MIT开源许可协议，允许商业使用和修改，但需保留原作者声明。

## 九、联系方式
如有问题或建议，可通过以下方式联系：
- 邮箱：hongzhe2022@163.com
- GitHub：https://github.com/hongzhe12/ExcelWindows
