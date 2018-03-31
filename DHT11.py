#!/usr/bin/python
# -*- coding: UTF-8 -*-

import RPi.GPIO as GPIO
import time
import datetime
import tm1637


class DHT11Reader:
    def __init__(self):
        self.channel = 18  # GPIO24
        self.disp = tm1637.TM1637(5, 3)
        self.disp.stop()

    def read_data_once(self):
        #########################################
        ### 通过单总线访问DTH11的读写协议顺序 ###
        ## 1.主机发开始信号
        ## 2.主机等待接收DHT11响应信号
        ## 3.主机连续接收40 Bit的数据和校验和
        ## 4.数据处理
        #########################################

        data = []                            # DHT11数据包
        j = 0                                # 读取bit计数器

        GPIO.setmode(GPIO.BOARD)
        time.sleep(1) 

        GPIO.setup(self.channel, GPIO.OUT)   # 设置该端口为输出
        GPIO.output(self.channel, GPIO.LOW)  # 用户主机发送一次开始信号（低电平）
        time.sleep(0.02)                     # 总线必须拉低至少18毫秒，保证DTH11能检测到起始信号
        GPIO.output(self.channel, GPIO.HIGH) # 主机开始信号结束（高电平），然后必须延时等待20-40微秒，再
        GPIO.setup(self.channel, GPIO.IN)    # 读取DHT11的回应信号

        while GPIO.input(self.channel) == GPIO.LOW:      # 读取总线为低电平，说明DHT11发送了响应信号  
            continue  
        while GPIO.input(self.channel) == GPIO.HIGH:     # DHT11发送响应信号后会把总线拉高，准备发送数据 
            continue  
        while j < 40:                                    # DHT11的数据包大小为5个bytes(40个bit)，循环读取40个bit   
            k = 0  
            while GPIO.input(self.channel) == GPIO.LOW:  # 接收DHT11数据：首先DHT11先把总线拉低12-14微秒
                 continue  
            while GPIO.input(self.channel) == GPIO.HIGH: # 然后拉高  
                k += 1  
                if k > 100:  
                    break  

            if k < 8:                       # 若拉高电平保持时间在26-28微秒这个范围内
                data.append(0)              # 则此bit为'0'电平
            else:                           # 若拉高电平保持时间在116-118微秒这个范围内
                data.append(1)              # 则此bit为'1'电平
            j += 1  

        humidity_bit = data[0:8]            # 湿度的整数部分（二进制）  
        humidity_point_bit = data[8:16]     # 湿度的小数部分（二进制） 
        temperature_bit = data[16:24]       # 温度的整数部分（二进制）
        temperature_point_bit = data[24:32] # 温度的小数部分（二进制）
        check_bit = data[32:40]             # 校验和（二进制）  

        humidity = 0  
        humidity_point = 0  
        temperature = 0  
        temperature_point = 0  
        check = 0  

        for i in range(8):                  # 二进制转十进制
            humidity += humidity_bit[i] * 2 ** (7-i)  
            humidity_point += humidity_point_bit[i] * 2 ** (7-i)  
            temperature += temperature_bit[i] * 2 ** (7-i)  
            temperature_point += temperature_point_bit[i] * 2 ** (7-i)  
            check += check_bit[i] * 2 ** (7-i)  

        tmp = humidity + humidity_point + temperature + temperature_point  # 加总校验和
         

        if check == tmp:  # 如果与校验和一致，说明是有效数据
            display_map = map(int,str(temperature)) + map(int,str(humidity))
            self.disp.set_values(display_map)
            time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print "["+ __name__ + "] Log >> Time: " + time_string + " Temperature :", temperature, "*C, Humidity :", humidity, "%"  
        else:  
            print "["+ __name__ + "] Log >> " + "Wrong data"  
            print "["+ __name__ + "] Log >> " + "temperature :", temperature, "*C, humidity :", humidity, "% check :", check, ", tmp :", tmp  
  
        #GPIO.cleanup()  

if __name__ == "__main__":
    myDHT11 = DHT11Reader()

    try:  
        while True:  
            myDHT11.read_data_once()
            time.sleep(3)  # 每3秒钟读取一次数据
    except KeyboardInterrupt:  
        myDHT11.disp.clear()
        myDHT11.disp.cleanup()
        GPIO.cleanup()
    