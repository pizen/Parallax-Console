#!/usr/bin/python

import serial
import sys
import curses

usage = "USAGE: console.py <serial device>"

if len(sys.argv) != 2:
	print usage
	exit()

port = sys.argv[1]
	
try:
	ser = serial.Serial(
		port=port,
		baudrate=57600,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
	)
except serial.serialutil.SerialException,reason:
	print "ERROR: %s" % reason
	exit()

ser.isOpen()

scr = curses.initscr()

def main(scr):
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
