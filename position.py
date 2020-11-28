import math
##각 노드, 디바이스 위치 정보 클래스
class Pos:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.baserssi=-20
        self.rssi=0
        self.distance=0
    def __sub__(self, other):
        return math.sqrt(math.pow((self.x - other.x), 2) + math.pow((self.y, other.y),2))
    def calc(self):
        self.distance=pow(10,(self.baserssi-self.rssi)/20)
##신호세기를 거리로 변환
def rssiToDistance(rssi, baserssi):
    return pow(10,(baserssi-rssi)/20)
##표준편차 계산
def bias(d1,d2,d3):
    return math.sqrt(pow(d1,2)+pow(d2,2)+pow(d3,2))
##신호가 센 쪽으로 좌표의 이동
def move(station,node,k):
    if station.x<node.x:
        station.x+=(50-node.distance)*k
    else:
        station.x-=(50-node.distance)*k
    if station.y < node.y:
        station.y += (50-node.distance) * k
    else:
        station.y -= (50-node.distance) * k
##디바이스의 위치 찾기
def distanceToLoc(node1,node2,node3):
    node1.calc()
    node2.calc()
    node3.calc()
    Pcenter=Pos()
    Pcenter.x=(node1.x+node2.x+node3.x)/3   ##무게중심에서 시작
    Pcenter.x=(node1.y+node2.y+node3.y)/3   ##무게중심에서 시작
    ##이전의 오차
    prev=bias(node1.distance-(node1-Pcenter),node2.distance-(node2-Pcenter),node2.distance-(node2-Pcenter))
    k=0.01
    move(Pcenter,node1,k)
    move(Pcenter,node2,k)
    move(Pcenter,node3,k)
    ##현재의 오차
    cur=bias(node1.distance-(node1-Pcenter),node2.distance-(node2-Pcenter),node2.distance-(node2-Pcenter))
    ##이전<현재 의 오차가 될 때까지 반복하여 이동
    while(prev>cur):
        prev=cur
        move(Pcenter, node1, k)
        move(Pcenter, node2, k)
        move(Pcenter, node3, k)
        cur=bias(node1.distance-(node1-Pcenter),node2.distance-(node2-Pcenter),node2.distance-(node2-Pcenter))
    return Pcenter