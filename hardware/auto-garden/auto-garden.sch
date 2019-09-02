EESchema Schematic File Version 4
LIBS:auto-garden-cache
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 2
Title "Auto-Garden-Top-Level"
Date "2019-08-27"
Rev "0.1"
Comp "SouderFamily"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Regulator_Linear:LM1085-5.0 U?
U 1 1 5D65C549
P 2550 1200
F 0 "U?" H 2550 1442 50  0000 C CNN
F 1 "LM1085-5.0" H 2550 1351 50  0000 C CNN
F 2 "" H 2550 1450 50  0001 C CIN
F 3 "http://www.ti.com/lit/ds/symlink/lm1085.pdf" H 2550 1200 50  0001 C CNN
	1    2550 1200
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5D663053
P 2550 1600
F 0 "#PWR?" H 2550 1350 50  0001 C CNN
F 1 "GND" H 2555 1427 50  0000 C CNN
F 2 "" H 2550 1600 50  0001 C CNN
F 3 "" H 2550 1600 50  0001 C CNN
	1    2550 1600
	1    0    0    -1  
$EndComp
Wire Wire Line
	2550 1600 2550 1500
$Comp
L power:+5V #PWR?
U 1 1 5D66445F
P 3000 1200
F 0 "#PWR?" H 3000 1050 50  0001 C CNN
F 1 "+5V" H 3015 1373 50  0000 C CNN
F 2 "" H 3000 1200 50  0001 C CNN
F 3 "" H 3000 1200 50  0001 C CNN
	1    3000 1200
	1    0    0    -1  
$EndComp
Wire Wire Line
	3000 1200 2850 1200
$Sheet
S 5200 1250 1050 850 
U 5D6656F0
F0 "CapacitiveMoistureSensor1" 50
F1 "CapacitiveMoistureSensor.sch" 50
$EndSheet
$Comp
L auto-garden:MCP1702-3302E_TO92-3 U?
U 1 1 5D68095A
P 2550 2350
F 0 "U?" H 2550 2592 50  0000 C CNN
F 1 "MCP1702-3302E_TO92-3" H 2550 2501 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-89-3" H 2550 2550 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/20005122B.pdf" H 2550 2300 50  0001 C CNN
	1    2550 2350
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR?
U 1 1 5D68250C
P 3200 2350
F 0 "#PWR?" H 3200 2200 50  0001 C CNN
F 1 "+3.3V" H 3215 2523 50  0000 C CNN
F 2 "" H 3200 2350 50  0001 C CNN
F 3 "" H 3200 2350 50  0001 C CNN
	1    3200 2350
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5D682FCF
P 2550 2850
F 0 "#PWR?" H 2550 2600 50  0001 C CNN
F 1 "GND" H 2555 2677 50  0000 C CNN
F 2 "" H 2550 2850 50  0001 C CNN
F 3 "" H 2550 2850 50  0001 C CNN
	1    2550 2850
	1    0    0    -1  
$EndComp
Wire Wire Line
	2550 2850 2550 2650
Wire Wire Line
	3200 2350 2850 2350
$EndSCHEMATC
