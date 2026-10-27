#pragma semicolon 1
#include <sourcemod>
#include <sdkhooks>
new String:svdgameinfo[64] = "Warcraft Source 0.78";
new bool:wcs_gminf = true; 
new Handle:gameinfo = INVALID_HANDLE; 
public Plugin:myinfo= 
{
	name="Warcraft Source - GameInfo",
	author="Don Revan",
	description="Change the gameinfo text",
	version="1.0",
	url="http://www.wcs-lagerhaus.de"
};

public OnPluginStart()
{
	gameinfo = CreateConVar("wcs_gamename", "Warcraft Source 0.78", "WCS GameName");
	HookConVarChange(gameinfo, smgameinfo); 
	PrintToServer("[WCS] Gamename Hooked!");
}

public OnAllPluginsLoaded()
{
	if (GetExtensionFileStatus("sdkhooks.ext") != 1)
	{
		SetFailState("SDKHooks not found");
	}
}

public OnLibraryRemoved(const String:name[])
{
	if (strcmp(name, "sdkhooks.ext") == 0)
	{
		SetFailState("SDKHooks not found");
	}
}

public Action:OnGetGameDescription(String:gameDesc[64])  
{ 
	if (wcs_gminf) 
	{ 
		strcopy(gameDesc, sizeof(gameDesc), svdgameinfo);
		return Plugin_Changed; 
	} 
	return Plugin_Continue; 
}

public smgameinfo(Handle:cvar, const String:oldValue[], const String:newValue[]) 
{ 
	strcopy(svdgameinfo, sizeof(svdgameinfo), newValue); 
	if (newValue[0] > 0) 
	{ 
		wcs_gminf = true; 
	} 
	else 
	{ 
		wcs_gminf = false; 
	} 
}  
