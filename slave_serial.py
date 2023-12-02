import serial_asyncio
import asyncio
import time
import threading

from PySide6.QtWidgets import QApplication, QWidget
from slave_ui import Ui_Form

register = [0]


class modbus(QWidget):
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # 提取要操作的控件
        self.run_sign = self.ui.label_3  # 运行提示
        self.stop_sign = self.ui.label_2  # 停止提示
        self.run_total = self.ui.lcdNumber  # 启动按钮
        self.rlight=self.ui.label_4
        self.glight=self.ui.label_5

        self.stop()
        self.rlight.show()

    def running(self):
        self.run_sign.show()
        self.stop_sign.hide()
        self.glight.show()
        self.rlight.hide()

    def stop(self):
        self.run_sign.hide()
        self.stop_sign.show()
        self.glight.hide()
        self.rlight.show()

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
        raw_data=data[:-2]
        raw_crc=int(data[-2:].hex(),base=16)
        crc = self.crc16(raw_data)
        if crc == raw_crc:
            return raw_data
        else:
            return False

    # 异步读取串口数据
    async def read_from_serial(self, reader):
        data = await reader.read(1000)
        p = time.strftime("%X", time.localtime())
        print(f"received at {p}, {data}")
        crc16_verify=self.crc16_verify(data)
        if crc16_verify:
            return crc16_verify
        else:
            return False

    # 异步写入串口数据
    async def write_to_serial(self, writer, data):
        crc16=self.crc16(data)
        message = bytes.fromhex(f"{data.hex()}{crc16:04X}")
        writer.write(message)
        await writer.drain()

    async def _run(self):
        self.reader, self.writer = await serial_asyncio.open_serial_connection(
            url=self.port, baudrate=self.baudrate
        )

        task = asyncio.create_task(self.autosend())

        await task

    def run(self):
        asyncio.run(self._run())

    async def autosend(self):
        # 当前运行状态
        status = False
        while True:
            # 等待主站发送数据
            read = asyncio.create_task(self.read_from_serial(self.reader))
            await read
            data = read.result()
            # 05 运行
            if data == bytes.fromhex(f"010500000001"):
                write = asyncio.create_task(
                    self.write_to_serial(
                        self.writer, bytes.fromhex(f"010500000001")
                    )
                )
                await write
                self.running()
                # 根据当前状态将运行次数写入寄存器
                if not status:
                    register[0] = register[0] + 1
                    status = True
            # 05 停止
            elif data == bytes.fromhex(f"010500000002"):
                self.stop()
                write = asyncio.create_task(
                    self.write_to_serial(
                        self.writer, bytes.fromhex(f"010500000002")
                    )
                )
                await write
                status = False
            # 根据寄存器中数据显示当前运行次数
            self.run_total.display(register[0])

            # 01 主站读取运行状态
            if data == bytes.fromhex(f"010100000001"):
                if status:
                    write = asyncio.create_task(
                        self.write_to_serial(
                            self.writer, bytes.fromhex(f"010100000001")
                        )
                    )
                    await write
                    print("running")
                else:
                    write = asyncio.create_task(
                        self.write_to_serial(
                            self.writer, bytes.fromhex(f"010100000002")
                        )
                    )
                    await write
                    print("stop\n")

            # 03 主站读取寄存器中运行次数信息
            elif data == bytes.fromhex(f"010300010001"):
                send_data = bytes.fromhex(f"01030001{register[0]:04X}")
                write = asyncio.create_task(self.write_to_serial(self.writer, send_data))
                await write
                print(f"number of runs: {register[0]} \n")



if __name__ == "__main__":
    app = QApplication([])
    m = modbus(port="com2", baudrate=9600)

    threading.Thread(target=m.run, daemon=True).start()
    # 展示窗口
    m.show()
    app.exec()
