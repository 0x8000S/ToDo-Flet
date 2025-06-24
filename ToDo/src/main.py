import asyncio
import json
import time
import flet as ft
import datetime as dt
import os

def CalculateDateDifference(date1, date2):
	d1 = dt.datetime.strptime(date1, "%Y/%m/%d").date()
	d2 = dt.datetime.strptime(date2, "%Y/%m/%d").date()
	return (d2 - d1).days


class ToDoItem(ft.Card):
	def __init__(self, ItemName:str, Date:str, page:ft.Page, ListView:ft.ListView, BriefIntroduction:str):
		super().__init__()
		self.env = os.environ.get('FLET_APP_STORAGE_DATA')
		self.FileEnv = self.env + "\\saved.json"
		self.LocalTime = time.strftime("%Y/%m/%d", time.localtime())
		self.running = False
		self.view = ListView
		self.page = page
		self.Item = ItemName
		self.H2 = ""
		self.TimeUN = ""
		self.Date = Date
		self.Late = None
		self.BriefIntroduction = BriefIntroduction
		self.TitText = ft.Text(f"{ItemName}", size=24, weight=ft.FontWeight.BOLD)
		self.ErrorItemName = ft.AlertDialog(
			modal=True,
			title=ft.Text("错误", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.RED),
			content=ft.Text("待办事项名为空！", size=18),
			actions=[
				ft.TextButton("知道了", on_click=lambda _:page.close(self.ErrorItemName))
		]
	)
		if BriefIntroduction == "" or BriefIntroduction == " ":
			self.H2 = Date
		elif Date == "":
			self.H2 = BriefIntroduction
		else:
			self.H2 = BriefIntroduction + " | " + Date
		if Date != "":
			if CalculateDateDifference(self.LocalTime, Date) == 0:
				self.Late = None
				self.TimeUN = " | 就是今天！"
				self.TitText.color = ft.Colors.GREEN
			elif CalculateDateDifference(self.LocalTime, Date) > 0:
				self.Late = False
				self.TimeUN = f" | 离截止日期还剩{CalculateDateDifference(self.LocalTime, Date)}天"
				self.TitText.color = None
			elif CalculateDateDifference(self.LocalTime, Date) < 0:
				self.Late = True
				self.TimeUN = f" | 已超出{abs(CalculateDateDifference(self.LocalTime, Date))}天"
				self.TitText.color = ft.Colors.RED
		self.SubTitleText = ft.Text(f"{self.H2} {self.TimeUN}")
		self.tit = ft.ListTile(self.TitText, self.SubTitleText)
		self.con = ft.Container(
			ft.Column(
				[
					self.tit,
					ft.Row(
						[
							ft.IconButton(ft.Icons.CHECK, on_click=self.Finish),
							ft.IconButton(ft.Icons.EDIT, on_click=self.Change),
							ft.IconButton(ft.Icons.DELETE, on_click=self.DelItem)
						], ft.MainAxisAlignment.END
					)
				]
			), padding=10
		)
		self.content = self.con
	def DelItem(self, e):
		self.view.controls.remove(self)
		self.page.update()
		self.SaveAllItem()
	def Change(self, e):
		Name = self.Item
		BriefIntroduction = self.BriefIntroduction
		def NameChange(e:ft.ControlEvent):
			nonlocal Name
			Name = e.control.value
		ItemNameInput = ft.TextField(on_blur=NameChange, value=self.Item)
		def BriefIntroductionChange(e:ft.ControlEvent):
			nonlocal BriefIntroduction
			BriefIntroduction = e.control.value
		BriefIntroductionInput = ft.TextField(on_change=BriefIntroductionChange, value=self.BriefIntroduction)
		Date = self.Date
		DateText = ft.Text(self.Date, size=28)
		def ClearDateFunc(e):
			nonlocal Date
			Date = ""
			DateText.value = ""
			ClearDate.visible = False
			self.page.update()
		ClearDate = ft.FilledButton("清除", icon=ft.Icons.DELETE, visible=False, on_click=ClearDateFunc)
		if self.Date != "":
			ClearDate.visible = True
		def DateSet(e:ft.ControlEvent):
			nonlocal Date
			DateText.value = e.control.value.strftime('当前所选: %Y/%m/%d')
			Date = e.control.value.strftime('%Y/%m/%d')
			ClearDate.visible = True
			self.page.update()
		
		def WhenCloseBottom(e):
			return
		bs = ft.BottomSheet(
		ft.Container(
				ft.Column(
				[
					ft.Text("编辑当前待办事项", size=24, weight=ft.FontWeight.BOLD),
					ft.Row(
					[
						ft.Text("待办名称: "),
						ItemNameInput
					]),
					ft.Row(
						[
							ft.Text("介绍: "),
							BriefIntroductionInput
						]
					),
					ft.Row(
						[
							ft.Text("截止日期: "),
							ft.FilledButton("选择日期", on_click=lambda _:self.page.open(
								ft.DatePicker(
									on_change=DateSet
								)
							)),
							DateText, ClearDate
						]
					),
					ft.FilledButton("修改", on_click=lambda _:self.ButtonClickSub(Name, Date, BriefIntroduction, bs))
				]
			),padding=10
		), on_dismiss=WhenCloseBottom
	)
		self.page.open(bs)
	def ButtonClickSub(self, N, D, B, b):
		if N == "" or N == " ":
			self.page.open(self.ErrorItemName)
			return
		self.Item = N
		self.Date = D
		self.BriefIntroduction = B
		self.TitText.value = self.Item
		if self.BriefIntroduction == "" or self.BriefIntroduction == " ":
			self.H2 = self.Date
		elif self.Date == "":
			self.H2 = self.BriefIntroduction
		else:
			self.H2 = self.BriefIntroduction + " | " + self.Date
		self.page.close(b)
		
		if self.Date != "":
			self.ChangeTimeText()
		else:
			self.TimeUN = ""
			self.TitText.color = None
		self.SubTitleText.value = f"{self.H2} {self.TimeUN}"
		self.page.update()
		self.SaveAllItem()
	def SaveAllItem(self):
		Item = []
		print(f"List: {self.view.controls}")
		print(f"Is: {self.view.controls[0] is ft.Container}")
		for i in range(len(self.view.controls)-1):
			print(self.view.controls[i].GetData())
			Item.append(self.view.controls[i])
		print(f"Item: {Item}")
		Data = []
		for i in Item:
			Data.append(i.GetData())
		print(f"Data: {Data}")
		with open(self.FileEnv, 'w') as f:
			json.dump(Data, f, indent=4)
	def Finish(self, e):
		if self.Late == None:
			self.page.open(ft.SnackBar(ft.Text(f"待办\"{self.Item}\"已完成！", weight=ft.FontWeight.BOLD)))
		elif self.Late == True:
			self.page.open(ft.SnackBar(ft.Text(f"逾期待办\"{self.Item}\"已完成", weight=ft.FontWeight.BOLD)))
		elif self.Late == False:
			self.page.open(ft.SnackBar(ft.Text(f"待办\"{self.Item}\"已提前完成！", weight=ft.FontWeight.BOLD)))
		self.view.controls.remove(self)
		self.page.update()
		self.SaveAllItem()
	def did_mount(self):
		self.running = True
		self.page.run_task(self.updateTime)
	def will_unmount(self):
		self.running = False
	def ChangeTimeText(self):
		self.LocalTime = time.strftime("%Y/%m/%d", time.localtime())
		if CalculateDateDifference(self.LocalTime, self.Date) == 0:
			self.Late = None
			self.TimeUN = "就是今天！"
			self.TitText.color = ft.Colors.GREEN
		elif CalculateDateDifference(self.LocalTime, self.Date) > 0:
			self.Late = False
			self.TimeUN = f"离截止日期还剩{CalculateDateDifference(self.LocalTime, self.Date)}天"
			self.TitText.color = None
		elif CalculateDateDifference(self.LocalTime, self.Date) < 0:
			self.Late = True
			self.TimeUN = f"已超出{abs(CalculateDateDifference(self.LocalTime, self.Date))}天"
			self.TitText.color = ft.Colors.RED
		self.SubTitleText.value = f"{self.H2} {self.TimeUN}"
		self.tit = ft.ListTile(self.TitText, self.SubTitleText)
		self.page.update()
	async def updateTime(self):
		while self.running and self.Date != "":
			self.ChangeTimeText()
			await asyncio.sleep(60)
	def GetData(self):
		return [self.Item, self.Date, self.BriefIntroduction]

