import time
import random
from pprint import pprint

global rooms
rooms = { 
  'throne': { 'descr':'''You are in a vast throne room.  It seems like it was recently (and hastily) redecorated.

To the west is a door.
  
To the east is a funny smelling tunnel.''', 
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
  'clearing': { 'descr':'''A small clearing in a dense wood. To the north it looks rather frosty.''', 
  'moves': { 's':'woodpath','n':'frostpath', } 
  },
  'frostpath': { 'descr':'''An extremely icy path leads north, it looks very hard to pass.''', 
  'moves': { 's':'clearing', }   #### special
  },

  'frostentrance': { 'descr':'''A vast, winter castle forebodes to the North, gisteningly beautiful, and yet very creepy...

  The icy wind blows through your hair and makes your teeth chatter.

  A frosty path leads south.
.''', 
  'moves': { 's':'frostpath', }   #### special
  },

  'rathole1': { 'descr':'''This place can only be described as a rathole.  The tunnel continues to the east.  You see a speck of light from the west. ''', 
  'moves': { 'w':'throne','e':'rathole2','s':'hiddenroom' } 
  },
  'hiddenroom' : { 'descr':'''You are in a tiny room.
  ''', 
  'moves': { 'n':'rathole1', } 
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
  'staff': 'A wooden staff made from a wizened old tree branch, on the tip is an embedded gem that seems to swirl with florescent green.',
  'pinecone': 'The most beautifule pinecone you have ever seen. It glows a bit...',
  'notebook': '''A dusty leather-bound notebook with lovely handwriting. Upon it is written:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   Spellcaster's First Guide
   ~~~~~~~~~~~~~~~~~~~~~~~~~

~ lightbloom ~

This lovely spell is great for entertaining 
yourself and your friends!

~ flyingcarpet ~

This powerful spell lets you get out of 
trouble fast. But careful, it is very hard 
to control where you end up!

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  ''',

  'redscroll': '''A red tinted scroll tied by a ribbon.  It looks very, very old and a bit dusty.
  Unrolling it you see:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   Spellcaster's Second Guide
   ~~~~~~~~~~~~~~~~~~~~~~~~~

~ vitality ~

This ancient spell brings forth the power
of life itself.  It allows you raise the
dead, good as new.

~ darkcloud ~

This evil spell of death must only be used 
in the gravest of moments.  Few can survive 
its deadly power.  Misuse of this spell is
grounds for permanent expulsion from the 
sorcerers guild.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  ''',

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
rooms['hiddenroom']['items'].append('redscroll')

global characters
characters = {
  'robot': {
    'items':['gem'],
    'state':None,
    'move_prob':0.1,
    'mana':0,'mana_regen':0,
    'say':['Leave me be you filthy scum!  But do give me all your precious items first :)']
    },
  'bat': {
    'items':[],
    'state':None,
    'move_prob':1.0,
    'mana':0,'mana_regen':0,
    'say':['Eeek!!!!','Screech!!!','chhhhiiiiiiiizzzzzzzzz!!!!!']
    },
  'talkingtree': {'items':['staff'],'state':None,'move_prob':0.0, 'mana':0,'mana_regen':0,'say':['There is a very special notebook in the basement east of the throne room...', 'The old lady was once the queen of all Terrainia. A fine queen she was too, until everything changed...', ]
  },
  'oldlady': {'items':['wool'],'state':None,    'mana':0,'mana_regen':0,
'move_prob':0.0,'say':['If only I had some needles.',]
  },
  'player': {'items':['gem'],'state':None,'move_prob':0.333,    'mana':1,'mana_regen':1,
'say':['I was just trying to play a game...!',]
  },
  'magician': {'items':[],'state':None,'move_prob':0.1,'mana':1000,'mana_regen':10,'say':['There is a one thing you should never, ever, ever do. If I had a gem, I could tell you about it...',]
  },
}


spells = {
  'vitality': { 'cost':20, 'ok': 'A glow slowly appears from your palms and extends out in a giant ball, encompassing everything and everyone nearby...','fail': '*fizzle*' },
  'flyingcarpet': {'cost':10, 'ok': 'A square of light appears below you and lifts you up, up .... suddenly your are spinning very fast and confused!  It sets you down.  You blink and look around....','fail': '*fizzle*' },
  'darkcloud': { 'cost':20,'ok': 'A putrid cloud slowly fills the room.  You cough your lungs out!  When it finally clears, you it is strangely quiet...','fail': '*fizzle*' },
  'lightbloom': { 'cost':1,'ok': 'A giant circle of light appears ahead of you.  It begins to pulse, as you hear the most beautiful music eminating from the center. You feel refreshed!','fail': '*fizzle*' },

}


def place_char(char,where):
  global characters, rooms
  characters[char]['where']=where
  rooms[where]['who'].append(char)

place_char('robot','throne')
place_char('bat','basement')
place_char('talkingtree','clearing')
place_char('oldlady','courtyard')
place_char('magician','basement')
place_char('player','throne')


me = 'player'

#myitems = ['',]


def plot_move_check(move_type,item=None,who=None):

  if move_type=="talk" and who=="talkingtree":

    # the talkingtree grants the staff
    if 'staff' in characters[who]['items']:
      characters[who]['items'].remove('staff')
      characters[me]['items'].append('staff')

      print("~~~~~~")
      print("The talkingtree gifts you a long, strong, very old looking staff!")
      print("~~~~~~")

    # the oldlady knits you a woolsuit, and the frozen path melts
  if move_type=="give" and who=="oldlady" and item=='needles' and 'wool' in characters[who]['items']:

    characters[who]['items'].remove('wool')
    characters[me]['items'].append('woolsuit')

    characters[who]['say']=[['''Good luck on your mission!''']]

    # melt the frozen path
    rooms['frostpath']['moves']['n']='frostentrance'
    rooms['frostpath']['moves']['descr']='''
    A muddy path leads north, it looks like part of it has melted recently.
    '''

    print("~~~~~~")
    print("The oldlady knits you a lovely warm woolsuit!")
    print("~~~~~~")

  if move_type=="give" and who=="magician" and item=='gem':

    print("~~~~~~")
    print("The old magician comes very close to you.  His breath smells very odd. In a hushed voice he whispers:")
    print("")
    print("Never try mindx on another character")
    print("All kinds of chaos would be unleashed")
    print("Do not say I didnt warn you!")
    print("")
    print("~~~~~~")

    characters[who]['say']=[['''Remember, just dont do it''']]


  if move_type=="kill" and who=="robot":

    # the spell on the oldlady is broken
    characters['oldlady']['moveprob']=0.666
    characters['oldlady']['say']=[['''That robot has enslaved us for 47 years.  
    Thank you for saving our kingdom from his tyranny! 
    I just cannot stop dancing...''']]
    print("~~~~~~")
    print("You hear birds chirping, music rising, and singing... You suddenly want to talk to the oldlady.")
    print("~~~~~~")





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
  print('mana         Check your mana score')
  print('inv          Inventory')
  print('')
  print('talk to person       Talk to someone')
  print('give item to person  Give something')
  print('kill person          Kill a person')
  print('')
  print('cast spellname       Cast a spell')
  print('')
  print('h   Help')
  print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  ')


print('~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print(' Roberts Creek Adventure ')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('')
print(' h for help ')
print('')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  ')
print('')
print('''You awaken as if from an endless sleep.  You do not remember how you arrived here.

You are a young magician...

''')
print('')
time.sleep(1.0)
xray_mode=False

while True:
  curroom_label = characters[me]['where']
  curroom = rooms[curroom_label]
  #print("curroom_label",curroom_label)

  print(curroom['descr'])
  #pprint(rooms)
  if xray_mode:
    print('\nXray Mode\n~~~~~~~')

  # let characters move
  for c in characters:
    characters[c]['mana']+=characters[c]['mana_regen']

    if c==me:
      # dont force player to move
      continue

    croom = characters[c]['where']
    actions = list(rooms[croom]['moves'].keys())

    if characters[c]['move_prob']==0.0:
        if xray_mode:
          # debug: show how other chars move
          print(c + " in "+croom+" *never* moves")
    if actions and characters[c]['move_prob']>0.0:
      r = random.random()
      if characters[c]['state']=='dead' or r>characters[c]['move_prob']:
        if xray_mode:
          # debug: show how other chars move
          print(c + " in "+croom+" does not move")
      else:
        ra = random.randint(0,len(actions)-1)
        action=actions[ra]
        newroom = rooms[croom]['moves'][action]
        characters[c]['where'] = newroom

        rooms[croom]['who'].remove(c)
        rooms[newroom]['who'].append(c)

        if xray_mode:
          # debug: show how other chars move
          print(c + " moves  "+action+ " from "+croom+" to "+newroom)

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
      if char==me:
        continue  # dont mention ourself
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

  if characters[me]['state']=='dead':
    print("You are dead.  There is not much you can do in this state.")
    print("")
    print("GAME OVER")
    print("")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    exit(0)

  reply = input("What shall you do? ")
  reply = reply.strip().lower()

  tokens = reply.split(" ")

  print(' '+'~~~ ' * 10)

  action = tokens[0]

  #print(action)
  #print("")

  if action in ['e','w','n','s','east','west','north','south']:
    action = action[0]
    if action in curroom['moves']:
      newroom = rooms[curroom_label]['moves'][action]

      rooms[curroom_label]['who'].remove(me)
      rooms[newroom]['who'].append(me)

      characters[me]['where']=curroom['moves'][action]

    else:
      print("Invalid move")

  elif action in ['get']:
    if len(tokens)!=2:
      print("Thats not how you that command works")
    else:
      item = tokens[1]
      if item in curroom['items']:
        rooms[curroom_label]['items'].remove(item)
        characters[me]['items'].append(item)
        print("You get the "+item)
        plot_move_check(action,item=item,who=None)
      else:
        print('Its not here!')

  elif action in ['put']:
    if len(tokens)!=2:
      print("Thats not how you that command works")
    else:
      item = tokens[1]
      if item in characters[me]['items']:
        rooms[curroom_label]['items'].append(item)
        characters[me]['items'].remove(item)
        print("You put down the "+item)
      else:
        print('You dont have it!')

  elif action in ['look']:
    if len(tokens)!=2:
      print("Thats not how you that command works")
    else:
      item = tokens[1]
      if item in rooms[curroom_label]['items'] or item in characters[me]['items']:
        print( items[item] )
      else:
        print("That isnt here!")

  elif action in ['give']:
    if len(tokens)!=4:
      print("Thats not how you that command works")
    else:
      item = tokens[1]
      who = tokens[3]
      if item not in characters[me]['items']:
        print("You dont have that!")
      elif who not in curroom['who']:
        print("They arent here!")
      else:
        characters[who]['items'].append(item)
        characters[me]['items'].remove(item)
        print("You give the "+item+" to "+who)
        plot_move_check(action,item,who)

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
        plot_move_check(action,who=who)

  elif action in ['kill']:
    if len(tokens)!=2:
      print("Thats not how you that command works")
    else:
      who = tokens[1]
      if who not in curroom['who']:
        print("They arent here!")
      elif characters[who]['state']=='dead':
        print("They are already dead!")
      elif 'axe' in characters[me]['items']:
        print("You brutally chop up "+who)
        characters[who]['state']='dead'
        print("")
        print("Why would you do such a horrible thing to another being?")
        print("")
        for i in characters[who]['items']:
          rooms[curroom_label]['items'].append(i)
        characters[who]['items']=[]
        plot_move_check(action,item=None,who=who)
      else:
        print("You dont have a weapon...")

  elif action in ['cast']:
    if len(tokens)!=2:
      print("Thats not how you that command works")
    else:
      spell = tokens[1]
      if spell not in spells.keys():
        print("That isnt a real spell, is it?")
      else:
        this_spell = spells[spell]
        cost = this_spell['cost']
        if cost > characters[me]['mana']:
          print("Not enough mana.  It costs ", cost," and you have ",characters[me]['mana'])
          continue

        print(this_spell['ok'])

        # if the spell has extra effect logic:
        if spell=='darkcloud':
          for who in curroom['who']:
            characters[who]['state']='dead'
            for i in characters[who]['items']:
              rooms[curroom_label]['items'].append(i)
            characters[who]['items']=[]

        elif spell=='flyingcarpet':
          characters[me]['where'] = random.choice( list(rooms.keys()) )

        elif spell=='vitality':
          for who in curroom['who']:
            if characters[who]['state']=='dead':
              characters[who]['state']=None

        #print(this_spell['fail'])

  elif action=='xray_mode':
    if xray_mode:
      xray_mode=False
    else:
      xray_mode=True
    print('xray_mode',xray_mode)

  elif action=='mindx':
    cost=30
    if characters[me]['mana']<cost:
        print("Not enough mana.  It costs ", cost," and you have ",characters[me]['mana'])
        continue

    if len(tokens)!=2:
      print("Thats not how you that command works")
    else:
      who = tokens[1]
      if who not in curroom['who']:
        print("They arent here!")
        #elif characters[who]['state']=='dead':
        #  print("But they are dead!")
      else:
        me=who
        print("You feel very strange... its a dizzy feeling, and the world is starting to spin.  You black out!  ... and when you come to, you dont quite feel like yourself anymore.")

  elif action in ['debug']:
    print('---characters---')
    pprint(characters)

    print('---rooms---')
    pprint(rooms)

    print('---items---')
    pprint(items)

    print('---myitems---')
    pprint(characters[me]['items'])




  elif action in ['h','help','?']:
    help()

  elif action in ['mana',]:
    print("Current mana: ", characters[me]['mana'])
    print("mana regen: ", characters[me]['mana_regen'])

  elif action in ['inv',]:
    print("")
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ')
    print('   Ye Olde Inventorie ')
    print('   ------------------ ')
    if characters[me]['items']:
      print('You have a '+ ", a ".join(characters[me]['items']) )
    else:
      print("You dont have anything")
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ')
    print("")
    print("")

  else:
    print("I dont know what you mean.  h for help.")


  print(' ')
  #print(' ~~~ ')
  print('')
