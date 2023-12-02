import serial_asyncio
import asyncio, nest_asyncio
import threading
import time
from PySide6.QtWidgets import QApplication, QWidget
from master_ui import Ui_Form

nest_asyncio.apply()


class modbus(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    # CRC16_MODBUS
    def crc16(self, data: bytes) -> int:
        crc = 0xFFFF
        for byte in data:
            # 将每个数据字节与crc进行异或操作
            crc ^= byte
            # 对crc的每一位进行处理
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc = crc >> 1
        # 高低位转换
        crc = int(f"{crc:04X}"[2:] + f"{crc:04X}"[:2], base=16)
        return crc

    def crc16_verify(self, data):
        raw_data = data[:-2]
        raw_crc = int(data[-2:].hex(), base=16)
        crc = self.crc16(raw_data)
        if crc == raw_crc:
            return raw_data
        else:
            return False

    # 异步读取串口数据
    async def read_from_serial(self, reader):
        data = await reader.read(1000)
        return data

    # 异步写入串口数据
    async def write_to_serial(self, writer, data):
        writer.write(data)
        await writer.drain()

    # 主站先发送请求，再读取从站数据
    async def post_data(self, data):
        # 为data添加crc
        crc16 = self.crc16(data)
        message = bytes.fromhex(f"{data.hex()}{crc16:04X}")
        all_task = asyncio.all_tasks(loop=self.loop)
        while True:
            if len(all_task) > 2:
                await asyncio.sleep(0.2)
            else:
                break
        try:
            await asyncio.wait_for(
                self.write_to_serial(self.writer, message), timeout=0.1
            )
            read = await asyncio.wait_for(
                self.read_from_serial(self.reader), timeout=0.1
            )
            raw = self.crc16_verify(read)
            if raw:
                return raw
            else:
                return None
        except TimeoutError:
            raise TimeoutError
        except:
            pass

    async def _run_serial(self):
        # 连接串口
        reader, writer = await serial_asyncio.open_serial_connection(
            url=self.port, baudrate=self.baudrate
        )
        return reader, writer

    async def read_status(self):
        _i = 0
        while True:
            if _i != 0:
                await asyncio.sleep(2)
            elif _i != 1:
                print("Getting Status...")

            try:
                # 01 读线圈，读取当前从站状态
                all_task = asyncio.all_tasks(loop=self.loop)
                if len(all_task) > 1:
                    await asyncio.sleep(0.5)
                    continue

                data = await self.post_data(bytes.fromhex(f"010100000001"))

                if data == bytes.fromhex(f"010100000001"):
                    self.running()
                elif data == bytes.fromhex(f"010100000002"):
                    self.stop()
                elif not data:
                    raise TimeoutError

                #  03 读寄存器，读取运行次数
                all_task = asyncio.all_tasks(loop=self.loop)
                if len(all_task) > 1:
                    await asyncio.sleep(0.5)
                    continue

                data = await self.post_data(bytes.fromhex(f"010300010001"))
                if data:
                    returns = data.hex()

                    if returns[:4] == "0103":
                        register = int(returns[8:], 16)
                        # 显示运行次数
                        self.run_total.display(register)
                        if _i != 1:
                            print("通讯成功")
                else:
                    raise TimeoutError
                _i = 1
            except TimeoutError:
                print("通讯失败")
                _i = 2
            except:
                pass

    async def read_status_TCP(self):
        _i = 0
        while True:
            if _i != 0:
                await asyncio.sleep(2)
            elif _i != 1:
                print("Getting Status...")

            try:
                # 01 读线圈，读取当前从站状态

                data = await self.tcp_post(bytes.fromhex(f"010100000001"))

                if data == bytes.fromhex(f"010100000001"):
                    self.running()
                elif data == bytes.fromhex(f"010100000002"):
                    self.stop()
                elif not data:
                    raise TimeoutError

                #  03 读寄存器，读取运行次数

                data = await self.tcp_post(bytes.fromhex(f"010300010001"))
                if data:
                    returns = data.hex()

                    if returns[:4] == "0103":
                        register = int(returns[8:], 16)
                        # 显示运行次数
                        self.run_total.display(register)
                        if _i != 1:
                            print("通讯成功")
                else:
                    raise TimeoutError
                _i = 1
            except TimeoutError:
                print("通讯失败")
                _i = 2
            except:
                pass

    async def _run_TCP(self):
        try:
            reader, writer = await asyncio.open_connection(
                self.TCP_host.text(), self.TCP_port.text()
            )
            return reader, writer
        except:
            print("连接失败")

    async def tcp_post(self, data):
        crc16 = self.crc16(data)
        message = bytes.fromhex(f"{data.hex()}{crc16:04X}")
        try:
            self.TCP_writer.write(message)
            await self.TCP_writer.drain()
            data = await self.TCP_reader.read(100)
            # print(f'Received: {data.decode()!r}')
            raw = self.crc16_verify(data)
            if raw:
                return raw
            else:
                return None
        except TimeoutError:
            raise TimeoutError
        except:
            pass

    def tcp_send(self, data):
        coro = self.tcp_post(data)
        try:
            future = asyncio.run_coroutine_threadsafe(coro, self.loop2)
            assert future.result(timeout=0.1)
        except:
            future.cancel()
            raise TimeoutError
        if future.result():
            return future.result()
        else:
            raise RuntimeError

    def run_serial(self):
        # 在新线程中启动事件循环
        new_loop = asyncio.new_event_loop()
        self.loop = new_loop
        t = threading.Thread(target=self.start_loop, args=(new_loop,), daemon=True)
        t.start()
        # 将coroutine添加到新线程的事件循环中
        coro1 = self._run_serial()
        coro2 = self.read_status()
        future = asyncio.run_coroutine_threadsafe(coro1, new_loop)
        self.reader, self.writer = future.result()
        asyncio.run_coroutine_threadsafe(coro2, new_loop)

    def run_TCP(self):
        new_loop = asyncio.new_event_loop()
        self.loop2 = new_loop
        t = threading.Thread(target=self.start_loop, args=(new_loop,), daemon=True)
        t.start()
        # 将coroutine添加到新线程的事件循环中
        coro1 = self._run_TCP()
        coro2 = self.read_status_TCP()
        future = asyncio.run_coroutine_threadsafe(coro1, new_loop)
        self.TCP_reader, self.TCP_writer = future.result()
        asyncio.run_coroutine_threadsafe(coro2, new_loop)

    def start_loop(self, loop):
        # 启动事件循环
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def send(self, data):
        # 发送和接收数据
        coro = self.post_data(data)
        try:
            future = asyncio.run_coroutine_threadsafe(coro, self.loop)
            assert future.result(timeout=0.1)
        except:
            future.cancel()
            raise TimeoutError
        if future.result():
            return future.result()
        else:
            raise RuntimeError

    def init_ui(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # 提取要操作的控件
        self.run_sign = self.ui.label  # 运行提示
        self.stop_sign = self.ui.label_2  # 停止提示
        self.run_btn = self.ui.btn1  # 启动按钮
        self.stop_btn = self.ui.btn2  # 停止按钮
        self.run_total = self.ui.lcdNumber  # 计数
        self.rlight = self.ui.label_4
        self.glight = self.ui.label_5
        self.serial_enable = self.ui.radioButton
        self.TCP_enable = self.ui.radioButton_2
        self.serial_port = self.ui.comboBox
        self.TCP_host = self.ui.lineEdit
        self.TCP_port = self.ui.lineEdit_2
        self.flash_btn = self.ui.pushButton
        self.run_btn.clicked.connect(self.click_run_btn)
        self.stop_btn.clicked.connect(self.click_stop_btn)
        self.flash_btn.clicked.connect(self.click_flash_btn)

        self.serial_enable.setChecked(True)
        self.mode = [1, 0]
        self.TCP_enable.setChecked(False)
        self.serial_enable.toggled.connect(lambda: self.btnstate(self.serial_enable))
        self.TCP_enable.toggled.connect(lambda: self.btnstate(self.TCP_enable))

        self.run_sign.hide()
        self.stop_sign.hide()
        self.rlight.hide()
        self.glight.hide()
        self.TCP_host.hide()
        self.TCP_port.hide()
        self.ui.label_6.hide()

    # 运行指示
    def running(self):
        self.run_sign.show()
        self.glight.show()
        self.stop_sign.hide()
        self.rlight.hide()

    # 停止指示
    def stop(self):
        self.run_sign.hide()
        self.glight.hide()
        self.stop_sign.show()
        self.rlight.show()

    def btnstate(self, btn):
        if btn.text() == "serial":
            if btn.isChecked() == True:
                self.mode[0] = 1
            else:
                self.mode[0] = 2
        if btn.text() == "TCP":
            if btn.isChecked() == True:
                self.mode[0] = 2
            else:
                self.mode[0] = 1
        print(self.mode)
        if self.mode[0] != self.mode[1]:
            self.flash_btn.setEnabled(True)
        else:
            self.flash_btn.setEnabled(False)

    def click_flash_btn(self):
        if self.mode[0] == 1:
            if not self.mode[1]:
                # try:
                self.port = self.serial_port.currentText()
                self.baudrate = 9600
                self.run_serial()
                self.flash_btn.setEnabled(False)
                self.mode[1] = 1
            # except:
            #     pass
            elif self.mode[1] == 2:
                try:
                    self.loop2.stop()
                    # self.loop.run_forever()
                    threading.Thread(target=self.loop.run_forever, daemon=True).start()
                    self.flash_btn.setEnabled(False)
                    self.mode[1] = 1
                except:
                    self.port = self.serial_port.currentText()
                    self.baudrate = 9600
                    self.run_serial()
                    self.flash_btn.setEnabled(False)
                    self.mode[1] = 1

        elif self.mode[0] == 2:
            if not self.mode[1]:
                self.run_TCP()
                self.flash_btn.setEnabled(False)
                self.mode[1] = 2
            elif self.mode[1] == 1:
                try:
                    self.loop.stop()
                    # self.loop2.run_forever()
                    threading.Thread(target=self.loop2.run_forever, daemon=True).start()
                    self.flash_btn.setEnabled(False)
                    self.mode[1] = 2
                except:
                    self.run_TCP()
                    self.flash_btn.setEnabled(False)
                    self.mode[1] = 2

    def click_run_btn(self):
        if self.mode[1] == 1:
            for i in range(3):
                try:
                    # 05 写线圈，将从站置为运行状态
                    self.send(bytes.fromhex(f"010500000001"))

                    # 01 读线圈，读取当前从站状态
                    data = self.send(bytes.fromhex(f"010100000001"))

                    if data == bytes.fromhex(f"010100000001"):
                        self.running()
                    elif data == bytes.fromhex(f"010100000002"):
                        self.stop()

                    #  03 读寄存器，读取运行次数
                    data = self.send(bytes.fromhex(f"010300010001"))
                    if data:
                        returns = data.hex()

                        if returns[:4] == "0103":
                            register = int(returns[8:], 16)
                            # 显示运行次数
                            self.run_total.display(register)
                    break

                except TimeoutError:
                    if i == 2:
                        print("Timeout Error")
                    time.sleep(0.1)
                except RuntimeError:
                    print("Data Error")
                except:
                    print("Unknown Error")
        elif self.mode[1] == 2:
            for i in range(3):
                try:
                    # 05 写线圈，将从站置为运行状态
                    self.tcp_send(bytes.fromhex(f"010500000001"))

                    # 01 读线圈，读取当前从站状态
                    data = self.tcp_send(bytes.fromhex(f"010100000001"))

                    if data == bytes.fromhex(f"010100000001"):
                        self.running()
                    elif data == bytes.fromhex(f"010100000002"):
                        self.stop()

                    #  03 读寄存器，读取运行次数
                    data = self.tcp_send(bytes.fromhex(f"010300010001"))
                    if data:
                        returns = data.hex()

                        if returns[:4] == "0103":
                            register = int(returns[8:], 16)
                            # 显示运行次数
                            self.run_total.display(register)
                    break

                except TimeoutError:
                    if i == 2:
                        print("Timeout Error")
                    time.sleep(0.1)
                except RuntimeError:
                    print("Data Error")
                except:
                    print("Unknown Error")

    def click_stop_btn(self):
        if self.mode[1] == 1:
            for i in range(3):
                try:
                    # 05 写线圈，将从站置为停止状态
                    self.send(bytes.fromhex(f"010500000002"))

                    # 01 读线圈，读取当前从站状态
                    data = self.send(bytes.fromhex(f"010100000001"))

                    if data == bytes.fromhex(f"010100000001"):
                        self.running()
                    elif data == bytes.fromhex(f"010100000002"):
                        self.stop()

                except TimeoutError:
                    if i == 2:
                        print("Timeout Error")
                    time.sleep(0.1)
                except RuntimeError:
                    print("Data Error")
                except:
                    print("Unknown Error")
        elif self.mode[1] == 2:
            for i in range(3):
                try:
                    # 05 写线圈，将从站置为停止状态
                    self.tcp_send(bytes.fromhex(f"010500000002"))

                    # 01 读线圈，读取当前从站状态
                    data = self.tcp_send(bytes.fromhex(f"010100000001"))

                    if data == bytes.fromhex(f"010100000001"):
                        self.running()
                    elif data == bytes.fromhex(f"010100000002"):
                        self.stop()

                except TimeoutError:
                    if i == 2:
                        print("Timeout Error")
                    time.sleep(0.1)
                except RuntimeError:
                    print("Data Error")
                except:
                    print("Unknown Error")


if __name__ == "__main__":
    app = QApplication([])
    m = modbus()
    # 展示窗口
    m.show()

    app.exec()
