import time
import random
from pprint import pprint

global rooms
rooms = { 
  'throne': { 'descr':'''You are in a giant throne room.
  To the west is a door.  To the east is a funny smelling tunnel.''', 
  'moves': { 'e':'rathole1','w':'courtyard' }
  },
  'courtyard': { 'descr':'''A courtyard.
  To the east is a massive wooden door. To the north is a path.''', 
  'moves': { 'e':'throne','n':'woodpath' } 
  },
  'woodpath': { 'descr':'''A narrow path winds through the woods.
  To the south is an old stone building. To the north is a clearing.''', 
  'moves': { 's':'courtyard','n':'clearing' } 
  },
  'clearing': { 'descr':'''A small clearing in a dense wood.''', 
  'moves': { 's':'courtyard','n':'clearing' } 
  },

  'rathole1': { 'descr':'''This place can only be described as a rathole.  The tunnel continues to the east.  You see a speck of light from the west. ''', 
  'moves': { 'w':'throne','e':'rathole2' } 
  },

  'rathole2': { 'descr':'''A deep dark tunnel continues to the west.  A faint light from the east.''', 
  'moves': { 'e':'basement','w':'rathole1' } 
  },
  'basement': { 'descr':'''A musty basement.  There is tunnel to the west.''', 
  'moves': { 'w':'rathole2' } 
  },
}

items = {
  'axe': 'A rusty axe',
  'pinecone': 'The most beautifule pinecone you have ever seen. It glows a bit...',
  'notebook': 'A dusty leather-bound notebook with lovely handwriting.',
  'string': 'A string that seems unusually strong',
  'arrow': 'An arrow with three bright blue feathers',
  'needles': 'A pair of shiny knitting needles, well used but in excellent condition',
}

for r in rooms.keys():
  rooms[r]['items']=[]
  rooms[r]['who']=[]

rooms['throne']['items'].append('pinecone')
rooms['courtyard']['items'].append('axe')
rooms['basement']['items'].append('notebook')
rooms['clearing']['items'].append('arrow')
rooms['woodpath']['items'].append('needles')

global characters
characters = {
  'robot': {
    'items':['gem'],
    'state':None,
    'move_prob':0.1,
    'say':['Leave me be you filthy scum!  But do give me all your precious items first :)']
    },
  'bat': {
    'items':[],
    'state':None,
    'move_prob':1.0,
    'say':['Eeek!!!!','Screech!!!','chhhhiiiiiiiizzzzzzzzz!!!!!']
    },
  'talkingtree': {'items':['staff'],'state':None,'move_prob':0.0,'say':['There is a notebook in the basement.', 'Be careful of the scarecrow.','The old lady was once the queen of all Terrainia.', ]
  },
  'oldlady': {'items':['wool'],'state':None,'move_prob':0.0,'say':['If only I had some needles.',]
  }


}

def place_char(char,where):
  global characters, rooms
  characters[char]['where']=where
  rooms[where]['who'].append(char)

place_char('robot','throne')
place_char('bat','basement')
place_char('talkingtree','clearing')
place_char('oldlady','courtyard')


global myitems
myitems = ['string',]
curroom_label = 'throne'

def help():
  print('Valid moves are:')
  print('')
  print('e   East')
  print('w   West')
  print('n   North')
  print('s   South')
  print('')
  print('get item     Pick up item')
  print('put item     Put item down')
  print('look item    Look at an item')
  print('inv          Inventory')

  print('')
  print('talk to person       Talk to someone')
  print('give item to person  Give something')
  print('kill person          Kill a person')
  print('')
  print('h   Help')


print('-----------------------------')
print('| ROBERTS CREEK ADVENTURE |')
print('-----------------------------')
print('')
help()
print('')
print(' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  ')
print('')
print('You awaken as if from an endless sleep.  You do not remember how you arrived here.')
print('')
time.sleep(1.0)

