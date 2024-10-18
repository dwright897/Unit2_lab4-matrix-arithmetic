import random

class River():
  def __init__(self, RIVER_SIZE, START_BEARS, START_FISH):
    self.size = RIVER_SIZE
    self.river = [['_']*RIVER_SIZE for p in range(RIVER_SIZE) ]
    self.START_BEARS = START_BEARS
    self.START_FISH = START_FISH
    self.animals = []
    self.population = 0
    self.__initial_population()

  def __initial_population(self):
    for _ in range(self.START_BEARS):
      self.place_baby(Bear)
    for _ in range(self.START_FISH):
      self.place_baby(Fish)

  def place_baby(self, animal):
    goal = True
    if self.population >= self.size * self.size:
      print("⚠️ The river is full!!")
      return self.size
    
    while goal:
      x = random.randint(0, self.size - 1)
      y = random.randint(0, self.size - 1)
      if self.river[y][x] == '_':
        baby = animal(x, y)
        self.river[y][x]= baby
        self.animals.append(baby)
        self.population +=1
        goal = False

  def animal_death(self, animal):
    if animal in self.animals:
      self.animals.remove(animal)
      self.population -=1
      self.river[animal.y][animal.x] = '_'
     
  def redraw_cells(self, old_y,old_x,new_y,new_x,animal):
    self.river[old_y][old_x] = '_'
    self.river[new_y][new_x] = animal
  
  def new_day(self):
    babies = []
    for animal in self.animals:
      baby= animal.move(self)
      babies.append(baby)
    for baby in babies:
      if baby != None:
        self.place_baby(baby)
    for item in self.animals:
      if type(item) == Bear:
        item.lives-=1
        if item.lives <= 0:
          item.starve(self)
    
  def __getitem__(self, other):
    return self.river[other]

  def __str__(self):
    new_river = ""
    for row in self.river:
      cell = ""
      for item in row:
        if item == '_':
          cell+= "🟦 "
        else:
          cell += str(item)+ " "
      new_river += cell + "\n"
    
    return new_river
#-----------------------------------------------
class Animal:
  def __init__(self,x,y):
    self.x = x
    self.y = y
    self.bred_today = False
  
  def death(self,river):
    river.animal_death(self)

  def move(self, river):
    old_y = self.y
    old_x = self.x
    new_x = []
    new_y = []
    valid = False
    baby = None
    while not valid:
      direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0), (0,0), (1,1), (-1,1), (1,-1),(-1,-1)])
      new_x = old_x + direction[0]
      new_y = old_y + direction[1]
      if 0<= new_x < river.size and 0 <= new_y < river.size:
        valid = True

    if river[new_y][new_x]=='_':
      river.redraw_cells(old_y, old_x, new_y, new_x, self)
      self.x = new_x
      self.y = new_y
    else:
      baby = self.collision(river, new_y, new_x)
      return baby
        
  def collision(self,river, new_y, new_x):
    other = river[new_y][new_x]
    new_baby=None
    if type(other) == type(self) and self.bred_today == other.bred_today == False:
      if type(other) == Bear:
          self.bred_today = True 
          other.bred_today = True
          new_baby=Bear
          print(f"A baby bear was bred!")
      elif type(other) == Fish:
        self.bred_today = True 
        other.bred_today = True
        new_baby=Fish
        print(f"A baby fish was bred!")
    
    elif type(other) != type(self):
      
      if type(self) == Bear:
        other.death(river)
        self.consume(other, river)
        print(f"{other }  has been consumed by {self}.")
      else:
        self.death(river)
        other.consume(self, river)
        print(f"{self }  has been consumed by {other}.")
    return new_baby

#------------------------------------------------

class Bear(Animal):
  max_lives = 5
  def __init__(self, x, y):
    super().__init__(x, y)
    self.lives = Bear.max_lives
    self.eaten_today = False

  def starve(self, river):
    if self.eaten_today==False:
      self.lives-=1
      if self.lives<=0:
        self.death(river)
        print(f"{self} starved to death.")
    self.eaten_today = False
  
  def consume(self, fish, river):
    self.eaten_today=True
    self.lives = Bear.max_lives
    river.animal_death(fish)

  def __str__(self):
    return "🐻"
#----------------------------------------------
class Fish(Animal):
  def __str__(self):
   return "🐟"
