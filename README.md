# AIRA

## 爬虫使用方法

在`AIRA/flight`下输入如下命令：

```bash
scrapy run -d [出发日期] -c [出发城市]
```

**Options**

| 选项                    | 参数解释                        |
| ----------------------- | ------------------------------- |
| --help, -h              | show this help message and exit |
| --date=DATE, -d DATE    | departure date, like 2020-12-01 |
| --dcity=DCITY, -c DCITY | departure city, like 福州       |

- 当添加`出发日期`和`出发城市`参数时，爬虫启动查询模式；
- 当缺少参数，即直接输入`scrapy run`时，爬虫启动日常模式（爬取从今天开始一星期的数据）。