while True:
  curroom = rooms[curroom_label]
  print(curroom['descr'])

  # let characters move
  for c in characters:
    croom = characters[c]['where']
    actions = list(rooms[croom]['moves'].keys())

    if actions and characters[c]['move_prob']>0.0:
      r = random.random()
      if r>characters[c]['move_prob']:
        pass
      else:
        ra = random.randint(0,len(actions)-1)
        action=actions[ra]
        newroom = rooms[croom]['moves'][action]
        characters[c]['where'] = newroom

        rooms[croom]['who'].remove(c)
        rooms[newroom]['who'].append(c)

        # debug: show how other chars move
        #print(c + " moves with "+action+ " from "+croom+" to "+newroom)

        if newroom == curroom_label:
          print("")
          print("Suddenly, "+c+" arrives!")
        if croom == curroom_label:
          print("")
          print(c+" left towards the "+action)


  if 'items' in curroom and curroom['items']:
    print('')
    print('There is a '+ ", a ".join(curroom['items']) )
    #for it in curroom['items']:

  if 'who' in curroom and curroom['who']:
    print('')
    for char in curroom['who']:
      if characters[char]['items']:
        it = " who has a "+ ", a ".join(characters[char]['items'])
      else:
        it =""
      descr=""
      if characters[char]['state']:
        descr = characters[char]['state']+" "
      print('You see a '+ descr+char + " "+it )

  print(' ~~~ ')
  print('')

  reply = input("What shall you do? ")
  reply = reply.strip().lower()

  tokens = reply.split(" ")

  action = tokens[0]

  print(action)
  print("")

  if action in ['e','w','n','s','east','west','north','south']:
    action = action[0]
    if action in curroom['moves']:
      curroom_label=curroom['moves'][action]
    else:
      print("Invalid move")

  elif action in ['get']:
    if len(tokens)!=2:
      print("Thats not how you that command works")
    else:
      item = tokens[1]
      if item in curroom['items']:
        rooms[curroom_label]['items'].remove(item)
        myitems.append(item)
        print("You get the "+item)
      else:
        print('Its not here!')

  elif action in ['put']:
    if len(tokens)!=2:
      print("Thats not how you that command works")
    else:
      item = tokens[1]
      if item in myitems:
        rooms[curroom_label]['items'].append(item)
        myitems.remove(item)
        print("You put down the "+item)
      else:
        print('You dont have it!')

  elif action in ['look']:
    if len(tokens)!=2:
      print("Thats not how you that command works")
    else:
      item = tokens[1]
      if item in rooms[curroom_label]['items'] or item in myitems:
        print( items[item] )
      else:
        print("That isnt here!")

  elif action in ['give']:
    if len(tokens)!=4:
      print("Thats not how you that command works")
    else:
      item = tokens[1]
      who = tokens[3]
      if item not in myitems:
        print("You dont have that!")
      elif who not in curroom['who']:
        print("They arent here!")
      else:
        characters[who]['items'].append(item)
        myitems.remove(item)
        print("You give the "+item+" to "+who)

  elif action in ['talk']:
    if len(tokens)!=3:
      print("Thats not how you that command works")
    else:
      who = tokens[2]
      if who not in curroom['who']:
        print("They arent here!")
      elif not characters[who]['say'] or characters[who]['state']=='dead':
        print("They do not reply.")
      else:
        saying = random.randint(0,len(characters[who]['say'])-1)
        print(who+" says: "+characters[who]['say'][saying])

  elif action in ['kill']:
    if len(tokens)!=2:
      print("Thats not how you that command works")
    else:
      who = tokens[1]
      if who not in curroom['who']:
        print("They arent here!")
      elif 'axe' in myitems:
        print("You brutally chop up "+who)
        characters[who]['move_prob']=0.0
        characters[who]['state']='dead'
        print("")
        print("Why would you do such a horrible thing to another being?")
        print("")
        for i in characters[who]['items']:
          rooms[curroom_label]['items'].append(i)
        characters[who]['items']=[]
      else:
        print("You dont have a weapon...")

  elif action in ['debug']:
    print('---characters---')
    pprint(characters)

    print('---rooms---')
    pprint(rooms)

    print('---items---')
    pprint(items)

    print('---myitems---')
    pprint(myitems)




  elif action in ['h','help','?']:
    help()

  elif action in ['inv',]:
    print("")
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ')
    print('   Ye Olde Inventorie ')
    print('   ------------------ ')
    if myitems:
      print('You have a '+ ", a ".join(myitems) )
    else:
      print("You dont have anything")
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ')
    print("")
    print("")

  else:
    print("I dont know what you mean.  h for help.")


  print(' ')
  print(' ~~~ ')
  print('')
