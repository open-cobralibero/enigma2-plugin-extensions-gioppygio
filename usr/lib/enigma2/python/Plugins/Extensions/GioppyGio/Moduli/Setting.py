#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Please don't remove this disclaimer
# Code by Madhouse
_L='services'
_K='transponders'
_J='rm -rf /etc/enigma2/*.del'
_I='rm -fr '
_H='/Settings/Temp/TrasponderListOldLamedb'
_G='/Settings/Temp/TerrestrialChannelListArchive'
_F='/Settings/Temp/ServiceListOldLamedb'
_E=':'
_D='w'
_C='r'
_B=True
_A=False
install_epg='cd /usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Panel && chmod 777 installepg.sh && ./installepg.sh'
from.import _
from enigma import eTimer,eDVBDB
from random import choice
import re,glob,shutil,os,ssl,time,sys,zipfile
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Console import Console
from Screens.Standby import TryQuitMainloop
from.Config import*
import socket
try:from urllib.request import urlopen,Request;from urllib.error import HTTPError,URLError
except ImportError:from urllib2 import urlopen,Request,HTTPError,URLError
Directory=os.path.dirname(sys.modules[__name__].__file__)
MinStart=int(choice(range(59)))
def TimerControl():now=time.localtime(time.time());Ora=str(now[3]).zfill(2)+_E+str(now[4]).zfill(2)+_E+str(now[5]).zfill(2);Date=str(now[2]).zfill(2)+'-'+str(now[1]).zfill(2)+'-'+str(now[0]);return'%s ora: %s'%(Date,Ora)
def StartSavingTerrestrialChannels(lamedb,type):
	B='/etc/enigma2/*.tv';A='eeee0000'
	def ForceSearchBouquetTerrestrial():
		for file in sorted(glob.glob(B)):
			f=open(file,_C).read();x=f.strip().lower()
			if x.find(A)!=-1:
				if x.find('82000')==-1 and x.find('c0000')==-1:return file;break
	def ResearchBouquetTerrestrial(search,search1):
		for file in sorted(glob.glob(B)):
			f=open(file,_C).read();x=f.strip().lower();x1=f.strip()
			if x1.find('#NAME')!=-1:
				if x.lower().find(search.lower())!=-1 or x.lower().find(search1.lower())!=-1:
					if x.find(A)!=-1:return file;break
	def SaveTrasponderService(lamedb):
		TrasponderListOldLamedb=open(Directory+_H,_D);ServiceListOldLamedb=open(Directory+_F,_D);Trasponder=_A;inTransponder=_A;inService=_A
		try:
			LamedbFile=open(lamedb,_C)
			while 1:
				line=LamedbFile.readline()
				if not line:break
				if not(inTransponder or inService):
					if line.find(_K)==0:inTransponder=_B
					if line.find(_L)==0:inService=_B
				if line.find('end')==0:inTransponder=_A;inService=_A
				line=line.lower()
				if line.find(A)!=-1:
					Trasponder=_B
					if inTransponder:TrasponderListOldLamedb.write(line);line=LamedbFile.readline();TrasponderListOldLamedb.write(line);line=LamedbFile.readline();TrasponderListOldLamedb.write(line)
					if inService:tmp=line.split(_E);ServiceListOldLamedb.write(tmp[0]+_E+tmp[1]+_E+tmp[2]+_E+tmp[3]+_E+tmp[4]+':0\n');line=LamedbFile.readline();ServiceListOldLamedb.write(line);line=LamedbFile.readline();ServiceListOldLamedb.write(line)
			TrasponderListOldLamedb.close();ServiceListOldLamedb.close()
			if not Trasponder:os.system(_I+Directory+_H);os.system(_I+Directory+_F)
		except:pass
		return Trasponder
	def CreateBouquetForce():
		WritingBouquetTemporary=open(Directory+_G,_D);WritingBouquetTemporary.write('#NAME terrestre\n');ReadingTempServicelist=open(Directory+_F).readlines()
		for jx in ReadingTempServicelist:
			if jx.find('eeee')!=-1:String=jx.split(_E);WritingBouquetTemporary.write('#SERVICE 1:0:%s:%s:%s:%s:%s:0:0:0:\n'%(hex(int(String[4]))[2:],String[0],String[2],String[3],String[1]))
		WritingBouquetTemporary.close()
	def SaveBouquetTerrestrial(istype):
		if istype:
			try:shutil.copyfile(Directory+'/Settings/Temp/enigma2dtt/dtt.tv',Directory+_G);return _B
			except:pass
		NameDirectory=ResearchBouquetTerrestrial('terr','dtt')
		if not NameDirectory:NameDirectory=ForceSearchBouquetTerrestrial()
		try:shutil.copyfile(NameDirectory,Directory+_G);return _B
		except:pass
	Service=SaveTrasponderService(lamedb)
	if Service:
		if not SaveBouquetTerrestrial(type):CreateBouquetForce()
		return _B
