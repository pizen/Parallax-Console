#!/usr/bin/python

import serial
import sys
import curses

scr = curses.initscr()

def main(scr):
	ser = serial.Serial(
		port='/dev/tty.usbserial-AH01N2HV',
		baudrate=57600,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
	)

	ser.isOpen()

	out = ''
	lines = ['']
	line_no = 0

	while 1 :
		try:
			out = ord(ser.read(1))
		except KeyboardInterrupt:
			break
		
		if out == 0x10:
			lines = ['']
			line_no = 0
		elif out >= 0x20 and out <= 0x7f:
			lines[line_no] += chr(out)
		elif out == 0xa or out == 0xd:
			scr.erase()
			i = 0
			for line in lines:
				scr.addstr(i, 0, line)
				i += 1
			scr.refresh()
			lines.append('')
			line_no += 1
		elif out == 0x2:
			n1 = ord(ser.read(1))
			if n1 == 0x12:
				line_no = ord(ser.read(1))

curses.wrapper(main)