def main(page: ft.Page):
	env = os.environ.get('FLET_APP_STORAGE_DATA')
	FileEnv = env + "\\saved.json"
	print(env)
	page.title = "ToDo"
	appBar = ft.AppBar(title=ft.Text("ToDo"))
	ItemName = ""
	Date = ""
	BriefIntroduction = ""
	DateText = ft.Text("", size=28)
	ListView = ft.ListView(expand=True)
	def CreateItem(Name:str, Date, BriefIntroduction):
		return ToDoItem(Name, Date, page, ListView, BriefIntroduction)
	if os.path.exists(FileEnv):
		Item = None
		with open(FileEnv, 'r') as f:
			Item = json.load(f)
		print(Item)
		for i in Item:
			ListView.controls.append(CreateItem(i[0], i[1], i[2]))
	else:
		f = open(FileEnv, 'w')
		f.close()
	ListView.controls.append(ft.Container(height=100))
	def SaveAllItem():
		Item = []
		print(f"List: {ListView.controls}")
		print(f"Is: {ListView.controls[0] is ft.Container}")
		for i in range(len(ListView.controls)-1):
			print(ListView.controls[i].GetData())
			Item.append(ListView.controls[i])
		print(f"Item: {Item}")
		Data = []
		for i in Item:
			Data.append(i.GetData())
		print(f"Data: {Data}")
		with open(FileEnv, 'w') as f:
			json.dump(Data, f, indent=4)
	ErrorItemName = ft.AlertDialog(
		modal=True,
		title=ft.Text("错误", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.RED),
		content=ft.Text("待办事项名为空！", size=18),
		actions=[
			ft.TextButton("知道了", on_click=lambda _:page.close(ErrorItemName))
		]
	)
	def ClearDateFunc(e):
		nonlocal Date
		Date = ""
		DateText.value = ""
		ClearDate.visible = False
		page.update()
	ClearDate = ft.FilledButton("清除", icon=ft.Icons.DELETE, visible=False, on_click=ClearDateFunc)
	def DateSet(e:ft.ControlEvent):
		nonlocal Date
		DateText.value = e.control.value.strftime('当前所选: %Y/%m/%d')
		Date = e.control.value.strftime('%Y/%m/%d')
		ClearDate.visible = True
		page.update()
	def NameChange(e:ft.ControlEvent):
		nonlocal ItemName
		ItemName = e.control.value
		print(ItemName)
	def BriefIntroductionChange(e:ft.ControlEvent):
		nonlocal BriefIntroduction
		BriefIntroduction = e.control.value
		print(BriefIntroduction)
	ItemNameInput = ft.TextField(on_change=NameChange)
	BriefIntroductionInput = ft.TextField(on_change=BriefIntroductionChange)
	def ClearItemName():
		nonlocal ItemName
		ItemNameInput.value = ""
		page.update()
		ItemName = ""
	
	def ButtonClickSub(e):
		nonlocal ItemName
		nonlocal Date
		nonlocal BriefIntroduction
		if ItemName != "":
			ListView.controls.insert(0, CreateItem(ItemName, Date, BriefIntroduction))
			print(Date)
			ClearDateFunc(None)
			ClearItemName()
			BriefIntroductionInput.value = ""
			page.update()
			ItemName = ""
			BriefIntroduction = ""
			page.close(bs)
			print(ListView.controls)
			SaveAllItem()
		else:
			page.open(ErrorItemName)
	
	def WhenCloseBottom(e:ft.ControlEvent):
		nonlocal ItemName
		nonlocal BriefIntroduction
		ClearItemName()
		ClearDateFunc(None)
		BriefIntroductionInput.value = ""
		page.update()
		ItemName = ""
		BriefIntroduction = ""
	bs = ft.BottomSheet(
		ft.Container(
				ft.Column(
				[
					ft.Text("新建待办事项", size=24, weight=ft.FontWeight.BOLD),
					ft.Row(
					[
						ft.Text("待办名称: "),
						ItemNameInput
					]),
					ft.Row(
						[
							ft.Text("介绍: "),
							BriefIntroductionInput
						]
					),
					ft.Row(
						[
							ft.Text("截止日期: "),
							ft.FilledButton("选择日期", on_click=lambda _:page.open(
								ft.DatePicker(
									on_change=DateSet
								)
							)),
							DateText, ClearDate
						]
					),
					ft.FilledButton("提交", on_click=ButtonClickSub)
				]
			),padding=10
		), on_dismiss=WhenCloseBottom
	)
	def fab_pressed(e):
		print(ItemName, Date)
		page.open(bs)
	page.floating_action_button = ft.FloatingActionButton(text="添加", icon=ft.Icons.ADD, on_click=fab_pressed)
	page.overlay.append(bs)
	page.add(appBar)
	page.add(ListView)
	page.update()

ft.app(main)