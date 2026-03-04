# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer

UP_BIT = 0
DOWN_BIT = 1

def set_bits(up: int, down: int) -> int:
    "returns the 8 bit ui_in value with up/down set, otherwise 0"
    return ((up & 1) << UP_BIT) | ((down & 1) << DOWN_BIT)

def get_count(dut) -> int:
    "count is on the lower 4 bits of uo_out"
    return int(dut.uo_out.value) & 0xF

async def clock_and_read(dut, cycles=1):
    "clock n cycles then wait 1ns for outputs to settle before reading"
    await ClockCycles(dut.clk, cycles)
    await Timer(1, unit="ns")

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start my counter test")

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset testing")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    dut.rst_n.value = 0  # active low reset
    await clock_and_read(dut, 2)
    assert get_count(dut) == 0, f"Expected count = 0 during reset, got {get_count(dut)}"

    dut.rst_n.value = 1  # deassert reset
    await clock_and_read(dut, 2)
    assert get_count(dut) == 0, f"Expected count = 0 after reset release, got {get_count(dut)}"

    # -------counting up 3 cycles-------------
    dut._log.info("Count up 3 cycles")
    dut.ui_in.value = set_bits(up=1, down=0)
    await clock_and_read(dut); assert get_count(dut) == 1
    await clock_and_read(dut); assert get_count(dut) == 2
    await clock_and_read(dut); assert get_count(dut) == 3

    # -------hold when both high (1 1)-------------
    dut._log.info("both high")
    dut.ui_in.value = set_bits(up=1, down=1)
    await clock_and_read(dut)
    assert get_count(dut) == 3, f"Holding value up = 1, down = 1 failed, got {get_count(dut)}"
    await clock_and_read(dut)
    assert get_count(dut) == 3, f"Holding value up = 1, down = 1 failed, got {get_count(dut)}"

    # -------count down for 2 cycles-------------
    dut._log.info("counting down for 2 cycles")
    dut.ui_in.value = set_bits(up=0, down=1)
    await clock_and_read(dut); assert get_count(dut) == 2
    await clock_and_read(dut); assert get_count(dut) == 1

    # -------overflowing test-------------
    dut._log.info("overflow test: reach 15 and then up to 0")
    dut.rst_n.value = 0
    dut.ui_in.value = 0  # clear input during reset
    await clock_and_read(dut, 2)
    dut.rst_n.value = 1
    await clock_and_read(dut)
    assert get_count(dut) == 0

    dut.ui_in.value = set_bits(up=1, down=0)
    await clock_and_read(dut, 15)
    assert get_count(dut) == 15, f"expected 15 before overflow, got {get_count(dut)}"
    await clock_and_read(dut)
    assert get_count(dut) == 0, f"overflow failed, expected 0, got {get_count(dut)}"

    # -------underflow test-------------
    dut._log.info("underflow test: reach 0 and then down to 15")
    dut.ui_in.value = set_bits(up=0, down=1)
    await clock_and_read(dut)
    assert get_count(dut) == 15, f"Underflow failed: expected 15, got {get_count(dut)}"

    dut._log.info("PASS: counter up/down/hold/reset/overflow/underflow")