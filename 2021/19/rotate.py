"""3d rotations."""



def rotations(x,y,z):
  yield ( x,  y,  z)
  yield ( x,  z, -y)
  yield ( x, -y, -z)
  yield ( x, -z,  y)

  yield ( y, -x,  z)
  yield ( y,  z,  x)
  yield ( y,  x, -z)
  yield ( y, -z, -x)

  yield (-x, -y,  z)
  yield (-x, -z, -y)
  yield (-x,  y, -z)
  yield (-x,  z,  y)

  yield (-y,  x,  z)
  yield (-y, -z,  x)
  yield (-y, -x, -z)
  yield (-y,  z, -x)

  yield ( z,  y, -x)
  yield ( z,  x,  y)
  yield ( z, -y,  x)
  yield ( z, -x, -y)

  yield (-z, -y, -x)
  yield (-z, -x,  y)
  yield (-z,  y,  x)
  yield (-z,  x, -y)


def rot_00(pos):
  return ( pos[0],  pos[1],  pos[2])
def rot_01(pos):
  return ( pos[0],  pos[2], -pos[1])
def rot_02(pos):
  return ( pos[0], -pos[1], -pos[2])
def rot_03(pos):
  return ( pos[0], -pos[2],  pos[1])
def rot_04(pos):
  return ( pos[1], -pos[0],  pos[2])
def rot_05(pos):
  return ( pos[1],  pos[2],  pos[0])
def rot_06(pos):
  return ( pos[1],  pos[0], -pos[2])
def rot_07(pos):
  return ( pos[1], -pos[2], -pos[0])
def rot_08(pos):
  return (-pos[0], -pos[1],  pos[2])
def rot_09(pos):
  return (-pos[0], -pos[2], -pos[1])
def rot_10(pos):
  return (-pos[0],  pos[1], -pos[2])
def rot_11(pos):
  return (-pos[0],  pos[2],  pos[1])
def rot_12(pos):
  return (-pos[1],  pos[0],  pos[2])
def rot_13(pos):
  return (-pos[1], -pos[2],  pos[0])
def rot_14(pos):
  return (-pos[1], -pos[0], -pos[2])
def rot_15(pos):
  return (-pos[1],  pos[2], -pos[0])
def rot_16(pos):
  return ( pos[2],  pos[1], -pos[0])
def rot_17(pos):
  return ( pos[2],  pos[0],  pos[1])
def rot_18(pos):
  return ( pos[2], -pos[1],  pos[0])
def rot_19(pos):
  return ( pos[2], -pos[0], -pos[1])
def rot_20(pos):
  return (-pos[2], -pos[1], -pos[0])
def rot_21(pos):
  return (-pos[2], -pos[0],  pos[1])
def rot_22(pos):
  return (-pos[2],  pos[1],  pos[0])
def rot_23(pos):
  return (-pos[2],  pos[0], -pos[1])

rot_func = [None] * 24
rot_func[ 0] = rot_00
rot_func[ 1] = rot_01
rot_func[ 2] = rot_02
rot_func[ 3] = rot_03
rot_func[ 4] = rot_04
rot_func[ 5] = rot_05
rot_func[ 6] = rot_06
rot_func[ 7] = rot_07
rot_func[ 8] = rot_08
rot_func[ 9] = rot_09
rot_func[10] = rot_10
rot_func[11] = rot_11
rot_func[12] = rot_12
rot_func[13] = rot_13
rot_func[14] = rot_14
rot_func[15] = rot_15
rot_func[16] = rot_16
rot_func[17] = rot_17
rot_func[18] = rot_18
rot_func[19] = rot_19
rot_func[20] = rot_20
rot_func[21] = rot_21
rot_func[22] = rot_22
rot_func[23] = rot_23

def pfunc():
  for fn in range(24):
     print('rot_func[%2d] = rot_%02d' % (fn, fn))
   

def check():
  for x,y,z in rotations(1, 2, 3):
    print('%2d' % x, '%2d' % y, '%2d' % z)
  print('Last 2')
  print(rot_func[22]((1, 2, 3)))
  print(rot_func[23]((1, 2, 3)))


if __name__ == '__main__':
  check()
  # pfunc()
