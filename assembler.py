#Standard IAS Opcodes
OPCODES = {
    'NOP': '00000000', 'HALT': '11111111',
    'LOAD': '00000001', 'ADD': '00000101', 'SUB': '00000110',
    'MUL': '00001011', 'DIV': '00001100',
    'LSH': '00010100', 'RSH': '00010101',
    'STOR': '00100001', 'STOR_L': '00010010', 
    'JUMP': '00001101', 'JUMP+': '00001111'
}

def assemble(input_file, output_file):
    lines = []        #To store the final clean assembly code
    memory_data = {}  #To store variables defined via DATA directive

    #Read assembly code file
    with open(input_file, 'r') as f:
        for line in f:
            #Strip comments and whitespace
            clean = line.split('//')[0].strip().upper()
            if not clean: continue
            
            #Check for Assembler Directives (DATA)
            if clean.startswith("DATA"):
                parts = clean.split()
                #Format: DATA <Address> <Value>
                address = int(parts[1])
                value = int(parts[2])
                memory_data[address] = value
            else:
                lines.append(clean)

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
        #Calculate where the instruction code ends
        code_lines_count = (len(lines) + 1) // 2 
        current_addr = code_lines_count
        
        #Determine the highest memory address we need to write to
        max_addr = max(memory_data.keys()) if memory_data else code_lines_count
        
        while current_addr <= max_addr:
            val = memory_data.get(current_addr, 0)
            #Handle negative numbers for 40-bit binary
            if val < 0: val = (1 << 40) + val
            f.write(format(val, '040b') + '\n')
            current_addr += 1

    print(f"Done. Binary saved to {output_file}")

if __name__ == "__main__":
    assemble("assembly_code.txt", "binary.txt")
