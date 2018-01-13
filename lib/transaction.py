from enum import Enum

class SpendType(Enum):
     P2PKH  = 0 
     P2WPKH = 1


class Encoder(object):

   @staticmethod
   def toVarint(n):
       if(n <= 0xfc): return n.to_bytes(1,'little')
       if(n <= 0xffff): return b'\xfd' + n.to_bytes(2,'little')
       if(n <= 0xffffffff): return b'\xfe' + n.to_bytes(4, 'little')
       if(n <= 0xffffffffffffffff): return b'\xff' + n.to_bytes(8, 'little') 


class TransactionInput(object):

   def __init__(self, prevTxHash, index, spendType):
       self.prevTxHash = prevTxHash
       self.index = index
       self.spendType = spendType
   
   def serialize(self):
       inputBytes = self.prevTxHash.to_bytes(32, 'little')
       inputBytes = inputBytes + self.index.to_bytes(4, 'big')

      
class Opcode(Enum):
  OP_CHECKSIG    = b'\xac'  
  OP_DUP         = b'\x76'
  OP_EQUALVERIFY = b'\x88'
  OP_HASH160     = b'\xa9'


class TransactionOutput(object):
   
   def __init__(self, satoshis, hash160, spendType):
       self.satoshis = satoshis;
       self.hash160 = hash160 
       self.spendType = spendType

   def lockScript(self):
       if(self.spendType == SpendType.P2PKH):
          hashBytes = self.hash160.to_bytes(20,'big')
          hashSize = self.size(hashBytes)
          pre = Opcode.OP_DUP.value + Opcode.OP_HASH160.value + hashSize + hashBytes + Opcode.OP_EQUALVERIFY.value + Opcode.OP_CHECKSIG.value
          return Opcode.OP_DUP.value + Opcode.OP_HASH160.value + hashSize + hashBytes + Opcode.OP_EQUALVERIFY.value + Opcode.OP_CHECKSIG.value

   def size(self, content):
       s = len(content)
       return Encoder.toVarint(s)

   def serialize(self):
       amount = self.satoshis.to_bytes(8, 'little')
       script = self.lockScript()
       return amount + self.size(script) + script 
       
