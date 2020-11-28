import time

if __name__ == "__main__":
    # x = '\u3002'
    # x = '\u2731'
    # x = '\u002a'
    # a = '\u003c'
    # b = '\u003e'
    # c = '\u005e'
    # a = '\u007c'
    # b = '\u005c'
    # c = '\u2012'
    # d = '\u002f'
    # animation = [a,b,c,d]
    #animation = [x,x+x,x+x+x,x+x+x+x,x+x+x+x+x,x+x+x+x,x+x+x,x+x,x]
    animation = [".","..","...","....",".....","....","...","..","."]
    #animation = ["|","||","|||","||||","|||||","||||||","|||||||","||||||||","|||||||","||||||","|||||","||||","|||","||","|"]
    idx = 0
    t = time.time()
    print("Time = " + str(t))
    print('\u3002')
    x = '\u3002'
    while (time.time() < t + 60):
        # print("Time = " + str(time.time()))
        # print("Expected End Time = " + str(t+5))
        # print(idx % len(animation),end='\r\t')
        print("                 ",end='\r')
        print(animation[idx % len(animation)], end='\r')
        time.sleep(1)
        idx+=1
else:
    print("Imported by " + __name__)