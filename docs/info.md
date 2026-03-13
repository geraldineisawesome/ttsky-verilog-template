<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

A 4-bit up/down counter controlled by two input bits. When `ui_in[0]` (up) is high, the counter increments each clock cycle. When `ui_in[1]` (down) is high, it decrements. When both are high, the counter holds its value. The count wraps around — overflowing from 15 back to 0 and underflowing from 0 back to 15. The current count is output on the lower 4 bits of `uo_out`

## How to test
1. Reset the counter by pulling `rst_n` low for at least 2 clock cycles, then release it high.
2. Set `ui_in[0] = 1, ui_in[1] = 0` to count up — the count on `uo_out[3:0]` should increment each clock cycle.
3. Set `ui_in[0] = 0, ui_in[1] = 1` to count down.
4. Set both `ui_in[0] = 1, ui_in[1] = 1` to hold the current value.
5. Verify overflow by counting up past 15 —> it should wrap to 0.
6. Verify underflow by counting down past 0 —> it should wrap to 15.

## Descirption of AI 
I used AI to help me understand the timing in my testbench because I always confused the way cocotb uses the clockcyle waiting time. Other than that all files were written by me

## External hardware

List external hardware used in your project (e.g. PMOD, LED display, etc), if any
