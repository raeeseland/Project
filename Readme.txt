Edit config file to add or delete lockers
Format: locker = 'row-col it is situated, color of locker'
example: "1 = '00,blue'"  situated in row 0 col 0 and color is blue 

set row pins and col pins in the following order:
row = row-0-pin, row-1-pin, row-2-pin ....
col = col-0-pin, col-1-pin, col-2-pin ....

note that row-0-pin and col-0-pin controls locker 1 and
row-0-pin and col-1-pin controls locker 2 and so forth
This configuration fits an nxn grid of lockers

if we have the following
row pins = 2,3,4
col pins = 17,27,22
and a 3x3 grid of lockers then
pins 2,17 controls locker 1
     2,27 controls locker 2
     2,22 controls locker 3
     3,17 controls locker 4
     3,27 controls locker 5 ...

Drive pin for power supply = GPIO pin 10
 
