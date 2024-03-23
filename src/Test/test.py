a = [1, 2, 3, 4, 5, 5, 5, 5, 6]
print('a: ', a)

# b = a.index(5)
a.remove(5)
a.remove(5)
a.remove(5)
a.remove(5)
print('hello')
print('a :', a)

a = ["Amir Hamidi", "Amir Hamidi", "Amir Hamidi", "Amir Hamidi"]
b = 1
print(a)



a=( "committee votes (round: 1, rejected rounds: 0):"
  "----------"
  "votes"

  "mission_votes (round: 1):"
  "----------"
  "votes"
  
  "Results"
  "----------"
  "city_won_round : 1"
  "evil_won_round : 0"
  "------------------------------"
  

  )
a="mission_votes (round: {round}):" + ("-" * 30)
print(a)