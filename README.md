# idiom_from_baidu
爬取百度成语数据

#### 说明
爬取百度成语数据，主要用于成语接龙。
成语接龙自动化测试方案：识别对方成语【尾字】，匹配下一个成语的【首字】，随机给出一个成语。
故爬取成语需要保存数据：成语，首字，尾字

#### 文件说明
- get_idiom_from_baidu.py : 主要代码
- idiom.sqlite3 : 完整数据30875条

#### 数据库字段说明
- ID：自增ID
- NAME: 成语
- PINYIN: 拼音
- NAMEF: 首字
- NAMEL: 尾字
- PINYINF: 首拼
- PINYINL: 尾拼
