#include <sourcemod>
#include <sdktools>
#include <sdkhooks>
#define TOKENCHAR "," //char used to explode the string(weapon_usp,weapon_glock,weapon_knife == token is ,)
new g_iGameID = 1;//gameid info : 1+other=css;2=dods,3=tf2 (on other games the restrict all command probably will not work)
new m_OffsetActiveWeapon;
new String:RestrictetWeapons[MAXPLAYERS+1][1024];
new bool:bAllRestrictet[MAXPLAYERS+1];
new Handle:g_hResetRestriction=INVALID_HANDLE;
new Handle:g_hWeaponC4=INVALID_HANDLE;
// wcs_changerace est déclaré par WCS (wcs/events/events.res) quand ES le charge, souvent après ce plugin
new bool:g_bChangeRaceHooked=false;
public Plugin:myinfo= 
{
	name="WCS - Restrictions",
	author="DonRevan",
	description="Handles the Weapon Restrictions",
	version="2.0",
	url="http://wcs-lagerhaus.de/"
};
public OnPluginStart()
{
	CreateTimer(0.6,Timer_CheckItems,_,TIMER_REPEAT);
	m_OffsetActiveWeapon=FindSendPropInfo("CBasePlayer","m_hActiveWeapon");
	if(m_OffsetActiveWeapon==-1) //a fancy offset :3
	{
		LogError("[WCS] Error finding active weapon offset.");
	}
	RegServerCmd("wcs_restrict", Command_Restrict, "<userid> <weapons> - restrict weapon(s)");
	RegServerCmd("wcs_unrestrict", Command_UnRestrict, "<userid> <weapons> - unrestrict weapon(s)");
	g_bChangeRaceHooked=HookEventEx("wcs_changerace",PlayerChangeEvent);
	g_hWeaponC4 = CreateConVar("wcs_restrict_ignorec4", "1", "If non-zero the restriction engine will ignore the bomb(CS:S only).");
	g_hResetRestriction = CreateConVar("wcs_restrict_autoreset", "1", "If non-zero the restriction engine will automatic reset restrictions on changerace.");
	PrintToServer("[WCS] Loaded : Restriction Engine");
	decl String:buffer[32]
	GetGameFolderName(buffer,sizeof(buffer));
	if (StrEqual(buffer, "dod")) {
		g_iGameID = 2;
		PrintToServer("[WCS] Restriction Mask Changed to \"Day of Defeat Source Items\"");
	}
	else if (StrEqual(buffer, "tf")) {
		g_iGameID = 3;
		PrintToServer("[WCS] Restriction Mask Changed to \"Team Fortress Items\"");
	}
}

public Action:PlayerChangeEvent(Handle:event, const String:name[], bool:dontBroadcast)
{
	if(GetConVarBool(g_hResetRestriction)) {
		new client = GetClientOfUserId(GetEventInt(event,"userid"));
		if(ValidPlayer(client,false)) {
			bAllRestrictet[client]=false;
			WCS_RestrictTo(client,"");
			return Plugin_Continue;
		}
	}
	return Plugin_Continue;
}

stock WCS_RestrictTo(const iClient,const String:strMask[1024])
{
	strcopy(RestrictetWeapons[iClient],1024,strMask);
}

stock WCS_AddRestriction(const iClient,String:strWeapon[32])
{
	StrCat(RestrictetWeapons[iClient], 1024, strWeapon);
	StrCat(",", 1024, strWeapon);
}

stock WCS_DelRestriction(const iClient,const String:strWeapon[32])
{
	ReplaceString(RestrictetWeapons[iClient], 1024, strWeapon, "", false);
}

