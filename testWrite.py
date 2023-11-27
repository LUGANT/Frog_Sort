from modules.write import readAnswer, writeAnswer

writeAnswer( [ (0,1) ] )

answer = readAnswer()
print(answer)
print(answer[0])
print(type(answer))
print(type(answer[0]))