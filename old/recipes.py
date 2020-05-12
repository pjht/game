from lib.gameregistry import GameRegistry

def init():
  GameRegistry.registerCrafting({"wood":6},"door")
  GameRegistry.registerCrafting({"wood":4},"workbench")
  GameRegistry.registerCrafting({"stone":8},"furnace")
  GameRegistry.registerSmelting("iron_ore","wood")
