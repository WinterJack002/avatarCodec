import numpy as np

def exponential_golomb_encode(values):
    bitstream = ''
    print('values: ', values)
    for value in values:
        m = value + 1 # 这里的+1是为了确保非负数
        q = int(np.floor(np.log2(m)))
        prefix = '0' * q + '1'
        suffix = format(m - (1 << q), '0{}b'.format(q))
        bitstream += prefix + suffix
        
    print('bitstream/8: ', len(bitstream)/8)
    return bitstream
	
def test_exponential_golomb_encode(n):
    unarycode = ''
    golombCode =''
    ###Quotient and Remainder Calculation
    groupID = np.floor(np.log2(n+1))
    temp_=groupID
    #print(groupID)
    
    while temp_>0:
        unarycode = unarycode + '0'
        temp_ = temp_-1
    unarycode = unarycode#+'1'

    index_binary=bin(n+1).replace('0b','')
    golombCode = unarycode + index_binary
    return golombCode


values = [256]

test1 = exponential_golomb_encode(values)
test2 = test_exponential_golomb_encode(values[0])
print("1: ", test1)
print("2: ", test2)