def TransferBouquetTerrestrialFinal():
	def RestoreTerrestrial():
		A='/etc/enigma2/'
		for file in os.listdir(A):
			if re.search('^userbouquet.*.tv',file):
				f=open(A+file,_C);x=f.read()
				if re.search('#NAME —  Digitale Terrestre Italia',x,flags=re.IGNORECASE):return A+file
	try:
		TerrestrialChannelListArchive=open(Directory+_G,_C).readlines();DirectoryUserBouquetTerrestrial=RestoreTerrestrial()
		if DirectoryUserBouquetTerrestrial:
			TrasfBouq=open(DirectoryUserBouquetTerrestrial,_D)
			for Line in TerrestrialChannelListArchive:
				if Line.lower().find('#name')!=-1:TrasfBouq.write('#NAME —  Digitale Terrestre Italia\n')
				else:TrasfBouq.write(Line)
			TrasfBouq.close();return _B
	except:return _A
def StartProcess(jLinkSat,jLinkDtt,Type,Personal):
	P='/Settings/Temp/*';O='/Settings/enigma2/* /etc/enigma2';N='#NAME User - bouquets (Tv)\n';M='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Moduli/Settings/Select';L='/usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Moduli/Settings/SelectBack';K='/Settings/Temp/enigma2dtt/lamedb';J='userbouquet.favourites_gio.tv';I='userbouquet.favourites.tv';H='/Settings/enigma2';G='/etc/enigma2/lamedb';F='rm -rf ';E='cp ';D='---';C='mkdir ';B='/etc/enigma2/bouquets.tv';A='/Settings/SelectFolder'
	def LamedbRestore():
		C='end\n';B='/Settings/Temp/ServiceListNewLamedb';A='/Settings/Temp/TrasponderListNewLamedb'
		try:
			TrasponderListNewLamedb=open(Directory+A,_D);ServiceListNewLamedb=open(Directory+B,_D);inTransponder=_A;inService=_A;infile=open(G,_C)
			while 1:
				line=infile.readline()
				if not line:break
				if not(inTransponder or inService):
					if line.find(_K)==0:inTransponder=_B
					if line.find(_L)==0:inService=_B
				if line.find('end')==0:inTransponder=_A;inService=_A
				if inTransponder:TrasponderListNewLamedb.write(line)
				if inService:ServiceListNewLamedb.write(line)
			TrasponderListNewLamedb.close();ServiceListNewLamedb.close();WritingLamedbFinal=open(G,_D);WritingLamedbFinal.write('eDVB services /4/\n');TrasponderListNewLamedb=open(Directory+A,_C).readlines()
			for x in TrasponderListNewLamedb:WritingLamedbFinal.write(x)
			try:
				TrasponderListOldLamedb=open(Directory+_H,_C).readlines()
				for x in TrasponderListOldLamedb:WritingLamedbFinal.write(x)
			except:pass
			WritingLamedbFinal.write(C);ServiceListNewLamedb=open(Directory+B,_C).readlines()
			for x in ServiceListNewLamedb:WritingLamedbFinal.write(x)
			try:
				ServiceListOldLamedb=open(Directory+_F,_C).readlines()
				for x in ServiceListOldLamedb:WritingLamedbFinal.write(x)
			except:pass
			WritingLamedbFinal.write(C);WritingLamedbFinal.close();return _B
		except:return _A
	def DownloadSettingAggDtt(jLinkDtt):
		F='/Settings/Temp/enigma2dtt';E='/Settings/Temp/settingdtt/userbouquet.favourites.tv';D='/Settings/Temp/settingdtt';B='/Settings/Temp/settingdtt/bouquets.tv';A='/Settings/Temp/listaE2dtt.zip'
		try:
			import requests;url_zip=requests.get(jLinkDtt,verify=_A)
			with open(Directory+A,'wb')as f:f.write(url_zip.content)
			if os.path.exists(Directory+A):
				os.system(C+Directory+D);image_zip=zipfile.ZipFile(Directory+A);image_zip.extractall(Directory+D)
				if os.path.exists(Directory+E):old_favorites=Directory+E;new_favorites=Directory+'/Settings/Temp/settingdtt/userbouquet.favourites_gio.tv';os.rename(old_favorites,new_favorites)
				if os.path.exists(Directory+B):f=open(Directory+B,_C);filedata=f.read();f.close();newdata=filedata.replace(I,J);f=open(Directory+B,_D);f.write(newdata);f.close()
				os.system(C+Directory+F);dir_name=Directory+'/Settings/Temp/settingdtt/';destination=Directory+F
				for filename in glob.glob(os.path.join(dir_name,'*')):shutil.copy(filename,destination)
				if os.path.exists(Directory+K):return _B
			return _A
		except:return
	def DownloadSettingAgg(jLinkSat,jLinkDtt):
		E='/Settings/Temp/setting/userbouquet.favourites.tv';D='/Settings/Temp/setting/bouquets.tv';B='/Settings/Temp/setting';A='/Settings/Temp/listaE2.zip';conferma=_B
		if jLinkDtt and str(jLinkDtt)!='0':
			if DownloadSettingAggDtt(jLinkDtt):conferma=_B
			else:conferma=_A
		try:
			import requests;url_zip=requests.get(jLinkSat,verify=_A)
			with open(Directory+A,'wb')as f:f.write(url_zip.content)
			if os.path.exists(Directory+A):
				os.system(C+Directory+B);image_zip=zipfile.ZipFile(Directory+A);image_zip.extractall(Directory+B)
				if os.path.exists(Directory+E):old_favorites=Directory+E;new_favorites=Directory+'/Settings/Temp/setting/userbouquet.favourites_gio.tv';os.rename(old_favorites,new_favorites)
				if os.path.exists(Directory+D):f=open(Directory+D,_C);filedata=f.read();f.close();newdata=filedata.replace(I,J);f=open(Directory+D,_D);f.write(newdata);f.close()
				os.system(C+Directory+'/Settings/Temp/enigma2');dir_name=Directory+B;destination=Directory+'/Settings/Temp/enigma2/'
				for filename in glob.glob(os.path.join(dir_name,'*')):shutil.copy(filename,destination)
				if os.path.exists(Directory+'/Settings/Temp/enigma2/lamedb')and conferma:return _B
			return _A
		except:return
	def SaveList(list):
		jw=open(L,_D)
		for(dir,name)in list:jw.write(dir+D+name)
		jw.close()
	def SavePersonalSetting():
		try:
			os.system(C+Directory+A);jw=open(M,_C);jjw=jw.readlines();jw.close();list=[]
			for x in jjw:
				try:jx=x.split(D);newfile=jx[0];os.system('cp /etc/enigma2/'+newfile+' '+Directory+A);os.system(E+Directory+'/Settings/Temp/enigma2/*'+' '+Directory+A);list.append((newfile,jx[1]))
				except:pass
			for file in glob.glob('/etc/enigma2/userbouquet.jmx*.tv'):os.system('cp /etc/enigma2/subbouquet.jmx*.tv'+' '+Directory+A)
			for file in glob.glob('/etc/enigma2/userbouquet.iptvdiv.tv'):os.system('cp /etc/enigma2/subbouquet.suls_iptv*.tv'+' '+Directory+A)
			if os.path.exists('userbouquet.TerrestrialScan.tv'):os.system('cp /etc/enigma2/userbouquet.TerrestrialScan.tv'+' '+Directory+A)
			SaveList(list)
		except:return
		return _B
	def TransferPersonalSetting():
		try:
			jw=open(L,_C);jjw=jw.readlines();jw.close()
			for x in jjw:
				try:jx=x.split(D);newfile=jx[0];os.system(E+Directory+'/Settings/SelectFolder/*.tv'+' /etc/enigma2')
				except:pass
		except:pass
		return _B
	def CreateUserbouquetPersonalSetting():
		C='" ORDER BY bouquet\n';A='#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "'
		try:jw=open(M,_C);jjw=jw.readlines();jw.close()
		except:pass
		jRewriteBouquet=open(B,_C);RewriteBouquet=jRewriteBouquet.readlines();jRewriteBouquet.close();WriteBouquet=open(B,_D)
		if int(Personal)==1:
			Writebouquets=open(B,_D);Writebouquets.write(N);Writebouquets.close()
			for x in jjw:
				try:
					jx=x.split(D)
					with open(B,'a')as f:f.write(A+jx[0].strip()+C)
				except:pass
			with open(B,'a')as f:f.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.favourites.tv" ORDER BY bouquet\n')
		else:
			Counter=0
			for xx in RewriteBouquet:
				if Counter==1:
					for x in jjw:
						if x[0].strip()!='':
							try:jx=x.split(D);WriteBouquet.write(A+jx[0].strip()+C)
							except:pass
					WriteBouquet.write(xx)
				else:WriteBouquet.write(xx)
				Counter=Counter+1
		WriteBouquet.close()
	def TransferNewSetting():
		M='/Settings/Temp/enigma2/satellites.xml /etc/tuxbox/';L='/Settings/Temp/enigma2/whitelist /etc/enigma2/';K='/etc/enigma2/whitelist';J='/Settings/Temp/enigma2/blacklist /etc/enigma2/';I='/etc/enigma2/blacklist';H='/Settings/Temp/enigma2/lamedb /etc/enigma2/';G='/Settings/Temp/enigma2/*.radio /etc/enigma2/';F='/etc/enigma2/userbouquet.favourites.tv';E='rm -rf /etc/enigma2/*.tv';D='rm -rf /etc/enigma2/*.radio';C='rm -rf /etc/enigma2/lamedb';A='cp -rf '
		try:
			if int(Personal)==1:
				os.system(C);os.system(D);os.system(_J);os.system(E);WriteBouquet=open(B,_D);WriteBouquet.write(N);WriteBouquet.close()
				if not os.path.exists(F):WriteFavorites=open(F,_D);WriteFavorites.write('#NAME @GioppyGio Favorites\n');WriteFavorites.close()
				os.system(A+Directory+G);os.system(A+Directory+H)
				if not os.path.exists(I):os.system(A+Directory+J)
				if not os.path.exists(K):os.system(A+Directory+L)
				os.system(A+Directory+M)
			else:
				os.system(C);os.system(D);os.system(E);os.system(_J);os.system(A+Directory+'/Settings/Temp/enigma2/*.tv /etc/enigma2/');os.system(A+Directory+G);os.system(A+Directory+H)
				if not os.path.exists(I):os.system(A+Directory+J)
				if not os.path.exists(K):os.system(A+Directory+L)
				os.system(A+Directory+M)
		except:return
		return _B
	Status=_B
	if int(Type)==1:SavingProcessTerrestrialChannels=StartSavingTerrestrialChannels(G,_A);os.system('cp -r /etc/enigma2/ '+Directory+H)
	if not DownloadSettingAgg(jLinkSat,jLinkDtt):os.system(E+Directory+O);os.system(F+Directory+H);Status=_A
	else:
		if int(Type)==0:SavingProcessTerrestrialChannels=StartSavingTerrestrialChannels(Directory+K,_B)
		personalsetting=_A
		if int(Personal)==1:personalsetting=SavePersonalSetting()
		if TransferNewSetting():
			if personalsetting:
				if TransferPersonalSetting():CreateUserbouquetPersonalSetting();os.system(_I+Directory+A);os.system('mv /usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Moduli/Settings/SelectBack /usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Moduli/Settings/Select');os.system(F+Directory+H)
		else:os.system(E+Directory+O);os.system(F+Directory+P);Status=_A
		if SavingProcessTerrestrialChannels and Status:TransferBouquetTerrestrialFinal()
	os.system(F+Directory+P);return Status
