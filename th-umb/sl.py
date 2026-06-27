_M='/Games/th-umb/charSave.json'
_L='worldLoc'
_K='Error loading world:'
_J='Save file not found. Generating a new world.'
_I='No data found for world at'
_H='waterLine'
_G='World Pos:'
_F='Error: Save file is empty or contains invalid JSON.'
_E='/Games/th-umb/worlds.json'
_D='entities'
_C='worldType'
_B='world'
_A=False
import sys,json
sys.path.append('/Games/th-umb')
def saveWorld(logic):
	world_key=f"world_{logic.worldCoords[0]}_{logic.worldCoords[1]}_{logic.floor}";data={_B:list(logic.world),_C:logic.worldType,_H:logic.waterLine,_D:logic.el.entities if logic.el else[],'floor':logic.floor}
	try:
		try:
			with open(_E,'r')as save_file:all_worlds=json.load(save_file)
		except(OSError,Exception):all_worlds={}
		all_worlds[world_key]=data
		with open(_E,'w')as save_file:json.dump(all_worlds,save_file)
		print('World saved successfully.')
	except OSError as e:print('Error saving world:',e)
def loadWorld(logic,Logic,sprites):
	world_key=f"world_{logic.worldCoords[0]}_{logic.worldCoords[1]}_{logic.floor}"
	try:
		with open(_E,'r')as save_file:
			try:all_worlds=json.load(save_file)
			except Exception:print(_F);return _A
			if world_key in all_worlds:
				data=all_worlds[world_key];logic.world=bytearray(data.get(_B,[0]*len(logic.world)));logic.worldType=data.get(_C,0);logic.waterLine=list(data.get(_H,[0,0,0]));logic.floor=data.get('floor',0);allEntities=list(data.get(_D,[]))
				if logic.firstLoad:logic.el=Logic(logic,allEntities,sprites);logic.firstLoad=_A
				else:logic.el.entities=allEntities
				print('World loaded successfully');print(_G,logic.worldCoords[0],logic.worldCoords[1]);return True
			else:print(_I,logic.worldCoords[0],logic.worldCoords[1]);return _A
	except OSError as e:
		if e.args[0]==2:print(_J);return _A
		else:print(_K,e);return _A
def loadSpecificWorld(logic,Logic,sprites,worldID):
	try:
		with open('/Games/th-umb/pSave.json','r')as save_file:
			try:all_worlds=json.load(save_file)
			except Exception:print(_F);return _A
			if worldID<len(all_worlds):
				data=all_worlds[worldID];logic.world=bytearray(data.get(_B,[0]*len(logic.world)));logic.worldType=data[_C];logic.waterLine=[0,0,0];allEntities=data.get(_D,[])
				if logic.firstLoad:logic.el=Logic(logic,allEntities,sprites);logic.firstLoad=_A
				else:logic.el.entities=allEntities
				print('World loaded successfully:',logic.world,logic.worldType,logic.waterLine);print(_G,logic.worldCoords[0],logic.worldCoords[1]);return True
			else:print(_I,logic.worldCoords[0],logic.worldCoords[1]);return _A
	except OSError as e:
		if e.args[0]==2:print(_J);return _A
		else:print(_K,e);return
def playerSave(logic):
	data={'pos':list(logic.pInt),'inv':list(logic.inv),_L:list(logic.worldCoords),'beds':list(logic.beds)}
	try:
		with open(_M,'w')as save_file:save_file.write('');json.dump(data,save_file)
	except OSError as e:print('Error saving player:',e);pass
def playerLoad(logic):
	try:
		with open(_M,'r')as save_file:
			try:playerData=json.load(save_file)
			except json.JSONDecodeError:print(_F);return _A
			logic.pInt=playerData.get('pos',[0,0]);logic.inv=playerData.get('inv',[0]*8);logic.worldCoords=playerData.get(_L,[0,0]);logic.beds=playerData.get('beds',[0,0]);print('Player loaded successfully:',logic.pInt,logic.inv);print(_G,logic.worldCoords[0],logic.worldCoords[1]);print('Beds: ',logic.beds);return True
	except OSError as e:
		if e.errno==2:print('Save file not found.')
		else:print('Error loading player:',e)
		return _A