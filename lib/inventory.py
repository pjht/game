class Inventory:
  def __init__(self):
    self.inv={}
    self.selected=""

  def addTile(self,name,amount):
    if name in self.inv.keys():
      self.inv[name]+=amount
    else:
      self.inv[name]=amount
    self.selected=name

  def remove(self,name,num=1):
    if not name in self.inv:
      raise Exception("No {} in inventory".format(name))
    amount=self.inv[name]
    amount-=num
    if amount<0:
      raise Exception("Attempted to remove more {} than avalible".format(name))
    self.inv[name]=amount
    if amount==0:
      del self.inv[name]
      self.selected=""

  def selPrev(self):
    newsel=""
    for item, count in self.inv.items():
      if item==self.selected:
        break
      newsel=item
    if newsel!="":
      self.selected=newsel

  def clearSel(self):
    self.selected=""

  def selNext(self):
    newsel=""
    ok_next=False
    for item, count in self.inv.items():
      if ok_next:
        newsel=item
        break
      if item==self.selected:
        ok_next=True
    if newsel!="":
      self.selected=newsel
