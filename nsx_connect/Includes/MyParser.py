#!/usr/bin/python3

def myJSONParser(data,output=''):
    # print('\n\n')
    # print('===========================Begin debug===========================')
    # print(output + " ++> "+ str(type(data)))
    # print('===========================End debug===========================')
    if type(data) == dict:
        for k in data:
            if type(data[k]) == dict:
                myJSONParser(data[k],output+ '[\'' + str(k)+'\']')
            elif type(data[k]) == list:
                myJSONParser(data[k],output+'[\''+str(k)+"\']")
            else:
                print(output +'[\'' + str(k) + "\'] ::===> " + str(data[k]))
        output = ''
    elif type(data) == list:
        for k in range(len(data)):
            if type(data[k]) == dict:
                myJSONParser(data[k],output+'['+str(k)+"]")
            elif type(data[k]) == list:
                myJSONParser(data[k],output+'['+str(k)+"]")
            else:
                print(output + "[" + str(k) + "] :{===> " + str(data[k]))
        output = ''
    else:
        print(str(data))
        output = ''