# 移动端访问

> 注意：
>
> 1. 按这种方式移动端访问，PC 端就不能访问
> 2. 请保证移动端和 PC 端位于同一个 WLAN 下，如果无法访问，可能是你的路由器设置了 AP 保护，需要关闭它

以 Windows 系统为例。

打开 `防火墙-高级设置` ，添加入站规则，端口是 `5000`；

![image-20200526093913960](.\img\image-20200526093913960.png)

运行 `ipconfig` 命令得到 IP 地址，如 `192.168.1.10`；

打开 `server.py` ，将 `app.run()` 部分修改为

```python
if __name__ == "__main__":
    # app.run()
    app.run(host='0.0.0.0',port=5000)
```

并运行。

在移动端访问 `192.168.1.10:5000` 就可以了。

<img src=".\img\743b0009de7318126593ef99e2a871d.jpg" alt="743b0009de7318126593ef99e2a871d" style="zoom:33%;" /><img src=".\img\32077de29e6ae28f8bcc40625d6bcd6.jpg" alt="32077de29e6ae28f8bcc40625d6bcd6" style="zoom:33%;" />