
# IAS Architecture Simulator

A full software simulation of the **IAS** computer architecture, implementing the stored-program concept. This project includes a custom Assembler, a Processor Simulator (with Disk-as-RAM functionality), and a demonstration of the `std::lower_bound` algorithm using **self-modifying code**.

## Project Overview

The IAS machine lacks modern features like index registers. To iterate through arrays, programs must dynamically modify their own instructions in memory during runtime.

This project demonstrates that capability by implementing **Binary Search (Lower Bound)** to find the first occurrence of a target number in a sorted array. The simulator treats the `binary.txt` file as the system's physical memory, allowing for persistent storage and modification during execution.

## Prerequisites

* Python 3


## How to Run

### Step 1: Write/Modify Assembly (Optional)
Open `assembly_code.txt` to modify the input data.
* **Instructions** are written using standard IAS mnemonics (e.g., `LOAD`, `STOR`, `ADD`).
* **Data** is defined at the bottom using the `DATA` directive:
    ```text
    DATA 103 25      // Change Target Value (edit '25')
    DATA 500 10      // Change Array Element (edit '10')
    ```

### Step 2: Assemble the Code
Run the assembler to convert your assembly code into machine language. This creates (or resets) the `binary.txt` file with the initial state.

```bash    
python3 assembler.py   
```
### Step 3: Run the processor simulator
Execute the simulator. It will read instructions from `binary.txt` and perform the Fetch-Decode-Execute cycle.
```bash
python3 ias.py
```
### Expected Output
The simulator will print a cycle-by-cycle trace of the processor state, showing the Program Counter (PC), Instruction Register (IR), Accumulator (AC), and others. Finally printing the answer.

---