stock WCS_AddRestrictionAll(const iClient)
{
	//reset buffer
	WCS_RestrictTo(iClient,"");
	if(g_iGameID==2) {
		//dod:s restrictions
		StrCat(RestrictetWeapons[iClient], 1024, "weapon_30cal,weapon_30calpr,weapon_30calsr,weapon_amerknife,weapon_bar,weapon_bazooka,weapon_bazookarocket,weapon_basebomb,weapon_c96,weapon_colt,weapon_frag,weapon_garand,weapon_garandgren,weapon_garandrggrenade,weapon_k98,weapon_k98rg,weapon_k98rggrenade,weapon_k98s,weapon_m4carb,weapon_mg42,weapon_mg42bd,weapon_mg42bu,weapon_mg42pr,weapon_mg42sr,weapon_mp40,weapon_mp44,weapon_p38,weapon_panzerschreckrocket,weapon_pschreck,weapon_smokeger,weapon_smokeus,weapon_spade,weapon_spring,weapon_stick,weapon_thompson,");
	}
	else if(g_iGameID==3) {
		//tf2 restrictions
		StrCat(RestrictetWeapons[iClient], 1024, "tf_weapon_revolver,tf_weapon_fireaxe,tf_weapon_flamethrower,tf_weapon_pistol_scout,tf_weapon_syringegun_medic,tf_weapon_invis,tf_weapon_invis,tf_weapon_shotgun_pyro,tf_weapon_scattergun,tf_weapon_sniperrifle,tf_weapon_smg,tf_weapon_fists,tf_weapon_medigun,tf_weapon_minigun,tf_weapon_bat,tf_weapon_shotgun_hwg,tf_weapon_bonesaw,tf_weapon_smg,tf_weapon_bottle,tf_weapon_pipebomblauncher,tf_weapon_shovel,tf_weapon_shotgun_soldier,tf_weapon_rocketlauncher,tf_weapon_shotgun_soldier,tf_weapon_shovel,tf_weapon_shotgun_hwg,tf_weapon_fireaxe")
	}
	//cs:s restrictions
	else {
		StrCat(RestrictetWeapons[iClient], 1024, "weapon_usp,weapon_glock,weapon_deagle,weapon_elite,weapon_p228,weapon_fiveseven,weapon_m3,weapon_xm1014,weapon_mp5navy,weapon_tmp,weapon_p90,weapon_mac10,weapon_ump45,weapon_galil,weapon_famas,weapon_ak47,weapon_sg552,weapon_m4a1,weapon_aug,weapon_scout,weapon_awp,weapon_g3sg1,weapon_sg550,weapon_m249,weapon_flashbang,weapon_smokegrenade,weapon_hegrenade,");
		if(!GetConVarBool(g_hWeaponC4)) {
			WCS_AddRestriction(iClient,"weapon_c4");
		}
	}
}

stock bool:WCS_IsRestrictet(const iClient,String:strWeapon[32],bool:stripWeaponPrefix=true) {
	/*if ( strncmp( strWeapon[7], "weapon_", 7 ,false ) == 0 )
	{
		strWeapon += 7;
	}*/
	if(stripWeaponPrefix) ReplaceString(strWeapon, sizeof(strWeapon), "weapon_", "", false);
	if(StrContains(RestrictetWeapons[iClient],strWeapon,false)!=-1) {
		return true;
	}
	return false;
}

public Action:Command_Restrict(args) {
	decl String:strTarget[64];
	decl String:strVar[512];
	if (args < 2)
	{
		PrintToServer("[WCSL] Usage : wcs_restrict <userid> <weapons>");
		return Plugin_Handled;
	}
	else {
		GetCmdArg(1, strTarget, sizeof(strTarget));
		GetCmdArg(2, strVar, sizeof(strVar));
		new uid = StringToInt(strTarget);
		new client = GetClientOfUserId(uid);	
		//PrintToChatAll("resolved client id(%i) from user id: %i",client,uid); debug stuff..
		//PrintToServer("resolved client id = %i from user id: %i",client,uid); same here :)
		if (ValidPlayer(client,false)) {
			TrimString(strVar);
			StripQuotes(strVar);
			if(strlen(strVar)>0) {
				if(!StrEqual(strVar, "all")) {					
					decl String:strBuffer[512][32];
					new num = ExplodeString(strVar, TOKENCHAR, strBuffer, 512, 32);
					for(new i = 0; i < num; i++) {
						//PrintToConsole(client,"[WCS] %i Restriction added(%s)",num,strBuffer[i]);
						WCS_AddRestriction(client,strBuffer[i]);
					}
					bAllRestrictet[client]=false;
				}
				else {
					WCS_AddRestrictionAll(client);
					bAllRestrictet[client]=true;
					//PrintToConsole(client,"[WCS] All Items got Restricted!");
				}
			}
		}
		else
		LogError("[SM] wcs_restrict : Invalid userid given!");		
	}
	return Plugin_Handled;
}

