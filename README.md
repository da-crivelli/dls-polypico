# dls-polypico

A Python interface to the Polypico Dispenser system.

## Getting started

`pipenv install`

`pipenv run python LinPolyPiCo-V5.py`



## Description

First looks for the platform.
- if Windows: look at COM ports
- if Linux: look at `/dev/ttyUSB`

It then sets the baud rate to `115200`



```mermaid
flowchart LR

A("kontrol.menuk()<br />displays the menu")-->
B("User input")

B--0-->ch_0
B--1-->ch_1
B--2-->ch_2
B--3-->ch_3
B--4-->ch_4
B--5-->ch_5
B--6-->ch_6
B--7-->ch_7
B--8-->ch_8
B--9-->ch_9
B--10-->ch_10
B--11-->ch_11
B--"12 to 20"-->ch_params

ch_0("kontrol.set_hardware()")
ch_1("kontrol.savef()") --save to file --> mdict
ch_2("kontrol.readf()") --read from file --> mdict

mdict("kontrol.mdict<br />(setup dictionary)")


subgraph dispensing["dispensing"]
    ch_3("start dispensing") --> dispense{"dispersion?"}

    dispense--1-->dispense_cont("Continuous dispensing") --> dc_cmd("PGD")
    dispense--2-->dispense_packet("Packet dispensing")

    dispense_packet--> dp_cmd("PN1{packet length}") --> dp_cmd_2("PGP")

    ch_4("Stop dispensing") --> stop_cmd("PGS")

    ch_5("Internal trigger") --> int_trig_cmd("PX0")
    ch_6("External trigger") --> ext_trig_cmd("PX1")

    ch_8("Purge") --> purge_cmd("PC100")

    ch_9("Adjust amplitude") --> amplitude_key{key press} --+--> amp_inc("Increment by AMP_ADJ_DELTA") --> pdisp_amp("PDisp.amp")
    amplitude_key --"-"--> amp_dec("Decrement by AMP_ADJ_DELTA") -->pdisp_amp
    
    pdisp_amp --> pdisp_ampd("ampd = 10.23*PDisp.amp")
    pdisp_ampd --"clamp between 0 and 1023" -->cmd_amp("PA1{ampd}")

end

ch_7("list_comports()<br />Lists serial ports")



ch_params("aa") --"Update parameters prompt"--> mdict

ch_0 -.-> mdict
ch_0 --> pdisp_disp("Pdisp.disp<br />") --> pd_disp_cmd("PF{Pdisp.disp}")
ch_0 --> pdisp_pw("Pdisp.pwidth<br />") --> pd_pw_cmd("PW1{Pdisp.pwidth}")
ch_0 --> pdisp_sa("Pdisp.strobe_amp<br />") --> pd_sa_cmd("PS4{Pdisp.strobe_amp}")
ch_0 --> pdisp_sd("Pdisp.strobe_delay<br />") --> pd_sd_cmd("PS1{Pdisp.strobe_delay}")

ch_10("Ping the board") --> cmd_ping("P?ERR")
ch_11("Exit") --> close_serial("close_serial()")
```

## Known serial commands

### Dispensing control
- `PGS`: stops dispensing
- `PGD`: continuous dispensing
- `PN1{packet_length}` then `PGP`: packet dispensing
- `PC100`: purge (`100` is set as a constant as `PURGE_CONST` -- could this be a time?)

### Dispensing settings

A few of these parameters are converted from the prompt from a % (0-100) to a +int value (0-1023); this is detailed below where it applies

- `PA1{amp}`: set amplitude to `amp`. +int (0, 1023) (0%-100% in prompt)
- `PF{disp}`: dispersion frequency in Hz. +int (10,10000)
- `PW{pulse_width}`: Pulse width (in % of cycle?). +int (102,1023) (10%-100% in prompt)
- `PS4{strobe_amp}`: strobe ampitude. +int (0, 1023) (0%-100% in prompt)
- `PS1{strobe_delay}`: strobe delay in us. Prompt: (0.6-312.5)
    - Multiplied by `F0`, set to 16.0 (16.0 MHz, clock of the strobe timer)
    - this makes it an integer between 10 (9.6 rounded up) to 5000


### Triggering
- `PX0`: internal trigger
- `PX1`: external trigger

### Control
- `P?ERR`: used to "ping" the board. Not sure if an actual command or just used to see if the board responds with an error.


## Usage

TODO 

Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support

TODO

Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.


## Authors and acknowledgment

TODO

 * Nikolay Pavlov (nikolaypavlov@polypico.com) - original Python code
 

Show your appreciation to those who have contributed to the project.

## License

TODO -- check with Polypico
For open source projects, say how it is licensed.

