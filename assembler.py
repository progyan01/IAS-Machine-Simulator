#Standard IAS Opcodes
OPCODES = {
    'NOP': '00000000', 'HALT': '11111111',
    'LOAD': '00000001', 'ADD': '00000101', 'SUB': '00000110',
    'MUL': '00001011', 'DIV': '00001100',
    'LSH': '00010100', 'RSH': '00010101',
    'STOR': '00100001', 'STOR_L': '00010010', 
    'JUMP': '00001101', 'JUMP+': '00001111'
}

#Variables & Array Data
MEMORY_DATA = {
    100: 0, 101: 9, 102: 0, 103: 25, 104: -1, 105: 1, 106: 500,
    #L, R, MID, TARGET, ANS, constant 1; in order
    107: 1 << 32, #Template instruction "LOAD M(0)"
    #Sorted Array
    500: 10, 501: 20, 502: 24, 503: 25, 504: 25,
    505: 30, 506: 40, 507: 50, 508: 60, 509: 70
}

def assemble(input_file, output_file):
    lines = []        #To store the final clean assembly code
    
    #Read assembly code file
    with open(input_file, 'r') as f:
        for line in f:
            #Strip comments and whitespace
            clean = line.split('//')[0].strip().upper()
            if clean: lines.append(clean)

    #Convert pairs of instructions to binary pairs
    with open(output_file, 'w') as f:
        #Loop through lines 2 at a time (Left & Right Instructions)
        for i in range(0, len(lines), 2):
            pair_binary = ""
            
            #Process Left and Right instruction(Loop runs twice)
            for j in [i, i+1]:
                if j >= len(lines): #Padding if odd number of lines
                    pair_binary += OPCODES['NOP'] + "000000000000"
                    continue
                
                parts = lines[j].split()        #Splitting by space
                cmd = parts[0]
                
                #Get Opcode
                opcode = OPCODES.get(cmd, '00000000')
                
                #Get Address
                addr = 0
                if len(parts) > 1:
                    #Takes string "M(123)", slices off "M(" and ")", then converts to int
                    addr_str = parts[1].replace("M(", "").replace(")", "")
                    addr = int(addr_str)
                
                pair_binary += opcode + format(addr, '012b')
                #Convert the memory address to a 12 bit binary string

            f.write(pair_binary + '\n')

        #Write Data (Variables + Array) and fill each gap with 40 bit 0 string
        current_addr = (len(lines) + 1) // 2            #Calculate how many code lines we wrote
        max_addr = max(MEMORY_DATA.keys())              #Last address of our memory
        
        while current_addr <= max_addr:
            val = MEMORY_DATA.get(current_addr, 0)
            #Handle negative numbers for 40-bit binary
            if val < 0: val = (1 << 40) + val
            f.write(format(val, '040b') + '\n')
            current_addr += 1

    print(f"Done. Binary saved to {output_file}")

if __name__ == "__main__":
    assemble("assembly_code.txt", "binary.txt")
