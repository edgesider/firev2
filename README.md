# Firev2

管理v2ray节点的命令行工具。

# 功能

- 订阅与订阅更新
- 节点管理

# 用法

1. 克隆项目

```bash
git clone https://github.com/edgesider/firev2.git
cd firev2
```

2. 创建配置文件

```bash
mkdir -p ~/.config/firev2
cp firev2.example.conf ~/.config/firev2/firev2.conf
```

这个文件中指定了模板、节点等文件的存储位置，你可以编辑这个文件。支持相对路径，相对于配置文件所在的目录。

3. 创建模板文件

```bash
cp -r templates ~/.config/firev2/
```

4. 创建systemd文件

```bash
./gen_systemd.py
```

5. 订阅节点

```bash
./firev2.py subscript vmess_url URL
```

6. 启动节点

```bash
./firev2.py list
./firev2.py start NODE_NAME
```

# 自动补全

项目的`completions`目录下有`bash`和`fish shell`的自动补全脚本，可以用以下命令添加补全：

- bash

```bash
touch ~/.bashrc
cat completions/firev2_completion.bash >> ~/.bashrc
```

- fish shell

```bash
touch ~/.config/fish/fish.config
cat completions/firev2_completion.fish >> ~/.config/fish/config.fish
```

# TODO

- 订阅管理、更新
- 模板操作
- 交互式选择