public Action:Command_UnRestrict(args){
	decl String:strTarget[64];
	decl String:strVar[512];
	if (args < 2)
	{
		PrintToServer("[WCSL] Usage : wcs_restrict <userid> <weapons>");
		return Plugin_Handled;
	}
	else {
		GetCmdArg(1, strTarget, sizeof(strTarget));
		GetCmdArg(2, strVar, sizeof(strVar));
		new client = GetClientOfUserId(StringToInt(strTarget));	
		if (ValidPlayer(client,false)) {	
			TrimString(strVar);
			StripQuotes(strVar);
			if(strlen(strVar)>0) {
				if(!StrEqual(strVar, "all")) {
					decl String:strBuffer[512][32];
					new num = ExplodeString(strVar, TOKENCHAR, strBuffer, 512, 32);
					for(new i = 0; i < num; i++) {
						//PrintToConsole(client,"[WCS] %i Restriction removed(%s)",num,strBuffer[i]);
						WCS_DelRestriction(client,strBuffer[i]);
					}
					if(num>0) {
						//PrintToConsole(client,"[WCS] Restriction(s) removed: %s",strVar);
						bAllRestrictet[client]=false; //just to be sure...
					}
				}
				else {
					bAllRestrictet[client]=false;
					WCS_RestrictTo(client,"");
					//PrintToConsole(client,"[WCS] All Items got Unrestricted!");
				}
			}
		}
		else
		LogError("[SM] wcs_unrestrict : Invalid userid given!");		
	}
	return Plugin_Handled;
}
GetCurrentWeaponEnt(const iClient){
	return GetEntDataEnt2(iClient,m_OffsetActiveWeapon);
}
public OnClientPutInServer(client){ //allow everything
	bAllRestrictet[client]=false;
	WCS_RestrictTo(client,"");
	PrintToConsole(client,"Restriction System by wcs-lagerhaus.de");
	SDKHook(client, SDKHook_WeaponCanUse, OnWeaponCanUse); //weapon touch and equip only
}
bool:ClientCanUseWeapon(client,weaponent){
	if(strlen(RestrictetWeapons[client])>0) {
		decl String:WeaponName[32];
		GetEdictClassname(weaponent, WeaponName, sizeof(WeaponName));//gets weaponname
		if(GetConVarBool(g_hWeaponC4)==true && StrContains(WeaponName,"c4")>-1){ //handles c4 stuff..
			return true;
		}
		if(bAllRestrictet[client]) {
			return false;//everything is restrictet don't bother with it...
		}
		else {
			if(WCS_IsRestrictet(client,WeaponName)) {
				return false;//check weapon and disallow if item is restrictet!
			}
		}
	}
	return true; //allow
}
public Action:OnWeaponCanUse(client, weaponent)
{
	if(!ClientCanUseWeapon(client,weaponent))
	{
		return Plugin_Handled;
	}
	return Plugin_Continue;
}
public Action:Timer_CheckItems(Handle:h){
	if(!g_bChangeRaceHooked)
		g_bChangeRaceHooked=HookEventEx("wcs_changerace",PlayerChangeEvent);
	for(new client=1;client<=MaxClients;client++){
		if(ValidPlayer(client,true)){				
			new wpnent = GetCurrentWeaponEnt(client);
			if(wpnent>0&&IsValidEdict(wpnent)){
				if (!ClientCanUseWeapon(client,wpnent)){
					decl String:WeaponName[32];
					GetEdictClassname(wpnent, WeaponName, sizeof(WeaponName));
					PrintToChat(client,"\x04[WCS] \x01Item \x03%s \x01is restricted!",WeaponName);
					SDKHooks_DropWeapon(client, wpnent);
				}
			}
		}
	}
}
stock bool:ValidPlayer(client,bool:check_alive=false){
	if(client>0 && client<=MaxClients && IsClientConnected(client) && IsClientInGame(client))
	{
		if(check_alive && !IsPlayerAlive(client))
		{
			return false;
		}
		return true;
	}
	return false;
}