class GioppyGioSettings:
	def __init__(self,session=None):self.session=session;self.iTimer1=eTimer();self.iTimer2=eTimer();self.iTimer3=eTimer();self.iTimer1.callback.append(self.startTimerSetting);self.iTimer2.callback.append(self.startTimerSetting);self.iTimer3.callback.append(self.startTimerSetting)
	def gotSession(self,session):
		self.session=session;Type,AutoTimer,Personal,NumberSat,NameSat,Date,NumberDtt,DowDate,NameInfo=Load()
		if int(AutoTimer)==1:self.TimerSetting()
	def StopTimer(self):
		try:self.iTimer1.stop()
		except:pass
		try:self.iTimer2.stop()
		except:pass
		try:self.iTimer3.stop()
		except:pass
	def TimerSetting(self):
		try:self.StopTimer()
		except:pass
		now=time.time();ttime=time.localtime(now);start_time4=ttime[0],ttime[1],ttime[2],6,MinStart,0,ttime[6],ttime[7],ttime[8];start_time5=ttime[0],ttime[1],ttime[2],12,MinStart,0,ttime[6],ttime[7],ttime[8];start_time6=ttime[0],ttime[1],ttime[2],22,MinStart,0,ttime[6],ttime[7],ttime[8];start_time1=time.mktime(start_time4);start_time2=time.mktime(start_time5);start_time3=time.mktime(start_time6)
		if start_time1<now+60:start_time1+=86400
		if start_time2<now+60:start_time2+=86400
		if start_time3<now+60:start_time3+=86400
		delta1=int(start_time1-now);delta2=int(start_time2-now);delta3=int(start_time3-now);self.iTimer1.start(1000*delta1,_B);self.iTimer2.start(1000*delta2,_B);self.iTimer3.start(1000*delta3,_B)
	def startTimerSetting(self,Auto=_A):
		B='https://gioppygio.it/';A='https://picons.gioppygio.it';Type,AutoTimer,Personal,NumberSat,NameSat,Date,NumberDtt,DowDate,NameInfo=Load()
		def OnDsl():
			try:req=Request('http://gioppygio.it',None,{'User-agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'});context=ssl._create_unverified_context();response=urlopen(req,timeout=5,context=context);return _B
			except URLError as Error:
				if isinstance(Error.reason,socket.timeout):print('URL ERROR: ',Error)
				return _A
			except HTTPError as Error:
				if isinstance(Error.reason,socket.timeout):print('HTTPError: ',Error)
				return _A
			except socket.timeout as Error:print('socket.timeout: ',Error);return _A
			except Exception:return _A
		if OnDsl():
			for(jNumberSat,jNameSat,jLinkSat,jDateSat,jNumberDtt,jNameDtt,jLinkDtt,jDateDtt)in DownloadSetting():
				jDate=jDateSat
				if jDateDtt:
					if int(jDateDtt)>int(jDateSat):jDate=jDateDtt
				if jNumberSat==NumberSat and NumberDtt==jNumberDtt and jNameSat==NameSat:
					if jLinkSat.startswith(A)or jLinkDtt.startswith(B)or jLinkSat.startswith(B)or jLinkDtt.startswith(A):
						if jDate>Date or Auto:
							if StartProcess(jLinkSat,jLinkDtt,Type,Personal):now=time.time();jt=time.localtime(now);DowDate=str(jt[2]).zfill(2)+'-'+str(jt[1]).zfill(2)+'-'+str(jt[0])+'   '+str(jt[3]).zfill(2)+_E+str(jt[4]).zfill(2)+_E+str(jt[5]).zfill(2);WriteSave(Type,AutoTimer,Personal,jNumberSat,jNameSat,jDateSat,jNumberDtt,DowDate,NameInfo);OnclearMem();eDVBDB.getInstance().reloadServicelist();eDVBDB.getInstance().reloadBouquets();os.system(_J);MyMessage=NameInfo+' '+ConverDate(jDate)+_('\ninstalled!\n\nDo you want to download the Epg?\nThe download takes place in the background.');self.session.openWithCallback(self.downloadepg,MessageBox,MyMessage,MessageBox.TYPE_YESNO,default=_A,timeout=15)
							else:MyMessage=_('Sorry, cannot download !');self.session.open(MessageBox,MyMessage,MessageBox.TYPE_ERROR,timeout=5)
						break
					else:MyMessage=_('YOU ARE NOT ALLOWED TO\n\nDownload the GioppyGio plugin only from official sources!');self.session.open(MessageBox,MyMessage,MessageBox.TYPE_INFO)
		else:MyMessage=_('Sorry.\nno internet connection !');self.session.open(MessageBox,MyMessage,MessageBox.TYPE_ERROR,timeout=5)
		self.TimerSetting()
	def downloadepg(self,answer):
		if answer is _B:
			if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/EPGImport/plugin.pyo')or os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/EPGImport/plugin.py')or os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/EPGImport/plugin.pyc'):
				if not os.path.exists('/etc/enigma2/epgimport.conf'):os.system('cp /usr/lib/enigma2/python/Plugins/Extensions/GioppyGio/Panel/epgimport.conf /etc/enigma2/')
				from Plugins.Extensions.EPGImport.plugin import AutoStartTimer,autoStartTimer,channelFilter,config,epgimport
				if autoStartTimer is not None and not epgimport.isImportRunning():autoStartTimer.runImport()
			else:self.session.openWithCallback(self.installepg,MessageBox,_('Epg Importer not found! Do you want to install it?'),MessageBox.TYPE_YESNO,default=_A,timeout=15)
		else:0
	def installepg(self,answer):
		if answer is _B:self.session.openWithCallback(self.instepg,Console,_('Install Epg Import'),[install_epg],closeOnSuccess=_B)
		else:0
	def instepg(self,string=''):MyMessage=_('Do you want to restart the GUI\nto apply the changes?');self.session.openWithCallback(self.downloadepginst,MessageBox,MyMessage,MessageBox.TYPE_YESNO,default=_A,timeout=15)
	def downloadepginst(self,answer):
		if answer is _B:self.session.open(TryQuitMainloop,3)
		else:0
