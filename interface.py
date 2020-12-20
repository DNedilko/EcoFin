from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager
from database import DataBase
from kivymd.uix.dialog import MDDialog
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.menu import MDDropdownMenu



class EcoApp(MDApp, Screen):

    def __init__(self, **kwargs):
        super().__init__( **kwargs)
        self.screen = Builder.load_file('D:\Ecoapp\kivy_venv\KV.kv')

    db = DataBase('D:/Ecoapp/kivy_venv/users.csv')




    def build(self):
        self.theme_cls.primary_palette = "Green"
        return self.screen



class LogIn(Screen):
    passw = ObjectProperty(None)
    login = ObjectProperty(None)
    def loginBtn(self):
        if db.validate(str(self.login.text),str(self.passw.text)):
            self.reset()
            return '1'
        else:
            self.reset()
            invalidLogin()

    def reset(self):
        self.login.text=''
        self.passw.text=''


class Registration(Screen):
    login = ObjectProperty(None)
    passw = ObjectProperty(None)
    city = ObjectProperty(None)
    email = ObjectProperty(None)
    def creation(self):
        print(self.login.text,self.passw.text,self.email.text,self.city.text)
        if self.login.text!='' and str(self.email.text) !='' and str(self.email.text).count('@')==1 and str(self.email.text).count('.')>0:
            if str(self.passw.text) !="":
                if db.add_user(str(self.login.text),str(self.passw.text),str(self.email.text),str(self.city.text))==-1:
                    self.reset()
                    Alr()

                else:
                    self.reset()
                    return '1'

            else:
                invalidForm()
                self.reset()
        else:
            invalidForm()
            self.reset()

    def log(self):
        self.reset()

    def reset(self):
        self.email.text=''
        self.passw.text=''
        self.login.text=''
        self.city.text=''



def invalidLogin():
    pop = MDDialog(size_hint=(0.4,0.2),title='OH NO!', radius=[20, 7, 20, 7],text='Hmmm...there`s no one with such login and password. Check your info.')
    pop.open()

def invalidForm():
    pop = MDDialog(size_hint=(0.4,0.2),title='OH NO!', radius=[20, 7, 20, 7],text='Hmmm...you forgot to fill something in. Check your info.')
    pop.open()

def Alr():
    pop = MDDialog(size_hint=(0.4,0.2),title='We already have someone with similar login!', radius=[20, 7, 20, 7],
                   text='Take another one (;')
    pop.open()


class Main(Screen):
    def __init__(self,**kwargs,):
        super().__init__(**kwargs)
        self.filename='mark.csv'
        self.marks=None
        self.file=None
        menu_items=[]
        self.marks={}
        self.file=open(self.filename, 'r')
        for i in self.file:
            marking, data = str(i).split(" * ")
            self.marks[marking] = (data)
        self.file.close()
        items=[]
        for a in self.marks:
            items.append(a[0])

        menu_items=[{'icon':"recycle-variant",'text': f'{i}'}for i in items]
        self.menu=MDDropdownMenu(
            id='markings',
            caller=self.screen.ids.drop_item,
            items=menu_items,
            position='center',
            width_mult=4
        )
        self.menu.bind(on_release=self.set_item)

    def set_item(self, ins_menu, ins_menu_item):
        self.screen.ids.drop_item.set_item(ins_menu.text)
        self.menu.dismiss()

    def build(self):
        return self.screen

class AccInfo(Screen):
    pass

m=ScreenManager()
db=DataBase('users.csv')
# m.add_widget(LogIn(name='LOG'))
# m.add_widget(Registration(name='registration'))
# m.add_widget(Main(name='main'))
# m.add_widget(AccInfo(name='acc'))


if __name__ == "__main__":
    EcoApp().run()